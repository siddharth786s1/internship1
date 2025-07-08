#!/usr/bin/env python3
"""
Simple manual debug for Tree Beautiful Set algorithm
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tree_beautiful_set import TreeBeautifulSet

def test_simple_cases():
    print("Testing simple cases manually...")
    
    # Test 1: Node 2 alone (leaf node with color 2)
    solver = TreeBeautifulSet()
    solver.build_tree(4, [-1, 0, 0, 1], [1, 1, 2, 1])
    
    print("Test 1: Query subtree rooted at node 2")
    result = solver.find_max_beautiful_set(2)
    print(f"Result: {result}")
    print("Expected: 1 (just node 2 with color 2)")
    print()
    
    # Test 2: Node 3 alone (leaf node with color 1)
    print("Test 2: Query subtree rooted at node 3")
    result = solver.find_max_beautiful_set(3)
    print(f"Result: {result}")
    print("Expected: 1 (just node 3 with color 1)")
    print()
    
    # Test 3: Subtree rooted at node 1 (nodes 1 and 3, both color 1)
    print("Test 3: Query subtree rooted at node 1")
    result = solver.find_max_beautiful_set(1)
    print(f"Result: {result}")
    print("Expected: 1 (can take either node 1 OR node 3, not both as they're adjacent)")
    print()
    
    # Test 4: Whole tree rooted at node 0
    print("Test 4: Query subtree rooted at node 0")
    result = solver.find_max_beautiful_set(0)
    print(f"Result: {result}")
    print("Expected: 2 (for color 1: take nodes 0 and 3, or for color 2: take node 2)")
    print()
    
    # Let's trace through manually
    print("Manual trace for query 0 (whole tree):")
    print("Tree: 0(color=1) -> [1(color=1), 2(color=2)]")
    print("      1(color=1) -> [3(color=1)]")
    print()
    print("For color 1: nodes 0, 1, 3")
    print("  - Can take: 0 and 3 (not adjacent) = 2")
    print("  - Or take: just 1 = 1")
    print("  - Maximum for color 1: 2")
    print()
    print("For color 2: nodes 2")
    print("  - Can take: 2 = 1")
    print("  - Maximum for color 2: 1")
    print()
    print("Overall maximum: max(2, 1) = 2")

if __name__ == "__main__":
    test_simple_cases()