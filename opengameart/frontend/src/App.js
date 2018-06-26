import React, { Component } from 'react';

import './App.css';
import AppHeader from './AppHeader'
import AppFooter from './AppFooter'
import AppMenu from "./AppMenu";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">PyGameArt</h1>
          <AppHeader />
        </header>
        <AppMenu />
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
          <footer className="App-footer">
              <AppFooter />
          </footer>
      </div>
    );
  }
}

export default App;