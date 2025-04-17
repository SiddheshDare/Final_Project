import React from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  return (
    <nav className="bg-blue-600 text-white py-4 flex justify-between items-center px-6">
      <button
        onClick={() => navigate("/")}
        className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700 transition"
      >
        Home
      </button>

      <h1 className="text-2xl font-bold flex-1 text-center">
        Employee Attrition Prediction
      </h1>
    </nav>
  );
}

export default Navbar;
