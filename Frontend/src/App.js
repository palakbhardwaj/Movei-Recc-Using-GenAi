import "./App.scss";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React, { useState } from 'react';
import Home from "./Components/Home/Home";
import Header from "./Components/Header/Header";
import { Widget } from 'react-chat-widget';
import Vocal from '@untemps/react-vocal'
import 'react-chat-widget/lib/styles.css';


function App() {
  const handleNewUserMessage = (newMessage) => {
    console.log(`New message incoming! ${newMessage}`);
    // Now send the message throught the backend API
  };
  const [result, setResult] = useState('')

  const _onVocalStart = () => {
    setResult('')
  }

  const _onVocalResult = (result) => {
    setResult(result)
  }

  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
