#!/usr/bin/env python
"""detect if headphones are plugged"""
import click
import mac_headphones

MODULE_NAME = "mac_headphones"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s' % MODULE_NAME


@click.command()
def _cli():
    if mac_headphones.isplugged():
        print('true')


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
