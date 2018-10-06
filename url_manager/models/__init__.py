"""
Models initialisation module.

Note that the model files cannot be be imported directly with
`python -m models/{model}.py`, if they have been included here. Because
this __init__ file will add the table names to the name space before the
file is run, which causes a conflict.
"""
# Create an _`_all__` list here, using values set in other application files.
from .model import __all__ as xModel
__all__ = xModel

# Make model classes available on the models module.
from .model import *
