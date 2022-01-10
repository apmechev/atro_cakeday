import './App.css';
import { useState } from 'react';
import axios from 'axios';

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
  const { API_GATEWAY_URL } = process.env;
  const [icalURL, updateIcalURL] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    console.log("submitting");
    console.log(formData);
    console.log(API_GATEWAY_URL);
    axios.post(API_GATEWAY_URL, formData)
        .then(response => updateIcalURL(response.body.cake)); 
    console.log(icalURL);
  }

  return(
   <div className="container" >
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
        <button type="submit">Submit</button>
      </form>
    </div>)
}

export default App;
