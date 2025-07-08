"""
Tree Beautiful Set Problem - Complete Solution with Input/Output Handling

This module provides a complete solution for the Tree Beautiful Set problem
with proper input/output handling for competitive programming format.
"""

import sys
from io import StringIO
from tree_beautiful_set import solve_tree_beautiful_set

def read_input():
    """
    Read input in the format expected by the problem.
    
    Returns:
        tuple: (n, parents, colors, queries)
    """
    # Read number of nodes
    n = int(input().strip())
    
    # Read parent array
    parents = list(map(int, input().strip().split()))
    
    # Read colors array
    colors = list(map(int, input().strip().split()))
    
    # Read number of queries
    q = int(input().strip())
    
    # Read queries
    queries = []
    for _ in range(q):
        queries.append(int(input().strip()))
    
    return n, parents, colors, queries

def solve_and_output():
    """
    Read input, solve the problem, and output the result.
    """
    n, parents, colors, queries = read_input()
    result = solve_tree_beautiful_set(n, parents, colors, queries)
    print(result)

def solve_from_string(input_string):
    """
    Solve the problem from a string input (for testing).
    
    Args:
        input_string: String containing the input
        
    Returns:
        int: Result of the problem
    """
    lines = input_string.strip().split('\n')
    n = int(lines[0])
    parents = list(map(int, lines[1].split()))
    colors = list(map(int, lines[2].split()))
    q = int(lines[3])
    queries = [int(lines[4 + i]) for i in range(q)]
    
    return solve_tree_beautiful_set(n, parents, colors, queries)

# Test cases in the expected format
def run_test_cases():
    """
    Run comprehensive test cases.
    """
    print("Running comprehensive test cases...")
    print("=" * 50)
    
    # Test case 1: Simple tree
    test1 = """4
0 1 1 2
1 2 3 2
2
1
2"""
    
    result1 = solve_from_string(test1)
    print(f"Test 1 result: {result1}")
    
    # Test case 2: Linear tree with all different colors
    test2 = """5
0 1 2 3 4
1 2 3 4 5
2
1
3"""
    
    result2 = solve_from_string(test2)
    print(f"Test 2 result: {result2}")
    
    # Test case 3: Tree with same colors
    test3 = """4
0 1 1 2
1 1 1 1
2
1
2"""
    
    result3 = solve_from_string(test3)
    print(f"Test 3 result: {result3}")
    
    # Test case 4: More complex tree
    test4 = """6
0 1 1 2 2 3
1 2 1 3 2 4
3
1
2
3"""
    
    result4 = solve_from_string(test4)
    print(f"Test 4 result: {result4}")
    
    # Test case 5: Single node
    test5 = """1
0
1
1
1"""
    
    result5 = solve_from_string(test5)
    print(f"Test 5 result: {result5}")
    
    # Test case 6: Edge case with large tree
    test6 = """10
0 1 1 2 2 3 3 4 4 5
1 2 3 4 5 6 7 8 9 10
5
1
2
3
4
5"""
    
    result6 = solve_from_string(test6)
    print(f"Test 6 result: {result6}")

def main():
    """
    Main function - handles both interactive and test modes.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test_cases()
    else:
        # Interactive mode - read from stdin
        try:
            solve_and_output()
        except EOFError:
            # If no input provided, run test cases
            run_test_cases()

if __name__ == "__main__":
    main()