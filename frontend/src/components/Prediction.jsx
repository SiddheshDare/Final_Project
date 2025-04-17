import React, { useState } from "react";
import { predictAttrition } from "../utils/httpsUtil";

const Prediction = () => {
  const [formData, setFormData] = useState({
    Age: "",
    BusinessTravel: "",
    DailyRate: "",
    Department: "",
    DistanceFromHome: "",
    Education: "",
    EducationField: "",
    EmployeeCount: "",
    EmployeeNumber: "",
    EnvironmentSatisfaction: "",
    Gender: "",
    HourlyRate: "",
    JobInvolvement: "",
    JobLevel: "",
    JobRole: "",
    JobSatisfaction: "",
    MaritalStatus: "",
    MonthlyIncome: "",
    MonthlyRate: "",
    NumCompaniesWorked: "",
    OverTime: "",
    PercentSalaryHike: "",
    PerformanceRating: "",
    RelationshipSatisfaction: "",
    StandardHours: "",
    StockOptionLevel: "",
    TotalWorkingYears: "",
    TrainingTimesLastYear: "",
    WorkLifeBalance: "",
    YearsAtCompany: "",
    YearsInCurrentRole: "",
    YearsSinceLastPromotion: "",
    YearsWithCurrManager: "",
  });

  const [predictionResult, setPredictionResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    
    e.preventDefault();
    setPredictionResult(null);
    const result = await predictAttrition(formData);
    setPredictionResult(result);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Employee Attrition Prediction</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-lg p-6 border rounded-lg shadow-lg">
        {Object.keys(formData).map((key) => (
          <div key={key} className="mb-4">
            <label className="block text-gray-700 font-semibold">{key}</label>
            <input
              type="text"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        ))}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
        >
          Predict
        </button>
      </form>
      
      {predictionResult && (
        <div className="mt-6 p-4 border rounded-lg shadow-md bg-gray-100 text-center">
          <h2 className="text-xl font-semibold">Prediction Result:</h2>
          <p className="text-lg">{predictionResult.prediction}</p>
          <p className="text-lg">{predictionResult.probability}</p>
        </div>
      )}
    </div>
  );
};

export default Prediction;
