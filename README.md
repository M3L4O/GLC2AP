# GLC2AP
Para utilizar a gramática a partir de um arquivo:
```jupyter
In [1]: from objects.grammar import ContextFreeGrammar

In [2]: grammar = ContextFreeGrammar.from_file("teste.txt")

In [3]: grammar
Out[3]: ContextFreeGrammar(V={'B', 'A'}, Σ={'b', 'a'}, R={'A': ['a', 'Ab'], 'B': 'b'}, S='A')
```
