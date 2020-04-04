import React from 'react';
import './App.css';
import Menu from './components/menu/Menu'
import MenuItem from './components/menu/MenuItem'

function App() {
  return (
    <div className="App">
      <Menu>
        <MenuItem text="Helms">
          <i className="flaticon-boat"></i>
        </MenuItem>
        <MenuItem text="Communications">
          <i className="flaticon-wifi"></i>
          </MenuItem>
        <MenuItem text="Engine room">
          <i className="flaticon-car"></i>
          </MenuItem>
        <MenuItem text="Crew">
          <i className="flaticon-group"></i>
        </MenuItem>
        <MenuItem text="Cargo hold">
          <i className="flaticon-crate"></i>
          </MenuItem>
      </Menu>
    </div>
  );
}

export default App;