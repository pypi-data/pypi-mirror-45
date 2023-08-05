A minimal, no-dependencies lock file mechanism, creating a temporary file to signal that a
specific file should not be touched by other scripts, or instances of the same script.

Created for [Europe 1° Warmer](https://www.onedegreewarmer.eu/).

This is module does _not_ implement OS level file locking. For that, see e.g. the built-in [lockfile](https://pythonhosted.org/lockfile/lockfile.html) module, [zc.lockfile](https://pypi.org/project/zc.lockfile/), or other similar projects.

## Installation

```sh
pip install tmplockfile
```

## Usage

```python3
from tmplockfile import LockFile, ResourceLocked

with LockFile("data.csv") as lockfile:
    # Do things involving data.csv here
    #
    # A lock-file is temporarily placed in the same directory,
    # in a way that avoids the most obvious race conditions.
    # The variable `lockfile` contains the name of the lock-file,
    # e.g. `data.csv~lock`.

except ResourceLocked:
    print("Another script is currently working on data.csv. Try again later!")
```

## Changelog

- 0.0.3

  - Don't crash when no lockfile could be created
