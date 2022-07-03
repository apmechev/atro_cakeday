import './App.css';
import cake from './static/cake.png';
import { useState } from 'react';
import axios from 'axios';
import MoonLoader from 'react-spinners/MoonLoader';
require('dotenv').config()

function App() {
  const [formData, updateFormField] = useState({
    'name':'',
    'birthyear': 1999,
    'birthmonth': 1,
    'birthday': 1,
    'mercury_stagger': 5,
    'venus_stagger': 2,
    'cal_start': 2019,
    'cal_end': 2100
  });
  const API_GATEWAY_URL = process.env.REACT_APP_API_GATEWAY_URL;
  const [icalURL, updateIcalURL] = useState('');
  const [isLoading, updateIsLoading] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    updateIsLoading(true);
    const config = {
      crossDomain: true,
      headers: {
        "Content-Type": "text/plain",
        "Access-Control-Allow-Origin": true,
      }
    }
    axios.post(API_GATEWAY_URL, formData, config)
        .then(response => {
          updateIcalURL(response.data.cake)}
          )
        .finally(() => {
          updateIsLoading(false);
        })
  }

  return(
   <div className="container" >
      {icalURL ? (
        <div>
           <div class="border">
          <h4>Download this file to your machine:</h4>
          <h4><a href={`${icalURL}`} download='calendar.ical'>{`${icalURL}`}</a></h4>
          <img class='cake' src={cake} alt='cake'/>
          <br/>
          <h4>To Add to Google Calendar:</h4>
          <h4>Paste the above URL into<a href="https://calendar.google.com/calendar/r/settings/addbyurl">this link</a></h4>
          </div>
        
        </div>
        ) : (<div> 
      <h1>When were you born? (On Earth)</h1>
      <form onSubmit={handleSubmit}>
        <label>Your name (optional)</label>
        <input type="text" name="name" className='validate_name' value={formData.name} onChange= {(e) => updateFormField({...formData, name: e.target.value})} />
        <br/>

        <label>Year</label>
        <input type="number" className='validate' value={formData.birthyear} onChange={(e) => updateFormField({...formData, birthyear: e.target.value})} />
        <label>Month</label>
        <input type="number" className='validate' value={formData.birthmonth} onChange={(e) => updateFormField({...formData, birthmonth: e.target.value})} />
        <label>Day</label>
        <input type="number" className='validate' value={formData.birthday} onChange={(e) => updateFormField({...formData, birthday: e.target.value})} />
        <br/>

        <label>Skip Mercury Birthdays by</label>
        <input type="number" className='validate' value={formData.mercury_stagger} onChange={(e) => updateFormField({...formData, mercury_stagger:e.target.value})} />
        <br/>

        <label>Skip Venus Birthdays by</label>
        <input type="number" className='validate' value={formData.venus_stagger} onChange={(e) => updateFormField({...formData, venus_stagger:e.target.value})} />
        <br/>

        <label>Start Year</label>
        <input type="number" className='validate' value={formData.cal_start} onChange={(e) => updateFormField({...formData, cal_start:e.target.value})} />
        <label>End Year</label>
        <input type="number" className='validate' value={formData.cal_end} onChange={(e) => updateFormField({...formData, cal_end: e.target.value})} />

        <br/>
        <button type="submit" disabled={isLoading}>Submit</button>
        <MoonLoader loading={isLoading} color="#FFFFFF" size={20}/>
      </form></div>)}
    </div>)
}

export default App;
