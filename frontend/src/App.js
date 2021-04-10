import React, { useState } from "react";
import logo from './logo.svg';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);

  const callback = (ev) => {
    ev.preventDefault();
    setIsLoading(true);

    const titleInput = document.getElementById('title-input');

    fetch('http://localhost:5001/?title=' + titleInput.value)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setIsLoading(false);
      });
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {
          isLoading ? (
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          ) : (
            <form onSubmit={callback}>
              <input type="text" id="title-input" />
            </form>
          )
        }
      </header>
    </div >
  );
}

export default App;
