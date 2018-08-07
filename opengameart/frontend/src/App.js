import React, { Component } from 'react';
import './styles/App.css';
import AppMenu from "./components/AppMenu";
import AppNavbar from "./components/AppNavbar";

class App extends Component {
   render() {
    return (
      <div>
        <header>
          <AppNavbar/>
        </header>
        <AppMenu name={'user'} />
      </div>
    );
  }
}

export default App;