"""Flow steps."""

from dataclasses import dataclass
from typing import Dict, Callable, List


@dataclass
class Prop:
    """Parameter for a step."""

    data: Dict
    description: str


@dataclass
class Step:
    """A Step of the flow."""

    forward_call: Callable[[List[Prop]], List[Prop]]
    forward_in: List[str]
    forward_out: List[str]
    backward_call: Callable[[List[Prop]], List[Prop]]
    backward_in: List[str]
    backward_out: List[str]


def dummy_backward(prop: List[Prop]) -> Prop:
    """Dummy backward step function."""
    return prop
