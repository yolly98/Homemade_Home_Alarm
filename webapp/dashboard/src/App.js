import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component{

  state = {
    alias_form: {
      node_id: '',
      alias: ''
    },
    commands: [
      {
        title: 'ALARM ON',
        resource: '/alarm_on'
      },
      {
        title: 'ALARM OFF',
        resource: '/alarm_off'
      },
      {
        title: 'REFRESH',
        resource: '/status'
      },
      {
        title: 'KEEP ALIVE',
        resource: '/keep_alive'
      },
      {
        title: 'RESET',
        resource: '/reset'
      }
    ],
    nodes: [],
    central_led: 'grey',
  }

  componentDidMount(){
    this.updateStatus();
  }

  updateStatus = () => {
    this.request('/status', 'all', null);
    setTimeout(() => {
      this.updateStatus();
    }, 5000);
  }

  open_alias_form = (node) => {
    let alias_form = this.state.alias_form;
    alias_form.node_id = node.node_id;
    alias_form.alias = node.alias;
    this.setState({alias_form}, () => {document.getElementById('alarm-alias-container').style.display = 'flex';});
  }

  close_alias_form = () => {
    let alias_form = this.state.alias_form;
    alias_form.node_id = '';
    alias_form.alias = '';
    this.setState({alias_form}, () => {document.getElementById('alarm-alias-container').style.display = 'none';});
  }

  handler = (msg) => {
    if (msg.request.resource == '/status'){
      let nodes = [];
      let central_led = 'grey';
      for(let key in msg.nodes){
        let node = msg.nodes[key];
        node.node_id = key;
        nodes.push(node); 
      }
      if(msg.alarm == 'armed')
        central_led = 'red';
      this.setState({nodes, central_led});
    }
  }

  request = (endpoint, type, node_id) => {

    let requestData = null;
    if(endpoint == '/alias'){
      let alias = document.getElementById('alarm-alias-input').value;
      requestData = {
          resource: endpoint,
          type: type,
          node_id: node_id,
          alias: alias
      };
      this.close_alias_form();
    }
    else
      requestData = {
          resource: endpoint,
          type: type,
          node_id: node_id
      };

    fetch(window.SERVER_URL + endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        let response = JSON.parse(data.body)
        // console.log(response);
        response.request = requestData;
        this.handler(response);
    })
    .catch(error => console.error("Error:", error));
  }

  render(){

    return(
      <div id='alarm-container'>
        <div id='alarm-alias-container' style={{'display': 'none'}}>
          <input id='alarm-alias-input' type='text' placeholder={this.state.alias_form.alias}/>
          <div id='alarm-alias-button-container'>
            <div className='sensor-button' onClick={() => this.request('/alias', 'node', this.state.alias_form.node_id)}>
              <label className='sensor-button-label'>CHANGE ALIAS</label>
            </div>
            <div className='sensor-button' onClick={() => this.close_alias_form()}>
              <label className='sensor-button-label'>CANCEL</label>
            </div>
          </div>
        </div>
        <label id='alarm-title'>ALARM DASHBOARD</label>
        <div id='alarm-central-led' style={{backgroundColor: this.state.central_led}}></div>
        <div id='alarm-button-container'>
          {
            this.state.commands.map(command => (
              <div key={command.title} className='alarm-button' onClick={() => this.request(command.resource, 'all', null)}>
                <label className='alarm-button-title'>{command.title}</label>
              </div>
            ))
          }
        </div>
        <div id='sensors-container'>
            {
              this.state.nodes.map(node => {

                let status_led = 'grey';
                let alarm_led = 'grey';
                if(node.status == 'alive')
                  status_led = 'green'
                if(node.alarm == 'on' && node.detection)
                  alarm_led = 'red'
                else if(node.alarm == 'on' && !node.detection)
                  alarm_led = 'blue'

                return <div key={node.node_id} className='sensor-card' id={node.node_id}>
                  <div className='sensor-data-container'>
                    <label className='sensor-data'>Node id: {node.node_id}</label>
                    <label className='sensor-data'>Address: {node.addr}</label>
                    <label className='sensor-data'>Port: {node.port}</label>
                    <label className='sensor-data'>Status: {node.status}</label>
                    <label className='sensor-data'>Alarm: {node.alarm}</label>
                    <div className='sensor-button' onClick={() => this.request('/alarm_on', 'node', node.node_id)}><label className='sensor-button-label'>ALARM ON</label></div>
                    <div className='sensor-button' onClick={() => this.request('/alarm_off', 'node', node.node_id)}><label className='sensor-button-label'>ALARM OFF</label></div>
                    <div className='sensor-button' onClick={() => this.request('/reset', 'node', node.node_id)}><label className='sensor-button-label'>RESET</label></div>
                    <div className='sensor-button' onClick={() => this.request('/remove', 'node', node.node_id)}><label className='sensor-button-label'>REMOVE</label></div>
                    <div className='sensor-button' onClick={() => this.open_alias_form(node)}><label className='sensor-button-label'>CHANGE ALIAS</label></div>
                  </div>
                  <div className='sensor-led-container'>
                    <label className='sensor-name'>{node.alias}</label>
                    <div className='sensor-led' style={{backgroundColor: status_led}}>
                      <label className='sensor-led-label'>STATUS</label>
                    </div>
                    <div className='sensor-led' style={{backgroundColor: alarm_led}}>
                      <label className='sensor-led-label'>ALARM</label>
                    </div>
                  </div>
                </div>
              })
            }
          </div>
      </div>
    );
  }
}

export default App;
