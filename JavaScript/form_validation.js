// ==========================================
// 2. FORM & INPUT VALIDATION LOGIC
// ==========================================

// Function 1: Username Check (Minimum 3 characters hona chahiye)
function isValidUsername(username) {
  if (!username || username.trim().length < 3) {
    return { status: false, message: "Username kam se kam 3 characters ka hona chahiye!" };
  }
  return { status: true, message: "Valid Username!" };
}

// Function 2: Password Check (Minimum 6 characters aur number hona chahiye)
function isStrongPassword(password) {
  // Check length
  if (password.length < 6) {
    return false;
  }
  
  // Check if password contains at least one number
  const hasNumber = /\d/.test(password);
  return hasNumber;
}

// Testing the validation logic
console.log("Username Check:", isValidUsername("Pan"));
console.log("Password Strong Check (pass123):", isStrongPassword("pass123"));
console.log("Password Strong Check (test):", isStrongPassword("test"));
