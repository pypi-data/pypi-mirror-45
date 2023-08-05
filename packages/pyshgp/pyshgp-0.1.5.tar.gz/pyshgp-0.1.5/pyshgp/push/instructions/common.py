"""Instructions common to all ``PushTypes`` and ``PushStacks``."""
from typing import Any, Union, Callable, Tuple
from functools import partial

from pyshgp.push.types import PushType
from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.instruction import (
    SimpleInstruction,
    TakesStateInstruction,
    StateToStateInstruction,
    ProducesManyOfTypeInstruction
)
from pyshgp.push.state import PushState
from pyshgp.push.atoms import Atom, Literal
from pyshgp.utils import Token


DUP_LIMIT = 500


def _dup_times(times, item):
    x = int(min(times, DUP_LIMIT))
    return [item] * x


# Disabled due to performance issues.
# def _dup_top_n_factory(type_name: str) -> Callable:
#     def f(state: PushState) -> PushState:
#         if state["int"].is_empty() or state[type_name].is_empty():
#             return Token.revert
#         ndx = max(0, min(state["int"].pop(), len(state[type_name]) - 1))
#         for item in state[type_name][:ndx]:
#             state[type_name].push(item)
#         return state
#     return f


def _flusher(type_name: str) -> Callable:
    def f(state: PushState) -> PushState:
        state[type_name].flush()
        return state
    return f


def _stack_depther(type_name: str) -> Callable:
    def f(state: PushState) -> int:
        return [len(state[type_name])]
    return f


def _yanker(type_name: str) -> Callable:
    def f(state: PushState) -> Union[PushState, Token]:
        if state["int"].is_empty() or state[type_name].is_empty():
            return Token.revert
        if type_name == "int" and len(state[type_name]) < 2:
            return Token.revert
        raw_ndx = state["int"].pop()
        ndx = max(0, min(raw_ndx, len(state[type_name]) - 1))
        item = state[type_name].pop(ndx)
        state[type_name].push(item)
        return state
    return f


def _yank_duper(type_name: str) -> Callable:
    def f(state: PushState) -> Union[PushState, Token]:
        if state["int"].is_empty() or state[type_name].is_empty():
            return Token.revert
        if type_name == "int" and len(state[type_name]) < 2:
            return Token.revert
        raw_ndx = state["int"].pop()
        ndx = max(0, min(raw_ndx, len(state[type_name]) - 1))
        item = state[type_name].nth(ndx)
        state[type_name].push(item)
        return state
    return f


def _shover(type_name: str) -> Callable:
    def f(state: PushState) -> Union[PushState, Token]:
        if state["int"].is_empty() or state[type_name].is_empty():
            return Token.revert
        if type_name == "int" and len(state[type_name]) < 2:
            return Token.revert
        raw_ndx = state["int"].pop()
        ndx = max(0, min(raw_ndx, len(state[type_name]) - 1))
        item = state[type_name].pop()
        state[type_name].insert(ndx, item)
        return state
    return f


def _shove_duper(type_name: str) -> Callable:
    def f(state: PushState) -> Union[PushState, Token]:
        if state["int"].is_empty() or state[type_name].is_empty():
            return Token.revert
        if type_name == "int" and len(state[type_name]) < 2:
            return Token.revert
        raw_ndx = state["int"].pop()
        ndx = max(0, min(raw_ndx, len(state[type_name])))
        item = state[type_name].top()
        state[type_name].insert(ndx, item)
        return state
    return f


def _is_emptyer(type_name: str) -> Callable:
    def f(state: PushState) -> bool:
        return [state[type_name].is_empty()]
    return f


def _make_code(x: Any, push_type: PushType) -> Tuple[Atom]:
    if isinstance(x, Atom):
        return x,
    else:
        return Literal(x, push_type),


