"""Flow Object."""

from dataclasses import dataclass, field
from enum import Enum, auto, unique
from typing import List

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
class Flow:
    """Flow Object."""

    steps: List[Step] = field(default_factory=list)
    inputs: List[List[Prop]] = field(default_factory=list)
    forward_outputs: List[List[Prop]] = field(default_factory=list)
    backward_outputs: List[List[Prop]] = field(default_factory=list)
    status: FlowStatus = FlowStatus.CREATED

    def add_step(self: "Flow", step: Step, inputs: List[Prop]) -> None:
        """Add a step to the flow."""
        # TODO: Add checks in future
        self.steps.append(step)
        self.inputs.append(inputs)
