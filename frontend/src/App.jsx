import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { SignIn, SignUp, useUser, useClerk } from "@clerk/clerk-react";
import Muihomepage from "./Components/MuiHomePage";
import HomePage from "./Components/Homepage";
import Login from "./Components/Login";

import { NavigationProvider } from "./Context/NavigationProvider";
import Ourteam from "./Components/OurTeam";

const API_URL = "http://127.0.0.1:5000"; // Backend API URL

function App() {
  return (
    <Router>
      <NavigationProvider>
        <AppContent />
      </NavigationProvider>
    </Router>
  );
}

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const { isSignedIn, user } = useUser();
  const { signOut } = useClerk(); // Clerk signOut function

  const [apiData, setApiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch API data on mount
  useEffect(() => {
    console.log("Fetching data from API...");
    fetch(API_URL)
      .then((response) => response.json())
      .then((data) => {
        console.log("Data received:", data);
        setApiData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Handle sign-in success
  useEffect(() => {
    if (isSignedIn) {
      handleSignInSuccess(user);
    }
  }, [isSignedIn, user]);

  const handleSignInSuccess = async (user) => {
    if (!user || !user.id) {
      console.error("User ID is missing!");
      return;
    }
  
    console.log("User signed in:", user.id);
  
    const email = user.primaryEmailAddress?.emailAddress || "";
    localStorage.setItem("userId", user.id);
    localStorage.setItem("email", email);
  
    try {
      console.log("hello");
      const response = await fetch(`${API_URL}/signin`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: user.id,  // Ensure Clerk provides a valid userId
          email: email,
        }),
      });
  
      if (!response.ok) throw new Error(`HTTP Error! Status: ${response.status}`);
  
      const data = await response.json();
      console.log("Backend response:", data);
      navigate("/homepage");
    } catch (error) {
      console.error("Error sending sign-in data:", error);
    }
  };
  

  const handleSignUpSuccess = (user) => {
    console.log("User signed up:", user.id);
    
    const email = user.primaryEmailAddress?.emailAddress || "";
    localStorage.setItem("userId", user.id);
    localStorage.setItem("email", email);

    fetch(`${API_URL}/signin`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: user.id,
        email: email,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Backend response:", data);
        navigate("/homepage");
      })
      .catch((error) => console.error("Error sending sign-up data:", error));
  };

  const handleLogout = async () => {
    try {
      await signOut();
      localStorage.removeItem("userId");
      localStorage.removeItem("email");

      window.location.href = "/"; // Redirect to Clerk sign-in
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <>
      {location.pathname === "/" && <Login />}

      <div
        className="auth-container"
        style={
          location.pathname === "/"
            ? {
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                backgroundColor: '#000000',
              }
            : {}
        }
      >
        <Routes>
          <Route
            path="/"
            element={<SignIn afterSignInUrl="/homepage" />}
          />
          <Route
            path="/signup"
            element={<SignUp afterSignUpUrl="/homepage" onSignUp={handleSignUpSuccess} />}
          />
          <Route
            path="/home"
            element={<Muihomepage data={apiData} loading={loading} error={error} />}
          />
          <Route path="/homepage" element={<HomePage handleLogout={handleLogout} />} />
          <Route path="/team" element={<Ourteam />} />
        </Routes>
      </div>
    </>
  );
}

export default App;