def instructions(type_library: PushTypeLibrary):
    """Return all core numeric instructions."""
    i = []

    for push_type in type_library.keys():
        i.append(SimpleInstruction(
            "{t}_pop".format(t=push_type),
            lambda x: [],
            input_stacks=[push_type],
            output_stacks=[],
            code_blocks=(1 if push_type == "exec" else 0),
            docstring="Pops the top {t}.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_dup".format(t=push_type),
            lambda x: [x, x],
            input_stacks=[push_type],
            output_stacks=[push_type, push_type],
            code_blocks=(1 if push_type == "exec" else 0),
            docstring="Duplicates the top {t}.".format(t=push_type)
        ))

        i.append(ProducesManyOfTypeInstruction(
            "{t}_dup_times".format(t=push_type),
            _dup_times,
            input_stacks=["int", push_type],
            output_stack=push_type,
            code_blocks=(1 if push_type == "exec" else 0),
            docstring="Duplicates the top {t} `n` times where `n` is from the int stack.".format(t=push_type)
        ))

        # Disabled due to performance issues.
        # i.append(StateToStateInstruction(
        #     "{t}_dup_top_n".format(t=push_type),
        #     _dup_top_n_factory(push_type),
        #     stacks_used=[push_type, "int"],
        #     code_blocks=0,
        #     docstring="Duplicates the top n items on the {t} stack.".format(t=push_type)
        # ))

        i.append(SimpleInstruction(
            "{t}_swap".format(t=push_type),
            lambda a, b: [a, b],
            input_stacks=[push_type, push_type],
            output_stacks=[push_type, push_type],
            code_blocks=(2 if push_type == "exec" else 0),
            docstring="Swaps the top two {t}s.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_rot".format(t=push_type),
            lambda a, b, c: [b, a, c],
            input_stacks=[push_type] * 3,
            output_stacks=[push_type] * 3,
            code_blocks=(3 if push_type == "exec" else 0),
            docstring="Rotates the top three {t}s.".format(t=push_type)
        ))

        i.append(StateToStateInstruction(
            "{t}_flush".format(t=push_type),
            _flusher(push_type),
            stacks_used=[push_type],
            code_blocks=0,
            docstring="Empties the {t} stack.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_eq".format(t=push_type),
            lambda a, b: [a == b],
            input_stacks=[push_type, push_type],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes True if the top two {t} are equal. Otherwise pushes False.".format(t=push_type)
        ))

        i.append(TakesStateInstruction(
            "{t}_stack_depth".format(t=push_type),
            _stack_depther(push_type),
            output_stacks=["int"],
            other_stacks=[push_type],
            code_blocks=0,
            docstring="Pushes the size of the {t} stack to the int stack.".format(t=push_type)
        ))

        i.append(StateToStateInstruction(
            "{t}_yank".format(t=push_type),
            _yanker(push_type),
            stacks_used=[push_type, "int"],
            code_blocks=0,
            docstring="Yanks a {t} from deep in the stack based on an index from the int stack and puts it on top.".format(t=push_type)
        ))

        i.append(StateToStateInstruction(
            "{t}_yank_dup".format(t=push_type),
            _yank_duper(push_type),
            stacks_used=[push_type, "int"],
            code_blocks=0,
            docstring="Yanks a copy of a {t} deep in the stack based on an index from the int stack and puts it on top.".format(t=push_type)
        ))

        i.append(StateToStateInstruction(
            "{t}_shove".format(t=push_type),
            _shover(push_type),
            stacks_used=[push_type, "int"],
            code_blocks=(1 if push_type == "exec" else 0),
            docstring="Shoves the top {t} deep in the stack based on an index from the int stack.".format(t=push_type)
        ))

        i.append(StateToStateInstruction(
            "{t}_shove_dup".format(t=push_type),
            _shove_duper(push_type),
            stacks_used=[push_type, "int"],
            code_blocks=(1 if push_type == "exec" else 0),
            docstring="Shoves a copy of the top {t} deep in the stack based on an index from the int stack.".format(t=push_type)
        ))

        i.append(TakesStateInstruction(
            "{t}_is_empty".format(t=push_type),
            _is_emptyer(push_type),
            output_stacks=["bool"],
            other_stacks=[push_type],
            code_blocks=0,
            docstring="Pushes True if the {t} stack is empty. Pushes False otherwise.".format(t=push_type)
        ))

    for push_type_name, push_type in type_library.items():
        if push_type_name == "code":
            continue
        i.append(SimpleInstruction(
            "code_from_{t}".format(t=push_type_name),
            partial(_make_code, push_type=push_type),
            input_stacks=[push_type_name],
            output_stacks=["code"],
            code_blocks=(1 if push_type_name == "exec" else 0),
            docstring="Moves the top {t} to the code stack.".format(t=push_type_name)
        ))

    return i
