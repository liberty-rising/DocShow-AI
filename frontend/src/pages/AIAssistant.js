import React, { useState, useRef, useEffect } from 'react';
import { Box, CircularProgress, TextField, Button, Typography, Paper } from '@mui/material';
import axios from 'axios';
import { API_URL } from '../utils/constants';

const AIAssistant = () => {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [chatHistory]);

  const handleSend = async () => {
    if (!userInput.trim() || isLoading) return;
  
    setIsLoading(true);
    setChatHistory(prevHistory => [...prevHistory, { role: 'You', message: userInput }]);
    setUserInput('');  // Clear the input field immediately
  
    try {
      const response = await axios.post(`${API_URL}chat/`, { user_input: userInput });
      const llmOutput = response.status === 200 ? response.data.llm_output : 'Failed to get response.';
      setChatHistory(prevHistory => [...prevHistory, { role: 'AI', message: llmOutput }]);
    } catch (error) {
      setChatHistory(prevHistory => [...prevHistory, { role: 'AI', message: 'An error occurred.' }]);
    }
  
    setIsLoading(false);
  };
  

  const handleDeleteHistory = async () => {
    // Make an API call to delete history
    try {
      const response = await axios.delete(`${API_URL}chat_history/`);
      if (response.status === 200) {
        setChatHistory([]);
      } else {
        console.error('Failed to delete chat history');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4">💬 AI Assistant</Typography>
      <Paper style={{ height: '200px', width: '100%', overflowY: 'auto', padding: '10px', marginTop: '10px', marginBottom: '10px' }}>
        {chatHistory.map((chat, index) => (
            <Typography key={index}>{`${chat.role}: ${chat.message}`}</Typography>
        ))}
        <div ref={chatEndRef} />
      </Paper>

      <TextField
        label="You"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        fullWidth
        margin="normal"
      />
      {isLoading && <Typography>Loading...</Typography>}
      <Button 
        variant="contained" 
        color="primary" 
        onClick={handleSend}
        disabled={isLoading}
      >
        {isLoading ? <CircularProgress size={24} /> : "Send"}
      </Button>
      <Button variant="contained" color="error" onClick={handleDeleteHistory}>Delete History</Button>
    </Box>
  );
};

export default AIAssistant;
