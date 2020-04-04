import React, {Component} from 'react';

class ItemSearch extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.searchItemInput = React.createRef()
        this.searchLocationSelect = React.createRef()
        this.state = {
            locations: props.locations
        }
    }

    handleSubmit(event) {
        event.preventDefault()
        this.props.handleSearch(this.searchItemInput.current.value, this.searchLocationSelect.current.value);
    }

    componentWillReceiveProps(newProps) {
        this.setState({
            locations: newProps.locations
        });
    }

    render() {
        const locationItems = this.state.locations.map((item) =>
            <option className="dropdown-item" key={item.id} value={item.id}>
                {item.name}
            </option>
        );

        return(
            <div className="row justify-content-center align-items-center pt-2">
                <div className="col justify-content-center align-items-center">
                    <form>
                        <div className="form-group">
                            <label htmlFor="itemInput">Where is</label>
                            <input id="itemInput" type="text"
                                   className="form-control"
                                   defaultValue=""
                                   ref={this.searchItemInput}
                            />
                            <label htmlFor="locationSelect">in</label>
                            <select className="custom-select"
                                    defaultValue={this.state.searchLocation}
                                    ref={this.searchLocationSelect}
                            >
                                {locationItems}
                            </select>
                        </div>
                        <button type="submit" className="btn btn-primary" onClick={this.handleSubmit}>
                            <i className="fas fa-search mr-2"></i>
                            Find!
                        </button>
                    </form>
                </div>
            </div>
        );
    }
}

export default ItemSearch;