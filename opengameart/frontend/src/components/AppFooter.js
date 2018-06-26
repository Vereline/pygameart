import React, { Component } from 'react';

import '../styles/AppFooter.css';

class AppFooter extends Component {
  render() {
    return (
      <div className="AppFooter">
        <p className="AppFooter-text">Victoria Stanko, 2018</p>
        <em className="AppFooter-email">vstanko1998@gmail.com</em>
      </div>
    );
  }
}

export default AppFooter;