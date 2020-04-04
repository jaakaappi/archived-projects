import React, {Component} from 'react';

class AddControls extends Component {
    constructor(props) {
        super(props);
        this.showAddModal = this.showAddModal.bind(this);
    }

    showAddModal(option){
        this.props.showAddModal(option);
    }

    render() {
        return(
            <div>
                <div className="row py-1">
                    <div className="col">
                        <button className="btn btn-success" onClick={()=>{this.showAddModal("item")}}>
                            <i className="fas fa-plus mr-2"></i>
                            Add a new item
                        </button>
                    </div>
                </div>
                <div className="row py-1">
                    <div className="col">
                        <button className="btn btn-success" onClick={()=>{this.showAddModal("location")}}>
                            <i className="fas fa-plus  mr-2"></i>
                            Add a new location
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}

export default AddControls;