"""
Tree Beautiful Set Problem Solution

This module implements a solution for finding beautiful sets in tree structures.
A beautiful set is defined as a set of nodes where no two nodes are adjacent
and all nodes have the same color.

Problem Description:
- Given a tree with N nodes, parent array, colors array, and Q queries
- Each query asks for the sum of maximum beautiful set sizes in subtrees
- Return the sum modulo 10^9 + 7

Author: Generated for internship1 repository
"""

from collections import defaultdict
from typing import List, Dict, Tuple, Optional


class TreeBeautifulSet:
    """
    A class to handle tree operations and queries for finding beautiful sets.
    
    A beautiful set is a set of nodes where:
    1. No two nodes in the set are adjacent (connected by an edge)
    2. All nodes in the set have the same color
    """
    
    MOD = 10**9 + 7
    
    def __init__(self):
        """Initialize the TreeBeautifulSet solver."""
        self.n = 0
        self.adj = defaultdict(list)
        self.colors = []
        self.parent = []  # Store parent information
        
    def build_tree(self, n: int, parents: List[int], colors: List[int]) -> None:
        """
        Build the adjacency list representation of the tree.
        
        Args:
            n (int): Number of nodes in the tree
            parents (List[int]): Parent array where parents[i] is parent of node i
                                (parents[0] should be -1 for root)
            colors (List[int]): Color array where colors[i] is color of node i
        """
        self.n = n
        self.colors = colors[:]
        self.parent = parents[:]
        self.adj = defaultdict(list)
        
        # Build adjacency list from parent array
        for i in range(n):
            if parents[i] != -1:
                self.adj[parents[i]].append(i)
                self.adj[i].append(parents[i])
    
    def find_max_beautiful_set(self, root: int) -> int:
        """
        Find the maximum beautiful set size in the subtree rooted at the given node.
        
        Args:
            root (int): Root node of the subtree
            
        Returns:
            int: Maximum beautiful set size in the subtree
        """
        if root >= self.n or root < 0:
            return 0
        
        # Get all nodes in the subtree rooted at 'root'
        # Use the parent information to determine the correct parent
        root_parent = self.parent[root]
        
        subtree_nodes = []
        
        def collect_subtree_nodes(node, parent):
            subtree_nodes.append(node)
            for child in self.adj[node]:
                if child != parent:
                    collect_subtree_nodes(child, node)
        
        collect_subtree_nodes(root, root_parent)
        
        # Get unique colors in this subtree only
        unique_colors = set(self.colors[node] for node in subtree_nodes)
        
        max_size = 0
        
        # For each color, find the maximum beautiful set of that color in this subtree
        for color in unique_colors:
            color_max = self._solve_for_color(root, root_parent, color, set(subtree_nodes))
            max_size = max(max_size, color_max)
        
        return max_size
    
    def _solve_for_color(self, node: int, parent: int, target_color: int, subtree_nodes: set) -> int:
        """
        Solve the maximum independent set problem for nodes of a specific color.
        
        This is a classic tree DP problem: for each node, we decide whether to include it or not.
        
        Args:
            node (int): Current node
            parent (int): Parent node (-1 if root)
            target_color (int): Target color for the beautiful set
            subtree_nodes (set): Set of all nodes in the current subtree
            
        Returns:
            int: Maximum beautiful set size for this color starting from this node
        """
        # If node is not in current subtree, return 0
        if node not in subtree_nodes:
            return 0
            
        # Get children in the subtree
        children = [child for child in self.adj[node] if child != parent and child in subtree_nodes]
        
        # Base case: leaf node
        if not children:
            return 1 if self.colors[node] == target_color else 0
        
        # Option 1: Include current node (only if it has target color)
        include_current = 0
        if self.colors[node] == target_color:
            include_current = 1
            # If we include current node, we cannot include any children
            # But we can include grandchildren
            for child in children:
                grandchildren = [gc for gc in self.adj[child] if gc != node and gc in subtree_nodes]
                for grandchild in grandchildren:
                    include_current += self._solve_for_color(grandchild, child, target_color, subtree_nodes)
        
        # Option 2: Exclude current node
        exclude_current = 0
        for child in children:
            exclude_current += self._solve_for_color(child, node, target_color, subtree_nodes)
        
        return max(include_current, exclude_current)
    
    def process_queries(self, queries: List[int]) -> int:
        """
        Process multiple queries and return the sum of results.
        
        Args:
            queries (List[int]): List of root nodes for subtree queries
            
        Returns:
            int: Sum of maximum beautiful set sizes for all queries modulo MOD
        """
        total_sum = 0
        
        for root in queries:
            max_beautiful = self.find_max_beautiful_set(root)
            total_sum = (total_sum + max_beautiful) % self.MOD
        
        return total_sum
    
    def solve(self, n: int, parents: List[int], colors: List[int], queries: List[int]) -> int:
        """
        Complete solution method that builds the tree and processes queries.
        
        Args:
            n (int): Number of nodes
            parents (List[int]): Parent array
            colors (List[int]): Colors array
            queries (List[int]): Query nodes
            
        Returns:
            int: Sum of results modulo MOD
        """
        self.build_tree(n, parents, colors)
        return self.process_queries(queries)


def solve_tree_beautiful_set(n: int, parents: List[int], colors: List[int], queries: List[int]) -> int:
    """
    Convenience function to solve the Tree Beautiful Set problem.
    
    Args:
        n (int): Number of nodes in the tree
        parents (List[int]): Parent array where parents[i] is parent of node i
        colors (List[int]): Color array where colors[i] is color of node i
        queries (List[int]): List of root nodes for subtree queries
        
    Returns:
        int: Sum of maximum beautiful set sizes for all queries modulo 10^9+7
    
    Example:
        >>> n = 5
        >>> parents = [-1, 0, 0, 1, 1]  # Tree: 0 -> [1, 2], 1 -> [3, 4]
        >>> colors = [1, 1, 2, 1, 2]   # Colors for each node
        >>> queries = [0, 1]           # Query subtrees rooted at 0 and 1
        >>> result = solve_tree_beautiful_set(n, parents, colors, queries)
        >>> print(result)
    """
    solver = TreeBeautifulSet()
    return solver.solve(n, parents, colors, queries)


# Input/Output handling functions
def read_input() -> Tuple[int, List[int], List[int], List[int]]:
    """
    Read input from standard input.
    
    Expected format:
    Line 1: n (number of nodes)
    Line 2: n space-separated integers (parent array)
    Line 3: n space-separated integers (colors array)
    Line 4: q (number of queries)
    Line 5: q space-separated integers (query nodes)
    
    Returns:
        Tuple containing n, parents, colors, and queries
    """
    n = int(input().strip())
    parents = list(map(int, input().strip().split()))
    colors = list(map(int, input().strip().split()))
    q = int(input().strip())
    queries = list(map(int, input().strip().split()))
    
    return n, parents, colors, queries


def main():
    """Main function for command-line usage."""
    try:
        n, parents, colors, queries = read_input()
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()