import CalculateElevationForm from './CalculateElevationForm';
import { Button, CustomProvider } from 'rsuite';
import 'rsuite/dist/rsuite.min.css';

document.addEventListener("wheel", function(event){
    if(document.activeElement.type === "number"){
        document.activeElement.blur();
    }
});

function App() {
  return (
    <CustomProvider theme="dark">
      <CalculateElevationForm/>
    </CustomProvider>
  )
}

export default App;
