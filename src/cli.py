import click

from .commands import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    complete_all_tasks,
    delete_all_tasks,
)


@click.group()
@click.version_option(version="0.1.0", prog_name="click")
def cli() -> None:
    pass


cli.add_command(add_task, name="add")
cli.add_command(add_task, name="a")

cli.add_command(list_tasks, name="list")
cli.add_command(list_tasks, name="l")

cli.add_command(complete_task, name="complete")
cli.add_command(complete_task, name="c")

cli.add_command(delete_task, name="delete")
cli.add_command(delete_task, name="d")
cli.add_command(complete_all_tasks, name="complete-all")
cli.add_command(complete_all_tasks, name="ca")

cli.add_command(delete_all_tasks, name="delete-all")
cli.add_command(delete_all_tasks, name="da")


if __name__ == "__main__":
    cli()
