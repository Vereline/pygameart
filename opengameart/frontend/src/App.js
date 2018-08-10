import React, { Component } from 'react';
import './styles/App.css';
import AppMenu from "./components/AppMenu";
import AppNavbar from "./components/AppNavbar";
import Card from './components/ImageCard'
import LightningCounterDisplay from './components/LightningCounter'

class App extends Component {
   render() {
    return (
      <div>
        <header>
          <AppNavbar/>
        </header>
        <div className={'container-full'}>
            <div className={'row justify-content-start'}>
                <div className={'col'}>
                    <AppMenu name={'user'} />
                    <LightningCounterDisplay/>
                </div>
                <div className={'col-10'}>
                    <Card color="#FF6663" />
                    <Card color="#FF6663" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#784c84" />
                    <Card color="#FF6663" />
                </div>
            </div>
            <div className={'row'}>
            </div>
        </div>
      </div>
    );
  }
}

export default App;