
import os
import getpass

import click

from . import autopack, project, workspace


@click.group()
def pipl():
    pass

#
#   PROJECT
#

@pipl.group()
def proj():
    pass

@proj.command('new')
@click.argument('name')
@click.argument('path')
def new_project(name, path):
    '''
    Creates a new project.
    '''
    click.echo(
        "Create project {!r} under {!r}".format(
            name, path
        )
    )
    project.new_project(name, path)

@proj.command('start')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def start_server(project_path):
    '''
    Start current project's server in **foreground**.
    '''
    project_path = project.find_project_path(project_path)
    click.echo('Staring server for "{}"'.format(project_path))
    project.start_server(project_path)

#
#   PROJECT USERS
#


@proj.group()
def user():
    '''
    Project users administration.
    '''
    pass

@user.command('list')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def list_users(project_path='.'):
    '''
    List the users in the project.
    '''
    project_path = project.find_project_path(project_path)
    users = project.list_users(project_path)
    click.echo('{} Users:'.format(len(users)))
    for user in users:
        click.echo('{:>20}'.format(user))

@user.command('add')
@click.argument('root_password')
@click.argument('login')
@click.argument('password')
@click.option('-e', '--email', default=None, help='user email address')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def add_user(root_password, login, password, email, project_path='.'):
    '''
    Add a user to the project.
    '''
    project_path = project.find_project_path(project_path)
    project.add_user(
        project_path, 
        root_password,
        login, 
        password,
        email,
    )

@user.command('set')
@click.argument('root_password')
@click.argument('login')
@click.option('--password', default=None, help='set user password')
@click.option('-e', '--email', default=None, help='set user email')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)

def set_user(root_password, login, password=None, email=None, project_path='.'):
    '''
    Update the given user password or email.
    '''
    project_path = project.find_project_path(project_path)
    project.update_user(
        project_path, 
        root_password,
        login, 
        password,
        email,
    )

#
#   PROJECT INDEXES
#

@proj.group()
def index():
    '''
    Project indexes administration.
    '''

@index.command('list-indexes')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def list_indexes(project_path='.'):
    '''
    List the indexes in the project.
    '''
    project_path = project.find_project_path(project_path)
    names = project.list_indices(project_path)
    click.echo('{} Indexes:'.format(len(names)))
    for name in names:
        click.echo('{:>20}'.format(name))


@index.command('create-default')
@click.argument('root_password')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def create_default_index(root_password, project_path='.'):
    '''
    Create the project's default index (root/PROJ).
    '''
    project_path = project.find_project_path(project_path)
    click.echo('Creating Project Index for "{}"'.format(project_path))
    project.create_proj_index(project_path, root_password)

# @task
# def create_sub_index(context, root_password, user_name, index_name, project_path='.'):
#     '''
#     List the indices in the project.
#     '''
#     project_path = project.find_project_path(project_path)
#     print 'Creating Project Index for', project_path
#     project.create_sub_index(project_path, root_password, user_name, index_name)

@index.command('list')
@click.option('-i', '--index_name', default=None)
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def list_index_packages(index_name=None, project_path='.'):
    '''
    List packages inside the index (defaults to "root/PROJ")
    '''
    project_path = project.find_project_path(project_path)
    names = project.list_index_packages(project_path)
    click.echo('{} Packages:'.format(len(names)))
    for name in names:
        click.echo('{:>30}'.format(name))



#
#
#   WORKSPACES
#
#

@pipl.group()
def work():
    pass

@work.command('create')
@click.argument('workspace_path')
@click.option(
    '-p', '--project-path', default='.', 
    help='Override current path'
)
def create_workspace(workspace_path, project_path='.'):
    '''
    Create a new workspace in the project.
    '''
    project_path = project.find_project_path(project_path)
    click.echo(
        "Create workspace {!r} in project {!r}".format(
            workspace_path, project_path
        )
    )
    workspace.create_workspace(
        project_path, workspace_path
    )

@work.command('shell')
@click.option(
    '-p', '--workspace-path', default='.', 
    help='Override current path'
)
def workspace_shell(workspace_path='.'):
    '''
    Open a shell with this workspace's virtualenv
    '''
    workspace_path = workspace.find_workspace_path(workspace_path)
    workspace.shell(workspace_path)


@work.command('py')
@click.option(
    '-p', '--workspace-path', default='.', 
    help='Override current path'
)
def workspace_python(workspace_path='.'):
    '''
    Launch a python REPL with this workspace virtual env
    '''
    workspace_path = workspace.find_workspace_path(workspace_path)
    workspace.python(workspace_path)

@work.command('upload')
@click.argument('pack_name')
@click.argument('password')
@click.option('-u', '--user', default=None)
@click.option(
    '-p', '--workspace-path', default='.', 
    help='Override current path'
)
def upload_package(pack_name, password, user=None, workspace_path='.'):
    '''
    Upload a package to the default index.

    user defaults to the current user.
    workspace_path defaults to the current directory

    '''
    user = user or getpass.getuser()
    workspace_path = workspace.find_workspace_path(workspace_path)
    workspace.upload_package(
        workspace_path, pack_name, 
        user, password
    )

#
#
#   PACKAGES
#
#

@pipl.group()
def pack():
    pass

@pack.command('create')
@click.argument('name')
@click.option(
    '-p', '--workspace-path', default='.', 
    help='Override current path'
)
def create_package(name, workspace_path='.'):
    '''
    Create a new package in the current workspace.
    '''
    workspace_path = workspace.find_workspace_path(workspace_path)
    click.echo(
        'Creating new package "{}" in workspace "{}"'.format(
            name, workspace_path
        )
    )
    workspace.new_package(workspace_path, name)

@pack.command('show')
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def show_package(package_path='.'):
    '''
    Show package setup for the given package.
    '''
    setup_filename = autopack.find_package_setup_file(package_path)
    autopack.show_setup(setup_filename)


@pack.group()
def bump():
    pass

@bump.command('major')
@click.argument('comment', default=None)
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def bump_version_major(comment=None, package_path='.'):
    '''Major version bump'''
    setup_filename = autopack.find_package_setup_file(package_path)
    autopack.bump_version_major(setup_filename)

@bump.command('minor')
@click.argument('comment', default=None)
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def bump_version_minor(comment=None, package_path='.'):
    '''Minor version bump'''
    setup_filename = autopack.find_package_setup_file(package_path)
    autopack.bump_version_minor(setup_filename)

@bump.command('patch')
@click.argument('comment', default=None)
@click.option(
    '-p', '--package-path', default='.', 
    help='Override current path'
)
def bump_version_patch(comment=None, package_path='.'):
    '''Patch version bump'''
    setup_filename = autopack.find_package_setup_file(package_path)
    autopack.bump_version_patch(setup_filename)


def main():
    pipl()

if __name__ == '__main__':
    main()
