import java.util.*;
import java.io.*;

/**
 * Tree Beautiful Set Problem Solution
 * 
 * This class implements a solution for finding beautiful sets in tree structures.
 * A beautiful set is a set of nodes where no node is an ancestor of another.
 * 
 * Key features:
 * - Tree construction from parent array
 * - DFS traversal for finding maximum beautiful sets
 * - Query processing for subtrees
 * - Modulo arithmetic (10^9 + 7)
 * 
 * @author Generated for Tree Beautiful Set Problem
 */
public class TreeBeautifulSet {
    
    private static final int MOD = 1000000007;
    private List<List<Integer>> adjacencyList;
    private int[] colors;
    private int nodeCount;
    
    /**
     * Constructor to initialize the tree structure
     * @param n Number of nodes in the tree
     */
    public TreeBeautifulSet(int n) {
        this.nodeCount = n;
        this.adjacencyList = new ArrayList<>();
        this.colors = new int[n];
        
        for (int i = 0; i < n; i++) {
            adjacencyList.add(new ArrayList<>());
        }
    }
    
    /**
     * Builds the tree from parent array
     * @param parents Array where parents[i] is the parent of node i (-1 for root)
     */
    public void buildTree(int[] parents) {
        for (int i = 0; i < parents.length; i++) {
            if (parents[i] != -1) {
                adjacencyList.get(parents[i]).add(i);
                adjacencyList.get(i).add(parents[i]);
            }
        }
    }
    
    /**
     * Sets colors for nodes
     * @param nodeColors Array of colors for each node
     */
    public void setColors(int[] nodeColors) {
        System.arraycopy(nodeColors, 0, this.colors, 0, nodeColors.length);
    }
    
    /**
     * DFS to find the maximum beautiful set in a subtree
     * A beautiful set contains nodes where no node is an ancestor of another
     * 
     * @param node Current node
     * @param parent Parent node (-1 if root)
     * @param memo Memoization map for dynamic programming
     * @return Pair of (include current node, exclude current node) maximum set sizes
     */
    public long[] dfsBeautifulSet(int node, int parent, Map<String, long[]> memo) {
        String key = node + "," + parent;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }
        
        long includeNode = 1; // Include current node
        long excludeNode = 0; // Exclude current node
        
        // Process all children
        for (int child : adjacencyList.get(node)) {
            if (child != parent) {
                long[] childResult = dfsBeautifulSet(child, node, memo);
                
                // If we include current node, we can only exclude children
                includeNode = (includeNode + childResult[1]) % MOD;
                
                // If we exclude current node, we can take max of including or excluding children
                excludeNode = (excludeNode + Math.max(childResult[0], childResult[1])) % MOD;
            }
        }
        
        long[] result = {includeNode, excludeNode};
        memo.put(key, result);
        return result;
    }
    
    /**
     * Processes a query for finding beautiful sets in a subtree
     * @param rootNode Root of the subtree to process
     * @return Maximum size of beautiful set in the subtree
     */
    public long processQuery(int rootNode) {
        Map<String, long[]> memo = new HashMap<>();
        long[] result = dfsBeautifulSet(rootNode, -1, memo);
        return Math.max(result[0], result[1]) % MOD;
    }
    
    /**
     * Processes multiple queries
     * @param queries Array of root nodes for queries
     * @return Array of results for each query
     */
    public long[] processQueries(int[] queries) {
        long[] results = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            results[i] = processQuery(queries[i]);
        }
        return results;
    }
    
    /**
     * Calculates sum of all query results modulo 10^9+7
     * @param queries Array of root nodes for queries
     * @return Sum of all query results modulo 10^9+7
     */
    public long calculateSumMod(int[] queries) {
        long sum = 0;
        for (int query : queries) {
            sum = (sum + processQuery(query)) % MOD;
        }
        return sum;
    }
    
    /**
     * Main method for testing the implementation
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        try {
            // Read number of nodes
            System.out.print("Enter number of nodes: ");
            int n = scanner.nextInt();
            
            TreeBeautifulSet tbs = new TreeBeautifulSet(n);
            
            // Read parent array
            System.out.println("Enter parent array (-1 for root): ");
            int[] parents = new int[n];
            for (int i = 0; i < n; i++) {
                parents[i] = scanner.nextInt();
            }
            tbs.buildTree(parents);
            
            // Read colors (optional)
            System.out.println("Enter colors for nodes: ");
            int[] colors = new int[n];
            for (int i = 0; i < n; i++) {
                colors[i] = scanner.nextInt();
            }
            tbs.setColors(colors);
            
            // Read number of queries
            System.out.print("Enter number of queries: ");
            int q = scanner.nextInt();
            
            int[] queries = new int[q];
            System.out.println("Enter query root nodes: ");
            for (int i = 0; i < q; i++) {
                queries[i] = scanner.nextInt();
            }
            
            // Process queries and calculate sum
            long result = tbs.calculateSumMod(queries);
            System.out.println("Sum of all beautiful set sizes (mod 10^9+7): " + result);
            
            // Individual query results
            long[] individualResults = tbs.processQueries(queries);
            System.out.println("Individual query results:");
            for (int i = 0; i < q; i++) {
                System.out.println("Query " + (i+1) + " (root " + queries[i] + "): " + individualResults[i]);
            }
            
        } catch (Exception e) {
            System.err.println("Error processing input: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }
    
    /**
     * Utility method to print tree structure for debugging
     */
    public void printTree() {
        System.out.println("Tree structure:");
        for (int i = 0; i < nodeCount; i++) {
            System.out.print("Node " + i + " -> ");
            for (int neighbor : adjacencyList.get(i)) {
                System.out.print(neighbor + " ");
            }
            System.out.println();
        }
    }
    
    /**
     * Test method with sample data
     */
    public static void runTests() {
        System.out.println("Running test cases...");
        
        // Test Case 1: Simple tree
        TreeBeautifulSet test1 = new TreeBeautifulSet(5);
        int[] parents1 = {-1, 0, 0, 1, 1}; // Tree: 0 is root, 1,2 are children of 0, 3,4 are children of 1
        test1.buildTree(parents1);
        test1.setColors(new int[]{1, 2, 1, 3, 2});
        
        System.out.println("Test 1 - Tree structure:");
        test1.printTree();
        
        int[] queries1 = {0, 1, 2};
        long[] results1 = test1.processQueries(queries1);
        System.out.println("Test 1 Results:");
        for (int i = 0; i < queries1.length; i++) {
            System.out.println("Query from root " + queries1[i] + ": " + results1[i]);
        }
        System.out.println("Sum: " + test1.calculateSumMod(queries1));
        
        System.out.println();
        
        // Test Case 2: Linear tree
        TreeBeautifulSet test2 = new TreeBeautifulSet(4);
        int[] parents2 = {-1, 0, 1, 2}; // Linear: 0->1->2->3
        test2.buildTree(parents2);
        test2.setColors(new int[]{1, 1, 1, 1});
        
        System.out.println("Test 2 - Linear tree:");
        test2.printTree();
        
        int[] queries2 = {0, 1};
        long[] results2 = test2.processQueries(queries2);
        System.out.println("Test 2 Results:");
        for (int i = 0; i < queries2.length; i++) {
            System.out.println("Query from root " + queries2[i] + ": " + results2[i]);
        }
        System.out.println("Sum: " + test2.calculateSumMod(queries2));
    }
}