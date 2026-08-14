// ==========================================
// 3. ASYNC / AWAIT & API DATA FETCHING LOGIC
// ==========================================

// Fake API Call simulate karne ke liye function (Promise use karke)
function fetchUserDataFromDatabase(userId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (userId > 0) {
        resolve({ id: userId, name: "Pankaj Panwar", role: "Developer" });
      } else {
        reject("Invalid User ID!");
      }
    }, 1500); // 1.5 second delay
  });
}

// Async Function to handle API Response
async function loadUserProfile(id) {
  try {
    console.log("Fetching user data... Please wait.");
    
    // await se jab tak data nahi aata, execution hold rehta hai
    const userData = await fetchUserDataFromDatabase(id);
    console.log("Data Received Successfully:", userData);
    
  } catch (error) {
    console.error("Error Fetching Data:", error);
  }
}

// Function call
loadUserProfile(1);
