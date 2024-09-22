import React, { useState } from 'react';
import CalculateElevationPolarForm from './CalculateElevationPolarForm';
import CalculateElevationGridForm from './CalculateElevationGridForm';
import { CustomProvider } from 'rsuite';
import { Button, InputPicker, Stack } from 'rsuite';
import 'rsuite/dist/rsuite.min.css';

document.addEventListener("wheel", function(event){
    if(document.activeElement.type === "number"){
        document.activeElement.blur();
    }
});


function App() {
  const [form, setForm] = useState(null);
  const formOptions = [
      { "label": "Polar w/ Observer", "value": "CalculatePolarElevationForm" },
      { "label": "Grid Coordinate to Grid Coordinate", "value": "CalculateGridCoordForm" },
  ];

  let component = <></>

  if (form == "CalculatePolarElevationForm") {
    component = <CalculateElevationPolarForm/>
  } else if (form == "CalculateGridCoordForm") {
    component = <CalculateElevationGridForm/>
  }

  return (
    <CustomProvider theme="dark">
      <Stack alignItems="flex-start" direction="column">
          <label>Calculator Type</label>
          <InputPicker size="sm" data={formOptions} onChange={(e) => setForm(e)}/>
      </Stack>
      {component}
    </CustomProvider>
  )
}

export default App;
