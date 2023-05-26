from os import system
from os.path import join, dirname

import click
import json

from utils import project_selector, env_selector, update_project

with open(join(dirname(__file__), 'commands.json')) as f:
    commands = json.load(f)

with open(join(dirname(__file__), 'projects.json')) as f:
    projects = json.load(f)


@click.group()
def cli():
    pass


@cli.command()
@click.option('-p', '--project', default=projects['default']['project'])
@click.option('-e', '--env', default=projects['default']['env'])
def aws_cluster_tunnel(project, env):
    if project == "" or project not in projects.keys():
        project = project_selector(projects)
    if env == "" or env not in projects[project].keys():
        env = env_selector(projects, project)

    click.echo(f"Oppening tunnel to AWS cluster {click.style(f'{project}-{env}', fg='green', bold=True)}...")
    profile = projects[project][env]['profile']
    region = projects[project][env]['region']
    cluster = projects[project][env]['cluster']
    command = commands['aws_cluster_tunnel'].format(profile=profile, region=region, cluster=cluster)
    system(command)

@click.command()
def add_project():
    update_project(projects)


@click.command()
def add_env():
    project = project_selector(projects)
    click.echo(f"Adding project to project {click.style(f'{project}', fg='blue', bold=True)}...")
    update_project(projects, project)


@click.command()
def delete_project():
    project = project_selector(projects)
    deletion_cofirmed = click.confirm(f"Are you sure you want to delete {project}?")
    if deletion_cofirmed:
        click.echo(f"Deleting project {click.style(f'{project}', fg='red', bold=True)}...")
        projects.pop(project)
        with open(join(dirname(__file__), 'projects.json'), 'w') as f:
            json.dump(projects, f, indent=4)
        click.echo(f"Project {click.style(f'{project}', fg='red', bold=True)} deleted!")

    else:
        click.echo(f"Project {click.style(f'{project}', fg='red', bold=True)} was not deleted!")


cli.add_command(aws_cluster_tunnel)
cli.add_command(add_project)
cli.add_command(add_env)
cli.add_command(delete_project)