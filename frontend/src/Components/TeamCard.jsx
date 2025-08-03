import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, Typography, Avatar, Box, IconButton } from "@mui/material";
import { FaLinkedin } from "react-icons/fa";
import { keyframes } from "@emotion/react";

// Glowing Border Animation
const glowingBorder = keyframes`
  0% { border-color: #A020F0; box-shadow: 0 0 8px #A020F0; }
  25% { border-color: #8A2BE2; box-shadow: 0 0 10px #8A2BE2; }
  50% { border-color: #7B68EE; box-shadow: 0 0 12px #7B68EE; }
  75% { border-color: #6A0DAD; box-shadow: 0 0 10px #6A0DAD; }
  100% { border-color: #A020F0; box-shadow: 0 0 8px #A020F0; }
`;

const TeamCard = ({ image, title, description, color, linkedin }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.85 }}
      whileInView={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      viewport={{ once: false, amount: 0.3 }}
    >
      <Card
        sx={{
          backgroundColor: "black",
          borderRadius: "15px",
          padding: "25px",
          position: "relative",
          overflow: "hidden",
          border: "2px solid transparent",
          
          minWidth: "370px",
          width: "90%",
          margin: "auto",
          minHeight: "420px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        {/* Avatar */}
        <Box display="flex" justifyContent="center" mb={2}>
          <Avatar
            src={image}
            alt={title}
            sx={{
              width: 150,
              height: 150,
              border: "3px solid",
            }}
          />
        </Box>

        <CardContent sx={{ textAlign: "center" }}>
          <Typography
            variant="h4"
            fontWeight="900"
            sx={{
              mb: 1,
              background: "linear-gradient(90deg, #1CAED7, #005FCC)",
              WebkitBackgroundClip: "text",
              color: "transparent",
            }}
          >
            {title}
          </Typography>
          <Typography
            variant="body2"
            sx={{ fontSize: "0.9rem", color: "rgba(255, 255, 255, 0.8)" }}
          >
            {description}
          </Typography>

          {/* LinkedIn Icon */}
          <Box mt={2}>
            <IconButton
              component="a"
              href={linkedin}
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                color: "#0077B5",
                fontSize: "2rem",
                "&:hover": {
                  color: "#005FCC",
                  transform: "scale(1.1)",
                },
                transition: "all 0.3s ease",
              }}
            >
              <FaLinkedin />
            </IconButton>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default TeamCard;