import React, { Component } from 'react';

import '../styles/AppPost.css';

class AppPost extends Component {
  render() {
    return (
      <div className="AppPost">
          <p className="PostItem">Name and avatar</p>
          <p className="PostItem">Content</p>
          <p className="PostItem">Like, comment, re-post</p>
      </div>
    );
  }
}

export default AppPost;