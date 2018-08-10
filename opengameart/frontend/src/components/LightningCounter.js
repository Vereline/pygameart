import React from "react";

class LightningCounter extends React.Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            strikes: 0
        };

        this.timerTick = this.timerTick.bind(this);
    }

    timerTick() {
        this.setState({
            strikes: this.state.strikes + 100
        });
    }

    componentDidMount() {
        setInterval(this.timerTick, 1000);
    }

    render() {
        var counterStyle = {
            color: "#66FFFF",
            fontSize: 50
        };

        var count = this.state.strikes.toLocaleString();

        return (
            <h1 style={counterStyle}>{count}</h1>
        );
    }
}

class LightningCounterDisplay extends React.Component {
    render() {
        let commonStyle = {
            margin: 0,
            padding: 0
        };

        let divStyle = {
            width: 200,
            textAlign: "center",
            backgroundColor: "#343a40",
            padding: 40,
            fontFamily: "sans-serif",
            color: "rgba(255, 255, 255, 0.7)",
            borderRadius: 10,
            marginTop: 10
        };

        let textStyles = {
            emphasis: {
                fontSize: 15,
                ...commonStyle
            },
            smallEmphasis: {
                ...commonStyle
            },
            small: {
                fontSize: 15,
                opacity: 0.5,
                ...commonStyle
            }
        };

        return (
            <div style={divStyle}>
                <LightningCounter/>
                <h3 style={textStyles.smallEmphasis}>LIGHTNING STRIKES</h3>
                <h3 style={textStyles.emphasis}>WORLDWIDE</h3>
                <p style={textStyles.small}>(since you loaded this example)</p>
            </div>
        );
    }
}

export default LightningCounterDisplay;
