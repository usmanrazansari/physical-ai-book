import React, { useState } from 'react';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);

  const BACKEND_URL = "https://usmanhello-physical-ai-book.hf.space";  // Your live HF URL

  const sendQuery = async () => {
    if (!query.trim()) return;
    setHistory([...history, { sender: 'You', text: query }]);
    try {
      const resp = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await resp.json();
      setHistory(prev => [...prev, { sender: 'Bot', text: data.answer || 'No answer' }]);
    } catch (e) {
      setHistory(prev => [...prev, { sender: 'Bot', text: 'Error: Connection issue. Try again.' }]);
    }
    setQuery('');
  };

  return (
    <>
      {/* Floating Bubble */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          background: '#007bff',
          color: 'white',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
          zIndex: 1000,
          fontSize: '30px'
        }}
      >
        💬
      </div>

      {/* Chat Modal */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '90px',
          right: '20px',
          width: '350px',
          height: '500px',
          background: 'white',
          borderRadius: '10px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
          display: 'flex',
          flexDirection: 'column',
          zIndex: 1000
        }}>
          <div style={{ background: '#007bff', color: 'white', padding: '10px', borderTopLeftRadius: '10px', borderTopRightRadius: '10px' }}>
            Physical AI Book Chatbot
          </div>
          <div style={{ flex: 1, padding: '10px', overflowY: 'auto' }}>
            {history.map((msg, i) => (
              <div key={i} style={{ textAlign: msg.sender === 'You' ? 'right' : 'left', margin: '5px 0' }}>
                <strong>{msg.sender}:</strong> {msg.text}
              </div>
            ))}
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendQuery()}
            placeholder="Ask a question..."
            style={{ width: '100%', padding: '10px', border: 'none', borderTop: '1px solid #eee' }}
          />
        </div>
      )}
    </>
  );
};


export default ChatWidget;
