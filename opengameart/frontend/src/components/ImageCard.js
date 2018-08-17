import React, { Component } from 'react';
import '../styles/ImageCard.css'
// import * as ReactDOM from "react-dom";

class Square extends Component {
    static onSquareClick(e) {
        alert('Image is tapped');
        console.log(e);
    };

    render() {
        let squareStyle = {
            height: 150,
            backgroundColor: this.props.color
        };

        return (
            <div onClick={Square.onSquareClick} style={squareStyle}>
            </div>
        );
    }
}

class TitleLabel extends Component {
    render() {
        let labelStyle = {
            fontFamily: "sans-serif",
            fontWeight: "bold",
            padding: 4,
            margin: 0
        };
        // props is not controlled by the component itself, it gets all data while creating
        // state is a thing, which is controlled by the component itself

        return (
            <p style={labelStyle}>{this.props.color}</p>
        );
    }
}

class NameLabel extends Component {
    render() {
        let labelStyle = {
            fontFamily: "sans-serif",
            fontSize: 12,
            padding: 3,
            margin: 0
        };

        return (
            <p style={labelStyle}>{this.props.color}</p>
        );
    }
}

class Card extends Component {
    componentWillUpdate(newProps, newState) {
        console.log("componentWillUpdate: Component is about to update!");
    }

    componentDidUpdate(prevProps, prevState) {
        console.log("componentDidUpdate: Component just updated!");
    }

    componentWillMount() {
        console.log("componentWillMount: Component is about to mount!");
        if (!this.props.title){
            this.titleName = "Title Name";
        }
        else {
            this.titleName = this.props.title;
        }
        console.log(this);
    }

    componentDidMount() {
        console.log("componentDidMount: Component just mounted!");
    }

    componentWillUnmount() {
        console.log("componentWillUnmount: Component is about to be removed from the DOM!");
    }

    shouldComponentUpdate(newProps, newState) {
        console.log("shouldComponentUpdate: Should component update?");

        // if (newState.count < 5) {
        //     console.log("shouldComponentUpdate: Component should update!");
        //     return true;
        // } else {
        //     ReactDOM.unmountComponentAtNode(destination);
        //     console.log("shouldComponentUpdate: Component should not update!");
        //     return false;
        // }
    }

    componentWillReceiveProps(newProps) {
        console.log("componentWillReceiveProps: Component will get new props!");
    }

    render() {
        let cardStyle = {
            height: 200,
            width: 150,
            padding: 0,
            margin: 10,
            display: 'inline-block',
            backgroundColor: "#FFF",
            WebkitFilter: "drop-shadow(0px 0px 5px #666)",
            filter: "drop-shadow(0px 0px 5px #666)"
        };

        return (
            <div className={'image-card'} style={cardStyle}>
                {/*this is made to transfer all the properties through several components*/}
                <Square {...this.props} />

                <TitleLabel color={this.titleName} />
                <NameLabel color={this.props.color} />
            </div>
        );
    }
}

export default Card;