"""Flow Object."""

from dataclasses import dataclass, field
from enum import auto, Enum, unique
import inspect
from typing import Any, List, Optional, Union

from blackcap.flow.step import FuncProp, Prop, Step


class AutoName(Enum):
    """Helper class to auto name enum."""

    def _generate_next_value_(
        name: Any, start: Any, count: Any, last_values: Any  # noqa: B902
    ) -> str:
        """Generate names."""
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


class FlowBuildError(Exception):
    """Errors while building flow."""

    human_description: str
    error: Any
    # TODO: Change it to enum?
    error_type: type
    error_in_function: str


def get_outer_function() -> str:
    """Return name of the outer function."""
    return inspect.getframeinfo(inspect.currentframe().f_back).function


@dataclass
class Flow:
    """Flow Object."""

    steps: List[Step] = field(default_factory=list)
    inputs: List[List[Union[Prop, FuncProp]]] = field(default_factory=list)
    forward_outputs: List[List[Prop]] = field(default_factory=list)
    backward_outputs: List[List[Prop]] = field(default_factory=list)
    status: FlowStatus = FlowStatus.CREATED
    errors: List[FlowExecError] = field(default_factory=list)

    def add_step(self: "Flow", step: Step, inputs: List[Prop]) -> None:
        """Add a step to the flow."""
        # TODO: Add checks in future
        self.steps.append(step)
        self.inputs.append(inputs)

    def get_froward_output(self: "Flow", index: int) -> Optional[List[Prop]]:
        """Lazily get list of prop from flow forward outputs."""
        return self.forward_outputs[index]

    def get_input(self: "Flow", index: int) -> Optional[List[Prop]]:
        """Lazily get list of prop from flow inputs."""
        return self.inputs[index]
