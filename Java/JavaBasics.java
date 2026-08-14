// ==========================================
// 1. JAVA BASICS & CONTROL FLOW
// ==========================================

public class JavaBasics {
    public static void main(String[] args) {
        // Data Types & Variables
        int studentAge = 21;
        double gpa = 8.5;
        String studentName = "Pankaj";
        boolean isPassed = true;

        System.out.println("Student Name: " + studentName);
        System.out.println("Age: " + studentAge + " | GPA: " + gpa);

        // Conditional Check (If-Else)
        if (isPassed && gpa >= 8.0) {
            System.out.println("Status: Outstanding Performance!");
        } else {
            System.out.println("Status: Needs Improvement.");
        }

        // Loop Logic (Printing numbers from 1 to 5)
        System.out.print("Counting: ");
        for (int i = 1; i <= 5; i++) {
            System.out.print(i + " ");
        }
        System.out.println();
    }
}
