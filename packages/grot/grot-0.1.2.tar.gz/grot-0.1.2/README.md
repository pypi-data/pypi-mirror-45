# Grot
**Grot** is a noun and means **arrowhead** in polish language.
  
### Makes graphviz usage simpler
Much less headache. Gets you faster into the point.
 
```python
import os
from grot import Grot

this_dir_path = os.path.dirname(__file__)  # if run in console - remove 'directory' parameter below
out_dir_path = os.path.join(this_dir_path, 'out')

g = Grot(name='example_01', format='png', directory=out_dir_path, graph_attrs={"rankdir": "LR"})

one = g.node("It is\neaiser")
two = g.node("graphs", color="#8a9bac")
ignored = g.node("Node floats when\nunconnected", color="#da3080")

g.edge(one, "to define", two)
g.render()

```

![Rendered graph image](examples/out/example_01.gv.png?raw=true "Grot")

It will generate a `example_01.png` file in current directory.

Refer to tests and examples for more features information.
