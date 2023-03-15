# GLC2AP
Para utilizar a gramática a partir de um arquivo:
```python
from objects.grammar import ContextFreeGrammar
```


```python
grammar = ContextFreeGrammar.from_file("teste.txt")
```


```python
grammar
```




    ContextFreeGrammar(V={'B', 'A'}, Σ={'b', 'a'}, R={'A': ['a', 'Ab'], 'B': 'b'}, S='A')


