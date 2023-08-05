# Setupmeta Builder

## Usage

Replace your `setup.py` file to:

```py
from setupmeta_builder import setup_it

setup_it(
    version='1.0.0'
)
```

Done!

`setupmeta_builder` try resolve other values like `install_requires` for you.
