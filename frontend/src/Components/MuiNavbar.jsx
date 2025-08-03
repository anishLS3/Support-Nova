import React, { useState } from "react";
import { AppBar, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useClerk } from "@clerk/clerk-react";

const MuiNavbar = ({ clearChat }) => {
  const navigate = useNavigate();
  const { signOut } = useClerk();

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

  const handleHome = () => {
    navigate("/homepage");
  };

  return (
    <AppBar position="relative" sx={{ backgroundColor: "#283045", padding: "5px 0", minHeight: "15px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 20px" }}>
        
        {/* Left Side: MuiDrawer + Title */}
        <div style={{ display: "flex", alignItems: "center" }}>
          
          <h2
            style={{
              fontWeight: "bold",
              fontFamily: "'Poppins', sans-serif",
              background: "linear-gradient(to right, #006eff, #6047bb)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              marginLeft: "15px",
            }}
          >
            Nova-Bot
          </h2>
        </div>

        {/* Right Side: Buttons (Home + Logout) */}
        <div style={{ display: "flex", gap: "10px" }}>
          <Button
            onClick={handleHome}
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
            Home
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

export default MuiNavbar;
