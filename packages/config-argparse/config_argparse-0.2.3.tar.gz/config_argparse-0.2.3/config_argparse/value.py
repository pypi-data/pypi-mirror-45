from __future__ import annotations

from typing import Callable, TypeVar, Union, Generic, Sequence, cast, Tuple, Dict, Any
import argparse
import builtins

T = TypeVar('T')


class Value(Generic[T]):
    def __init__(
            self,
            default: T = None,
            *,
            type: Callable[[str], T] = None,
            choices: Sequence[T] = None,
            required: bool = False,
            nargs: Union[int, str] = None,
            help: str = None,
            metavar: Union[str, Tuple[str, ...]] = None,
    ) -> None:

        # infer type
        if type is None:
            if default is not None:
                if isinstance(default, (list, tuple)):
                    if len(default) > 0:
                        type = builtins.type(default[0])
                else:
                    type = builtins.type(default)
            elif choices is not None:
                if len(choices) > 0:
                    type = builtins.type(choices[0])

        if type is None:
            raise Exception('failed to infer type ({} {})'.format(default, choices))

        # set nargs
        if nargs is None:
            if isinstance(default, (list, tuple)):
                nargs = '+'

        # check
        if type == bool and default is not False:
            raise Exception('bool type only supports store_true action.')

        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.nargs = nargs
        self.help = help
        self.metavar = metavar

    def add_argument(
            self,
            parser: argparse._ActionsContainer,
            name: str,
            dest: str = None,
    ) -> None:
        kwards: Dict[str, Any] = {
            "default": self.default,
            "required": self.required,
            "help": self.help,
            "dest": dest,
        }
        if self.type == bool:
            kwards["action"] = cast(argparse.Action, argparse._StoreTrueAction if self.default is False else argparse._StoreFalseAction)
        else:
            kwards["type"] = self.type
            kwards["nargs"] = self.nargs
            kwards["choices"] = self.choices
            kwards["metavar"] = self.metavar

        parser.add_argument(name, **kwards)

    def __repr__(self) -> str:
        res = str(self.default) if not self.required else 'required'
        if self.choices is not None:
            res += ', one of [{}]'.format(', '.join(list(map(str, self.choices))))
        return '{}({})'.format(self.__class__.__name__, res)
