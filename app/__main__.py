""" Main file """

import os
import sys
import subprocess
import click
import github

from app.my_secrets import USERNAME, PERSONAL_TOKEN

project_types = ["Python", "Flutter"]


def create_folder(name):
    """Create a new folder for the project in the current directory

    Params
    ------
    name : str
        Name of the project and folder to create
    """
    click.echo("Creating project folder...")
    path = os.path.join(os.getcwd(), name)

    try:
        os.mkdir(path)
    except FileExistsError:
        click.echo("Error: Project folder with same name already exits!")
        click.echo("exiting...")
        sys.exit()
    click.echo("-> Folder created")


def add_readme(name):
    """Add a README.md file to the project

    Params
    ------
    name : str
        The name of the project to add the README to
    """
    click.echo("Adding README.md to folder...")
    with open("README.md", "w") as readme:
        readme.write(f"# {name.title()}\n")
        readme.write("This is the first version of the README")
    click.echo("-> README added")


def run_commands(commands: list):
    """Run a subprocess and suppress the output

    Params
    ------
    commands : list of str
        The commands to execute
    """
    subprocess.run(
        commands,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )


def initialize_git():
    """ Initialize a Git repository """
    click.echo("Initializing Git repository...")
    run_commands(["git", "init"])
    click.echo("-> Git repo initialized")


def commit_all_files():
    """ Commit all local files with the message "First commit" """
    click.echo("Commiting the 'First commit'...")
    run_commands(["git", "add", "."])
    run_commands(["git", "commit", "-m", "First commit"])
    click.echo("-> First commit completed")


def create_github_repo(name, description, private):
    """Creates a new GitHub repository with the project name and description

    Params
    ------
    name : str
        The name of the project
    description : str, optional
        The description of the project
    private : bool, optional
        Whether the repo should be private or not
    """
    click.echo("Creating GitHub repository...")

    g = github.Github(login_or_token=USERNAME, password=PERSONAL_TOKEN)
    user = g.get_user()

    if not description:
        description = github.GithubObject.NotSet
    if not private:
        private = github.GithubObject.NotSet

    user.create_repo(name, description=description, private=private)
    click.echo("-> GitHub repository created")


@click.command()
@click.argument("name")
@click.option(
    "--public/--private",
    default=True,
    help="Whether the GitHub repository should be public or private\n"
    + "[default: True, --public]",
)
@click.option("-d", "--desc", "--description", help="Description of the GitHub repo")
@click.option(
    "-t",
    "--project-type",
    "--type",
    type=click.Choice(project_types, case_sensitive=False),
    help="The type of the project to create",
)
def create_project(name, public, desc, project_type):
    """ Creates a new project """
    click.echo(f"Creating project: {name}")
    create_folder(name)

    project_path = os.path.join(os.getcwd(), name)
    os.chdir(project_path)

    add_readme(name)

    initialize_git()

    commit_all_files()

    create_github_repo(name=name, description=desc, private=not public)

    if project_type:
        click.echo(f"Type is: {project_type}")
    else:
        click.echo("Empty folder, only Git, no setup")

    if public:
        click.echo("Creating PUBLIC repository")
    else:
        click.echo("Creating PRIVATE repository")
    if desc:
        click.echo(f"Description: {desc}")


if __name__ == "__main__":
    create_project()
