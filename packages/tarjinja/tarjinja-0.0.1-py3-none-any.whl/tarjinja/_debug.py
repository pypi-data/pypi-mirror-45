import sys
import json
import click
from jinja2 import Template


@click.command()
@click.option("--arg", default="{}")
@click.argument("input", type=click.File("r"), default=sys.stdin)
def main(input, arg):
    tmpl = Template(input.read())
    data = json.loads(arg)
    click.echo(tmpl.render(**data))


if __name__ == "__main__":
    main()
