#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Shared metaclasses."""

__all__ = ("SingletonMeta",)

# Standard Library
import abc
import threading
import typing


class SingletonMeta(abc.ABCMeta):
    """Metaclass for Singleton.

    Main goals: not need to implement __new__ in singleton classes
    """

    _instances: typing.Dict[type, typing.Any] = {}
    _lock: threading.RLock = threading.RLock()

    def __call__(cls: "SingletonMeta", *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Singleton."""
        with cls._lock:
            if cls not in cls._instances:
                # noinspection PySuperArguments
                cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingleLock(abc.ABCMeta):
    """Metaclass for creating classes with single lock instance per class."""

    def __init__(cls, name: str, bases: typing.Tuple[type, ...], namespace: typing.Dict[str, typing.Any]) -> None:
        """Create lock object for class."""
        super(SingleLock, cls).__init__(name, bases, namespace)
        cls.__lock = threading.RLock()

    def __new__(
        mcs: typing.Type["SingleLock"],
        name: str,
        bases: typing.Tuple[type, ...],
        namespace: typing.Dict[str, typing.Any],
        **kwargs: typing.Any,
    ) -> "SingleLock":
        """Create lock property for class instances."""
        namespace["lock"] = property(fget=lambda self: self.__class__.lock)
        return super().__new__(mcs, name, bases, namespace, **kwargs)  # type: ignore

    @property
    def lock(cls) -> threading.RLock:
        """Lock property for class."""
        return cls.__lock
