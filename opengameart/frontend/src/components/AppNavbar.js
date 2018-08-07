import React, { Component } from 'react';
import '../styles/AppNavbar.css'

class AppNavbar extends Component {
    render() {
        return (
            <div className="app-navbar" >
                <nav className ="navbar navbar-expand-lg navbar-dark bg-dark">
                    <h2 className="app-logo">PyGameArt</h2>
                    <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
                        <li className="nav-item">
                            <a className="nav-link" href={null}>Home</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href={null}>News</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href={null}>Contacts</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href={null}>About</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href={null}>Sandbox</a>
                        </li>
                    </ul>

                    <form id="searchform" className="form-inline my-2 my-lg-0" method="get">
                        <input className="form-control mr-sm-2" type="text" name="search_field" placeholder="Search" />
                        <button className="btn btn-success" type="submit">Search</button>
                    </form>

                    <a className="btn btn-success login-button" href={'/'}>Login</a>
                    <a className="btn btn-success login-button" href={'/'}>Sign Up</a>
                </nav>
            </div>
        );
    }
}

export default AppNavbar;