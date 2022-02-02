"""Flow executor."""

from dataclasses import dataclass
from typing import Dict

from blackcap.flow.flow import Flow, FlowStatus


@dataclass
class Executor:
    """Flow executor."""

    flow: Flow
    # TODO: Strongly type it in the future
    config: Dict

    def run(self: "Executor") -> Flow:
        """Execute flow."""
        # Set Flow status to executing
        self.flow.status = FlowStatus.EXECUTING
        for index, step in enumerate(self.flow.steps):
            try:
                forward_out = step.forward_call(self.flow.inputs[index])
                self.flow.forward_outputs.append(forward_out)
            except:
                # TODO: Add logging for failed forward calls
                # Set flow status to failed
                self.flow.status = FlowStatus.FAILED
                for back_index in reversed(range(0, index)):
                    try:
                        backward_out = self.flow.steps[back_index].backward_call(
                            self.flow.inputs[back_index],
                            self.flow.forward_outputs[back_index],
                        )
                        self.flow.backward_outputs.append(backward_out)
                    except:
                        # TODO: Add central logging here
                        pass
                return self.flow
        self.flow.status = FlowStatus.PASSED
        return self.flow
