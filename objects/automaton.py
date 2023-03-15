from dataclasses import dataclass, field
from grammar import ContextFreeGrammar


@dataclass
class StackAutomaton:
    Q: set
    Σ: set
    δ: set
    q: set
    F: set
    V: set
    stack: list = field(init=False)

    def step(self, state: str, char: str):
        try:
            new_state, top_stack = self.δ[state][char][self.stack.pop()]
        except IndexError:
            new_state = self.δ[state][char]

        self.stack.insert(0, top_stack)
        print(f"δ({state}, {char} ,{self.stack[0]}) -> ({new_state}, {top_stack})")
        return new_state

    def recognition(self, word: str):
        state = self.q
        for char in word:
            state = self.step(state, char)

    @classmethod
    def from_grammar(cls, grammar: ContextFreeGrammar):
        pass
