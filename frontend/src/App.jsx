import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Training from "./components/Training";
import Prediction from "./components/Prediction";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/training" element={<Training />} />
        <Route path="/prediction" element={<Prediction />} />
      </Routes>
    </Router>
  );
}

export default App;