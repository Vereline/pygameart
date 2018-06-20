import React, { Component } from 'react';

import './AppHeader.css';

class AppHeader extends Component {
  render() {
    return (
      <div className="AppHeader">
        <ul className="AppHeader-list">
          <li className="AppHeader-listItem"><a href="#">Home</a></li>
          <li className="AppHeader-listItem"><a href="#">News</a></li>
          <li className="AppHeader-listItem"><a href="#">Contact</a></li>
          <li className="AppHeader-listItem"><a href="#">Popular Today</a></li>
          <li className="AppHeader-listItem"><a href="#">About</a></li>
        </ul>
      </div>
    );
  }
}

export default AppHeader;