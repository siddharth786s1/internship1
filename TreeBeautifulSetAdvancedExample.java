/**
 * Advanced example demonstrating Tree Beautiful Set with a more complex tree structure
 */
public class TreeBeautifulSetAdvancedExample {
    
    public static void main(String[] args) {
        System.out.println("=== Advanced Tree Beautiful Set Example ===\n");
        
        // Create a more complex tree structure
        /*
         * Tree structure:
         *       0
         *     /   \
         *    1     2
         *   / \   / \
         *  3   4 5   6
         * /   /     \
         *7   8       9
         */
        
        TreeBeautifulSet complexTree = new TreeBeautifulSet(10);
        int[] parents = {-1, 0, 0, 1, 1, 2, 2, 3, 4, 6};
        int[] colors = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        
        complexTree.buildTree(parents);
        complexTree.setColors(colors);
        
        System.out.println("Complex tree structure:");
        complexTree.printTree();
        
        // Test various queries
        int[] queries = {0, 1, 2, 3, 4, 5, 6};
        long[] results = complexTree.processQueries(queries);
        
        System.out.println("\nQuery results:");
        for (int i = 0; i < queries.length; i++) {
            System.out.println("Query from root " + queries[i] + ": " + results[i]);
        }
        
        long totalSum = complexTree.calculateSumMod(queries);
        System.out.println("\nTotal sum of all queries (mod 10^9+7): " + totalSum);
        
        // Demonstrate the beautiful set property
        System.out.println("\n=== Beautiful Set Property Explanation ===");
        System.out.println("A beautiful set contains nodes where no node is an ancestor of another.");
        System.out.println("For example, in the tree above:");
        System.out.println("- {0, 3, 4, 5, 6} is NOT a beautiful set (0 is ancestor of 3, 4, 5, 6)");
        System.out.println("- {3, 4, 5, 6, 7, 8, 9} IS a beautiful set (no node is ancestor of another)");
        System.out.println("- {1, 2} IS a beautiful set (siblings, neither is ancestor of the other)");
        
        // Test with a subtree
        System.out.println("\n=== Subtree Analysis ===");
        System.out.println("Analyzing subtree rooted at node 1:");
        long subtreeResult = complexTree.processQuery(1);
        System.out.println("Maximum beautiful set size in subtree rooted at 1: " + subtreeResult);
        
        System.out.println("\nAnalyzing subtree rooted at node 2:");
        subtreeResult = complexTree.processQuery(2);
        System.out.println("Maximum beautiful set size in subtree rooted at 2: " + subtreeResult);
    }
}