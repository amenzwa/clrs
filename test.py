#!/usr/bin/env python3

"""
This module runs the tests.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

# these dummy imports are necessary for the Python test framework to see the test cases in clrs
from clrs.egatest import BFSTestCase, DFSTestCase, SCCTestCase, TSortTestCase
from clrs.msttest import MSTTestCase
from clrs.ssptest import BellmanFordDAWGTestCase, BellmanFordSSPTestCase, DijkstraSSPTestCase
from clrs.asptest import FloydWarshallASPTestCase, TransitiveClosureTestCase
from unittest import main

if __name__ == '__main__': main()
