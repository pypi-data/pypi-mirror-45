"""
Machine types commands
"""

import click

from onepanel.commands.base import APIViewController
from onepanel.commands.login import login_required


class EnvironmentViewController(APIViewController):

    def __init__(self,conn):
        APIViewController.__init__(self,conn)

@click.group(help='Environment (machine types) commands group')
@click.pass_context
def environments(ctx):
    ctx.obj['vc'] = EnvironmentViewController(ctx.obj['connection'])


@environments.command('list', help='Show available environments')
@click.pass_context
@login_required
def list_environments(ctx):
    vc = ctx.obj['vc']
    print_data = vc.list(params='/instance_templates?instance_type=mod')
    fields = ['uid','name']
    field_names = ['ID','ENVIRONMENT']
    empty_message = 'No environments found.'
    vc.print_items(print_data,fields,field_names,empty_message)

