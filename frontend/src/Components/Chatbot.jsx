import React, { useState } from "react";
import "../styles.css"; // Make sure this file exists and is in the correct location

const API_URL = "http://127.0.0.1:5000/query";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (event) => {
    event.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setInput("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      const botMessage = { role: "bot", text: data.answer };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      backgroundColor: "#1e1e2e",
      height: "100vh",
      maxWidth: "750px",
      margin: "auto",
      padding: "20px",
      borderRadius: "10px",
      boxSizing: "border-box"
    }}>
      <div style={{
        display: "flex",
        flexDirection: "column",
        flex: 1,
        overflowY: "auto",
        marginBottom: "20px"
      }}>
        {messages.map((msg, index) => (
          <div key={index} style={{
            alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
            backgroundColor: msg.role === "user" ? "#4a4e69" : "#22223b",
            color: "#fff",
            padding: "10px 15px",
            borderRadius: "20px",
            maxWidth: "70%",
            marginBottom: "10px"
          }}>
            {msg.text}
          </div>
        ))}
        {loading && <div style={{
          alignSelf: "flex-start",
          backgroundColor: "#22223b",
          color: "#fff",
          padding: "10px 15px",
          borderRadius: "20px",
          maxWidth: "70%",
          marginBottom: "10px"
        }}>Typing...</div>}
      </div>

      <form onSubmit={sendMessage} style={{
        display: "flex",
        marginTop: "auto"
      }}>
        <input
          type="text"
          placeholder="Ask CopBotChatBox"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "20px 0 0 20px",
            border: "none",
            outline: "none"
          }}
        />
        <button type="submit" style={{
          padding: "10px 20px",
          backgroundColor: "#4a4e69",
          color: "#fff",
          border: "none",
          borderRadius: "0 20px 20px 0",
          cursor: "pointer"
        }}>⏎</button>
      </form>
    </div>
  );
};

export default Chatbot;
