#!/usr/bin/env python3
"""
Tree Beautiful Set Problem - Example Usage

This script demonstrates how to use the Tree Beautiful Set solution
with concrete examples.
"""

from tree_beautiful_set import TreeBeautifulSet, solve_tree_beautiful_set

def example_1():
    """
    Example 1: Simple binary tree
    
    Tree structure:
        1(color=1)
       / \
      2   3
   (c=2) (c=3)
     |
     4
   (c=2)
    """
    print("Example 1: Simple binary tree")
    print("=" * 40)
    
    n = 4
    parents = [0, 1, 1, 2]  # Node 1 is root, 2&3 are children of 1, 4 is child of 2
    colors = [1, 2, 3, 2]   # Colors: 1=1, 2=2, 3=3, 4=2
    queries = [1, 2]        # Query subtrees rooted at 1 and 2
    
    print(f"Tree: n={n}")
    print(f"Parents: {parents}")
    print(f"Colors: {colors}")
    print(f"Queries: {queries}")
    
    solver = TreeBeautifulSet(n, parents, colors)
    
    # Show tree structure
    print("\nTree structure:")
    for i in range(1, n + 1):
        children = solver.tree[i]
        color = colors[i - 1]
        print(f"Node {i} (color {color}): children {children}")
    
    # Process queries
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"\nResult for queries {queries}: {result}")
    
    # Show individual results
    for query in queries:
        individual_result = solver._find_max_beautiful_set_in_subtree(query)
        print(f"Subtree rooted at {query}: {individual_result}")

def example_2():
    """
    Example 2: Linear tree (path)
    
    Tree structure: 1 -> 2 -> 3 -> 4 -> 5
    All nodes have different colors
    """
    print("\nExample 2: Linear tree with different colors")
    print("=" * 50)
    
    n = 5
    parents = [0, 1, 2, 3, 4]  # Linear chain
    colors = [1, 2, 3, 4, 5]   # All different colors
    queries = [1, 3]           # Query subtrees rooted at 1 and 3
    
    print(f"Tree: n={n}")
    print(f"Parents: {parents}")
    print(f"Colors: {colors}")
    print(f"Queries: {queries}")
    
    solver = TreeBeautifulSet(n, parents, colors)
    
    # Show tree structure
    print("\nTree structure (linear):")
    for i in range(1, n + 1):
        children = solver.tree[i]
        color = colors[i - 1]
        parent = solver.parent[i]
        print(f"Node {i} (color {color}): parent={parent}, children={children}")
    
    # Process queries
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"\nResult for queries {queries}: {result}")
    
    # Show individual results
    for query in queries:
        individual_result = solver._find_max_beautiful_set_in_subtree(query)
        print(f"Subtree rooted at {query}: {individual_result}")

def example_3():
    """
    Example 3: Tree with repeated colors
    
    Tests how the algorithm handles nodes with same colors
    """
    print("\nExample 3: Tree with repeated colors")
    print("=" * 45)
    
    n = 6
    parents = [0, 1, 1, 2, 2, 3]  # Tree with multiple levels
    colors = [1, 2, 1, 3, 2, 4]   # Some repeated colors
    queries = [1, 2, 3]           # Multiple queries
    
    print(f"Tree: n={n}")
    print(f"Parents: {parents}")
    print(f"Colors: {colors}")
    print(f"Queries: {queries}")
    
    solver = TreeBeautifulSet(n, parents, colors)
    
    # Show tree structure
    print("\nTree structure:")
    for i in range(1, n + 1):
        children = solver.tree[i]
        color = colors[i - 1]
        parent = solver.parent[i]
        print(f"Node {i} (color {color}): parent={parent}, children={children}")
    
    # Process queries
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"\nResult for queries {queries}: {result}")
    
    # Show individual results
    for query in queries:
        individual_result = solver._find_max_beautiful_set_in_subtree(query)
        print(f"Subtree rooted at {query}: {individual_result}")
    
    # Show detailed analysis for each query
    print("\nDetailed analysis:")
    for query in queries:
        print(f"\nAnalyzing subtree rooted at {query}:")
        
        # Get all nodes in subtree
        from collections import deque
        subtree_nodes = []
        queue = deque([query])
        
        while queue:
            node = queue.popleft()
            subtree_nodes.append(node)
            
            for child in solver.tree[node]:
                queue.append(child)
        
        print(f"Nodes in subtree: {subtree_nodes}")
        
        # For each node, show the chain it can form
        for node in subtree_nodes:
            chain_length = solver._find_longest_chain_from_node(node, set(subtree_nodes))
            ancestors = solver._get_ancestors(node)
            # Filter ancestors to only those in subtree
            ancestors_in_subtree = [a for a in ancestors if a in subtree_nodes]
            print(f"  Node {node}: chain length = {chain_length}, ancestors in subtree = {ancestors_in_subtree}")

def main():
    """
    Run all examples
    """
    print("Tree Beautiful Set Problem - Examples")
    print("=" * 60)
    
    example_1()
    example_2()
    example_3()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")

if __name__ == "__main__":
    main()