import React from "react";
import TeamCard from "./TeamCard";
import { Box, Grid } from "@mui/material";
import DanushImage from "../assets/Danush.png";
import AnishImage from "../assets/Anish.png";
import HariImage from "../assets/Hari.png";

function OurTeamData() {
  const teamData = [
    {
      image: AnishImage,
      title: "Anish",
      description: "Get precise, relevant answers using real-time context and user intent.",
      color: "green",
      linkedin: "https://www.linkedin.com/in/anish-profile/", // Add correct LinkedIn URL
    },
    {
      image: DanushImage,
      title: "Danush",
      description: "Engage in natural conversations with the ability to ask.",
      color: "blue",
      linkedin: "https://www.linkedin.com/in/DanushSenthilkumar",
    },
    {
      image: HariImage,
      title: "Hari Sabapaty",
      description: "Communicate easily in multiple languages, ensuring broad accessibility.",
      color: "red",
      linkedin: "https://www.linkedin.com/in/hari-profile/",
    },
  ];

  return (
    <Box
      id="our-team-section"
      sx={{
        p: 4,
        background: "linear-gradient(to top, black, #3b0078)",
        minHeight: "100vh",
      }}
    >
      <Grid container spacing={2}>
        {teamData.map((member, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <TeamCard {...member} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default OurTeamData;