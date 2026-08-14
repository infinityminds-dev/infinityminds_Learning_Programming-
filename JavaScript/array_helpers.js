// ==========================================
// 1. ARRAY & DATA MANIPULATION LOGIC
// ==========================================

// Sample student data (Array of Objects)
const students = [
  { id: 1, name: "Pankaj", score: 85, passed: true },
  { id: 2, name: "Rahul", score: 40, passed: false },
  { id: 3, name: "Amit", score: 92, passed: true },
  { id: 4, name: "Vikas", score: 35, passed: false }
];

// Function 1: Sirf passed students ko filter karna
function getPassedStudents(studentList) {
  // .filter() array me se condition ke hisab se data alag karta hai
  return studentList.filter(student => student.passed === true);
}

// Function 2: Sabhi students ke scores ka average nikalna
function calculateAverageScore(studentList) {
  let totalScore = 0;
  
  // forEach loop se har student ka score add kar rahe hain
  studentList.forEach(student => {
    totalScore += student.score;
  });

  return totalScore / studentList.length;
}

// Output testing
console.log("Passed Students:", getPassedStudents(students));
console.log("Average Class Score:", calculateAverageScore(students));
