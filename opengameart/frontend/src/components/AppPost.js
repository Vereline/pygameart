import React, { Component } from 'react';

import '../styles/AppPost.css';

class AppPost extends Component {
  render() {
    return (
      <div className="AppPost">
          <p className="PostItem">
              <a href='#'>Name</a> and and avatar
          </p>
          <p className="PostItem">Content</p>
          <p className="PostItem">
              <button>Like,</button> comment, <button>re-post</button>
          </p>
      </div>
    );
  }
}

export default AppPost;