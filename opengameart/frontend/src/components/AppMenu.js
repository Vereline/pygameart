import React, { Component } from 'react';

import '../styles/AppMenu.css';

class AppMenu extends Component {
  render() {
    return (
      <div className="AppMenu">
        <ul className="AppMenu">
          <li className="AppMenu-listItem"><a href="#">My photos</a></li>
          <li className="AppMenu-listItem"><a href="#">My music</a></li>
          <li className="AppMenu-listItem"><a href="#">My friends</a></li>
          <li className="AppMenu-listItem"><a href="#">Popular Today</a></li>
          <li className="AppMenu-listItem"><a href="#">Latest news</a></li>
        </ul>
      </div>
    );
  }
}

export default AppMenu;