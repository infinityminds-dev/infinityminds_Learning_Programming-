// ===================================================
// JAVASCRIPT ALL OPERATORS MASTER FILE
// ===================================================

// 1. ARITHMETIC OPERATORS (Maths)
let num1 = 10;
let num2 = 3;

console.log("Addition (+):", num1 + num2);        // 13
console.log("Subtraction (-):", num1 - num2);     // 7
console.log("Multiplication (*):", num1 * num2);  // 30
console.log("Division (/):", num1 / num2);        // 3.333...
console.log("Modulus/Remainder (%):", num1 % num2); // 1
console.log("Exponentiation (**):", num1 ** num2); // 10^3 = 1000

// ---------------------------------------------------

// 2. INCREMENT & DECREMENT OPERATORS
let count = 5;
count++; // Increment (Value + 1)
console.log("Count after ++:", count); // 6

count--; // Decrement (Value - 1)
console.log("Count after --:", count); // 5

// ---------------------------------------------------

// 3. ASSIGNMENT OPERATORS (Value set/update karna)
let score = 50;

score += 10; // score = score + 10 (60)
score -= 5;  // score = score - 5  (55)
score *= 2;  // score = score * 2  (110)
score /= 2;  // score = score / 2  (55)
console.log("Final Score:", score);

// ---------------------------------------------------

// 4. COMPARISON OPERATORS (Tulna karna)
let x = 10;
let y = "10";
let z = 20;

console.log("Equal to (==) [Value Only]:", x == y);     // true
console.log("Strict Equal (===) [Value + Type]:", x === y); // false (Number vs String)
console.log("Not Equal (!=):", x != z);                 // true
console.log("Greater Than (>):", z > x);                // true
console.log("Less Than (<):", x < z);                   // true
console.log("Greater Than or Equal (>=):", x >= 10);    // true
console.log("Less Than or Equal (<=):", x <= 5);        // false

// ---------------------------------------------------

// 5. LOGICAL OPERATORS (Multiple conditions check karna)
let isAdult = true;
let hasLicense = false;

// AND (&&): Dono condition true honi chahiye
console.log("Can Drive (&&):", isAdult && hasLicense); // false

// OR (||): Ek bhi condition true ho toh chalega
console.log("Has Any ID (||):", isAdult || hasLicense); // true

// NOT (!): Reverse/Ulla kar deta hai
console.log("NOT Operator (!):", !isAdult); // false
