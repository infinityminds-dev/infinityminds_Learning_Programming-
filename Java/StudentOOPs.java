// ==========================================
// 2. OOPS CONCEPT: ENCAPSULATION & CLASSES
// ==========================================

class Student {
    // Private fields (Data Protection)
    private String name;
    private int marks;

    // Constructor
    public Student(String name, int marks) {
        this.name = name;
        this.marks = marks;
    }

    // Getter Method
    public int getMarks() {
        return this.marks;
    }

    // Setter Method (Validation ke saath)
    public void setMarks(int newMarks) {
        if (newMarks >= 0 && newMarks <= 100) {
            this.marks = newMarks;
        } else {
            System.out.println("Invalid Marks!");
        }
    }

    public void displayDetails() {
        System.out.println("Student: " + name + " | Score: " + marks);
    }
}

public class StudentOOPs {
    public static void main(String[] args) {
        // Object creation
        Student s1 = new Student("Amit", 85);
        s1.displayDetails();

        // Updating marks using Setter
        s1.setMarks(95);
        System.out.println("Updated Marks: " + s1.getMarks());
    }
}
