// ==========================================
// 3. JAVA ARRAYS & SEARCHING LOGIC
// ==========================================

public class ArrayOperations {
    public static void main(String[] args) {
        // Array Initialization
        int[] scores = {45, 88, 92, 67, 34, 90};

        // 1. Array me se Maximum Value dhoondna
        int maxScore = scores[0];
        for (int score : scores) {
            if (score > maxScore) {
                maxScore = score;
            }
        }
        System.out.println("Highest Score in Array: " + maxScore);

        // 2. Average Score Calculate karna
        int sum = 0;
        for (int score : scores) {
            sum += score;
        }
        double average = (double) sum / scores.length;
        System.out.println("Average Score: " + average);
    }
}
