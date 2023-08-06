import argparse
import configparser
import json
import logging
import os
import pathlib
import requests
import sys
import subprocess


import fiddler.dataset_yaml_generator
from fiddler.cli_utils import req_get, req_post
from fiddler.clone_cmd import CloneCmd
from fiddler.execute_cmd import ExecuteCmd
from fiddler.explain_cmd import ExplainCmd
from fiddler.import_cmd import ImportCmd


class CommandOptionsError(Exception):
    """Generic exception for insufficient args or configuration."""
    def __init__(self, *args, **kwargs):
        pass


# Configuration schema:
# --------------------
# [default]
# organization = my_org
# auth_key = user_bearer_key_for_API
CONFIG_FILE = '{}/.fidl/config'.format(os.environ['HOME'])


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'default' not in config.sections():
        config['default'] = {}
    return config


def write_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE),
                exist_ok=True)
    with open(CONFIG_FILE, 'w') as out:
        config.write(out)


# Implements basic cli : fiddler-cli command --org ... --project ...


def api_url(args, api_method):
    """ Returns 'api_endpoint/api_method/org/project/model' """
    ensure_arg(args, 'project')
    return '%s/%s/%s/%s/%s' % (args.api_endpoint, api_method, args.org,
                               args.project, args.model)


def print_response(resp):
    for line in resp.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)


def process_response(resp):
    """
    If the response is not successful, throws an
    exception with details about the error.
    Logs the response if the succeeds.
    """
    resp_str = resp.text
    try:
        resp_str = json.dumps(json.loads(resp_str), indent=4)
    except ValueError:
        # Response is not a json we print the raw text.
        pass
    if resp.status_code == requests.codes.ok:
        logging.info('Response from the service : %s', resp_str)
    else:
        logging.error('Request failed : %s', resp_str)
        resp.raise_for_status()

# Implementation of commands


def deploy_cmd(args):
    # Service should be updated to
    #   - support deploying a specific commit
    #   - return a json
    url = '%s/deploy_org/%s' % (args.api_endpoint, args.org)
    print('Deploying ', args.org,' at ', url)
    resp = req_get(args.auth_key, url)
    print_response(resp)
    print('Deployed ', args.org,' successfully')
    return resp


def train_cmd(args):
    url = api_url(args, 'train')
    logging.info('Training model %s at %s ...', args.model, url)
    resp = req_get(args.auth_key, api_url(args, 'train'))
    process_response(resp)
    logging.info('Successfully trained model %s', args.model)
    return resp


def clone_cmd(args):
    return CloneCmd(args.org, args.auth_key).run()


def execute_cmd(args):
    return ExecuteCmd(args).run()


def explain_cmd(args):
    return ExplainCmd(args).run()


def gen_yaml_cmd(args):
    # ensure csv files are valid
    csv_paths = [pathlib.Path(p) for p in args.csv_paths]
    not_found_paths = [str(path) for path in csv_paths if not path.exists()]
    if len(not_found_paths) > 0:
        raise ValueError(f'The following path(s) do not exist: '
                         f'{not_found_paths}.')

    # parse output directory
    out_dir = pathlib.Path(args.output)
    if not out_dir.is_dir():
        raise NotADirectoryError(f'Output directory "{out_dir}" not found.')

    # check if yaml already exists
    yaml_out_path = out_dir / (out_dir.stem + '.yaml')
    if yaml_out_path.exists():
        raise FileExistsError('This YAML file already exists. If you want to '
                              'overwrite the YAML file, simply delete the '
                              'existing file and rerun this command.')

    # create the yaml
    print(f'Inferring dataset information from '
          f'{[str(p) for p in csv_paths]} and generating yaml at '
          f'"{yaml_out_path}".')
    fiddler.dataset_yaml_generator.infer_yaml(csv_paths, yaml_out_path)


def configure_cmd(args):
    config = read_config()
    section = config['default']
    for prop in ['organization', 'auth_key', 'api_endpoint']:
        cur = str(section.get(prop, ''))
        new = input(f'{prop}[{cur}] = ')
        if new:
            section[prop] = new
            if prop == 'auth_key':
                config_git(new)
    write_config(config)


def config_git(auth_key):
    subprocess.call(['git', 'config', '--global', '--unset-all',
                     'http.http://repo.fiddler.ai.extraheader'])
    subprocess.call(['git', 'config', '--global', '--add',
                     'http.http://repo.fiddler.ai.extraheader',
                     'Authorization: Bearer {}'.format(auth_key)])
    logging.info('Done configuring git')


def publish_cmd(args):
    url = api_url(args, 'external_event')
    logging.info('Publishing event at {}'.format(url))
    resp = req_post(args.auth_key, url, args.data)
    process_response(resp)
    return resp


def import_cmd(args):
    return ImportCmd(args).run()


# More commands to add:
# list_models --project   # returns all the models in a project  --server

def ensure_arg(args, arg_name):
    if not getattr(args, arg_name):
        raise CommandOptionsError(f'Cli option \'{arg_name}\' is required.')


