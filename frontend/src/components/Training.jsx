import React, { useState } from "react";
import { trainModel } from "../utils/httpsUtil";

function Training() {
  const [response, setResponse] = useState(null);
  const [isLoading,setIsLoading] = useState(false);

  const handleTraining = async () => {
    setResponse(null);
    setIsLoading(true);
    const data = await trainModel();
    setTimeout(()=>{
      setIsLoading(false);
      setResponse(data);
    },1000);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h2 className="text-2xl font-bold mb-4">Model Training</h2>
      <button
        onClick={handleTraining}
        className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-700 mb-4"
      >
        Start Training
      </button>
      {isLoading && <p>Training in progress....</p>}
      {response && (
        <div className="p-4 bg-gray-100 rounded-lg shadow-md text-center">
          <h3 className="font-bold text-lg">Training Response:</h3>
          <p>{JSON.stringify(response)}</p>
        </div>
      )}
    </div>
  );
}

export default Training;