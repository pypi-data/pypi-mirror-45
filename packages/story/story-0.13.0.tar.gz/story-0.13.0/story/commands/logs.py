# -*- coding: utf-8 -*-
import re
import sys
from datetime import datetime

from blindspin import spinner

import click

import requests

from .. import cli
from .. import options
from ..api import Apps


@cli.cli.command()
@click.option('--follow', '-f', is_flag=True, help='Follow the logs')
@click.option('--all', '-a', is_flag=True,
              help='Return logs from all services')
@click.option(
    '--level',
    '-l',
    default='info',
    type=click.Choice(['debug', 'info', 'warning', 'error']),
    help='Specify the minimum log level',
)
@options.app()
def logs(follow, all, app, level):
    """Fetch the logs of your Storyscript Cloud app."""

    if follow:
        click.echo('-f (following log output) is not supported yet.')
        return

    cli.user()

    url = 'https://stories.storyscriptapp.com/logs'
    click.echo(f'Retrieving logs of {app}… ', nl=False)
    params = {'access_token': cli.get_access_token(), 'level': level}

    if all:
        params['all'] = 'true'

    with spinner():
        params['app_id'] = Apps.get_uuid_from_hostname(app)
        r = requests.get(url, params=params)

    click.echo()

    try:
        arr = r.json()
        assert isinstance(arr, list)
    except BaseException:
        click.echo(
            'Logs for your app aren\'t available right now.\n'
            'If this error persists, please shoot us an email '
            'on support@storyscript.io',
            err=True,
        )
        sys.exit(1)

    cli.track('App Logs Retrieved', {'App name': app, 'Log count': len(arr)})

    if len(arr) == 0:
        click.echo(f'No logs found for {app}')
        return

    arr.reverse()  # Latest is at the head.

    for log in arr:
        if not all:
            message: str = log['payload']['message']
            level = log['payload']['level']
        else:
            message: str = log['payload']
            level = log['severity']

        # In some cases, if the log line is a map,
        # the log service will convert it to a json map.
        message = str(message)

        level = level[:6].rjust(6)

        # Replace the ":" in the timezone field for datetime.
        ts = log['timestamp']
        ts = ts[0: ts.rindex(':')] + ts[ts.rindex(':') + 1:]
        if all:
            # Truncate milliseconds from the date
            # (sometimes this appears, and sometimes it doesn't appear)
            ts = re.sub(r'\.[0-9]*', '', ts)
            date = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S%z')
        else:
            date = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f%z')

        pretty_date = date.astimezone().strftime('%b %d %H:%M:%S')

        tag = None
        if all:
            tag = log['resource'][1]['container_name'][:21]

        colourize_and_print(pretty_date, tag, level, message.strip())


def colourize_and_print(date, tag, level, message):
    level_col = 'green'  # Default for info.
    level = level.lower()

    if 'debug' in level:
        level_col = 'blue'
    elif 'warn' in level:
        level_col = 'yellow'
    elif 'crit' in level or 'error' in level:
        level_col = 'red'

    if tag:
        click.echo(
            f'{click.style(date, fg="white")} '
            f'{click.style(level.upper(), fg=level_col)} '
            f'{click.style(tag, fg="blue")}: '
            f'{message}'
        )
    else:
        click.echo(
            f'{click.style(date, fg="white")} '
            f'{click.style(level.upper(), fg=level_col)} '
            f'{message}'
        )
