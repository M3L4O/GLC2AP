from dataclasses import dataclass

from exceptions import ValueNotExists


@dataclass
class ContextFreeGrammar:
    V: set
    Σ: set
    R: dict
    S: str

    @classmethod
    def from_file(cls, filename: str) -> "ContextFreeGrammar":
        component: dict = dict()
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = "".join(line.split())
                key: str
                values: str | list[str]
                key, values = line.split(":")
                values = values.split(",")
                if key not in ("V", "T", "P", "S"):
                    raise ValueNotExists()
                else:
                    match key:
                        case "P":
                            P = dict()
                            for value in values:
                                right: str
                                left: str | list[str]
                                right, left = value.split("->")
                                if "|" in left:
                                    left = left.split("|")
                                P[right] = left

                            component[key] = P
                        case "S":
                            component[key] = values[0]
                        case _:
                            component[key] = set(sorted(values))

        return ContextFreeGrammar(
            component["V"], component["T"], component["P"], component["S"]
        )

    def __str__(self):
        return str((self.V, self.Σ, self.R, self.S))
