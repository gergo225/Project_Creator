""" Main file """

import click

project_types = ["Python", "Flutter"]

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
    if public:
        click.echo("Creating PUBLIC repository")
    else:
        click.echo("Creating PRIVATE repository")
    if desc:
        click.echo(f"Description: {desc}")
    if project_type:
        click.echo(f"Type is: {project_type}")
    else:
        click.echo("Empty folder, only Git, no setup")



if __name__ == "__main__":
    create_project()
