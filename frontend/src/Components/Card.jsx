import React from "react";
import { motion } from "framer-motion";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { keyframes } from "@mui/system";

// Smoother glowing border animation
const glowingBorder = keyframes`
  0% { border-color: #A020F0; box-shadow: 0 0 8px #A020F0; }
  25% { border-color: #8A2BE2; box-shadow: 0 0 10px #8A2BE2; }
  50% { border-color: #7B68EE; box-shadow: 0 0 12px #7B68EE; }
  75% { border-color: #6A0DAD; box-shadow: 0 0 10px #6A0DAD; }
  100% { border-color: #A020F0; box-shadow: 0 0 8px #A020F0; }
`;

function MsgCard({ icon: Icon, title, description, color }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }} // Starts hidden and small
      whileInView={{ opacity: 1, scale: 1 }} // Animates when in viewport
      transition={{ duration: 0.8, ease: "easeOut" }} // Smooth transition
      viewport={{ once: false, amount: 0.3 }} // Triggers every time it appears
    >
      <Card
        sx={{
          backgroundColor: "black",
          borderRadius: "15px",
          padding: "20px",
          position: "relative",
          overflow: "hidden",
          border: "2px solid transparent",
          animation: `${glowingBorder} 5s ease-in-out infinite alternate`,
          maxWidth: "350px",
          margin: "auto",
          minHeight: "300px",
        }}
      >
        {/* Icon with a refined glow effect */}
        <Box
          sx={{
            fontSize: "3rem",
            color,
            mb: 2,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Icon
            style={{
              fontSize: "3rem",
              filter: `drop-shadow(0px 0px 12px ${color})`,
            }}
          />
        </Box>

        <CardContent sx={{ p: 0, textAlign: "center" }}>
  <Typography
    variant="h4" // Changed from h6 to h5 (larger size)
    fontWeight="900" // Increased font weight for extra bold
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
    sx={{ fontSize: "0.875rem", color: "rgba(255, 255, 255, 0.7)" }} // Kept description smaller
  >
    {description}
  </Typography>
</CardContent>

      </Card>
    </motion.div>
  );
}

export default MsgCard;