"""
:mod:`miraiml` provides the following classes:

- :class:`miraiml.HyperSearchSpace` represents the search space of hyperparameters
- :class:`miraiml.Config` defines the general behavior of :class:`miraiml.Engine`
- :class:`miraiml.Engine` manages the optimization process

You can import them by doing

>>> from miraiml import HyperSearchSpace, Config, Engine
"""

__version__ = '1.0.0'

from .main import HyperSearchSpace, Config, Engine

__all__ = ['HyperSearchSpace', 'Config', 'Engine']
