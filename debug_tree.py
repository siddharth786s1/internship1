#!/usr/bin/env python3
"""
Debug script to understand the Tree Beautiful Set algorithm better
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tree_beautiful_set import TreeBeautifulSet, solve_tree_beautiful_set

def debug_test_case():
    """Debug the failing test case step by step"""
    print("Debugging Test Case: Multiple Queries")
    print("=" * 50)
    
    # Tree: 0 -> [1, 2], 1 -> [3]
    n = 4
    parents = [-1, 0, 0, 1]
    colors = [1, 1, 2, 1]
    queries = [0, 1, 2, 3]
    
    print(f"Tree structure:")
    print(f"  n = {n}")
    print(f"  parents = {parents}")
    print(f"  colors = {colors}")
    print(f"  queries = {queries}")
    
    # Build the tree
    solver = TreeBeautifulSet()
    solver.build_tree(n, parents, colors)
    
    print(f"\nAdjacency list:")
    for i in range(n):
        print(f"  Node {i}: {list(solver.adj[i])}")
    
    print(f"\nColors:")
    for i in range(n):
        print(f"  Node {i}: color {solver.colors[i]}")
    
    # Analyze each query
    total_sum = 0
    for i, root in enumerate(queries):
        result = solver.find_max_beautiful_set(root)
        total_sum += result
        print(f"\nQuery {i+1}: Subtree rooted at node {root}")
        print(f"  Maximum beautiful set size: {result}")
        
        # Debug each color
        unique_colors = set(solver.colors)
        for color in unique_colors:
            solver.memo = {}
            try:
                include, exclude = solver.dfs_beautiful_sets(root, -1, color)
                color_max = max(include, exclude)
                print(f"    Color {color}: include={include}, exclude={exclude}, max={color_max}")
            except Exception as e:
                print(f"    Color {color}: Error - {e}")
    
    print(f"\nTotal sum: {total_sum}")
    print(f"Expected by test: 5")
    print(f"Match: {total_sum == 5}")

def debug_simple_case():
    """Debug a very simple case"""
    print("\n\nDebugging Simple Case")
    print("=" * 50)
    
    # Tree: 0 -> [1]
    n = 2
    parents = [-1, 0]
    colors = [1, 1]
    queries = [0]
    
    print(f"Tree: {parents}, Colors: {colors}")
    
    solver = TreeBeautifulSet()
    solver.build_tree(n, parents, colors)
    
    result = solver.find_max_beautiful_set(0)
    print(f"Result: {result}")
    print("Expected: 1 (can take either node 0 OR node 1, not both)")

def debug_star_case():
    """Debug the star case that was passing"""
    print("\n\nDebugging Star Case")
    print("=" * 50)
    
    # Star tree: 0 -> [1, 2, 3, 4] (all children of root)
    n = 5
    parents = [-1, 0, 0, 0, 0]
    colors = [1, 2, 2, 2, 2]  # Root has color 1, all children have color 2
    queries = [0]
    
    print(f"Tree: {parents}, Colors: {colors}")
    
    solver = TreeBeautifulSet()
    solver.build_tree(n, parents, colors)
    
    result = solver.find_max_beautiful_set(0)
    print(f"Result: {result}")
    print("Expected: 4 (all children with color 2 are not adjacent to each other)")

if __name__ == "__main__":
    debug_test_case()
    debug_simple_case()
    debug_star_case()