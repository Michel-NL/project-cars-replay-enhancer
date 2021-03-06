"""
Provides base class for dynamic objects. Dynamic objects are those
objects that update continuously based on the telemetry feed.
"""

import abc

from StaticBase import StaticBase

class DynamicBase(StaticBase, metaclass=abc.ABCMeta):
    """
    Defines base class for dynamic objects, including default object
    return methods. Methods are named to be compatible with MoviePy's
    UpdatedVideoClip object. Typically, they will be called from
    that object.

    To update the object state, `update` is called.

    To get the representation of the dynamic object at the current
    world state, `to_frame` is called. Execution chain is `to_frame` ->
    `update` -> `_make_material` -> `_write_data`.

    To get the mask of the dynamic oject, `make_mask` is called.
    Exectuion chain is `make_mask` -> `update` -> `_make_material`.
    """
    @property
    @abc.abstractmethod
    def ups(self):
        """Updates per second of the simulation."""

    @ups.setter
    @abc.abstractmethod
    def ups(self, value):
        return

    @property
    @abc.abstractmethod
    def clip_t(self):
        """Current time in simulation."""

    @clip_t.setter
    @abc.abstractmethod
    def clip_t(self, value):
        return

    @abc.abstractmethod
    def update(self):
        """Update the simulation including updating clip_t"""
