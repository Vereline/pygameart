import React, { Component } from 'react';
import { connect } from 'react-redux'

import {echo} from './actions/echo'
import {serverMessage} from './reducers'

// import AppHeader from './components/AppHeader'
// import AppFooter from './components/AppFooter'
// import AppMenu from "./components/AppMenu";
// import AppPost from "./components/AppPost";

class App extends Component {
  componentDidMount() {
      this.props.fetchMessage('Hi!')
  }

  render() {
    return (
      <div>
          {/*<header className="App-header">*/}
          {/*<h1 className="App-title">PyGameArt</h1>*/}
          {/*<AppHeader />*/}
        {/*</header>*/}
        {/*<AppMenu />*/}
        {/*<AppPost />*/}

        {/*<p className="App-intro">*/}
          {/*To get started, edit <code>src/App.js</code> and save to reload.*/}
        {/*</p>*/}
          {/*<footer className="App-footer">*/}
              {/*<AppFooter />*/}
          {/*</footer>*/}
        <h2>Welcome to React</h2>
        <p>
          {this.props.message}
        </p>
      </div>
    );
  }
}

export default connect(
  state => ({ message: serverMessage(state) }),
  { fetchMessage: echo }
)(App);
