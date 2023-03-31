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

        δ[("q1", "?", "?")] = ("q2", "ε")

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

    def step(
        self,
        state: str,
        word: str,
        char: str,
        from_stack: str,
        recognition_process: list = [],
        stack: list = [],
    ) -> str:
        new_state, new_top_stack = self.δ[(state, char, stack)]
        recognition_step = (
            f"δ({state}, {char}, {from_stack}) -> ({new_state}, {new_top_stack})"
        )

        recognition_process.append(recognition_step)

        if new_top_stack != "ε":
            if len(new_top_stack) > 1:
                for element in new_top_stack[::-1]:
                    stack.insert(0, new_top_stack)
            else:
                stack.insert(0, new_top_stack)

        return new_state, recognition_process, stack

    def search_way(
        self, state: str, word: str, recognition_process: list = [], stack: list = []
    ) -> str:
        if word == "":
            char, word = "", ""
        else:
            char, word = [*word][0], "".join([*word][1:])

        void_possibilites = [(state, "ε", "ε"), (state, char, "ε")]

        if len(stack) > 0:
            void_possibilites.append((state, "ε", stack[0]))
            try:
                from_stack = stack.pop()
                new_state, recognition_process, stack = self.step(
                    state, word, char, from_stack, recognition_process, stack
                )
                self.search_way(new_state, word, recognition_process, stack)
            except IndexError:
                pass

        for void_possibility in void_possibilites:
            state, char, from_stack = void_possibility
            try:
                new_state, recognition_process, stack = self.step(
                    state, word, char, from_stack, recognition_process, stack
                )
                self.search_way(new_state, word, recognition_process, stack)
            except IndexError:
                pass

        if word == "" and len(stack) == 0:
            if state in self.F:
                print("\n".join(recognition_process))
                return
            else:
                try:
                    char, from_stack = "?", "?"
                    new_state, recognition_process, stack = self.step(
                        state, word, char, from_stack, recognition_process, stack
                    )
                    self.search_way(new_state, word, recognition_process, stack)
                except IndexError:
                    return

    def recognition(self, word: str) -> bool:
        state = self.q
        self.search_way(state, word)
