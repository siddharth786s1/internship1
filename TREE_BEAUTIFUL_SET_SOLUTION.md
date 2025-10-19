# Tree Beautiful Set Problem Solution

## Problem Description

The Tree Beautiful Set problem asks us to find the maximum size of beautiful sets in a tree where:

1. **All nodes in the set have different colors**
2. **For any pair of nodes, one must be an ancestor of the other**

The solution processes a tree with n nodes rooted at node 1, handles color arrays, processes multiple queries for different subtrees, and returns the sum of answers modulo 10^9+7.

## Key Insights

1. **Beautiful Set Structure**: A beautiful set where every pair of nodes has an ancestor-descendant relationship forms a **chain (path)** in the tree.

2. **Algorithm**: For each subtree, we need to find the longest chain of nodes with all different colors.

3. **Implementation**: For each node in the subtree, we compute the longest path going towards the root with all different colors.

## Solution Components

### 1. Main Solution Class (`TreeBeautifulSet`)

```python
class TreeBeautifulSet:
    def __init__(self, n: int, parents: List[int], colors: List[int])
    def process_queries(self, queries: List[int]) -> int
```

### 2. Key Methods

- **`_build_tree()`**: Constructs the tree structure from parent array
- **`_find_max_beautiful_set_in_subtree()`**: Finds maximum beautiful set in a subtree
- **`_find_longest_chain_from_node()`**: Finds longest chain with different colors starting from a node
- **`_is_ancestor()`**: Checks ancestor-descendant relationship
- **`_get_ancestors()`**: Gets all ancestors of a node

### 3. Helper Functions

- **`solve_tree_beautiful_set()`**: Main solving function
- **Input/Output handling functions** for competitive programming format

## Algorithm Complexity

- **Time Complexity**: O(n * q) where n is number of nodes and q is number of queries
- **Space Complexity**: O(n) for storing tree structure and auxiliary data

## Usage Examples

### Example 1: Simple Tree
```
Input:
4
0 1 1 2
1 2 3 2
2
1
2

Output: 3
```

### Example 2: Linear Tree
```
Input:
5
0 1 2 3 4
1 2 3 4 5
2
1
3

Output: 8
```

## Files Structure

1. **`tree_beautiful_set.py`**: Core implementation with main algorithm
2. **`tree_beautiful_set_solver.py`**: Complete solution with input/output handling
3. **`test_tree_beautiful_set.py`**: Comprehensive test cases
4. **`TREE_BEAUTIFUL_SET_SOLUTION.md`**: This documentation file

## Running the Solution

### Run with test cases:
```bash
python tree_beautiful_set_solver.py test
```

### Run interactively:
```bash
python tree_beautiful_set_solver.py
```

### Run unit tests:
```bash
python test_tree_beautiful_set.py
```

## Test Results

The solution has been tested with various cases:
- ✅ Simple trees with different structures
- ✅ Linear trees (path graphs)
- ✅ Trees with repeated colors
- ✅ Single node trees
- ✅ Edge cases (empty queries, invalid nodes)
- ✅ Complex trees with multiple levels

All test cases pass successfully, demonstrating the correctness of the implementation.

## Implementation Notes

1. **Tree Building**: Uses adjacency list representation for efficient tree traversal
2. **Ancestor Tracking**: Maintains parent pointers for quick ancestor lookup
3. **Color Validation**: Ensures beautiful sets have all different colors
4. **Modular Design**: Separates core logic from input/output handling
5. **Error Handling**: Handles edge cases like invalid queries and empty inputs

The solution efficiently handles the constraints and provides correct results for all test cases.