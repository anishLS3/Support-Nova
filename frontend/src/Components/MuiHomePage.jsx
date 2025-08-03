import React, { useState, useEffect, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMicrophone, faArrowUp, faArrowRight, faPlus } from "@fortawesome/free-solid-svg-icons";
import "../styles.css";
import MuiNavbar from "./MuiNavbar";
import ReactMarkdown from 'react-markdown';

const API_URL = "http://127.0.0.1:5000";

const Chatbot = ({ input, setInput, sendMessage, followups, setFollowups }) => {
  const [isTyping, setIsTyping] = useState(false);
  const carouselRef = useRef(null);

  const handleInputChange = (event) => {
    setInput(event.target.value);
    setIsTyping(event.target.value.length > 0);
    if (event.target.value.length > 0) {
      setFollowups([]);
    }
  };

  const handleFollowupClick = (question) => {
    setInput(question);
    setFollowups([]);
  };

  return (
    <>
      <div className={`container ${isTyping ? "hidden" : ""}`}>
        <header className={`app-header ${isTyping ? "hidden" : ""}`}>
          <h1 className="heading">Hello, there</h1>
          <h2 className="sub-heading">How can I help you?</h2>
        </header>

        <ul className={`suggestions ${isTyping ? "hidden" : ""}`}>
          {[
            "Help me with my order status.",
            "What is your customer support number?",
            "How can I return a product?",
            "I need assistance with my recent purchase."
          ].map((text, index) => (
            <li key={index} className="suggestions-item" onClick={() => setInput(text)}>
              <span className="text">{text}</span>
              <FontAwesomeIcon icon={faArrowRight} />
            </li>
          ))}
        </ul>
      </div>

      <div className="container1">
        <div className="prompt-container">
          <div className="prompt-wrapper">
            <form className="prompt-form" onSubmit={(e) => e.preventDefault()}>
              <div className="prompt-actions">
                
                {/* Removed New Chat Button */}

                <input
                  type="text"
                  className="prompt-input"
                  placeholder="Ask CopBotChatBox"
                  value={input}
                  onChange={handleInputChange}
                />

                <div className="right-icons">
                  <button id="send-prompt-btn" type="button" onClick={sendMessage} className="icon-button">
                    <FontAwesomeIcon icon={faArrowUp} />
                  </button>
                  <button id="voice-btn" type="button" onClick={sendMessage} className="icon-button">
                    <FontAwesomeIcon icon={faMicrophone} />
                  </button>
                </div>
              </div>
            </form>
          </div>

          <div className="followup-container">
            {followups.length > 0 ? (
              <div className="followup-carousel">
                <div className="followup-questions">
                  {followups.map((question, index) => (
                    <div key={index} className="followup-question" onClick={() => handleFollowupClick(question)}>
                      {question}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="no-followups">No follow-up suggestions</p>
            )}
          </div>
        </div>
      </div>
    </>
  );
};


// Muihomepage component
const Muihomepage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [followups, setFollowups] = useState([]);

  const clearChat = () => {
    setMessages([]);
    setFollowups([]);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userId = localStorage.getItem("userId");
    const email = localStorage.getItem("email");

    setMessages((prev) => [...prev, { role: "user", text: input }]);
    setFollowups([]);
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, email, query: input }),
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      if (data.chat_id) localStorage.setItem("chatId", data.chat_id);

      setMessages((prev) => [...prev, { role: "bot", text: data.answer }]);
      if (data.followups) setFollowups(data.followups);
    } catch (error) {
      console.error("❌ Error fetching response:", error);
    } finally {
      setLoading(false);
      setInput("");
    }

    const handleNewChat = () => {
      clearChat();
      setInput("");
    };
    
  };

  return (
    <div>
  <MuiNavbar clearChat={clearChat} />
  <Chatbot
    input={input}
    setInput={setInput}
    sendMessage={sendMessage}
    followups={followups}
    setFollowups={setFollowups}
    clearChat={clearChat}
  />
  <div className="chat-container">
    <div className="chat-messages">
      {messages.map((msg, index) => (
        <div key={index} className={msg.role === "user" ? "user-msg" : "bot-msg"}>
          <ReactMarkdown>{msg.text}</ReactMarkdown>
        </div>
      ))}
      {loading && <p className="loading">Thinking...</p>}
    </div>
  </div>
</div>

  );
};

export default Muihomepage;
