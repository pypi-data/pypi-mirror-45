# Setupmeta Builder

## Usage

Replace your `setup.py` file to:

```py
from setupmeta_builder import setup_it

setup_it()
```

Done!

`setupmeta_builder` try resolve other values like `install_requires` for you.

|meta|resolve source|
|:-|:-|
|`packages`|`find_packages()`|
|`name`|packages|
|`version`|`git.tag`|
|`long_description`|file: `README.[md|rst]`|
|`author` and `author_email`|file: `.pkgit.json`|
|`url`|`git.origin.url`|
|`license`|file: `LICENSE`|
|`classifiers`|license and file `.travis.yml`|
|`install_requires`|files: `requirements.txt` or `pipfile`|
|`tests_require`|file: `pipfile`|

Current project is the first example.
