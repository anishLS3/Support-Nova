import React, { useState } from "react";
import { AppBar, Toolbar, Typography, IconButton, Avatar, Menu, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "../home.css"; 
import Robot from "./Robot";
import Messages from "./Messages";
import Questions from "./Questions";
import "@fortawesome/fontawesome-free/css/all.min.css";
import HomeNavbar from "./HomeNavbar";

const HomePage = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const userId = localStorage.getItem("userId");
  
  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNavigation = () => {
    navigate("/home");
  };

  return (
    <>
      <HomeNavbar />

      <div className="robot-fullpage">
        <div className="overlay-bg"></div>

        <div className="robot-container">
          <Robot />
        </div>

        <div className="overlay-text">
          <h1>Welcome to Nova-Bot !</h1>
          <button className="cta-button" onClick={() => navigate("/home")}>
            Navigate To Personalised Nova-Bot
          </button>
        </div>
      </div>

      <Questions />
      <Messages />

      <footer className="footer">
    {/* Social Media Icons with Spacing */}
    <div className="social-icons">
        <a href="#"><i className="fab fa-facebook"></i></a>
        <a href="#"><i className="fab fa-instagram"></i></a>
        <a href="#"><i className="fab fa-twitter"></i></a>
        <a href="#"><i className="fab fa-google"></i></a>
        <a href="#"><i className="fab fa-youtube"></i></a>
    </div>

    {/* Navigation Links with Spacing */}
    <div className="footer-links">
        <a href="#">Home</a>
        <a href="#">News</a>
        <a href="#">About</a>
        <a href="#">Contact Us</a>
        <a onClick={() => navigate("/team")} style={{ cursor: "pointer", textDecoration: "none" }}>Our Team</a>
    </div>

    {/* Copyright Text with Team Name Highlighted */}
    <p>Copyright © 2025, Designed & Developed by <span style={{ color: "#8a2be2" }}>Shaurya</span></p>
</footer>


    </>
  );
};

export default HomePage;