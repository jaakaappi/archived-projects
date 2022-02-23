import React from "react";
import { useState, useEffect } from "react";

const App = () => {
  const [response, setResponse] = useState(null);

  useEffect(() => {
    fetch(process.env.REACT_APP_SERVER_URL)
      .then((response) => response.text())
      .then((data) => setResponse(data));
  });

  return <div className="App">Response: {response ? response : "Loading"}</div>;
};

export default App;
