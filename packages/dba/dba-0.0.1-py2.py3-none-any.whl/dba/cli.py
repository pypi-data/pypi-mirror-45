# -*- coding: utf-8 -*-

"""Console script for dba."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for dba."""
    click.echo("Replace this message by putting your code into "
               "dba.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
