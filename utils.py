import json
from os.path import dirname, join

import click
import inquirer


def project_selector(projects):
    projects_list = list(projects.keys())
    projects_list.pop(0)
    select_project_prompt = [
        inquirer.List('project',
                      message="Choose the project you want",
                      choices=projects_list,
                      ),
    ]
    return inquirer.prompt(select_project_prompt)['project']


def env_selector(projects, selected_project):
    select_env_prompt = [
        inquirer.List('env',
                      message="Choose the env you want",
                      choices=projects[selected_project].keys(),
                      ),
    ]
    return inquirer.prompt(select_env_prompt)['env']


def update_project(projects, project_name="", project_env="", project_profile="", project_region="",
                   project_cluster=""):
    if project_name == "":
        project_name = click.prompt('Project name', type=str)
    if project_env == "":
        project_env = click.prompt('Project environment', type=str)
    if project_profile == "":
        project_profile = click.prompt('Project profile', type=str)
    if project_region == "":
        project_region = click.prompt('Project region', type=str)
    if project_cluster == "":
        project_cluster = click.prompt('Project cluster', type=str)

    projects[project_name] = {
        project_env: {
            'profile': project_profile,
            'region': project_region,
            'cluster': project_cluster
        }
    }

    with open(join(dirname(__file__), 'projects.json'), 'w') as f:
        json.dump(projects, f, indent=4)
