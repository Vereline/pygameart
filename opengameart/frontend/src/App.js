import React, { Component } from 'react';
import { connect } from 'react-redux'

import {echo} from './actions/echo'
import {serverMessage} from './reducers'

import AppHeader from './components/AppHeader'
import AppFooter from './components/AppFooter'
import AppMenu from "./components/AppMenu";
import AppPost from "./components/AppPost";

class App extends Component {
  componentDidMount() {
      this.props.fetchMessage('Hi!')
  }

  render() {
    return (
      <div>
          <header className="App-header">
          <h1 className="App-title">PyGameArt</h1>
          <AppHeader />
        </header>
        <AppMenu />
          <p>
              {this.props.message}
          </p>
        <AppPost />
          <footer className="App-footer">
              <AppFooter />
          </footer>

      </div>
    );
  }
}

export default connect(
  state => ({ message: serverMessage(state) }),
  { fetchMessage: echo }
)(App);
