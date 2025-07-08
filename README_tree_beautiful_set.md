# Tree Beautiful Set Problem Solution

This implementation solves the Tree Beautiful Set problem, which involves finding the maximum size of a "beautiful set" in tree subtrees.

## Problem Description

Given a tree with N nodes, where each node has a color, find the maximum size of a beautiful set in various subtrees. A **beautiful set** is defined as:

1. A set of nodes where no two nodes are adjacent (connected by an edge)
2. All nodes in the set have the same color

## Algorithm

The solution uses dynamic programming on trees:

1. **Build Tree**: Convert parent array to adjacency list representation
2. **Subtree Collection**: For each query, collect all nodes in the specified subtree
3. **Color-wise DP**: For each color, solve the maximum independent set problem
4. **Combine Results**: Take the maximum across all colors

### Time Complexity
- **Build Tree**: O(N)
- **Per Query**: O(N × C) where C is the number of unique colors
- **Overall**: O(Q × N × C) where Q is the number of queries

### Space Complexity
- **Tree Storage**: O(N)
- **Recursion Stack**: O(N) in worst case (linear tree)

## Usage

### Basic Usage

```python
from tree_beautiful_set import solve_tree_beautiful_set

# Define tree structure
n = 4
parents = [-1, 0, 0, 1]  # Tree: 0 -> [1, 2], 1 -> [3]
colors = [1, 1, 2, 1]    # Colors for each node
queries = [0, 1, 2, 3]   # Query subtrees rooted at these nodes

result = solve_tree_beautiful_set(n, parents, colors, queries)
print(f"Result: {result}")  # Sum of all query results mod 10^9+7
```

### Using the Class Interface

```python
from tree_beautiful_set import TreeBeautifulSet

# Create solver instance
solver = TreeBeautifulSet()

# Build tree
solver.build_tree(n, parents, colors)

# Process individual queries
for root in [0, 1, 2, 3]:
    result = solver.find_max_beautiful_set(root)
    print(f"Subtree {root}: {result}")

# Process multiple queries at once
total = solver.process_queries([0, 1, 2, 3])
print(f"Total: {total}")
```

### Command Line Usage

```bash
# Run with standard input
python tree_beautiful_set.py

# Input format:
# Line 1: n (number of nodes)
# Line 2: n space-separated integers (parent array)
# Line 3: n space-separated integers (colors array)
# Line 4: q (number of queries)
# Line 5: q space-separated integers (query nodes)
```

## Examples

### Example 1: Simple Tree
```
Input:
n = 3
parents = [-1, 0, 0]
colors = [1, 1, 2]
queries = [0]

Tree structure: 0 -> [1, 2]
Colors: 0(1), 1(1), 2(2)

Output: 1
Explanation: For color 1, can take either node 0 OR 1 (max=1)
             For color 2, can take node 2 (max=1)
             Overall maximum: 1
```

### Example 2: Linear Tree
```
Input:
n = 4
parents = [-1, 0, 1, 2]
colors = [1, 1, 1, 1]
queries = [0]

Tree structure: 0 -> 1 -> 2 -> 3
Colors: All nodes have color 1

Output: 2
Explanation: Can take alternating nodes: {0, 2} or {1, 3}
             Maximum beautiful set size: 2
```

### Example 3: Star Tree
```
Input:
n = 5
parents = [-1, 0, 0, 0, 0]
colors = [1, 2, 2, 2, 2]
queries = [0]

Tree structure: 0 -> [1, 2, 3, 4]
Colors: 0(1), 1,2,3,4(2)

Output: 4
Explanation: For color 1, can take only node 0 (max=1)
             For color 2, can take all children {1,2,3,4} (max=4)
             Children are not adjacent to each other
             Maximum: 4
```

## Files

- **`tree_beautiful_set.py`**: Main implementation
- **`test_tree_beautiful_set.py`**: Comprehensive test suite
- **`tree_beautiful_set_examples.py`**: Usage examples and interactive demo
- **`README_tree_beautiful_set.md`**: This documentation

## Testing

Run the test suite:
```bash
python test_tree_beautiful_set.py
```

Run examples:
```bash
python tree_beautiful_set_examples.py
```

## Key Features

1. **Efficient Algorithm**: O(Q × N × C) time complexity
2. **Memory Optimized**: Proper subtree collection avoids unnecessary computations
3. **Modular Design**: Separate class for reusable functionality
4. **Comprehensive Testing**: 12 test cases covering edge cases and performance
5. **Clear Documentation**: Extensive examples and usage instructions
6. **Input Validation**: Handles invalid queries gracefully
7. **Interactive Demo**: User-friendly interface for testing custom inputs

## Limitations

- **Recursion Depth**: May hit recursion limit for very deep trees (>1000 nodes)
- **Memory Usage**: Stores full adjacency list and parent information
- **Color Complexity**: Performance degrades with many unique colors

## Future Improvements

1. **Iterative Implementation**: Replace recursion with iterative approach for deep trees
2. **Memoization Optimization**: Better caching strategy for repeated queries
3. **Parallel Processing**: Color-wise processing can be parallelized
4. **Memory Optimization**: Reduce memory footprint for large trees

---

*This implementation was created as part of the internship1 repository requirements.*