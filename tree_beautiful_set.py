"""
Tree Beautiful Set Problem Solution

This module implements a solution for finding the maximum size of beautiful sets in a tree.
A beautiful set is a set of nodes where:
1. All nodes have different colors
2. For any pair of nodes, one must be an ancestor of the other

The solution processes a tree with n nodes rooted at node 1, handles color arrays,
and processes multiple queries for different subtrees.
"""

from collections import defaultdict, deque
from typing import List, Dict, Set, Tuple
import sys

MOD = 10**9 + 7

class TreeBeautifulSet:
    """
    Main class for solving the Tree Beautiful Set problem.
    """
    
    def __init__(self, n: int, parents: List[int], colors: List[int]):
        """
        Initialize the tree structure.
        
        Args:
            n: Number of nodes in the tree
            parents: Parent array where parents[i] is the parent of node i+1
            colors: Color array where colors[i] is the color of node i+1
        """
        self.n = n
        self.colors = colors
        self.tree = defaultdict(list)
        self.parent = [0] * (n + 1)
        
        # Build tree structure
        self._build_tree(parents)
    
    def _build_tree(self, parents: List[int]):
        """
        Build the tree structure from parent array.
        
        Args:
            parents: Parent array where parents[i] is the parent of node i+1
        """
        for i in range(self.n):
            node = i + 1
            parent_node = parents[i]
            
            if parent_node != 0:  # Not root
                self.tree[parent_node].append(node)
                self.parent[node] = parent_node
            else:
                self.parent[node] = 0  # Root has no parent
    
    def _get_ancestors(self, node: int) -> List[int]:
        """
        Get all ancestors of a node including the node itself.
        
        Args:
            node: The node to find ancestors for
            
        Returns:
            List of ancestors from node to root
        """
        ancestors = []
        current = node
        
        while current != 0:
            ancestors.append(current)
            current = self.parent[current]
        
        return ancestors
    
    def _is_ancestor(self, ancestor: int, descendant: int) -> bool:
        """
        Check if one node is an ancestor of another.
        
        Args:
            ancestor: Potential ancestor node
            descendant: Potential descendant node
            
        Returns:
            True if ancestor is an ancestor of descendant
        """
        current = descendant
        while current != 0:
            if current == ancestor:
                return True
            current = self.parent[current]
        return False
    
    def _find_max_beautiful_set_in_subtree(self, root: int) -> int:
        """
        Find the maximum size of beautiful set in a subtree.
        
        Args:
            root: Root of the subtree
            
        Returns:
            Maximum size of beautiful set in the subtree
        """
        # Get all nodes in the subtree
        subtree_nodes = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            subtree_nodes.append(node)
            
            for child in self.tree[node]:
                queue.append(child)
        
        # Find maximum beautiful set - it must be a chain (path) in the tree
        max_size = 0
        
        # For each node in the subtree, find the longest chain going up with different colors
        for node in subtree_nodes:
            max_size = max(max_size, self._find_longest_chain_from_node(node, set(subtree_nodes)))
        
        return max_size
    
    def _find_longest_chain_from_node(self, start_node: int, subtree_nodes: Set[int]) -> int:
        """
        Find the longest chain (path towards root) starting from a node with all different colors.
        
        Args:
            start_node: Starting node
            subtree_nodes: Set of nodes in the subtree
            
        Returns:
            Length of longest chain with different colors
        """
        seen_colors = set()
        chain_length = 0
        current = start_node
        
        while current != 0 and current in subtree_nodes:
            color = self.colors[current - 1]  # Convert to 0-indexed
            
            if color in seen_colors:
                break
            
            seen_colors.add(color)
            chain_length += 1
            current = self.parent[current]
        
        return chain_length
    
    def _is_valid_beautiful_set(self, nodes: List[int]) -> bool:
        """
        Check if a set of nodes forms a valid beautiful set.
        
        Args:
            nodes: List of nodes to check
            
        Returns:
            True if it's a valid beautiful set
        """
        if not nodes:
            return True
        
        # Check if all colors are different
        colors_used = set()
        for node in nodes:
            color = self.colors[node - 1]
            if color in colors_used:
                return False
            colors_used.add(color)
        
        # Check if for any pair, one is ancestor of another
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                node1, node2 = nodes[i], nodes[j]
                if not (self._is_ancestor(node1, node2) or self._is_ancestor(node2, node1)):
                    return False
        
        return True
    
    def process_queries(self, queries: List[int]) -> int:
        """
        Process multiple queries for different subtrees.
        
        Args:
            queries: List of root nodes for subtree queries
            
        Returns:
            Sum of answers for all queries modulo 10^9+7
        """
        total_sum = 0
        
        for root in queries:
            if 1 <= root <= self.n:
                max_size = self._find_max_beautiful_set_in_subtree(root)
                total_sum = (total_sum + max_size) % MOD
        
        return total_sum


def solve_tree_beautiful_set(n: int, parents: List[int], colors: List[int], queries: List[int]) -> int:
    """
    Main function to solve the Tree Beautiful Set problem.
    
    Args:
        n: Number of nodes
        parents: Parent array
        colors: Color array
        queries: List of subtree root queries
        
    Returns:
        Sum of answers for all queries modulo 10^9+7
    """
    solver = TreeBeautifulSet(n, parents, colors)
    return solver.process_queries(queries)


# Example usage and test cases
def main():
    """
    Main function with example test cases.
    """
    print("Tree Beautiful Set Problem Solution")
    print("=" * 50)
    
    # Test case 1: Simple tree
    print("\nTest Case 1:")
    n1 = 4
    parents1 = [0, 1, 1, 2]  # Node 1 is root, 2,3 are children of 1, 4 is child of 2
    colors1 = [1, 2, 3, 2]   # Colors for nodes 1,2,3,4
    queries1 = [1, 2]        # Query subtrees rooted at 1 and 2
    
    result1 = solve_tree_beautiful_set(n1, parents1, colors1, queries1)
    print(f"Input: n={n1}, parents={parents1}, colors={colors1}, queries={queries1}")
    print(f"Output: {result1}")
    
    # Test case 2: Larger tree
    print("\nTest Case 2:")
    n2 = 6
    parents2 = [0, 1, 1, 2, 2, 3]  # More complex tree
    colors2 = [1, 2, 1, 3, 2, 4]   # Mixed colors
    queries2 = [1, 2, 3]           # Multiple queries
    
    result2 = solve_tree_beautiful_set(n2, parents2, colors2, queries2)
    print(f"Input: n={n2}, parents={parents2}, colors={colors2}, queries={queries2}")
    print(f"Output: {result2}")
    
    # Test case 3: Single node
    print("\nTest Case 3:")
    n3 = 1
    parents3 = [0]
    colors3 = [1]
    queries3 = [1]
    
    result3 = solve_tree_beautiful_set(n3, parents3, colors3, queries3)
    print(f"Input: n={n3}, parents={parents3}, colors={colors3}, queries={queries3}")
    print(f"Output: {result3}")


if __name__ == "__main__":
    main()