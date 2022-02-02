"""Flow Object."""

from dataclasses import dataclass, field
from enum import Enum, auto, unique
import inspect
from typing import Any, List, Optional
import sys

from blackcap.flow.step import Prop, Step


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


@unique
class FlowStatus(AutoName):
    """Status of the Flow."""

    CREATED = auto()
    EXECUTING = auto()
    PASSED = auto()
    FAILED = auto()


@dataclass
class FlowExecError(Exception):
    """Errors while executing flow."""

    human_description: str
    error: Any
    # TODO: Change it to enum?
    error_type: type
    error_in_function: str
    step_index: Optional[int] = None
    is_user_facing: bool = False
    user_facing_msg: Optional[str] = None


def get_outer_function() -> str:
    """Return name of the outer function."""
    return inspect.getframeinfo(inspect.currentframe().f_back).function


@dataclass
class Flow:
    """Flow Object."""

    steps: List[Step] = field(default_factory=list)
    inputs: List[List[Prop]] = field(default_factory=list)
    forward_outputs: List[List[Prop]] = field(default_factory=list)
    backward_outputs: List[List[Prop]] = field(default_factory=list)
    status: FlowStatus = FlowStatus.CREATED
    errors: List[FlowExecError] = field(default_factory=list)

    def add_step(self: "Flow", step: Step, inputs: List[Prop]) -> None:
        """Add a step to the flow."""
        # TODO: Add checks in future
        self.steps.append(step)
        self.inputs.append(inputs)