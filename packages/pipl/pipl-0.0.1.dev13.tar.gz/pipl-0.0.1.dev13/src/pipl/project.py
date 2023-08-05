'''

manage project structure:

    parent/project_name/
            .pypipipe                   <- identifies a pypipipe project
            server/                     <- devpi server files
            workspaces/
                user/
                    workspace_name

as well as administration
    
    new_project(name, path)
    exists(projct_path)
    start_server(project_path)          <- blocking (test server for now...)
    add_user(login, mail, pass)
    list_indexes()
    create_index(user, index_name, bases=[], volatile=False)

'''

'''

    TODO: 
        Use devpi "-getjson" for listing infos instead of "user --list" and "use -l" ?


'''

import os
from devpi_plumber.client import DevpiClient


def new_project(name, path):

    if not os.path.isdir(path):
        raise ValueError('Folder {!r} does not exists !'.format(path))

    root = os.path.join(path, name)
    if os.path.exists(root):
        raise ValueError('Folder {!r} already exists !'.format(root))

    os.mkdir(root)

    system = os.path.join(root, 'system')
    os.mkdir(system)

    dot_pypipipe = os.path.join(root, '.pypipipe')
    with open(dot_pypipipe, 'w') as fh:
        fh.write('# This is the root of the pypipipe project\n\n')

    server_path = os.path.abspath(
        os.path.join(system, 'server')
    )
    os.mkdir(server_path)

    server_config = os.path.join(system, 'server_config.yaml')
    with open(server_config, 'w') as fh:
        fh.write(
'''
devpi-server:
  serverdir: {}
  host: localhost
  port: 4040
  role: standalone
  no-root-pypi: 1

'''.format(server_path)
        )

    print 'Initializing Server'
    os.system('devpi-server -c {} --init'.format(server_config))

    workspaces_path = os.path.join(root, 'workspaces')
    os.mkdir(workspaces_path)

def find_project_path(from_path):
    print 'Resolving project path', from_path
    current = os.path.abspath(from_path)
    dot_pypipipe = '.pypipipe'
    while current:
        this_dot_pypipipe = os.path.join(current, dot_pypipipe)
        if os.path.exists(this_dot_pypipipe):
            print 'Found project at', current
            return current
        dirname = os.path.dirname(current)
        if dirname == current:
            # case of D:\
            break
        current = dirname
    raise ValueError(
        'Could not find the project root path under {!r}'.format(
            from_path
        )
    )

def _get_server_url_from_config(server_config):
    with open(server_config, 'r') as fh:
        content = fh.read()

    host = 'localhost'
    port = ''
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('host'):
            host = line.split(':')[-1].strip()
        elif line.startswith('port'):
            port = line.split(':')[-1].strip()

    if port:
        port = ':'+port
    return 'http://{}{}'.format(host, port or '')

def start_server(project_path):
    if not os.path.exists(
        os.path.join(
            project_path, '.pypipipe'
        )
    ):
        raise ValueError(
            'Folder {!r} is not a pypipipe project !'.format(
                project_path
            )
        )

    server_url_file = os.path.join(project_path, 'system', '.running_url')
    if os.path.exists(server_url_file):
        raise ValueError(
            'The server seems to be running (see {})'.format(
                server_url_file
            )
        )

    server_config = os.path.join(
        project_path, 'system', 'server_config.yaml'
    )
    server_url = _get_server_url_from_config(server_config)

    with open(server_url_file, 'w') as fh:
        print 'Running Server on', server_url
        fh.write(server_url+'\n')
    try:
        os.system('devpi-server -c {}'.format(server_config))
    finally:
        os.unlink(server_url_file)
    print 'Sever down from', server_url

def get_server_url(project_path):
    server_url_file = os.path.join(project_path, 'system', '.running_url')
    if not os.path.exists(server_url_file):
        raise ValueError(
            'The server does not seem to be running (missing {})'.format(
                server_url_file
            )
        )
    with open(server_url_file) as fh:
        url = fh.read()

    return url.strip()

def add_user(project_path, root_password, login, password, email):
    url = get_server_url(project_path)
    with DevpiClient(url, 'root', root_password) as devpi:
        devpi.create_user(login, password=password, email=email)

def update_user(project_path, root_password, login, password=None, email=None):
    kwargs = {}
    if password is not None:
        kwargs['password'] = password
    if email is not None:
        kwargs['email'] = email
    if not kwargs:
        raise ValueError('No password or email given, nothing to update')

    url = get_server_url(project_path)
    with DevpiClient(url, 'root', root_password) as devpi:
        devpi.modify_user(login, **kwargs)

def list_users(project_path):
    url = get_server_url(project_path)
    with DevpiClient(url) as devpi:
        return devpi.list_users()

def list_indices(project_path, user=None):
    url = get_server_url(project_path)
    with DevpiClient(url) as devpi:
        indices_names = devpi.list_indices(user)
    return indices_names

def create_proj_index(project_path, root_password):
    url = get_server_url(project_path)
    index = 'root/PROJ'
    with DevpiClient(url, 'root', root_password) as devpi:
        devpi.create_index(index, volatile=False, acl_upload=':ANONYMOUS:')

def create_sub_index(project_path, root_password, user_name, index_name, volatile=True, *acl_upload):
    '''
    Create an new index. 
    All *acl_upload must be user logins or ':ANONYMOUS:'. Defaults to ':ANONYMOUS:'
    '''
    url = get_server_url(project_path)
    index = '{}/{}'.format(user_name, index_name)
    bases = 'root/PROJ'
    acl_upload_str = acl_upload and ','.join(acl_upload) or ':ANONYMOUS:'
    with DevpiClient(url, 'root', root_password) as devpi:
        devpi.create_index(
            index, 
            bases=bases,
            volatile=volatile, 
            acl_upload=acl_upload_str
        )

def list_index_packages(project_path, index=None):
    '''
    Returns a list of all packages inside this index.
    If index is None, the default index is used.
    '''
    url = get_server_url(project_path)
    index_name = index or 'root/PROJ'
    with DevpiClient(url) as devpi:
        devpi.use(index_name)
        package_names = devpi.list()

    return package_names
