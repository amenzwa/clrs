"""
This module contains tests for the algorithms implemented in the ssp module.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

from unittest import TestCase

from src.graph import draw
from src.ssp import DijkstraSSPGraph, SSPGraph, sspBellmanFord, sspBellmanFordDAWG, sspDijkstra
from src.util import isSome

## Bellman-Ford SSP algorithm

class BellmanFordSSPTestCase(TestCase):
  # Figure 22.4 p.613
  vs = ["s", "t", "x", "y", "z"]
  es = {  # directed edges
    "s": ["t", "y"],
    "t": ["x", "y", "z"],
    "x": ["t"],
    "y": ["x", "z"],
    "z": ["s", "x"],
  }
  ew = {
    "s-t": 6,
    "s-y": 7,
    "t-x": 5,
    "t-y": 8,
    "t-z": -4,
    "x-t": -2,
    "y-x": -3,
    "y-z": 9,
    "z-s": 2,
    "z-x": 7,
  }
  g = SSPGraph("dummy")

  def setUp(self) -> None:
    self.g = SSPGraph("Bellman-Ford")
    self.g.makeVEw(self.vs, self.es, self.ew)

  def tearDown(self) -> None:
    pass

  def testBellmanFord(self) -> None:
    print(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} directed, weighted graph").render(f"viz-{self.g.tag}")
    s = self.g.getV("s")
    p = sspBellmanFord(self.g, s)
    if isSome(p):
      print(p)
      draw(p, directed=True, label=f"{p.tag} Single-Source Shortest Path").render(f"viz-{p.tag}")

class BellmanFordDAWGTestCase(TestCase):
  # Figure 22.5 p.618
  vs = ["r", "s", "t", "x", "y", "z"]
  es = {  # directed edges
    "r": ["s", "t"],
    "s": ["t", "x"],
    "t": ["x", "y", "z"],
    "x": ["y", "z"],
    "y": ["z"],
    "z": [],
  }
  ew = {
    "r-s": 5,
    "r-t": 3,
    "s-t": 2,
    "s-x": 6,
    "t-x": 7,
    "t-y": 4,
    "t-z": 2,
    "x-y": -1,
    "x-z": 1,
    "y-z": -2,
  }
  g = SSPGraph("dummy")

  def setUp(self) -> None:
    self.g = SSPGraph("Bellman-Ford DAWG")
    self.g.makeVEw(self.vs, self.es, self.ew)

  def tearDown(self) -> None:
    pass

  def testBellmanFordDAWG(self) -> None:
    print(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} directed, acyclic, weighted graph").render(f"viz-{self.g.tag}")
    s = self.g.getV("s")
    p = sspBellmanFordDAWG(self.g, s)
    if isSome(p):
      print(p)
      draw(p, directed=True, label=f"{p.tag} Single-Source Shortest Path").render(f"viz-{p.tag}")

class DijkstraSSPTestCase(TestCase):
  # Figure 22.6 p.621
  vs = ["s", "t", "x", "y", "z"]
  es = {  # directed edges
    "s": ["t", "y"],
    "t": ["x", "y"],
    "x": ["z"],
    "y": ["t", "x", "z"],
    "z": ["s", "x"],
  }
  ew = {
    "s-t": 10,
    "s-y": 5,
    "t-x": 1,
    "t-y": 2,
    "x-z": 4,
    "y-t": 3,
    "y-x": 9,
    "y-z": 2,
    "z-s": 7,
    "z-x": 6,
  }
  g = SSPGraph("dummy")

  def setUp(self) -> None:
    self.g = DijkstraSSPGraph("Dijkstra")
    self.g.makeVEw(self.vs, self.es, self.ew)

  def tearDown(self) -> None:
    pass

  def testDijkstra(self) -> None:
    print(self.g)
    draw(self.g, directed=True, label=f"{self.g.tag} directed, weighted graph").render(f"viz-{self.g.tag}")
    s = self.g.getV("s")
    p = sspDijkstra(self.g, s)
    print(p)
    draw(p, directed=True, label=f"{p.tag} Single-Source Shortest Path").render(f"viz-{p.tag}")