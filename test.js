import React, { useState } from 'react';
import axios from 'axios';

const MyComponent = () => {
    const [array, setArray] = useState([1, 2, 3, 4]);
    const [result, setResult] = useState(null);

    const sendData = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/process', { array });
            setResult(response.data.result);
        } catch (error) {
            console.error('Error sending data:', error);
        }
    };

    return (
        <div>
            <button onClick={sendData}>Send Array</button>
            {result !== null && <p>Result: {result}</p>}
        </div>
    );
};

export default MyComponent;
