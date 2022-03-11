"""Flow executor."""

from dataclasses import dataclass
from typing import Dict

from blackcap.flow.flow import Flow, FlowExecError, FlowStatus, get_outer_function
from blackcap.flow.step import FuncProp, Prop


@dataclass
class Executor:
    """Flow executor."""

    flow: Flow
    # TODO: Strongly type it in the future
    config: Dict

    def run(self: "Executor") -> Flow:  # noqa: C901
        """Execute flow."""
        # Set Flow status to executing
        self.flow.status = FlowStatus.EXECUTING
        for index, step in enumerate(self.flow.steps):
            try:
                # Prepare function inputs
                functions_inputs = []
                # Check the prop type
                for item in self.flow.inputs[index]:
                    if type(item) == FuncProp:
                        try:
                            input_list_from_func = item.func(**item.params)
                        except Exception as e:
                            raise FlowExecError(
                                human_description="Invoking FuncProp failed",
                                error=e,
                                error_type=type(e),
                                is_user_facing=False,
                                error_in_function=item.func,
                                step_index=index,
                            ) from e
                        functions_inputs += input_list_from_func
                    elif type(item) == Prop:
                        functions_inputs.append(item)
                    else:
                        raise FlowExecError(
                            human_description="Unkown type of input is used to invoke a step function",
                            error=f"Input type: {type(self.flow.inputs[index])} is not recognised",
                            error_type="Unkown input error",
                            is_user_facing=False,
                            error_in_function=get_outer_function(),
                        )
                # Replace current function input with the prepared inputs
                self.flow.inputs[index] = functions_inputs

                # Invoke function with prepared inputs
                forward_out = step.forward_call(self.flow.inputs[index])
                self.flow.forward_outputs.append(forward_out)
            except Exception as e:
                # TODO: Add logging for failed forward calls
                # Set flow status to failed and append error
                self.flow.status = FlowStatus.FAILED
                flow_error = FlowExecError(
                    human_description="A forward step function failed",
                    error=e,
                    error_type=type(e),
                    is_user_facing=False,
                    error_in_function=get_outer_function(),
                )
                flow_error.step_index = index
                self.flow.errors.append(flow_error)
                for back_index in reversed(range(0, index)):
                    try:
                        backward_out = self.flow.steps[back_index].backward_call(
                            self.flow.inputs[back_index]
                            + self.flow.forward_outputs[back_index],
                        )
                        self.flow.backward_outputs.append(backward_out)
                    except Exception as e:
                        # TODO: Add central logging here
                        flow_error = FlowExecError(
                            human_description="A backward step function failed",
                            error=e,
                            error_type=type(e),
                            is_user_facing=False,
                            error_in_function=get_outer_function(),
                        )
                        flow_error.step_index = index
                        self.flow.errors.append(flow_error)
                return self.flow
        self.flow.status = FlowStatus.PASSED
        return self.flow
