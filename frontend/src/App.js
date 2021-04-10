import logo from './logo.svg';
import './App.css';

function App() {
  const callback = (ev) => {
    ev.preventDefault();
    const titleInput = document.getElementById('title-input');

    fetch('http://localhost:5001/?title=' + titleInput.value)
      .then(response => response.json())
      .then(data => console.log(data));
}

return (
  <div className="App">
    <header className="App-header">
      <img src={logo} className="App-logo" alt="logo" />
      <form onSubmit={callback}>
        <input type="text" id="title-input" />
      </form>
    </header>
  </div>
);
}

export default App;
