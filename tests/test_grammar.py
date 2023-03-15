import pytest

from objects.grammar import ContextFreeGrammar


@pytest.fixture
def grammar():
    V = {"A", "B", "S"}
    Σ = {"a", "b"}
    R = {"S": [["A", "S", "B"], ["A"], ["B"]], "A": "a", "B": "b"}
    S = "S"

    grammar = ContextFreeGrammar(V, Σ, R, S)

    return grammar


@pytest.mark.unit
def test_str_grammar(grammar):
    pass
