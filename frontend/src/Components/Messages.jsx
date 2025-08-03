import React from "react";
import MsgCard from "./Card";
import { Box, Grid } from "@mui/material";
import { FaLightbulb, FaReply, FaGlobe, FaVolumeUp, FaClock, FaSearch } from "react-icons/fa";

function Messages() {
  const messageData = [
    {
      icon: FaLightbulb,
      title: "Intelligent Document Understanding",
      description: "Extracts insights from PDFs, DOCX, and PNGs using OCR + NLP, then embeds them for deep semantic search.",
      color: "green",
    },
    {
      icon: FaSearch,
      title: "Real-Time Semantic Search",
      description: "Leverages RAG + Qdrant to instantly retrieve top-k relevant documents for accurate, contextual answers.",
      color: "blue",
    },
    {
      icon: FaReply,
      title: "Dynamic Tool Invocation",
      description: "Automatically invokes tools like search_docs or add_docs based on user intent using OpenAI Function Calling.",
      color: "purple",
    },
    {
      icon: FaClock,
      title: "Seamless Backend Operations",
      description: "FastAPI backend handles uploads, ticket creation, and doc updates without manual effort.",
      color: "orange",
    },
    {
      icon: FaGlobe,
      title: "Proactive Support Agent",
      description: "Parses queries, reasons through context, and takes action — from updating docs to generating tickets.",
      color: "red",
    },
    {
      icon: FaVolumeUp,
      title: "Contextual Responses at Scale",
      description: "Combines RAG with tool chaining to deliver accurate answers and resolve issues faster than ever.",
      color: "teal",
    },
  ];
  

  return (
    <Box sx={{ 
      p: 4, 
      background: "linear-gradient(to top, black, #3b0078)", 
      minHeight: "100vh" 
    }}>
      <Grid container spacing={2}>
        {messageData.map((msg, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <MsgCard {...msg} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default Messages;
