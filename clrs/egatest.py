"""
This module contains tests for the algorithms implemented in the ega module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from clrs.graph import Graph, draw
from clrs.ega import bfs, bft, dff, dfs, scc, tsort
from clrs.util import Intv

def dummy() -> None: pass

## BFS

class BFSTestCase(TestCase):
  # Figure 20.3 p.557
  vt = ["s", "r", "t", "u", "v", "w", "x", "y", "z"]
  et = [
    "s-r", "s-u", "s-v",
    "r-s", "r-t", "r-w",
    "t-r", "t-u",
    "u-s", "u-t", "u-y",
    "v-s", "v-w", "v-y",
    "w-r", "w-v", "w-x", "w-z",
    "x-w", "x-y", "x-z",
    "y-u", "y-v", "y-x",
    "z-w", "z-x", ]
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("BFS")
    self.g.makeVE(self.vt, self.et)

  def tearDown(self) -> None:
    pass

  def testBFS(self) -> None:
    self.g = bfs(self.g, self.g.getV("s"))
    print(self.g)
    draw(self.g, directed=False, label=f"{self.g.tag} with vertex discovery times").render(f"viz-{self.g.tag}")
    s = self.g.getV("s")
    t = bft(self.g, s)
    assert (t.numEE() == t.numVV() - 1)  # Theorem B.2 p.1169
    print(t)
    draw(t, directed=False, label=f"{t.tag} with vertex discovery times").render(f"viz-{t.tag}")

## DFS

class DFSTestCase(TestCase):
  # Figure 20.4 p.566
  vt = ["u", "v", "w", "x", "y", "z"]
  et = [  # directed edges
    "u-v", "u-x",
    "v-y",
    "w-y", "w-z",
    "x-v",
    "y-x",
    "z-z", ]
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("DFS")
    self.g.makeVE(self.vt, self.et)

  def tearDown(self) -> None:
    pass

  def testDFS(self) -> None:
    self.g = dfs(self.g)
    f = dff(self.g)
    for e in self.g.getEE():
      u = e.u
      v = e.v
      ui = Intv(u.dis, u.fin)
      vi = Intv(v.dis, v.fin)
      assert ((ui.isDisjoint(vi) and not f.isDescendant(u, v) and not f.isDescendant(v, u)) or
              (ui.isInside(vi) and f.isDescendant(u, v) or
              (vi.isInside(ui) and f.isDescendant(v, u))))
    print(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} with vertex discovery and finish times").render(f"viz-{self.g.tag}")
    print(f)
    draw(f, directed=True, label=f"{f.tag} with vertex discovery and finish times").render(f"viz-{f.tag}")

## TSort

class TSortTestCase(TestCase):
  # Figure 20.7 p.574
  vt = ["belt", "jacket", "pants", "shirt", "shoes", "socks", "tie", "undershorts", "watch"]
  et = [  # directed edges
    "belt-jacket",
    "pants-belt", "pants-shoes",
    "shirt-belt", "shirt-tie",
    "socks-shoes",
    "tie-jacket",
    "undershorts-pants", "undershorts-shoes", ]
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("TSort")
    self.g.makeVE(self.vt, self.et)

  def tearDown(self) -> None:
    pass

  def testTSort(self) -> None:
    vv = tsort(self.g)
    for u in vv: print(u)
    draw(self.g, directed=True, label=f"{self.g.tag} vertices descending sorted by finish times", engine="circo").render(f"viz-{self.g.tag}")

## SCC

class SCCTestCase(TestCase):
  # Figure 20.9 p.577
  vt = ["a", "b", "c", "d", "e", "f", "g", "h"]
  et = [  # directed edges
    "a-b",
    "b-c", "b-e", "b-f",
    "c-d", "c-g",
    "d-c", "d-h",
    "e-a", "e-f",
    "f-g",
    "g-f", "g-h",
    "h-h", ]
  g = Graph("dummy")

  def setUp(self) -> None:
    self.g = Graph("SCC")
    self.g.makeVE(self.vt, self.et)

  def tearDown(self) -> None:
    pass

  def testTSort(self) -> None:
    c = scc(self.g)
    print(c)
    draw(c, directed=True, label=f"{c.tag} strongly connected components").render(f"viz-{c.tag}")
