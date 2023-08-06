# autohooks-plugin-autopep8 [![Build Status](https://travis-ci.com/LeoIV/autohooks-plugin-autopep8.svg?branch=master)](https://travis-ci.com/LeoIV/autohooks-plugin-autopep8)

An [autohooks](https://github.com/greenbone/autohooks) plugin for python code
formatting via [autopep8](https://github.com/hhatto/autopep8).

## Installation

### Install using pip

You can install the latest stable release of autohooks-plugin-autopep8 from the
Python Package Index using [pip](https://pip.pypa.io/):

    pip install autohooks-plugin-autopep8

Note the `pip` refers to the Python 3 package manager. In a environment where
Python 2 is also available the correct command may be `pip3`.

### Install using pipenv

It is highly encouraged to use [pipenv](https://github.com/pypa/pipenv) for
maintaining your project's dependencies. Normally autohooks-plugin-autopep8 is
installed as a development dependency.

    pipenv install --dev autohooks-plugin-autopep8

## Usage

To activate the autopep8 autohooks plugin please add the following setting to your
`pyproject.toml` file.

````toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.autopep8"]
````
### Customizing the `autopep8` behavior

To pass options to `autopep8`, you have to add an additional 
````toml
[tool.autohooks.plugins.autopep8]
option = value
````

block to your `pyproject.toml` file. Possible options are explained in the following.
#### Included files
By default, autohooks plugin autopep8 checks all files with a *.py* ending. If only
files in a sub-directory or files with different endings should be formatted,
just add the following setting:

```toml
include = ['foo/*.py', '*.foo']
````

#### Experimental `autopep8` features
Experimental features can be enabled by adding the following setting:
```toml
experimental-features = true
```
The are disabled by default.
#### Ignored errors
You can specificy which errors should be ignored as follows:
````toml
ignore_errors = ['E101', ...]
````
where the errors should match to the [list of errors fixed by `autopep8`](https://github.com/hhatto/autopep8).

The default is `['E226', 'E24', 'W50', 'W690']`.

#### Maximum line length
The maximum allowed line length can be set with
````toml
max_line_length = 79
````

The default is 79.




## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/LeoIV/autohooks-plugin-autopep8/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/LeoIV/autohooks-plugin-autopep8/issues)
first.

## License

Licensed under the [GNU General Public License v3.0 or later](LICENSE).
