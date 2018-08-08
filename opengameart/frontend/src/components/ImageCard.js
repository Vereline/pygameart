import React, { Component } from 'react';
import '../styles/ImageCard.css'

class Square extends Component {
    render() {
        let squareStyle = {
            height: 150,
            backgroundColor: "#FF6663"
        };

        return (
            <div style={squareStyle}>

            </div>
        );
    }
}

class TitleLabel extends Component {
    render() {
        var labelStyle = {
            fontFamily: "sans-serif",
            fontWeight: "bold",
            padding: 4,
            margin: 0
        };

        return (
            <p style={labelStyle}>#FF6663</p>
        );
    }
}

class NameLabel extends Component {
    render() {
        var labelStyle = {
            fontFamily: "sans-serif",
            fontSize: 12,
            padding: 3,
            margin: 0
        };

        return (
            <p style={labelStyle}>#FF6663</p>
        );
    }
}

class Card extends Component {
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
            <div style={cardStyle}>
                <Square/>
                <TitleLabel/>
                <NameLabel/>
            </div>
        );
    }
}

export default Card;