import CalculateElevationForm from './CalculateElevationForm';

document.addEventListener("wheel", function(event){
    if(document.activeElement.type === "number"){
        document.activeElement.blur();
    }
});

function App() {
  return <CalculateElevationForm/>
}

export default App;
