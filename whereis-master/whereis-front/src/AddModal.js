import React, {Component} from 'react';
import Modal from 'react-bootstrap/Modal'

class AddModal extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.addNameInput = React.createRef()
        this.addDescriptionInput  = React.createRef()
        this.addItemImageInput  = React.createRef()
        this.addLocationInput = React.createRef()
        this.addLocationImageInput = React.createRef()

        this.state = {
            showModal: props.show,
            option: props.option,
            locations: props.locations
        }
    }

    handleSubmit(event) {
        event.preventDefault()
        var jsonBody = {
            name: this.addNameInput.current.value
        }
        if(this.state.option == "item"){
            jsonBody.description = this.addDescriptionInput.current.value
            jsonBody.image = this.addItemImageInput.current.value
            jsonBody.location = this.addLocationInput.current.value
        } else if (this.state.option == "location") {
            jsonBody.locationImage = this.addLocationImageInput.current.value
        }
        fetch(`http://localhost:5000/items`,{
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },         
            body: JSON.stringify(jsonBody)
        })
        .then( (response) => {
            return response.json();
        }).then((jsonResult) => {
            console.log(jsonResult)
        })
    }

    componentWillReceiveProps(newProps) {
        this.setState({
            showModal: newProps.show,
            option: newProps.option,
            locations: newProps.locations
        });
    }

    handleClose(){
        this.setState({showModal: false});
    }

    render() {
        const locationItems = this.state.locations.map((item) =>
            <option className="dropdown-item" key={item.id} value={item.id}>
                {item.name}
            </option>
        );
        return(
            <Modal show={this.state.showModal} onHide={this.handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Add {this.state.option}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form className="m-1">
                        <div className="form-group">
                            <label>Name</label>
                            <input type="text" className="form-control" ref={this.addNameInput}></input>
                            {this.state.option == "item" ? (
                                <div>
                                    <label>Description</label>
                                    <input type="text" className="form-control" 
                                    defaultValue=""
                                    ref={this.addDescriptionInput}></input>
                                    <label>Image</label>
                                    <div className="custom-file">
                                        <label className="custom-file-label" htmlFor="inputGroupFile02">
                                            Choose file
                                        </label>
                                        <input type="file" className="custom-file-input" 
                                        id="inputGroupFile02" aria-describedby="inputGroupFileAddon02"
                                        defaultValue=""
                                        ref={this.addItemImageInput}/>
                                    </div>
                                    <label>Location</label>
                                    <select className="custom-select" 
                                    defaultValue=""
                                    ref={this.addLocationInput}>
                                        {locationItems}
                                    </select>
                                </div>
                            ) : (
                                <div>
                                    <label>Floorplan image</label>
                                    <div className="custom-file">
                                        <label className="custom-file-label" htmlFor="inputGroupFile01">
                                            Choose file
                                        </label>
                                        <input type="file" className="custom-file-input" 
                                        id="inputGroupFile01" 
                                        aria-describedby="inputGroupFileAddon01" 
                                        defaultValue=""
                                        ref={this.addLocationImageInput} />
                                    </div>
                                </div>
                            )}
                        </div>
                        <button type="submit" className="btn btn-primary"
                        onClick={this.handleSubmit}>
                            Add
                        </button>
                    </form>
                </Modal.Body>
            </Modal>
        );
    }
}

export default AddModal;