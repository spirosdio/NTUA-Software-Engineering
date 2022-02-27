import './App.css';
import { Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);


const data = {
    labels: ['Jan', 'Mar', 'May', 'July', 'Oct'],
    datasets: [
        {
            label: 'Iphone sales',
            data: [400, 1000, 4000, 800, 1500],
            fill: true,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
            ],
            pointBorderColor:"#8884d8",
            pointBorderWidth:5,
            pointRadius:8,
            tension: 0.4
        },
    ],
};

const options = {
    plugins:{legend:{display:false}},
    layout:{padding:{bottom:20}},
    scales: {
        y:{
            ticks:{
                color:"black",
                font:{
                    size:18
                }
            },
            grid:{
                color:"#243240"
            }
        },
        x:{
            ticks:{
                color:"black",
                font:{
                    size:18
                }
            }
        }
    },
};

function App() {
    return (
        <div className="App-header">
            <div className="App">
                <h2>Funds I owe</h2>
                <Bar data={data} options={options}/>
            </div>
            <div className="App">
                <h2>Funds they owe</h2>
                <Bar data={data} options={options}/>
            </div>
        </div>
    );
}

export default App;