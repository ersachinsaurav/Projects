import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

function App() {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([
    {
      role: 'assistant',
      content:
        'Hello, I’m Entrata Dev Assist aka DevTa. What kind of support are you looking for?',
    },
  ]);
  const [isChatVisible, setIsChatVisible] = useState(false);
  const [stage, setStage] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [showOptions, setShowOptions] = useState(true);
  const [showQuitOption, setShowQuitOption] = useState(false);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [showInput, setShowInput] = useState(false);
  const chatContainerRef = useRef(null);

  const initialOptions = [
    { label: 'Docker', value: 'Docker' },
    { label: 'PHPStorm', value: 'PHPStorm' },
    { label: 'GIT', value: 'GIT' },
    { label: 'Other', value: 'Other' },
  ];

  const subOptions = {
    Docker: [
      { label: 'Docker Setup', value: 'Docker Setup' },
      { label: 'Docker Commands', value: 'Docker Commands' },
      { label: 'Issues', value: 'Issues' },
    ],
    PHPStorm: [
      { label: 'PHPStorm Setup', value: 'PHPStorm Setup' },
      { label: 'PHPUnit Setup', value: 'PHPUnit Setup' },
      { label: 'Codesniffer Setup', value: 'Codesniffer Setup' },
      { label: 'Issues', value: 'Issues' },
    ],
    GIT: [
      { label: 'GIT Setup', value: 'GIT Setup' },
      { label: 'GIT Commands', value: 'GIT Commands' },
      { label: 'Issues', value: 'Issues' },
    ],
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory, isBotTyping]);

  const handleOptionSelect = (option) => {
    setChatHistory((prevChatHistory) => [
      ...prevChatHistory,
      { role: 'user', content: option.label },
    ]);

    if (option.value === 'quit') {
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        {
          role: 'assistant',
          content: 'Thank you for using EntrataDevAssist. Have a great day!',
        },
      ]);
      setShowOptions(false);
      setShowQuitOption(false);
      setTimeout(() => {
        setIsChatVisible(false);
        resetChat();
      }, 2000);
      return;
    }

    if (stage === 0) {
      setSelectedCategory(option.value);
      setShowInput(false);
      if (option.value === 'Other') {
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { role: 'assistant', content: 'Please type your question.' },
        ]);
        setShowQuitOption(true);
        setShowInput(true);
      } else {
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          {
            role: 'assistant',
            content: `In ${option.label}, how can I help you with?`,
          },
        ]);
        setShowQuitOption(false); // Do not show Quit option yet
      }
      setStage(1);
      setShowOptions(true);
    } else if (stage === 1) {
      if (option.value === 'Issues') {
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          {
            role: 'assistant',
            content: 'Please type your question regarding issues.',
          },
        ]);
        setShowOptions(false);
        setShowQuitOption(true);
        setShowInput(true);
      } else {
        askQuestion(option.value);
        setShowOptions(false);
        setStage(0);
        setSelectedCategory('');
        setShowQuitOption(false); // Hide Quit option when asking a sub-option question
        setShowInput(false);
      }
    }
  };

  const askQuestion = async (userQuestion) => {
    const newChatHistory = [
      ...chatHistory,
      { role: 'user', content: userQuestion },
    ];
    setChatHistory(newChatHistory);
    setQuestion('');
    setIsBotTyping(true);

    try {
      const response = await axios.post('http://localhost:3001/ask', {
        question: userQuestion,
        history: newChatHistory.map((message) => ({
          role: message.role,
          content: message.content,
        })),
      });

      const answer = response.data.answer;
      setIsBotTyping(false);
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { role: 'assistant', content: answer },
        { role: 'assistant', content: 'Anything else I can help you with?' },
      ]);
      setShowOptions(true);
      setStage(0);
      setShowInput(false);
      setShowQuitOption(true); // Show Quit option after one interaction cycle
    } catch (error) {
      setIsBotTyping(false);
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { role: 'assistant', content: 'An error occurred.' },
      ]);
      setShowOptions(true);
      setStage(0);
      setShowInput(false);
      setShowQuitOption(true); // Show Quit option even if an error occurs
    }
  };

  const createMarkup = (html) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const htmlWithLinks = html.replace(urlRegex, (url) => {
      return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
    });
    return { __html: htmlWithLinks.replace(/\n/g, '<br>') };
  };

  const renderOptions = (options, includeQuit) => (
    <div className="options">
      {options.map((option, index) => (
        <button key={index} onClick={() => handleOptionSelect(option)}>
          {option.label}
        </button>
      ))}
      {includeQuit && (
        <button
          onClick={() => handleOptionSelect({ label: 'Quit', value: 'quit' })}
        >
          Quit
        </button>
      )}
    </div>
  );

  const resetChat = () => {
    setQuestion('');
    setChatHistory([
      {
        role: 'assistant',
        content:
          'Hello, I’m Entrata Dev Assist aka DevTa. What kind of support are you looking for?',
      },
    ]);
    setStage(0);
    setSelectedCategory('');
    setShowOptions(true);
    setShowQuitOption(false);
    setShowInput(false);
  };

  return (
    <div className="App">
      <button
        className="toggle-chat-btn"
        onClick={() => setIsChatVisible(!isChatVisible)}
      >
        {isChatVisible ? 'Hide DevTa' : 'Launch DevTa'}
      </button>
      {isChatVisible && (
        <div className="chat-window">
          <div className="chat-header">
            <i className="fas fa-robot"></i>
            <h1>DevTa</h1>
          </div>
          <div className="chat-container" ref={chatContainerRef}>
            {chatHistory.map((message, index) => (
              <div key={index} className={`chat-message ${message.role}`}>
                <div className="chat-avatar">
                  <i
                    className={`fas ${
                      message.role === 'user' ? 'fa-user' : 'fa-robot'
                    }`}
                  ></i>
                </div>
                <div
                  className="chat-bubble"
                  dangerouslySetInnerHTML={createMarkup(message.content)}
                ></div>
              </div>
            ))}
            {isBotTyping && (
              <div className="chat-message assistant">
                <div className="chat-avatar">
                  <i className="fas fa-robot"></i>
                </div>
                <div className="chat-bubble">
                  <i>Bot is typing...</i>
                </div>
              </div>
            )}
            {showOptions && (
              <>
                {stage === 0 && renderOptions(initialOptions, false)}
                {stage === 1 &&
                  selectedCategory !== 'Other' &&
                  !showInput &&
                  renderOptions(subOptions[selectedCategory], false)}
              </>
            )}
            {showInput && (
              <div className="input-container">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder={`Type your question regarding ${selectedCategory}`}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') askQuestion(question);
                  }}
                />
                <button onClick={() => askQuestion(question)}>
                  <i className="fas fa-paper-plane"></i>
                </button>
              </div>
            )}
            {showQuitOption && stage === 0 && (
              <div className="options">
                <button
                  onClick={() =>
                    handleOptionSelect({ label: 'Quit', value: 'quit' })
                  }
                >
                  Quit
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
