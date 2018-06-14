import React, { Component } from 'react';

// import logo from './logo.svg';
import './App.css';

// class App extends Component {
//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <h1 className="App-title">Welcome to React</h1>
//         </header>
//         <p className="App-intro">
//           To get started, edit <code>src/App.js</code> and save to reload.
//         </p>
//       </div>
//     );
//   }
// }

// const list = [
//   {
//     'id': 1,
//     'title': '1st Item',
//     'description': 'Description here.'
//   },
//   {
//     'id': 2,
//     'title': '2nd Item',
//     'description': 'Another description here.'
//   },
//   {
//     'id': 3,
//     'title': '3rd Item',
//     'description': 'Third description here.'
//   }
// ];
//
//
// class App extends Component {
//   constructor(props) {
//     super(props);
//     this.state = { list };
//   }
//
//   render() {
//     return (
//       <div>
//         {this.state.list.map(item => (
//           <div>
//             <h1>{item.title}</h1>
//             <span>{item.description}</span>
//           </div>
//         ))}
//       </div>
//     );
//   }
// }

class App extends Component {
  state = {
    arts: []
  };

  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/arts/');
      const arts = await res.json();
      this.setState({
        arts
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
      <div>
        {this.state.arts.map(item => (
          <div key={item.id}>
            <h1>{item.title}</h1>
            <span>{item.description}</span>
            <img src={"opengameart/"+item.file_path}  alt="logo"/>
            <h2>{item.file_path}</h2>
            <h2>{item.likes}</h2>
            <p>
                Likes
                <h2>{item.likes}</h2>
            </p>
          </div>
        ))}
      </div>
    );
  }
}



export default App;
