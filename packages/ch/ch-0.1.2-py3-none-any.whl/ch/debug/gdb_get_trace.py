import logging
import os
import subprocess
import sys
import tempfile

from itertools import chain
from pathlib import Path

import requests

from more_itertools import flatten


logger = logging.getLogger(__name__)


python_gdb_url = os.environ.get(
    'PYTHON_GDB_URL',
    'https://raw.githubusercontent.com/python/cpython/master/Tools/gdb/libpython.py',
)


def get_python_gdb(pid):
    """Get applicable python-gdb.py given a pid.
    """
    python = Path(f'/proc/{pid}/exe').resolve()
    python_gdb = Path(f'{python}-gdb.py')
    if python_gdb.exists():
        return python_gdb

    # Otherwise we need to retrieve it.
    response = requests.get(python_gdb_url)
    response.raise_for_status()
    fd, name = tempfile.mkstemp(suffix='.py', text=True)
    os.write(fd, response.content)
    os.fsync(fd)
    os.close(fd)
    return Path(name)


def run_python_gdb(pid, commands):
    attach_args = [
        # Avoid warning in case there is actually a python-gdb.py in the
        # correct place, we manually source it later.
        ['-ex', 'set auto-load no'],
        # Use this as the executable file.
        ['-ex', f'file /proc/{pid}/exe'],
        ['-ex', f'attach {pid}'],
    ]

    python_gdb = get_python_gdb(pid)
    if python_gdb:
        attach_args.append(['-ex', f'source {python_gdb}'])

    command_args = [['-ex', c] for c in commands]
    args = [
        'gdb',
        # No introductory message.
        '--batch',
        # No .gdbinit.
        '--nx',
        *flatten(attach_args),
        *flatten(command_args),
        # So we aren't prompted for confirmation.
        '-ex', 'set confirm off',
        '-ex', 'quit',
    ]
    logger.debug('Running %s', args)
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout.decode('utf-8')


def get_process_stack(pid):
    commands = [
        'info threads',
        'thread apply all bt',
        'thread apply all py-bt',
    ]
    return run_python_gdb(pid, commands)


def main(pid):
    stacks = get_process_stack(pid)
    print(stacks)


if __name__ == '__main__':
    main(sys.argv[1])
