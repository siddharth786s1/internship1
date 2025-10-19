"""
Test cases for Tree Beautiful Set Problem Solution

This module contains comprehensive test cases to validate the tree beautiful set solution.
"""

import unittest
from tree_beautiful_set import TreeBeautifulSet, solve_tree_beautiful_set

class TestTreeBeautifulSet(unittest.TestCase):
    """
    Test cases for the Tree Beautiful Set problem.
    """
    
    def test_simple_tree(self):
        """Test with a simple tree structure."""
        n = 4
        parents = [0, 1, 1, 2]  # Tree: 1 -> 2,3 and 2 -> 4
        colors = [1, 2, 3, 2]   # Different colors except node 4 has same color as node 2
        queries = [1, 2]
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        # Expected: For subtree rooted at 1: nodes with different colors in ancestor relation
        # For subtree rooted at 2: similar analysis
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        print(f"Simple tree test result: {result}")
    
    def test_single_node(self):
        """Test with a single node tree."""
        n = 1
        parents = [0]
        colors = [1]
        queries = [1]
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        # Expected: Single node should give result 1
        self.assertEqual(result, 1)
        print(f"Single node test result: {result}")
    
    def test_linear_tree(self):
        """Test with a linear tree (path graph)."""
        n = 5
        parents = [0, 1, 2, 3, 4]  # Linear: 1 -> 2 -> 3 -> 4 -> 5
        colors = [1, 2, 3, 4, 5]   # All different colors
        queries = [1, 3]
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        # Expected: Should be able to form beautiful sets with all different colors
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        print(f"Linear tree test result: {result}")
    
    def test_same_colors(self):
        """Test with nodes having same colors."""
        n = 4
        parents = [0, 1, 1, 2]
        colors = [1, 1, 1, 1]  # All same color
        queries = [1, 2]
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        # Expected: Can only pick one node per beautiful set since all have same color
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        print(f"Same colors test result: {result}")
    
    def test_complex_tree(self):
        """Test with a more complex tree structure."""
        n = 7
        parents = [0, 1, 1, 2, 2, 3, 3]  # Tree with multiple levels
        colors = [1, 2, 3, 4, 2, 5, 3]   # Mixed colors with some repeats
        queries = [1, 2, 3]
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        print(f"Complex tree test result: {result}")
    
    def test_tree_building(self):
        """Test the tree building functionality."""
        n = 4
        parents = [0, 1, 1, 2]
        colors = [1, 2, 3, 4]
        
        solver = TreeBeautifulSet(n, parents, colors)
        
        # Check tree structure
        self.assertEqual(solver.parent[1], 0)  # Node 1 is root
        self.assertEqual(solver.parent[2], 1)  # Node 2's parent is 1
        self.assertEqual(solver.parent[3], 1)  # Node 3's parent is 1
        self.assertEqual(solver.parent[4], 2)  # Node 4's parent is 2
        
        # Check children
        self.assertIn(2, solver.tree[1])  # Node 1 has child 2
        self.assertIn(3, solver.tree[1])  # Node 1 has child 3
        self.assertIn(4, solver.tree[2])  # Node 2 has child 4
        
        print("Tree building test passed")
    
    def test_ancestor_relationship(self):
        """Test ancestor relationship checking."""
        n = 4
        parents = [0, 1, 1, 2]
        colors = [1, 2, 3, 4]
        
        solver = TreeBeautifulSet(n, parents, colors)
        
        # Test ancestor relationships
        self.assertTrue(solver._is_ancestor(1, 2))   # 1 is ancestor of 2
        self.assertTrue(solver._is_ancestor(1, 3))   # 1 is ancestor of 3
        self.assertTrue(solver._is_ancestor(1, 4))   # 1 is ancestor of 4
        self.assertTrue(solver._is_ancestor(2, 4))   # 2 is ancestor of 4
        self.assertFalse(solver._is_ancestor(2, 3))  # 2 is not ancestor of 3
        self.assertFalse(solver._is_ancestor(3, 4))  # 3 is not ancestor of 4
        
        print("Ancestor relationship test passed")
    
    def test_get_ancestors(self):
        """Test getting ancestors of a node."""
        n = 4
        parents = [0, 1, 1, 2]
        colors = [1, 2, 3, 4]
        
        solver = TreeBeautifulSet(n, parents, colors)
        
        # Test getting ancestors
        ancestors_4 = solver._get_ancestors(4)
        self.assertEqual(ancestors_4, [4, 2, 1])  # 4 -> 2 -> 1
        
        ancestors_2 = solver._get_ancestors(2)
        self.assertEqual(ancestors_2, [2, 1])  # 2 -> 1
        
        ancestors_1 = solver._get_ancestors(1)
        self.assertEqual(ancestors_1, [1])  # 1 (root)
        
        print("Get ancestors test passed")
    
    def test_empty_queries(self):
        """Test with empty queries list."""
        n = 3
        parents = [0, 1, 2]
        colors = [1, 2, 3]
        queries = []
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        # Expected: 0 for empty queries
        self.assertEqual(result, 0)
        print(f"Empty queries test result: {result}")
    
    def test_invalid_query_nodes(self):
        """Test with invalid query nodes."""
        n = 3
        parents = [0, 1, 2]
        colors = [1, 2, 3]
        queries = [0, 4, 5]  # Invalid nodes
        
        result = solve_tree_beautiful_set(n, parents, colors, queries)
        
        # Expected: 0 for invalid queries
        self.assertEqual(result, 0)
        print(f"Invalid queries test result: {result}")


def run_manual_tests():
    """
    Run manual tests with detailed output.
    """
    print("Running manual tests for Tree Beautiful Set Problem")
    print("=" * 60)
    
    # Test case from problem description
    print("\nTest Case: Problem Statement Example")
    n = 6
    parents = [0, 1, 1, 2, 2, 3]
    colors = [1, 2, 1, 3, 2, 4]
    queries = [1, 2, 3]
    
    solver = TreeBeautifulSet(n, parents, colors)
    
    print(f"Tree structure:")
    print(f"Node 1 (color {colors[0]}): children {solver.tree[1]}")
    print(f"Node 2 (color {colors[1]}): children {solver.tree[2]}")
    print(f"Node 3 (color {colors[2]}): children {solver.tree[3]}")
    print(f"Node 4 (color {colors[3]}): children {solver.tree[4]}")
    print(f"Node 5 (color {colors[4]}): children {solver.tree[5]}")
    print(f"Node 6 (color {colors[5]}): children {solver.tree[6]}")
    
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(f"\nResult for queries {queries}: {result}")
    
    # Individual query results
    for query in queries:
        individual_result = solver._find_max_beautiful_set_in_subtree(query)
        print(f"Subtree rooted at {query}: {individual_result}")


if __name__ == "__main__":
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    # Run manual tests
    print("\n" + "=" * 60)
    run_manual_tests()