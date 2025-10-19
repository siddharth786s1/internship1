#!/usr/bin/env python3
"""
Usage examples and demonstration for Tree Beautiful Set Problem

This script shows how to use the TreeBeautifulSet class and solve_tree_beautiful_set function
with various examples and use cases.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tree_beautiful_set import TreeBeautifulSet, solve_tree_beautiful_set

def example_1_simple_tree():
    """Example 1: Simple tree with mixed colors"""
    print("Example 1: Simple tree with mixed colors")
    print("=" * 50)
    
    # Tree structure: 0 -> [1, 2]
    n = 3
    parents = [-1, 0, 0]
    colors = [1, 1, 2]
    queries = [0]
    
    print(f"Tree structure:")
    print(f"  Node 0 (color {colors[0]}) -> Node 1 (color {colors[1]}), Node 2 (color {colors[2]})")
    print(f"Query: Find maximum beautiful set in subtree rooted at 0")
    
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"Result: {result}")
    print(f"Explanation: For color 1, we can take either node 0 OR node 1 (max=1)")
    print(f"             For color 2, we can take node 2 (max=1)")
    print(f"             Overall maximum: 1")
    print()

def example_2_linear_tree():
    """Example 2: Linear tree with same colors"""
    print("Example 2: Linear tree with same colors")
    print("=" * 50)
    
    # Tree structure: 0 -> 1 -> 2 -> 3
    n = 4
    parents = [-1, 0, 1, 2]
    colors = [1, 1, 1, 1]
    queries = [0]
    
    print(f"Tree structure:")
    print(f"  Node 0 (color {colors[0]}) -> Node 1 (color {colors[1]}) -> Node 2 (color {colors[2]}) -> Node 3 (color {colors[3]})")
    print(f"Query: Find maximum beautiful set in subtree rooted at 0")
    
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"Result: {result}")
    print(f"Explanation: All nodes have color 1. We can take alternating nodes:")
    print(f"             Take nodes 0, 2 (not adjacent) = 2, OR")
    print(f"             Take nodes 1, 3 (not adjacent) = 2")
    print(f"             Maximum: 2")
    print()

def example_3_star_tree():
    """Example 3: Star tree with different colors"""
    print("Example 3: Star tree with different colors")
    print("=" * 50)
    
    # Tree structure: 0 -> [1, 2, 3, 4]
    n = 5
    parents = [-1, 0, 0, 0, 0]
    colors = [1, 2, 2, 2, 2]
    queries = [0]
    
    print(f"Tree structure:")
    print(f"  Node 0 (color {colors[0]}) -> Nodes 1,2,3,4 (all color {colors[1]})")
    print(f"Query: Find maximum beautiful set in subtree rooted at 0")
    
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"Result: {result}")
    print(f"Explanation: For color 1, we can take only node 0 (max=1)")
    print(f"             For color 2, we can take all children 1,2,3,4 (max=4)")
    print(f"             Since children are not adjacent to each other")
    print(f"             Maximum: 4")
    print()

def example_4_multiple_queries():
    """Example 4: Multiple queries on the same tree"""
    print("Example 4: Multiple queries on the same tree")
    print("=" * 50)
    
    # Tree structure: 0 -> [1, 2], 1 -> [3]
    n = 4
    parents = [-1, 0, 0, 1]
    colors = [1, 1, 2, 1]
    queries = [0, 1, 2, 3]
    
    print(f"Tree structure:")
    print(f"  Node 0 (color {colors[0]}) -> Node 1 (color {colors[1]}), Node 2 (color {colors[2]})")
    print(f"  Node 1 (color {colors[1]}) -> Node 3 (color {colors[3]})")
    print(f"Queries: Find maximum beautiful set for subtrees rooted at 0, 1, 2, 3")
    
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"Result: {result}")
    print(f"Explanation:")
    print(f"  Query 0 (whole tree): max beautiful set = 2 (nodes 0,3 or just node 2)")
    print(f"  Query 1 (subtree 1->3): max beautiful set = 1 (either node 1 or 3)")
    print(f"  Query 2 (node 2 alone): max beautiful set = 1 (just node 2)")
    print(f"  Query 3 (node 3 alone): max beautiful set = 1 (just node 3)")
    print(f"  Sum: 2 + 1 + 1 + 1 = 5")
    print()

def example_5_class_usage():
    """Example 5: Using the TreeBeautifulSet class directly"""
    print("Example 5: Using TreeBeautifulSet class directly")
    print("=" * 50)
    
    # Create solver instance
    solver = TreeBeautifulSet()
    
    # Build tree
    n = 6
    parents = [-1, 0, 0, 1, 1, 2]
    colors = [1, 2, 1, 2, 1, 2]
    
    solver.build_tree(n, parents, colors)
    
    print(f"Tree built with {n} nodes")
    print(f"Parents: {parents}")
    print(f"Colors: {colors}")
    print()
    
    # Test individual queries
    for root in range(n):
        result = solver.find_max_beautiful_set(root)
        print(f"Subtree rooted at {root}: max beautiful set = {result}")
    
    # Process multiple queries
    queries = [0, 1, 2]
    total = solver.process_queries(queries)
    print(f"\nTotal for queries {queries}: {total}")
    print()

def interactive_demo():
    """Interactive demo where user can input their own tree"""
    print("Interactive Demo")
    print("=" * 50)
    print("Enter your own tree to test the algorithm!")
    print()
    
    try:
        n = int(input("Enter number of nodes: "))
        print(f"Enter parent array for {n} nodes (use -1 for root):")
        parents = list(map(int, input().split()))
        print(f"Enter colors for {n} nodes:")
        colors = list(map(int, input().split()))
        print(f"Enter number of queries:")
        q = int(input())
        print(f"Enter {q} query nodes:")
        queries = list(map(int, input().split()))
        
        print("\nProcessing...")
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        print(f"Result: {result}")
        
    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")
        print("Please ensure all inputs are valid integers.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main function to run all examples"""
    print("Tree Beautiful Set Problem - Usage Examples")
    print("=" * 60)
    print()
    
    # Run all examples
    example_1_simple_tree()
    example_2_linear_tree()
    example_3_star_tree()
    example_4_multiple_queries()
    example_5_class_usage()
    
    # Ask if user wants to try interactive demo
    print("Would you like to try the interactive demo? (y/n)")
    response = input().strip().lower()
    if response == 'y' or response == 'yes':
        interactive_demo()
    
    print("\nThank you for using Tree Beautiful Set solver!")

if __name__ == "__main__":
    main()