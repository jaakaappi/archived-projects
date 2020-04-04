import React, { Component } from 'react';
import AddControls from './AddControls.js';
import AddModal from './AddModal.js';
import ItemSearch from './ItemSearch.js';
import ResultView from './ResultView.js';
import './App.css';

class App extends Component{

  constructor(props){
      super(props);
      this.handleSearch = this.handleSearch.bind(this);
      this.showAddModal = this.showAddModal.bind(this);
      this.update = this.update.bind(this);
      this.state = {
          items: [],
          locations: [],    
          showModal: false,
          modalOption: ""
      }
  }

  componentDidMount(){
    this.update();
  }

  update(){
    this.getItems();
    this.getLocations();
  }

  getItems(){
      fetch('http://localhost:5000/items/10')
          .then( (response) => {
              return response.json();
      }).then((jsonResult) => {
          console.log('items');
          this.setState({
              items: jsonResult
          });
          this.forceUpdate();
      });
  }

  getLocations(){
    fetch('http://localhost:5000/locations')
        .then( (response) => {
            return response.json();
    }).then((jsonResult) => {
        console.log('locations');
        this.setState({
            locations: jsonResult
        });
        this.forceUpdate();
    });
  }

  handleSearch(name, location){
      fetch(`http://localhost:5000/items?name=${name}&location=${location}`)
          .then( (response) => {
              return response.json();
      }).then((jsonResult) => {
          this.setState({
              items: jsonResult
          });
      })
  }

  showAddModal(option){
      this.setState({
          showModal: true,
          modalOption: option
      });
  }

  render() {
       return (
           <div className="container justify-content-center align-items-center">
               <AddModal show={this.state.showModal} option={this.state.modalOption}
                    update={this.update} locations={this.state.locations}/>
               <div className="row justify-content-center align-items-center">
                   <div className="col justify-content-center align-items-center">
                       <ItemSearch handleSearch={this.handleSearch} 
                       locations={this.state.locations}/>
                   </div>
                   <div className="col-md-3 justify-content-center align-items-center">
                       <AddControls showAddModal={this.showAddModal}/>
                   </div>
               </div>
               <ResultView items={this.state.items}/>
           </div>
       )
  }
}

export default App;
