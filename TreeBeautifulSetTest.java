/**
 * Test runner for TreeBeautifulSet
 * This class provides automated tests without requiring user input
 */
public class TreeBeautifulSetTest {
    
    public static void main(String[] args) {
        System.out.println("=== Tree Beautiful Set Test Suite ===\n");
        
        runBasicTests();
        runEdgeCaseTests();
        runPerformanceTest();
        
        System.out.println("=== All tests completed ===");
    }
    
    /**
     * Run basic functionality tests
     */
    public static void runBasicTests() {
        System.out.println("1. Running Basic Tests...");
        
        // Test Case 1: Simple binary tree
        System.out.println("\nTest 1.1: Simple binary tree");
        TreeBeautifulSet test1 = new TreeBeautifulSet(5);
        int[] parents1 = {-1, 0, 0, 1, 1}; // Tree: 0 is root, 1,2 are children of 0, 3,4 are children of 1
        test1.buildTree(parents1);
        test1.setColors(new int[]{1, 2, 1, 3, 2});
        
        System.out.println("Tree structure:");
        test1.printTree();
        
        int[] queries1 = {0, 1, 2};
        long[] results1 = test1.processQueries(queries1);
        System.out.println("Results:");
        for (int i = 0; i < queries1.length; i++) {
            System.out.println("  Query from root " + queries1[i] + ": " + results1[i]);
        }
        System.out.println("  Sum: " + test1.calculateSumMod(queries1));
        
        // Test Case 2: Linear tree (path)
        System.out.println("\nTest 1.2: Linear tree");
        TreeBeautifulSet test2 = new TreeBeautifulSet(4);
        int[] parents2 = {-1, 0, 1, 2}; // Linear: 0->1->2->3
        test2.buildTree(parents2);
        test2.setColors(new int[]{1, 1, 1, 1});
        
        System.out.println("Tree structure:");
        test2.printTree();
        
        int[] queries2 = {0, 1};
        long[] results2 = test2.processQueries(queries2);
        System.out.println("Results:");
        for (int i = 0; i < queries2.length; i++) {
            System.out.println("  Query from root " + queries2[i] + ": " + results2[i]);
        }
        System.out.println("  Sum: " + test2.calculateSumMod(queries2));
        
        // Test Case 3: Single node
        System.out.println("\nTest 1.3: Single node");
        TreeBeautifulSet test3 = new TreeBeautifulSet(1);
        int[] parents3 = {-1};
        test3.buildTree(parents3);
        test3.setColors(new int[]{1});
        
        long result3 = test3.processQuery(0);
        System.out.println("Single node result: " + result3);
    }
    
    /**
     * Run edge case tests
     */
    public static void runEdgeCaseTests() {
        System.out.println("\n2. Running Edge Case Tests...");
        
        // Test Case 1: Star tree (one root with many children)
        System.out.println("\nTest 2.1: Star tree");
        TreeBeautifulSet starTest = new TreeBeautifulSet(6);
        int[] starParents = {-1, 0, 0, 0, 0, 0}; // Node 0 is root, all others are its children
        starTest.buildTree(starParents);
        starTest.setColors(new int[]{1, 2, 3, 4, 5, 6});
        
        System.out.println("Star tree structure:");
        starTest.printTree();
        
        long starResult = starTest.processQuery(0);
        System.out.println("Star tree result: " + starResult);
        
        // Test Case 2: Deep tree
        System.out.println("\nTest 2.2: Deep linear tree");
        int depth = 10;
        TreeBeautifulSet deepTest = new TreeBeautifulSet(depth);
        int[] deepParents = new int[depth];
        int[] deepColors = new int[depth];
        deepParents[0] = -1;
        deepColors[0] = 1;
        for (int i = 1; i < depth; i++) {
            deepParents[i] = i - 1;
            deepColors[i] = i + 1;
        }
        deepTest.buildTree(deepParents);
        deepTest.setColors(deepColors);
        
        long deepResult = deepTest.processQuery(0);
        System.out.println("Deep tree (depth " + depth + ") result: " + deepResult);
    }
    
    /**
     * Run performance test with larger input
     */
    public static void runPerformanceTest() {
        System.out.println("\n3. Running Performance Test...");
        
        int n = 1000;
        TreeBeautifulSet perfTest = new TreeBeautifulSet(n);
        
        // Create a balanced-ish tree
        int[] perfParents = new int[n];
        int[] perfColors = new int[n];
        perfParents[0] = -1;
        perfColors[0] = 1;
        
        for (int i = 1; i < n; i++) {
            perfParents[i] = (i - 1) / 2; // Binary tree structure
            perfColors[i] = (i % 10) + 1;
        }
        
        long startTime = System.currentTimeMillis();
        perfTest.buildTree(perfParents);
        perfTest.setColors(perfColors);
        
        // Test multiple queries
        int[] perfQueries = {0, 1, 2, 10, 50, 100};
        long perfSum = perfTest.calculateSumMod(perfQueries);
        
        long endTime = System.currentTimeMillis();
        
        System.out.println("Performance test with " + n + " nodes:");
        System.out.println("  Sum of query results: " + perfSum);
        System.out.println("  Execution time: " + (endTime - startTime) + " ms");
    }
}