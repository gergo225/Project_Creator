""" Main file """

import os
import sys
import subprocess
import click
import github

from app.my_secrets import USERNAME, PERSONAL_TOKEN


class ProjectType:
    """The type of the project

    This is the language the project is written in.
    """

    PYTHON = "Python"
    FLUTTER = "Flutter"


project_types = [ProjectType.PYTHON, ProjectType.FLUTTER]


def create_folder(name):
    """Create a new folder for the project in the current directory

    Params
    ------
    name : str
        Name of the project and folder to create
    """
    click.echo("Creating project folder...")
    path = os.path.join("C:\\Users\\user\\Desktop", name)  # TODO: change later

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


def create_python_project():
    """ Set up a Python project """
    global_python = "C:\\Python38\\python.exe" # change according to your Python location
    run_commands([global_python, "-m", "venv", "venv"])

    # venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    # run_commands([venv_python, "-m", "pip", "install", "pylint"])
    # run_commands([venv_python, "-m", "pip", "install", "black"])

    os.mkdir(os.path.join(os.getcwd(), ".vscode"))
    file_path = os.path.join(os.getcwd(), ".vscode", "settings.json")
    with open(file_path, "w") as settings:
        settings.writelines(
            "{\n"
            '\t"python.pythonPath": "venv\\\Scripts\\\python.exe",\n'  # pylint: disable=anomalous-backslash-in-string
            '\t"python.linting.pylintEnabled": true,\n'
            '\t"python.linting.enabled": true,\n'
            '\t"python.formatting.provider": "black",\n'
            '\t"python.terminal.activateEnvInCurrentTerminal": true\n'
            "}\n"
        )

    with open(".gitignore", "w") as gitignore:
        gitignore.write("__pycache__/\n")
        gitignore.write("venv/\n")

    app_folder = os.path.join(os.getcwd(), "app")
    os.mkdir(app_folder)

    main_py_file = os.path.join(app_folder, "__main__.py")
    with open(main_py_file, "w"):
        pass

    init_py_file = os.path.join(app_folder, "__init__.py")
    with open(init_py_file, "w"):
        pass

    # run_commands(
    #     [venv_python, "-", "pip", "freeze", ">", "requirements.txt"], shell=True
    # )


def create_flutter_project():
    """ Set up a Flutter project """
    # TODO: Manage to access variables outside the virtual environment
    # run_commands(["flutter", "create", "."])
    click.echo("Sorry, Flutter projects can't be created just yet... :(")


def create_type_of_project(project_type: str):
    """ Sets up a project for the appropriate type"""
    if project_type == ProjectType.PYTHON:
        click.echo("Setting up a Python project...")
        create_python_project()
        click.echo("-> Python project set up")
    elif project_type == ProjectType.FLUTTER:
        click.echo("Setting up a Flutter project...")
        create_flutter_project()
        click.echo("-> Flutter project set up")


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
    public_or_private = "public"
    if private:
        public_or_private = "private"
    click.echo(f"Creating {public_or_private} GitHub repository...")

    github_client = github.Github(login_or_token=USERNAME, password=PERSONAL_TOKEN)
    user = github_client.get_user()

    if not description:
        description = github.GithubObject.NotSet
    if not private:
        private = github.GithubObject.NotSet

    user.create_repo(name, description=description, private=private)
    click.echo("-> GitHub repository created")


def add_remote_branch_and_push(name):
    """Adds a remote to the local Git, creates a master branch and
    pushes all files

    Params
    ------
    name : str
        The name of the project, based on which we can
        generate the remote's address
    """
    name = name.replace(" ", "-")
    remote = f"https://github.com/{USERNAME}/{name}.git"
    run_commands(["git", "remote", "add", "origin", remote])

    run_commands(["git", "branch", "-M", "master"])

    run_commands(["git", "push", "-u", "origin", "master"])
    click.echo("-> Files pushed to GitHub")


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

    project_path = os.path.join("C:\\Users\\user\\Desktop", name)  # TODO: change later
    os.chdir(project_path)

    add_readme(name)

    initialize_git()

    create_type_of_project(project_type)

    commit_all_files()

    create_github_repo(name=name, description=desc, private=not public)

    add_remote_branch_and_push(name=name)

    click.echo("-- Project successfully created! --")


if __name__ == "__main__":
    create_project()  # pylint: disable=no-value-for-parameter
