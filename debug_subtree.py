#!/usr/bin/env python3
"""
Debug the subtree collection
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tree_beautiful_set import TreeBeautifulSet

def debug_subtree_collection():
    solver = TreeBeautifulSet()
    solver.build_tree(4, [-1, 0, 0, 1], [1, 1, 2, 1])
    
    print("Tree structure:")
    for i in range(4):
        print(f"  Node {i}: adj={list(solver.adj[i])}, color={solver.colors[i]}, parent={solver.parent[i]}")
    
    print("\nDebugging subtree collection for node 2:")
    
    # Get parent of node 2
    root_parent = solver.parent[2]
    print(f"Parent of node 2: {root_parent}")
    
    # Manual subtree collection
    subtree_nodes = []
    
    def collect_subtree_nodes(node, parent):
        print(f"  Visiting node {node} (parent={parent})")
        subtree_nodes.append(node)
        for child in solver.adj[node]:
            if child != parent:
                print(f"    Child {child} of {node}")
                collect_subtree_nodes(child, node)
    
    collect_subtree_nodes(2, root_parent)
    print(f"Subtree nodes: {subtree_nodes}")
    
    print(f"\nColors in subtree: {[solver.colors[n] for n in subtree_nodes]}")
    unique_colors = set(solver.colors[node] for node in subtree_nodes)
    print(f"Unique colors: {unique_colors}")
    
    # Test the algorithm for each color
    for color in unique_colors:
        result = solver._solve_for_color(2, root_parent, color, set(subtree_nodes))
        print(f"Color {color}: max beautiful set = {result}")

if __name__ == "__main__":
    debug_subtree_collection()