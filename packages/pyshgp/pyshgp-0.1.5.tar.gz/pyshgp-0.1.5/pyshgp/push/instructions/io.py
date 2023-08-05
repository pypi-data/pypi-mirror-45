"""Definitions for all core I/O instructions, including input instructions."""
from typing import Sequence, Callable

from pyshgp.push.state import PushState
from pyshgp.push.atoms import Atom, Literal
from pyshgp.push.instruction import SimpleInstruction, TakesStateInstruction
from pyshgp.push.type_library import PushTypeLibrary


def _nth_inputer(ndx: int) -> Callable:
    # @TODO: Replace with partial
    def f(state: PushState) -> Sequence[Literal]:
        input_value = state.inputs[ndx]
        if isinstance(input_value, Atom):
            return input_value,
        return input_value,
    return f


def make_input_instruction(ndx: int) -> TakesStateInstruction:
    """Return insctuction to push a copy of the input value at the given index."""
    return TakesStateInstruction(
        "input_{i}".format(i=ndx),
        _nth_inputer(ndx),
        output_stacks=["untyped"],
        other_stacks=[],
        code_blocks=0,
        docstring="Push a copy of input at index {i}.".format(i=ndx)
    )


def make_input_instructions(num_inputs: int) -> Sequence[TakesStateInstruction]:
    """Return insctuctions to push a copy of the input value at the given index."""
    return [make_input_instruction(i) for i in range(num_inputs)]


# Printing instructions

def instructions(type_library: PushTypeLibrary):
    """Return all core printing instructions."""
    i = []

    for push_type in type_library.keys():
        i.append(SimpleInstruction(
            "print_{t}".format(t=push_type),
            lambda x: [str(x)],
            input_stacks=[push_type],
            output_stacks=["stdout"],
            code_blocks=0,
            docstring="Prints the top {t}.".format(t=push_type)
        ))
    return i
