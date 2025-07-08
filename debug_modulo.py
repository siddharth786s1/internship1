#!/usr/bin/env python3
"""
Debug the modulo test case
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tree_beautiful_set import TreeBeautifulSet, solve_tree_beautiful_set

def debug_modulo_test():
    print("Debugging modulo test case...")
    
    # Create a scenario that might produce large sums
    n = 10
    parents = [-1] + [0] * 9  # Star with 9 children
    colors = [1] + [1] * 9    # All same color
    queries = [0] * 100      # Many queries of the same subtree
    
    print(f"Tree structure: Star with {n} nodes")
    print(f"Parents: {parents}")
    print(f"Colors: {colors}")
    print(f"Number of queries: {len(queries)}")
    
    # Test a single query first
    single_result = solve_tree_beautiful_set(n, parents, colors, [0])
    print(f"Single query result: {single_result}")
    
    # Expected reasoning:
    # In a star tree with all nodes having the same color,
    # we can only take the root node (since all children are adjacent to root)
    # OR we can take no nodes from the root and take none of the children
    # So the maximum should be 1
    
    # But let's check what colors we actually have
    solver = TreeBeautifulSet()
    solver.build_tree(n, parents, colors)
    
    print(f"Root node: 0, color: {solver.colors[0]}")
    print(f"Children of root: {list(solver.adj[0])}")
    for child in solver.adj[0]:
        print(f"  Child {child}, color: {solver.colors[child]}")
    
    # Test the find_max_beautiful_set function directly
    result = solver.find_max_beautiful_set(0)
    print(f"Maximum beautiful set for subtree rooted at 0: {result}")
    
    # Now test the full query
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"Full test result: {result}")
    print(f"Expected: {100}")

if __name__ == "__main__":
    debug_modulo_test()