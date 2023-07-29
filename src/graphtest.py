"""
This module contains tests for the algorithms implemented in the graph module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from src.graph import Graph, bfs, bft, dff, draw, scc, tsort

def dummy() -> None: pass

## BFS

class BFSTestCase(TestCase):
  vs = ["s", "r", "t", "u", "v", "w", "x", "y", "z"]
  es = {
    "s": ["r", "u", "v"],  # source
    "r": ["s", "t", "w"],
    "t": ["r", "u"],
    "u": ["s", "t", "y"],
    "v": ["s", "w", "y"],
    "w": ["r", "v", "x", "z"],
    "x": ["w", "y", "z"],
    "y": ["u", "v", "x"],
    "z": ["w", "x"],
  }
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("BFS")
    self.g.makeVE(self.vs, self.es)

  def tearDown(self) -> None:
    pass

  def testBFS(self) -> None:
    self.g = bfs(self.g, self.g.getV("s"))
    print(self.g)
    draw(self.g, directed=False, label=f"{self.g.tag} with vertex discovery times").render(f"vis-{self.g.tag}")
    s = self.g.getV("s")
    t = bft(self.g, s)
    assert (t.numEE() == t.numVV() - 1)  # Theorem B.2 p.1169
    print(t)
    draw(t, directed=False, label=f"{t.tag} with vertex discovery times").render(f"vis-{t.tag}")

## DFS

class DFSTestCase(TestCase):
  vs = ["u", "v", "w", "x", "y", "z"]
  es = {  # directed edges
    "u": ["v", "x"],
    "v": ["y"],
    "w": ["y", "z"],
    "x": ["v"],
    "y": ["x"],
    "z": ["z"],
  }
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("DFS")
    self.g.makeVE(self.vs, self.es)

  def tearDown(self) -> None:
    pass

  def testDFS(self) -> None:
    f = dff(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} with vertex discovery and finish times").render(f"vis-{self.g.tag}")
    print(f)
    draw(f, directed=True, label=f"{f.tag} with vertex discovery and finish times").render(f"vis-{f.tag}")

## TSort

class TSortTestCase(TestCase):
  vs = ["belt", "jacket", "pants", "shirt", "shoes", "socks", "tie", "undershorts", "watch"]
  es = {  # directed edges
    "belt": ["jacket"],
    "jacket": [],
    "pants": ["belt", "shoes"],
    "shirt": ["belt", "tie"],
    "shoes": [],
    "socks": ["shoes"],
    "tie": ["jacket"],
    "undershorts": ["pants", "shoes"],
    "watch": [],
  }
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("TSort")
    self.g.makeVE(self.vs, self.es)

  def tearDown(self) -> None:
    pass

  def testTSort(self) -> None:
    s = tsort(self.g)
    for u in s: print(u)
    draw(self.g, directed=True, label=f"{self.g.tag} vertices descending sorted by finish times", engine="circo").render(f"vis-{self.g.tag}")

## SCC

class SCCTestCase(TestCase):
  vs = ["a", "b", "c", "d", "e", "f", "g", "h"]
  es = {  # directed edges
    "a": ["b"],
    "b": ["c", "e", "f"],
    "c": ["d", "g"],
    "d": ["c", "h"],
    "e": ["a", "f"],
    "f": ["g"],
    "g": ["f", "h"],
    "h": ["h"],
  }
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("SCC")
    self.g.makeVE(self.vs, self.es)

  def tearDown(self) -> None:
    pass

  def testTSort(self) -> None:
    c = scc(self.g)
    print(c)
    draw(c, directed=True, label=f"{c.tag} strongly connected components").render(f"vis-{c.tag}")
