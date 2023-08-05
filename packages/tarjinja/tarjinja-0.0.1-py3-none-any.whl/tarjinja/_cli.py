import os
import sys
import click
import yaml
from .choice import input_items, output_items, filter_items
from .multifilter import MultiFilter
from .iface import Pipeline
from logging import getLogger, basicConfig, INFO, DEBUG

log = getLogger(__name__)

VERSION = "0.0.1"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def set_verbose(flag):
    fmt = '%(asctime)s %(levelname)s %(message)s'
    if flag:
        basicConfig(level=DEBUG, format=fmt)
    else:
        basicConfig(level=INFO, format=fmt)


def auto_detect(filename, defval):
    extmap = {
        ".tar.gz": "Tar",
        ".tar.bz2": "Tar",
        ".tar.xz": "Tar",
        ".tar": "Tar",
        ".tgz": "Tar",
        ".tbz2": "Tar",
        ".txz": "Tar",
        ".zip": "Zip",
    }
    if os.path.isdir(filename):
        return "Dir"
    for k, v in extmap.items():
        if filename.endswith(k):
            return v
    return defval


def do_pipe(in_type, out_type, input, output, filter_type, vals, thru=None):
    log.debug("input: %s (%s), output: %s (%s), filter: %s",
              input, in_type, output, out_type, filter_type)
    input_val = dict(input_items()).get(in_type)(input)
    output_val = dict(output_items()).get(out_type)(output)
    if isinstance(filter_type, (list, tuple)):
        if len(filter_type) == 1:
            filter_val = dict(filter_items()).get(filter_type[0])()
        else:
            filter_val = MultiFilter()
            for f in filter_type:
                filter_val.add_filter(dict(filter_items()).get(f)())
    else:
        filter_val = dict(filter_items()).get(filter_type)()
    pipeline = Pipeline(input_val, filter_val, output_val, thru)
    pipeline.render(vals)


@cli.command()
@click.option("--input", type=click.Path(), required=True)
@click.option("--output", type=click.Path(), required=True)
@click.option("--out-type", type=click.Choice(dict(output_items())), required=True)
@click.option("--in-type", type=click.Choice(dict(input_items())), required=True)
@click.option("--filter-type", type=click.Choice(dict(filter_items())), multiple=True)
@click.option("--value", type=click.File('r'), default=sys.stdin)
@click.option("--verbose/--no-verbose")
@click.option("--thru", type=str, default=None)
def copy(in_type, out_type, filter_type, input, output, value, verbose, thru):
    vals = yaml.load(value, Loader=yaml.FullLoader)
    set_verbose(verbose)
    do_pipe(in_type, out_type, input, output, filter_type, vals, thru)


@cli.command()
@click.option("--filter-type", type=click.Choice(dict(filter_items())), default="Jinja")
@click.option("--value", type=click.File('r'), default=sys.stdin)
@click.option("--verbose/--no-verbose")
@click.argument("output", type=click.Path(), required=True)
@click.argument("input", type=click.Path(), required=True)
def tarc(output, input, value, filter_type, verbose):
    vals = yaml.load(value, Loader=yaml.FullLoader)
    set_verbose(verbose)
    out_type = auto_detect(output, "Tar")
    in_type = auto_detect(input, "Dir")
    do_pipe(in_type, out_type, input, output, filter_type, vals)


@cli.command()
@click.option("--filter-type", type=click.Choice(dict(filter_items())), default="Jinja")
@click.option("--value", type=click.File('r'), default=sys.stdin)
@click.option("--verbose/--no-verbose")
@click.argument("input", type=click.Path(), required=True)
@click.argument("output", type=click.Path(), required=True)
def tarx(output, input, value, filter_type, verbose):
    vals = yaml.load(value, Loader=yaml.FullLoader)
    set_verbose(verbose)
    out_type = auto_detect(output, "Dir")
    in_type = auto_detect(input, "Tar")
    do_pipe(in_type, out_type, input, output, filter_type, vals)


@cli.command()
@click.option("--filter-type", type=click.Choice(dict(filter_items())), default="Jinja")
@click.option("--value", type=click.File('r'), default=sys.stdin)
@click.option("--verbose/--no-verbose")
@click.option("--dry/--no-dry")
@click.argument("input", type=click.Path(), required=True)
@click.argument("output", type=click.Path(), required=True)
def rsync(output, input, value, filter_type, verbose, dry):
    vals = yaml.load(value, Loader=yaml.FullLoader)
    set_verbose(verbose)
    in_type = auto_detect(input, "Single")
    if dry:
        out_type = "List"
    else:
        out_type = auto_detect(output, "Dir")
    do_pipe(in_type, out_type, input, output, filter_type, vals)


if __name__ == "__main__":
    cli()
