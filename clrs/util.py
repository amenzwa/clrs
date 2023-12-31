"""
This module contains type variables, utility types, and utility functions.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

import sys
from typing import Callable, TypeVar

Infinity = sys.maxsize

α = TypeVar("α")

def todo() -> None: raise Exception("to do")

### Tag

Tag = str  # label

class Tagged:  # base for tagged types
  def __init__(self, tag: Tag):
    self.tag = tag

### Option

Option = None | α  # same as typing.Optional

def isNone(o: Option[α]) -> bool: return o is None

def isSome(o: Option[α]) -> bool: return not isNone(o)

### Result

Result = Exception | α

def isError(r: Result[α]) -> bool: return type(r) is Exception

def isResult(r: Result[α]) -> bool: return not isError(r)

### Interval

class Intv:
  def __init__(self, lo: int, hi: int):
    self.i = (lo, hi)

  def contains(self, v: int) -> bool: return v in self.i
  def isInside(self, j: "Intv") -> bool:
    (ilo, ihi) = self.i
    (jlo, jhi) = j.i
    return ilo >= jlo and ihi <= jhi
  def isDisjoint(self, j: "Intv") -> bool: return not self.isInside(j) and not j.isInside(self)

### Chapter 19 Data Structures for Disjoint Sets p.520

class SSet:  # sorted set
  def __init__(self, i: [α], attr: Callable[[float], float]):
    super().__init__()
    self.ii = set(i)  # guaranteed to contain at least one item
    self.attr = attr  # sorting attribute selector

  def ins(self, i: α) -> None: self.ii = set(sorted([i, *self.ii], key=self.attr))
  def getII(self) -> [α]: return list(self.ii)
  def getRep(self) -> str: return str(self.getII()[0])  # return the representative item string

  def contains(self, i: α) -> bool: return i in self.ii

class DSet:  # disjoint sets (a collection of sorted sets)
  def __init__(self, attr: Callable[[float], float]):
    super().__init__()
    self.ss: {str, SSet} = {}  # {str(rep): SSet}
    self.attr = attr

  def getSS(self) -> [SSet]:
    return list(self.ss.values())

  def makeSet(self, x: α) -> None:
    s = self.findSet(x)
    if isNone(s):  # x is not in the collection
      s = SSet([x], attr=self.attr)
      self.ss[s.getRep()] = s

  def findSet(self, x: α) -> Option[SSet]:
    ss = [s for s in self.getSS() if s.contains(x)]
    return ss[0] if ss != [] else None

  def union(self, x: α, y: α) -> SSet:
    if x == y: return self.findSet(x)
    sx = self.findSet(x)
    sy = self.findSet(y)
    if sx == sy: return sx
    ii = []
    if isSome(sx):
      self.ss.pop(sx.getRep())
      ii += sx.getII()
    if isSome(sy):
      self.ss.pop(sy.getRep())
      ii += sy.getII()
    su = SSet(ii, attr=self.attr)
    self.ss[su.getRep()] = su

### PQueue

