import React, { useState, useEffect } from 'react';
import { 
  Container, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  Box,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [agentUsed, setAgentUsed] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [serverStatus, setServerStatus] = useState('checking');

  // Check server status on component mount and periodically
  useEffect(() => {
    checkServerStatus();
    const interval = setInterval(checkServerStatus, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const checkServerStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      if (response.data.status === "healthy") {
        setServerStatus('connected');
        setError('');
      }
    } catch (error) {
      console.error('Server status check failed:', error);
      setServerStatus('disconnected');
      setError('Backend server is not running or not healthy. Please check the server and refresh this page.');
    }
  };

  const getAgentName = (id) => {
    switch(id) {
      case 1: return "General Agent";
      case 2: return "SQL Query Generator";
      case 3: return "Calculator";
      default: return "Unknown Agent";
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (serverStatus !== 'connected') {
      setError('Cannot send message: Backend server is not connected');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      console.log('Sending request to backend...');
      const result = await axios.post(`${API_BASE_URL}/chat`, {
        message
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 60000 // Increased timeout to 60 seconds for Ollama responses
      });
      
      console.log('Received response:', result.data);
      setResponse(result.data.response);
      setAgentUsed(result.data.agent_used);
    } catch (error) {
      console.error('Error details:', error);
      let errorMessage = 'An error occurred while processing your request. ';
      
      if (error.response) {
        errorMessage += error.response.data.detail || `Server responded with: ${error.response.status}`;
      } else if (error.request) {
        if (error.code === 'ECONNABORTED') {
          errorMessage = 'The request took too long to complete. The AI model might be busy. Please try again in a few moments.';
        } else {
          errorMessage += 'No response received from server. Please check if the backend server is running.';
          // Try to reconnect to server
          checkServerStatus();
        }
      } else {
        errorMessage += error.message;
      }
      
      setError(errorMessage);
      setResponse('');
      setAgentUsed(null);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        AI Agent Chat Interface
      </Typography>
      
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
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            label="Enter your question or command"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            sx={{ mb: 2 }}
            placeholder="Try asking something like: 'Show all users from customers where age > 25' or 'Calculate 5 + 3'"
            disabled={serverStatus !== 'connected' || loading}
          />

          <Button 
            variant="contained" 
            type="submit" 
            fullWidth
            disabled={loading || serverStatus !== 'connected'}
          >
            {loading ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} />
                Processing...
              </>
            ) : 'Send'}
          </Button>
        </form>
      </Paper>

      {response && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ mr: 2 }}>
              Response:
            </Typography>
            {agentUsed && (
              <Chip 
                label={getAgentName(agentUsed)} 
                color="primary" 
                variant="outlined"
              />
            )}
          </Box>
          <Box sx={{ 
            p: 2, 
            bgcolor: 'grey.100', 
            borderRadius: 1,
            whiteSpace: 'pre-wrap'
          }}>
            {response}
          </Box>
        </Paper>
      )}
    </Container>
  );
}

export default App; 