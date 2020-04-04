import React from 'react'
import './MenuItem.css'

class MenuItem extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            text: props.text,
            focusClassName: "",
        };

        this.onClick = this.onClick.bind(this);
    }
    onClick(event){
        console.log("Clicked");
        this.setState({
            focusClassName: this.state.focusClassName === "" ? "focus" : ""
        })
    }
    render(){
        return (
        <div className={"MenuItem "+this.state.focusClassName} onClick={this.onClick}>
            {this.props.children}
            <p>{this.state.text}</p>
        </div>
        );
    }
}

export default MenuItem;