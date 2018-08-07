import React, { Component } from 'react';
import '../styles/AppMenu.css'

class AppMenu extends Component {
    render() {
        return (
            <div className="app-menu">
                {/*<h2>Welcome, {this.props.name}</h2>*/}
                <ul className="list-group">
                    <li className="list-group-item  active">
                        <a className='' href={null}>Arts</a>
                    </li>
                    <li className="list-group-item ">
                        <a href={null}>Music</a>
                    </li>
                    <li className="list-group-item ">
                        <a href={null}>Gallery</a>
                    </li>
                    <li className="list-group-item ">
                        <a href={null}>Followers</a>
                    </li>
                    <li className="list-group-item ">
                        <a href={null}>Messages</a>
                    </li>
                    <li className="list-group-item ">
                        <a href={null}>Latest news</a>
                    </li>
                    <li className="list-group-item ">
                        <a href={null}>Configure account</a>
                    </li>
                </ul>
            </div>
        );
    }
}

export default AppMenu;