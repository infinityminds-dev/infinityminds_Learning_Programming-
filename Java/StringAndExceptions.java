// ==========================================
// 4. JAVA STRINGS & EXCEPTION HANDLING
// ==========================================

public class StringAndExceptions {
    public static void main(String[] args) {
        // --- A. STRING METHODS ---
        String text = "Java Programming";
        
        System.out.println("Original String: " + text);
        System.out.println("Length: " + text.length());
        System.out.println("Uppercase: " + text.toUpperCase());
        System.out.println("Contains 'Prog': " + text.contains("Prog"));

        // --- B. EXCEPTION HANDLING (Try-Catch) ---
        System.out.println("\n--- Exception Handling Demo ---");
        try {
            int number = 10;
            int result = number / 0; // Divided by zero error
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error Caught: Cannot divide by zero!");
        } finally {
            System.out.println("Finally block: Always executes.");
        }
    }
}
