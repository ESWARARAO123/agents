import React, { useState, useEffect, useRef } from 'react';
import {
  TextField,
  Button,
  Paper,
  Typography,
  Box,
  Chip,
  Alert,
  CircularProgress,
  Avatar,
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

const agentInfo = {
  1: { name: "General Agent", color: "primary", avatar: "🤖" },
  2: { name: "SQL Query Generator", color: "success", avatar: "🗄️" },
  3: { name: "Calculator", color: "warning", avatar: "🧮" },
};

function App() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [serverStatus, setServerStatus] = useState('checking');
  const chatEndRef = useRef(null);

  useEffect(() => {
    checkServerStatus();
    const interval = setInterval(checkServerStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chat, loading]);

  const checkServerStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      if (response.data.status === "healthy") {
        setServerStatus('connected');
        setError('');
      }
    } catch (error) {
      setServerStatus('disconnected');
      setError('Backend server is not running or not healthy. Please check the server and refresh this page.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    if (serverStatus !== 'connected') {
      setError('Cannot send message: Backend server is not connected');
      return;
    }
    setLoading(true);
    setError('');
    setChat(prev => [...prev, { role: 'user', text: message }]);
    try {
      const result = await axios.post(`${API_BASE_URL}/chat`, { message }, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 60000
      });
      setChat(prev => [
        ...prev,
        {
          role: 'agent',
          text: result.data.response,
          agentUsed: result.data.agent_used
        }
      ]);
    } catch (error) {
      let errorMessage = 'An error occurred while processing your request. ';
      if (error.response) {
        errorMessage += error.response.data.detail || `Server responded with: ${error.response.status}`;
      } else if (error.request) {
        if (error.code === 'ECONNABORTED') {
          errorMessage = 'The request took too long to complete. The AI model might be busy. Please try again in a few moments.';
        } else {
          errorMessage += 'No response received from server. Please check if the backend server is running.';
          checkServerStatus();
        }
      } else {
        errorMessage += error.message;
      }
      setChat(prev => [
        ...prev,
        { role: 'agent', text: errorMessage, agentUsed: null, error: true }
      ]);
    }
    setLoading(false);
    setMessage('');
  };

  return (
    <Box
      sx={{
        width: '100vw',
        height: '100vh',
        bgcolor: 'grey.200',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Paper
        elevation={6}
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          borderRadius: 0,
          minHeight: 0,
        }}
      >
        <Box
          sx={{
            p: 3,
            borderBottom: 1,
            borderColor: 'divider',
            bgcolor: 'primary.main',
            color: 'primary.contrastText',
          }}
        >
          <Typography variant="h5" align="left" fontWeight={600}>
            AI Agent Chat
          </Typography>
        </Box>
        <Box
          sx={{
            flex: 1,
            overflowY: 'auto',
            p: 4,
            bgcolor: 'grey.100',
            display: 'flex',
            flexDirection: 'column',
            minHeight: 0,
          }}
        >
          {serverStatus === 'checking' && (
            <Alert severity="info" sx={{ mb: 2 }}>
              Checking server connection...
            </Alert>
          )}
          {serverStatus === 'disconnected' && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Backend server is not connected. Please make sure the server is running.
            </Alert>
          )}
          {chat.length === 0 && (
            <Typography variant="body1" color="text.secondary" align="center" sx={{ mt: 4 }}>
              Start the conversation! <br />
              Try: <i>Show all users from customers where age &gt; 25</i> or <i>Calculate 5 + 3</i>
            </Typography>
          )}
          {chat.map((msg, idx) => (
            <Box
              key={idx}
              sx={{
                display: 'flex',
                flexDirection: msg.role === 'user' ? 'row-reverse' : 'row',
                alignItems: 'flex-end',
                mb: 2,
              }}
            >
              {msg.role === 'agent' && (
                <Avatar
                  sx={{
                    bgcolor: agentInfo[msg.agentUsed]?.color || 'grey.400',
                    width: 40,
                    height: 40,
                    mr: 2,
                  }}
                >
                  {agentInfo[msg.agentUsed]?.avatar || '🤖'}
                </Avatar>
              )}
              <Box
                sx={{
                  maxWidth: '40vw',
                  bgcolor: msg.role === 'user' ? 'primary.main' : 'grey.300',
                  color: msg.role === 'user' ? 'primary.contrastText' : 'text.primary',
                  p: 2,
                  borderRadius: 2,
                  borderBottomRightRadius: msg.role === 'user' ? 0 : 2,
                  borderBottomLeftRadius: msg.role === 'user' ? 2 : 0,
                  boxShadow: 2,
                  whiteSpace: 'pre-wrap',
                  fontSize: 16,
                  minHeight: 40,
                  wordBreak: 'break-word',
                }}
              >
                {msg.text}
                {msg.role === 'agent' && msg.agentUsed && (
                  <Box sx={{ mt: 1 }}>
                    <Chip
                      size="small"
                      label={agentInfo[msg.agentUsed]?.name || "Agent"}
                      color={agentInfo[msg.agentUsed]?.color || "default"}
                      variant="outlined"
                    />
                  </Box>
                )}
                {msg.error && (
                  <Typography variant="caption" color="error" sx={{ mt: 0.5, display: 'block' }}>
                    Error
                  </Typography>
                )}
              </Box>
            </Box>
          ))}
          {loading && (
            <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', mb: 2 }}>
              <Avatar sx={{ bgcolor: 'grey.400', width: 40, height: 40, mr: 2 }}>🤖</Avatar>
              <Box
                sx={{
                  bgcolor: 'grey.300',
                  p: 2,
                  borderRadius: 2,
                  borderBottomLeftRadius: 0,
                  boxShadow: 2,
                  minWidth: 120,
                }}
              >
                <CircularProgress size={20} sx={{ mr: 1 }} /> Processing...
              </Box>
            </Box>
          )}
          <div ref={chatEndRef} />
        </Box>
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            p: 3,
            borderTop: 1,
            borderColor: 'divider',
            bgcolor: 'background.paper',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <TextField
            fullWidth
            multiline
            maxRows={4}
            variant="outlined"
            placeholder="Type a message"
            value={message}
            onChange={e => setMessage(e.target.value)}
            disabled={serverStatus !== 'connected' || loading}
            sx={{ mr: 2, fontSize: 16 }}
          />
          <Button
            variant="contained"
            type="submit"
            disabled={loading || serverStatus !== 'connected' || !message.trim()}
            sx={{ minWidth: 100, fontSize: 16, py: 1.5 }}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

export default App;