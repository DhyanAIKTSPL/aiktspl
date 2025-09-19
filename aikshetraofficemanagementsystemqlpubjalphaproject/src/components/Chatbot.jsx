import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Send, X, Bot } from 'lucide-react';

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);
  
  useEffect(() => {
    if (isOpen) {
      setMessages([{ from: 'bot', text: 'Hello! How can I assist you today? Try asking about "attendance", "tasks", or "leave".' }]);
    }
  }, [isOpen]);

  const getBotResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    if (lowerInput.includes('attendance')) {
      return 'You can manage your attendance, including check-in/out and leave applications, on the Attendance page.';
    }
    if (lowerInput.includes('task')) {
      return 'Your assigned tasks are listed on the Tasks page. You can view pending, accepted, and completed tasks there.';
    }
    if (lowerInput.includes('leave')) {
      return 'To apply for leave, go to the Attendance page and use the "Apply for Leave" feature.';
    }
    if (lowerInput.includes('hello') || lowerInput.includes('hi')) {
      return 'Hello there! How can I help?';
    }
    if (lowerInput.includes('help')) {
      return 'I can help with questions about attendance, tasks, and leave. What do you need assistance with?';
    }
    return "I'm sorry, I don't have information about that. Please contact support for more detailed questions.";
  };

  const handleSend = (text) => {
    const userInput = text.trim();
    if (userInput === '') return;
    
    const newMessages = [...messages, { from: 'user', text: userInput }];
    setMessages(newMessages);
    setInput('');

    setTimeout(() => {
      const botResponse = getBotResponse(userInput);
      setMessages(prev => [...prev, { from: 'bot', text: botResponse }]);
    }, 1000);
  };

  const suggestionChips = ["Attendance", "Tasks", "Apply for Leave"];

  return (
    <>
      <div className="fixed bottom-6 right-6 z-50">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsOpen(!isOpen)}
          className="bg-primary hover:bg-primary-hover text-white rounded-full p-4 shadow-lg shadow-primary/30"
        >
          {isOpen ? <X className="h-6 w-6" /> : <MessageSquare className="h-6 w-6" />}
        </motion.button>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            transition={{ duration: 0.3 }}
            className="fixed bottom-24 right-6 w-80 h-[32rem] bg-surface border border-border rounded-2xl shadow-2xl flex flex-col z-50"
          >
            <div className="flex items-center justify-between p-4 border-b border-border">
              <div className="flex items-center space-x-2">
                <Bot className="h-6 w-6 text-primary" />
                <h3 className="font-semibold text-text-primary">AIKSHETRA Bot</h3>
              </div>
              <button onClick={() => setIsOpen(false)} className="text-text-secondary hover:text-text-primary">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="flex-1 p-4 space-y-4 overflow-y-auto">
              {messages.map((msg, index) => (
                <div key={index} className={`flex ${msg.from === 'bot' ? 'justify-start' : 'justify-end'}`}>
                  <div className={`max-w-[80%] p-3 rounded-xl ${
                    msg.from === 'bot'
                      ? 'bg-background text-text-primary rounded-bl-none'
                      : 'bg-primary text-white rounded-br-none'
                  }`}>
                    <p className="text-sm">{msg.text}</p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div className="p-4 border-t border-border">
              <div className="flex flex-wrap gap-2 mb-2">
                {suggestionChips.map(chip => (
                  <button key={chip} onClick={() => handleSend(chip)} className="px-3 py-1 bg-background text-text-secondary text-xs rounded-full hover:bg-primary hover:text-white transition-colors">
                    {chip}
                  </button>
                ))}
              </div>
              <div className="relative">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend(input)}
                  placeholder="Type a message..."
                  className="w-full bg-background border border-border rounded-lg pl-4 pr-12 py-2 text-text-primary focus:ring-2 focus:ring-primary"
                />
                <button onClick={() => handleSend(input)} className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-text-secondary hover:text-primary">
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export default Chatbot;
