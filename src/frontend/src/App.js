import React, { useState } from 'react';

// current 81mm mortar estimated v_0: 121.305

function App() {
  const [mortar_easting, setmortar_easting] = useState(0);
  const [mortar_northing, setmortar_northing] = useState(0);
  const [observer_easting, setobserver_easting] = useState(0);
  const [observer_northing, setobserver_northing] = useState(0);
  const [enemy_easting, setenemy_easting] = useState(0);
  const [enemy_northing, setenemy_northing] = useState(0);
  const [obs_to_enemy_azimuth, setobs_to_enemy_azimuth] = useState(0);
  const [obs_to_enemy_distance, setobs_to_enemy_distance] = useState(0);
  const [target_height, settarget_height] = useState(0);
  const [obsResult, setobsResult] = useState(null);
  const [noObsResult, setnoObsResult] = useState(null);
  const [obsElevation, setObsElevation] = useState(null);

  const submitObserver = async (e) => {
    e.preventDefault();

    const azimuth_queryParams = new URLSearchParams({
      mortar_easting: mortar_easting,
      mortar_northing: mortar_northing,
      observer_easting: observer_easting,
      observer_northing: observer_northing,
      obs_to_enemy_azimuth: obs_to_enemy_azimuth,
      obs_to_enemy_distance: obs_to_enemy_distance
    }).toString();

    const azimuth_response = await fetch(`http://127.0.0.1:8000/calculate?${azimuth_queryParams}`, {
      method: 'POST'
    });

    const azimuth_data = await azimuth_response.json();
    setobsResult(azimuth_data);

    const elevation_queryParams = new URLSearchParams({
      initial_velocity: 375,
      target_height: target_height,
      distance: azimuth_data.distance,
      upper_half: true
    }).toString();

    const elevation_response = await fetch(`http://127.0.0.1:8000/calculate3?${elevation_queryParams}`, {
      method: 'POST'
    });

    const elevation_data = await elevation_response.json();
    setObsElevation(elevation_data)
  };

  const submitNoObserver = async (e) => {
    e.preventDefault();

    const queryParams = new URLSearchParams({
      mortar_easting: mortar_easting,
      mortar_northing: mortar_northing,
      enemy_easting: enemy_easting,
      enemy_northing: enemy_northing
    }).toString();

    const response = await fetch(`http://127.0.0.1:8000/calculate2?${queryParams}`, {
      method: 'POST'
    });

    const data = await response.json();
    setobsResult(data);
  };

  return (
    <div style={{ display: 'flex' }}>
      <div className="App inline-block">
        <h1>No Observer</h1>
        <form onSubmit={submitNoObserver}>
          <label>
            Mortar Easting:
            <input
              type="number"
              value={mortar_easting}
              onChange={(e) => setmortar_easting(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Mortar Northing:
            <input
              type="number"
              value={mortar_northing}
              onChange={(e) => setmortar_northing(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Enemy Easting:
            <input
              type="number"
              value={enemy_easting}
              onChange={(e) => setenemy_easting(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Enemy Northing:
            <input
              type="number"
              value={enemy_northing}
              onChange={(e) => setenemy_northing(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <button type="submit">Calculate</button>
        </form>

        {noObsResult !== null && (
          <>
            <h2>Azimuth: {noObsResult.azimuth}</h2>
            <h2>Distance: {noObsResult.distance}</h2>
          </>

        )}
      </div>
      <div className="App inline-block">
        <h1>Observer</h1>
        <form onSubmit={submitObserver}>
          <label>
            Mortar Easting:
            <input
              type="number"
              value={mortar_easting}
              onChange={(e) => setmortar_easting(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Mortar Northing:
            <input
              type="number"
              value={mortar_northing}
              onChange={(e) => setmortar_northing(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Observer Easting:
            <input
              type="number"
              value={observer_easting}
              onChange={(e) => setobserver_easting(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Observer Northing:
            <input
              type="number"
              value={observer_northing}
              onChange={(e) => setobserver_northing(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Observer Azimuth to Enemy:
            <input
              type="number"
              value={obs_to_enemy_azimuth}
              onChange={(e) => setobs_to_enemy_azimuth(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Observer Distance to Enemy:
            <input
              type="number"
              value={obs_to_enemy_distance}
              onChange={(e) => setobs_to_enemy_distance(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <label>
            Target height:
            <input
              type="number"
              value={target_height}
              onChange={(e) => settarget_height(parseFloat(e.target.value))}
              required
            />
          </label>
          <br />
          <button type="submit">Calculate</button>
        </form>

        {/* Display the result inside the box below the button */}
        {obsResult !== null && obsElevation !== null && (
          <div className="result">
            <h2>Azimuth: {obsResult.azimuth}</h2>
            <h2>Elevation: {obsElevation.elevation}</h2>
            <h2>Time to Impact: {obsElevation.time_to_impact}</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
