# Hello Grot
To generate a graph you need to import Grot class, create its instance and
define nodes and edges. While `g.edge()` call, you can pass unlimited
number of nodes or plain strings (creates implicit node).

If you don't connect given node (as `unconnected`) it's going to float somewhere around.
```python
def example_01():
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
Source of this example is in [example_01.py](example_01.py).

It generates raw dot-syntax text file in: [out/example_01.gv](out/example_01.gv).
And the final graph file is in: [out/example_01.gv.png](out/example_01.gv.png):

[![Rendered example image to be shown in gitlab)](out/example_01.gv.png?raw=true "example_01")](out/example_01.gv.png)

# Branches

One call of `g.edge(node1, node2, node3, ...)` creates single chain of arrows.
To make a branch, you need to call `g.edge` once again.
```python
def example_02a():
    from grot import Grot

    this_dir_path = os.path.dirname(__file__)  # if run in console - remove 'directory' parameter below
    out_dir_path = os.path.join(this_dir_path, 'out')
    g = Grot(name='example_02a', format='png', directory=out_dir_path, graph_attrs={"rankdir": "LR"})

    one = g.node("One")
    two = g.node("Two")
    three = g.node("Three")
    four = g.node("Four")
    five = g.node("Five")
    six = g.node("Six")
    seven = g.node("Seven")

    g.edge(one, two, three, four, 'A')
    g.edge(two, five, six, 'B')
    g.edge(two, seven, 'C')

    g.render()


```
Source of this example is in [example_02.py](example_02.py).

It generates raw dot-syntax text file in: [out/example_02a.gv](out/example_02a.gv).
And the final graph file is in: [out/example_02a.gv.png](out/example_02a.gv.png):

[![Rendered example image to be shown in gitlab)](out/example_02a.gv.png?raw=true "example_02a")](out/example_02a.gv.png)

# Branches - syntax variant
You don't have to assign nodes to variables. However it's a good practice to do so.
You can define nodes while `g.edge(...)` call.
Here node `two` is assigned to a local variable, because we refer it several times.
```python
def example_02b():
    from grot import Grot

    this_dir_path = os.path.dirname(__file__)  # if run in console - remove 'directory' parameter below
    out_dir_path = os.path.join(this_dir_path, 'out')

    g = Grot(name='example_02b', format='png', directory=out_dir_path, graph_attrs={"rankdir": "LR"})

    two = g.node("Two")
    g.edge(g.node("One"), two, g.node("Three"), g.node("Four"), 'A')
    g.edge(two, g.node("Five"), g.node("Six"), 'B')
    g.edge(two, g.node("Seven"), 'C')

    g.render()


```
Source of this example is in [example_02.py](example_02.py).

It generates raw dot-syntax text file in: [out/example_02b.gv](out/example_02b.gv).
And the final graph file is in: [out/example_02b.gv.png](out/example_02b.gv.png):

[![Rendered example image to be shown in gitlab)](out/example_02b.gv.png?raw=true "example_02b")](out/example_02b.gv.png)

