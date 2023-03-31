from dataclasses import dataclass, field
from .grammar import ContextFreeGrammar
from .exceptions import ValueNotExists


@dataclass
class StackAutomaton:
    Σ: set
    Q: set
    δ: dict
    q: str
    F: set
    V: set
    stack: list[str] = field(default_factory=lambda: [])

    def __str__(self):
        return f"({self.Σ}, {self.Q}, δ, {self.q}, {self.F}, {self.V})"

    @classmethod
    def from_grammar(cls, grammar: ContextFreeGrammar) -> "StackAutomaton":
        Σ = grammar.Σ
        Q = {"q0", "q1", "q2"}
        F = {"q2"}
        V = grammar.V
        δ = dict()
        δ[("q0", "ε", "ε")] = ("q1", grammar.S)

        for key, values in grammar.R.items():
            for value in values:
                δ[("q1", "ε", key)] = ("q1", value)

        return StackAutomaton(Σ, Q, δ, "q0", F, V)

    @classmethod
    def from_file(cls, filename: str) -> "StackAutomaton":
        with open(filename, "r") as file:
            lines = file.readlines()
            component: dict = dict()
            for line in lines:
                line = "".join(line.split())
                key: str
                values: str
                key, values = line.split(":")
                if key not in ("T", "Q", "P", "q", "F", "V"):
                    raise ValueNotExists("no automato")
                else:
                    match key:
                        case "q":
                            component[key] = values
                        case "P":
                            component[key] = dict()
                            productions: list[str] = values.split(";")
                            for production in productions:
                                left: str | list[str]
                                right: str | list[str]
                                left, right = production.split("->")
                                left, right = left.split(","), right.split(",")
                                component[key][tuple(left)] = tuple(right)
                        case _:
                            component[key] = set(values.split(","))
        return StackAutomaton(
            component["T"],
            component["Q"],
            component["P"],
            component["q"],
            component["F"],
            component["V"],
        )

    def step(self, state: str, word: str, recognition_process: list = []) -> str:
        transitions = [
            transition for transition in self.δ.keys() if state in transition
        ]
        char, word = [*word][0], "".join([*word][1:])

        for transition in transitions:
            pass

    def recognition(self, word: str) -> bool:
        state = self.q
        self.step(state, word)
