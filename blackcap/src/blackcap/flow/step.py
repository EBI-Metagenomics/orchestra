"""Flow steps."""

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass
class Prop:
    """Parameter for a step."""

    data: Dict
    description: str


@dataclass
class FuncProp:
    """Function parameter for a step."""

    func: Callable
    params: Dict
    description: str


@dataclass
class Step:
    """A Step of the flow."""

    forward_call: Callable[[List[Prop]], List[Prop]]
    backward_call: Callable[[List[Prop]], List[Prop]]


def dummy_backward(prop: List[Prop]) -> Prop:
    """Dummy backward step function."""
    return prop
