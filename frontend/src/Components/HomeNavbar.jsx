import React from "react";
import { AppBar, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useClerk } from "@clerk/clerk-react";

const HomeNavbar = () => {
  const navigate = useNavigate();
  const { signOut } = useClerk();

  const handleChat = () => {
    navigate("/home"); // Redirect to the chat page
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
    <AppBar position="relative" sx={{ backgroundColor: "#000000", padding: "5px 0", minHeight: "15px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 20px" }}>

        {/* Left Side: Title */}
        <h2
          style={{
            fontWeight: "bold",
            fontFamily: "'Poppins', sans-serif",
            background: "linear-gradient(to right, #006eff, #6047bb)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Nova-Bot
        </h2>

        {/* Right Side: Buttons (Chat + Logout) */}
        <div style={{ display: "flex", gap: "10px" }}>
          <Button
            onClick={handleChat}
            sx={{
              color: "#fff",
              background: "linear-gradient(to right, #006eff, #6047bb)",
              fontSize: "12px",
              fontWeight: "bold",
              borderRadius: "50px",
              padding: "10px 20px",
              transition: "all 0.3s ease",
              "&:hover": {
                background: "#0264e3",
              },
            }}
          >
            Chat
          </Button>

          <Button
            onClick={handleLogout}
            sx={{
              color: "#fff",
              background: "linear-gradient(to right, #006eff, #6047bb)",
              fontSize: "12px",
              fontWeight: "bold",
              borderRadius: "50px",
              padding: "10px 20px",
              transition: "all 0.3s ease",
              "&:hover": {
                background: "#0264e3",
              },
            }}
          >
            Logout
          </Button>
        </div>

      </div>
    </AppBar>
  );
};

export default HomeNavbar;
