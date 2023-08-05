# setup_utility

Utility functions for setuptools utilities - my standard source checks, testing, cleanup, deployment, etc.

See [LICENSE](LICENSE) for important licensing information.

## Installing

Your `setup.py` will need `jfaleiro.setup_utility` to start - so you either make sure you have it pre-installed using pip:

```bash
pip install jfaleiro.setup_utility
```

or add this on the very top of your `setup.py` and forget about it moving forward.

```python
try:
    import setup_utility
except ModuleNotFoundError as e:
    from pip._internal import main
    assert main('install jfaleiro.setup_utility'.split()) == 0
    
from setup_utility import (
    BehaveTestCommand,
    CleanCommand,
    LicenseHeaderCommand,
    version_from_git,
)
```

and

```python
cmd_classes = {
    'license_headers': LicenseHeaderCommand,
    'behave_test': BehaveTestCommand,
    'clean': CleanCommand,
}
```

## Using

```bash
python setup.py --help-commands
```

You should have commands `license_headers`, `clean`, and `behave_test` listed. To know what you can configure try `python setup.py <command> --help`:

```bash
python setup.py license_headers --help
```

You can use command line parameters or add the same commands on `setup.cfg`:


```
[license_headers]
header-file = HEADER

[aliases]
test=pytest

[tool:pytest]
addopts = --cov=setup_utility --cov-report html
```

You can also produce your version number from standard git information (tag, branch name, and number of differences):

```python
setup(
	...
    version=version_from_git(),
	...
)
```

Release tags `release/<version>` with `nnn` differences from master will produce version `<version>.dev<nnn>` and a tagged version `<tag>` on master will produce the version `<tag>`. Everything else will produce `master.dev<nnn>` for master or `no-version.dev<nnn>` for any other branch. 


Enjoy.
