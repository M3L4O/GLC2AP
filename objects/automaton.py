from dataclasses import dataclass, field

from grammar import ContextFreeGrammar

from exceptions import ValueNotExists


@dataclass
class StackAutomaton:
    Σ: set
    Q: set
    δ: set
    q: set
    F: set
    V: set
    stack: list[str] = field(default_factory=lambda: [])

    def __str__(self):
        return f"({self.Σ}, {self.Q}, δ, {self.q}, {self.F}, {self.V})"

    @classmethod
    def from_grammar(cls, grammar: ContextFreeGrammar) -> "StackAutomaton":
        pass

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
                            productions: list[str] = values.split(";")
                            for production in productions:
                                left: str | list[str]
                                right: str | list[str]
                                left, right = production.split("->")
                                left, right = left.split(","), right.split(",")
                                component[key] = dict()
                                component[key][left[0]] = dict()
                                component[key][left[0]][left[1]] = dict()
                                component[key][left[0]][left[1]][left[2]] = right
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

    def step(self, state: str, char: str) -> str:
        try:
            new_state, top_stack = self.δ[state][char][self.stack.pop()]
        except IndexError:
            new_state = self.δ[state][char]

        self.stack.insert(0, top_stack)
        print(f"δ({state}, {char} ,{self.stack[0]}) -> ({new_state}, {top_stack})")

        return new_state

    def recognition(self, word: str) -> bool:
        state = self.q
        for char in word:
            state = self.step(state, char)
