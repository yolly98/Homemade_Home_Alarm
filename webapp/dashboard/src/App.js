import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component{

  state = {
    commands: [
      'ALARM ON',
      'ALARM OFF',
      'STATUS',
      'KEEP ALIVE',
      'RESET'
    ],
    nodes: [
      {
        'node_id': '/hall/24',
        'addr': '192.168.178.45',
        'port': 2910,
        'room': 'hall', 
        'id': 24, 
        'status': 'alive', 
        'alarm': 'off', 
        'detection': false
      },
      {
        'node_id': '/bathroom/1',
        'addr': '192.168.178.51',
        'port': 2910,
        'room': 'bathroom', 
        'id': 1, 
        'status': 'dead', 
        'alarm': 'off', 
        'detection': false
      },
      {
        'node_id': '/badroom/5',
        'addr': '192.168.178.57',
        'port': 2910,
        'room': 'badroom', 
        'id': 5, 
        'status': 'alive', 
        'alarm': 'on', 
        'detection': false
      },
      {
        'node_id': '/kitchen/8',
        'addr': '192.168.178.32',
        'port': 2910,
        'room': 'badroom', 
        'id': 8, 
        'status': 'alive', 
        'alarm': 'on', 
        'detection': true
      }
    ]
  }

  render(){
    return(
      <div id='alarm-container'>
        <label id='alarm-title'>ALARM DASHBOARD</label>
        <div id='alarm-button-container'>
          {
            this.state.commands.map(command => (
              <div key={command} className='alarm-button'>
                <label className='alarm-button-title'>{command}</label>
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

                return <>
                <div key={node.node_id} className='sensor-card'>
                  <div className='sensor-data-container'>
                    <label className='sensor-data'>Node id: {node.node_id}</label>
                    <label className='sensor-data'>Address: {node.addr}</label>
                    <label className='sensor-data'>Port: {node.port}</label>
                    <label className='sensor-data'>Status: {node.status}</label>
                    <label className='sensor-data'>Alarm: {node.alarm}</label>
                    <label className='sensor-data'>Detection: {node.detection}</label>
                    <div className='sensor-button'><label className='sensor-button-label'>ALARM ON</label></div>
                    <div className='sensor-button'><label className='sensor-button-label'>ALARM OFF</label></div>
                    <div className='sensor-button'><label className='sensor-button-label'>ALARM RESET</label></div>
                    <div className='sensor-button'><label className='sensor-button-label'>REMOVE</label></div>
                  </div>
                  <div className='sensor-led-container'>
                    <div className='sensor-led' style={{backgroundColor: status_led}}>
                      <label className='sensor-led-label'>STATUS</label>
                    </div>
                    <div className='sensor-led' style={{backgroundColor: alarm_led}}>
                      <label className='sensor-led-label'>ALARM</label>
                    </div>
                  </div>
                </div>
                </>
              })
            }
          </div>
      </div>
    );
  }
}

export default App;
