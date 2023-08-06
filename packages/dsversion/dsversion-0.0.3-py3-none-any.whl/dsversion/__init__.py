import distutils.spawn
import os
import subprocess
import sys

this = sys.modules[__name__]
this.cache = {}

def get_version_str(cwd, cached_version=[]):
    cwd = os.path.realpath(cwd)
    if not os.path.exists(cwd):
        raise FileNotFoundError(f'Path {cwd} does not exist...')
    if not os.path.isdir(cwd):
        cwd = os.path.dirname(cwd)

    if cwd in this.cache:
        return this.cache[cwd]

    # Default values.
    version = '0.0.0'
    version_suffix = ''

    # Query a .version file for the 'main' version number.
    version_file = os.path.join(cwd, '.version')
    if os.path.exists(version_file):
        with open(version_file, 'rt') as fid:
            version_split = fid.readline().strip().split('+')
            version = version_split[0]
            if len(version_split) > 1:
                version_suffix = '+'.join(version_split[1:])

    # In case the `site-packages` folder is detected, it is assumed that this is not a dev install and no
    # dynamic version numbering is required.
    two_up = os.path.basename(os.path.dirname(os.path.dirname(__file__))).lower()
    if two_up != 'site-packages':
        # In case a git working copy is found, append it to the full version number.
        git = distutils.spawn.find_executable('git')

        if git:
            command = [git, 'describe', '--always', '--match', "NOT A TAG", '--dirty']
            wd = cwd if os.path.isdir(cwd) else os.path.dirname(cwd)
            revision = subprocess.check_output(command, cwd=wd).decode().strip()
            version_suffix = '+dev.' + revision

    this.cache[cwd] = '+'.join([version, version_suffix])
    return get_version_str(cwd)

