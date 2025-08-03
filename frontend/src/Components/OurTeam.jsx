import React from "react";
import OurTeamData from "./OurTeamData";
import { Box, Typography } from "@mui/material";
import { keyframes } from "@emotion/react";

// Glowing Animation
const glow = keyframes`
  0% { text-shadow: 0 0 10px #A020F0, 0 0 20px #8A2BE2; }
  50% { text-shadow: 0 0 20px #7B68EE, 0 0 30px #6A0DAD; }
  100% { text-shadow: 0 0 10px #A020F0, 0 0 20px #8A2BE2; }
`;

const Ourteam = () => {
  return (
    <Box
      sx={{
        textAlign: "center",
        p: 4,
        background: "linear-gradient(to top, black, #3b0078)",
        minHeight: "100vh",
      }}
    >
      {/* Title with Gradient & Glow Effect */}
      <Typography
        variant="h2"
        sx={{
          fontWeight: "bold",
          backgroundColor:"white",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          
        }}
      >
        Shaurya
      </Typography>

      {/* Team Members Section */}
      <OurTeamData />
    </Box>
  );
};

export default Ourteam;