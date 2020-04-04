import React, {Component} from 'react';

class ResultView extends Component {
    constructor(props) {
        super(props);
        this.state = {
            items: props.items
        }
    }

    componentWillReceiveProps(newProps) {
        this.setState({items: newProps.items});
    }

    render() {
        const imgStyle = {
            width: '64px'
        };
        const itemItems = this.state.items.map((item) =>
            <li className="list-group-item" key={item.id}>
                <img className="img-thumbnail mr-2"
                     src={"http://localhost:5000/static/images/"+item.image}
                     alt="Item image"
                     style={imgStyle}
                />
                {item.name}: {item.description}
            </li>
        );

        return(
            <div>
                <hr />
                <div className="row">
                    <div className="col">
                        {this.state.items.length > 0 ? (
                            <ul className="list-group">
                                {itemItems}
                            </ul>) : (
                            "No items added yet ;_;"
                        )}
                    </div>
                </div>
            </div>
        );
    }
}

export default ResultView;