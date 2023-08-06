import os
import sys
import warnings

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

    version_file = os.path.join(cwd, '.version')
    if os.path.exists(version_file):
        with open(version_file, 'rt') as fid:
            this.cache[cwd] = fid.readline().strip()
        return get_version_str(cwd)

    # Try to get the git revision.
    import distutils.spawn
    import subprocess
    git = distutils.spawn.find_executable('git')

    if git:
        command = [git, 'describe', '--always', '--match', "NOT A TAG", '--dirty']
        wd = cwd if os.path.isdir(cwd) else os.path.dirname(cwd)
        revision = subprocess.check_output(command, cwd=wd).decode().strip()
        this.cache[cwd] = '0.0.0+dev.' + revision
        return get_version_str(cwd)

    warnings.warn('Could not find .version file and could not determine git revision')
    this.cache[cwd] = '0.0.0+dev'
    return get_version_str(cwd)

