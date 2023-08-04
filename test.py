#!/usr/bin/env python3

"""
This module runs the tests.

Author: Amen Zwa, Esq.
Copyright sOnit, Inc. 2023
"""

# these dummy imports are necessary for the Python test framework to see the test cases in src
from src.graphtest import BFSTestCase, DFSTestCase, SCCTestCase, TSortTestCase
from src.msttest import MSTTestCase
from src.ssptest import BellmanFordDAWGTestCase, BellmanFordSSPTestCase, DijkstraSSPTestCase
from unittest import main

if __name__ == '__main__': main()
