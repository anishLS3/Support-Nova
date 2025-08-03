import React from "react";
import "../styles1.css"; 

const Questions = () => {
    return (
        <div className="questions-container">

            {/* First Row (Text Right, Image Left) */}
            <div className="full-width-card">
                <img src="/chat-icon.png" alt="Chatbot Assistance" className="card-image" />
                <div className="card-content">
                    <h2>Instant Customer Assistance</h2>
                    <p>Get personalized support for your queries anytime with our AI chatbot.</p>
                </div>
            </div>

            {/* Second Row (Text Left, Image Right) */}
            <div className="full-width-card reverse">
                <div className="card-content">
                    <h2>Order Tracking & Help</h2>
                    <p>Track your orders and get instant updates or solutions for delivery issues.</p>
                </div>
                <img src="/order-icon.png" alt="Order Assistance" className="card-image" />
            </div>

            {/* Third Row (Text Right, Image Left) */}
            <div className="full-width-card">
                <img src="/return-icon.png" alt="Return or Refund" className="card-image" />
                <div className="card-content">
                    <h2>Returns & Refunds Made Easy</h2>
                    <p>Need help with returns? Our chatbot guides you through the entire process.</p>
                </div>
            </div>
        </div>
    );
};

export default Questions;