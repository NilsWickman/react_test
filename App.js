import logo from './logo.svg'; // If you're using the logo, otherwise you can remove this
import './App.css';
import React, { useState } from 'react'
import axios from 'axios'

let current_player_red = true
let active_row = 6
let game_state = Array.from({ length: 12 }, () => Array(6).fill(0.5));

function App() {

  const handleButtonClick = async (index) => {

    for (let i = 6; i > 0; i--) {
      const circle = document.getElementById([active_row, index + 1])
      if (window.getComputedStyle(circle).backgroundColor != "rgb(255, 255, 255)") {
        active_row = active_row - 1
      } 
    }
    if (active_row > 0) {
    const changed_circle = document.getElementById([active_row, index + 1])
    if (current_player_red) {
      changed_circle.style.backgroundColor = "red";
      current_player_red = false
      game_state[index][6 - active_row] = 1.0

      active_row = 6

      setTimeout(async () => {
        const action = await sendData(game_state)
        handleButtonClick(action)
        //handleButtonClick(Math.floor(Math.random() * 6 + 1))
  
      }, 200)
      //console.log(action)
    } else {
      changed_circle.style.backgroundColor = "yellow";
      current_player_red = true
      game_state[index][6 - active_row] = 0.0

      active_row = 6
    }
    } else {
      active_row = 6
      console.log(game_state)
      alert("Nja inte riktigt helt rätt där...")
    }
  }
  const sendData = async (gameState) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/process', {array: gameState})
      return response.data.result
    } catch (error) {
      console.error('Error sending data:', error)
      return null
    }
  }
  return (
      <div id="container">
          <h1>Fem i rad</h1>
          <div id="button-container">
              {Array.from({ length: 12 }).map((_, index) => (
                  <div 
                    className="button" 
                    key={index} 
                    onClick={() => handleButtonClick(index)}
                    >
                    Press 
                  
                  </div>
              ))}
          </div>

          <div id="game">
            {Array.from({ length: 72 }).map((_, index) => {
                const row = Math.floor(index / 12 + 1); // 12 columns
                const column = index % 12 + 1;           // 12 columns
                const circle_id = [row, column]
                return (
                    <div className="cirkel" key={circle_id} id={circle_id}>
                        {`${circle_id}`}
            </div>
        );
    })}
</div>


          <div id="holdupper"></div>
      </div>
  );
}

export default App;