def parse_args():
    """
    Parses command line arguments and runs the sub command.
    """

    common_args = argparse.ArgumentParser(description='Common Args',
                                          add_help=False)

    # Common args:
    # TODO: default project and other credentials
    #  could be stored in something like ~/.fiddler

    common_args.add_argument('--api-endpoint',
                             default='http://api.fiddler.ai',
                             help='Optional override of Fiddler API Endpoint')

    common_args.add_argument('--org', '--organization', '--workspace',
                             help='Organization name. '
                                  'Default is read from config.')

    common_args.add_argument('--auth-key',
                             help='Bearer key used to '
                                  'authenticate REST API requests.')

    model_args = argparse.ArgumentParser(
        description='Parser for --project & --model',
        add_help=False)

    model_args.add_argument('--project',
                            help='Project name in the organization. '
                                 'Default is read from config')

    model_args.add_argument('--model',
                            required=False,
                            help='Name of the model')

    input_args = argparse.ArgumentParser(description='Parser for --input-json',
                                         add_help=False)

    input_args.add_argument('--data', '--input-json',
                            required=False,
                            help='JSON input data such as '
                                 'features (e.g. to execute or explain)')

    parser = argparse.ArgumentParser(prog='fiddler-cli',
                                     description='Fiddler CLI')

    subparsers = parser.add_subparsers(title='Available commands',
                                       dest='command',
                                       metavar='')

    # deploy command
    deploy_desc = 'Deploys repo for the organization on executor'
    deploy_parser = subparsers.add_parser('deploy',
                                          parents=[common_args],
                                          description=deploy_desc,
                                          help=deploy_desc)
    deploy_parser.set_defaults(func=deploy_cmd)

    # clone command
    clone_desc = 'Clones the repo locally'
    clone_parser = subparsers.add_parser('clone',
                                         parents=[common_args],
                                         description=clone_desc,
                                         help=clone_desc)
    clone_parser.set_defaults(func=clone_cmd)

    # train command
    train_desc = 'Trains the model currently deployed'
    train_parser = subparsers.add_parser('train',
                                         parents=[common_args, model_args],
                                         description=train_desc,
                                         help=train_desc)
    train_parser.set_defaults(func=train_cmd)

    # execute command
    execute_desc = 'Runs inference on the the input ' \
                   'using on the specified model'
    execute_parser = subparsers.add_parser('execute',
                                           parents=[common_args,
                                                    model_args, input_args],
                                           description=execute_desc,
                                           help=execute_desc)
    execute_parser.set_defaults(func=execute_cmd)

    # explain command
    explain_desc = 'Explain prediction of the model for the input'
    explain_parser = subparsers.add_parser('explain',
                                           parents=[common_args,
                                                    model_args, input_args],
                                           description=explain_desc,
                                           help=explain_desc)
    explain_parser.set_defaults(func=explain_cmd)

    # generate yaml command
    gen_yaml_desc = 'Generate a YAML file to describe a CSV-formatted dataset'
    gen_yaml_parser = subparsers.add_parser('generate-yaml',
                                            description=gen_yaml_desc,
                                            help=gen_yaml_desc)
    gen_yaml_parser.add_argument('csv_paths', nargs='+',
                                 help='List of paths to CSV files')
    gen_yaml_parser.add_argument('-o', '--output', default=os.getcwd(),
                                 help='Directory to put the YAML file in')
    gen_yaml_parser.set_defaults(func=gen_yaml_cmd)

    # configure command
    configure_desc = 'Update Fiddler configuration'
    configure_parser = subparsers.add_parser('configure',
                                             description=configure_desc,
                                             help=configure_desc)
    configure_parser.set_defaults(func=configure_cmd)

    # publish
    publish_desc = 'Publish an event (such as an ' \
                   'inference event) to Fiddler service'
    publish_parser = subparsers.add_parser('publish',
                                           parents=[common_args,
                                                    model_args, input_args],
                                           description=publish_desc,
                                           help=publish_desc)
    publish_parser.set_defaults(func=publish_cmd)

    # import dataset command
    import_desc = 'Import the given dataset'
    import_parser = subparsers.add_parser('import',
                                          parents=[common_args],
                                          description=import_desc,
                                          help=import_desc)
    import_parser.set_defaults(func=import_cmd)

    args = parser.parse_args()

    if args.command:
        try:
            # Read values configuration file for options
            # if they are not specified on cmdline.
            config = read_config()['default']
            if hasattr(args, 'org') and not args.org:
                args.org = config.get('organization', '')
                if not args.org:
                    raise CommandOptionsError(
                        '--organization option is required. '
                        'Run \'configure\' to set default organization')
            if hasattr(args, 'auth_key') and not args.auth_key:
                args.auth_key = config.get('auth_key', '')
                if not args.auth_key:
                    logging.warning('Auth key is not available. '
                                    'The requests will likely fail.')
            if hasattr(args, 'project') and not args.project:
                args.project = config.get('project', '')

            if hasattr(args, 'api_endpoint') and not args.api_endpoint:
                args.api_endpoint = config.get('api_endpoint', '')

            if hasattr(args, 'data') and args.data:
                if args.data.startswith('@'):
                    with open(args.data[1:], 'r') as file:
                        args.data = file.read()

            if hasattr(args, 'api_endpoint'):
                args.api_endpoint = args.api_endpoint.rstrip('/')

            args.func(args)

        except CommandOptionsError as e:
            logging.error(f'{str(e)}')
            parser.print_help()
            sys.exit(1)
        except Exception as e:
            logging.error(f'Command "{args.command}" failed '
                          f'with the following error: {str(e)}',
                          exc_info=True)
            sys.exit(1)

        sys.exit(0)
    else:
        parser.print_help()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-7s: %(message)s')
    parse_args()


if __name__ == '__main__':
    main()
