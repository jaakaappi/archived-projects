'use strict';

class App extends React.Component{

    constructor(props){
        super(props);
        this.handleSearch = this.handleSearch.bind(this);
        this.showAddModal = this.showAddModal.bind(this);
        this.state = {
            items: [],
            showModal: false,
            modalOption: ""
        }
    }

    componentDidMount(){
        this.getAllItems();
    }

    getAllItems(){
        fetch('/items/10')
            .then( (response) => {
                return response.json();
        }).then((jsonResult) => {
            this.setState({
                items: jsonResult
            });
            forceUpdate();
        });
    }

    handleSearch(name, location){
        fetch(`/items?name=${name}&location=${location}`)
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
                 <AddModal show={this.state.showModal} option={this.state.modalOption}/>
                 <div className="row justify-content-center align-items-centers">
                     <div className="col justify-content-center align-items-center">
                         <ItemSearch handleSearch={this.handleSearch} />
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

ReactDOM.render(<App />, document.querySelector("#container"));