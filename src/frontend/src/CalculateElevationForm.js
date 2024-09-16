import React, { useState } from 'react';
import axios from 'axios';

function CalculateElevationForm() {
    const [mortarEasting, setMortarEasting] = useState(0);
    const [mortarNorthing, setMortarNorthing] = useState(0);
    const [mortarHeight, setMortarHeight] = useState(0);
    const [observerEasting, setObserverEasting] = useState(0);
    const [observerNorthing, setObserverNorthing] = useState(0);
    const [observerHeight, setObserverHeight] = useState(0);
    const [observerToEnemyAzimuth, setObserverToEnemyAzimuth] = useState(0);
    const [observerToEnemyHorizontal, setObserverToEnemyHorizontal] = useState(0);
    const [observerToEnemyVertical, setObserverToEnemyVertical] = useState(0);
    const [artillery, setArtillery] = useState('m252');

    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const data = {
            mortar_easting: mortarEasting,
            mortar_northing: mortarNorthing,
            mortar_height: mortarHeight,
            observer_easting: observerEasting,
            observer_northing: observerNorthing,
            observer_height: observerHeight,
            observer_to_enemy_azimuth: observerToEnemyAzimuth,
            observer_to_enemy_horizontal: observerToEnemyHorizontal,
            observer_to_enemy_vertical: observerToEnemyVertical,
            artillery: artillery
        };


        try {
            const response = await axios.post('/api/calculate_elevation', data);
            console.log(response)
            setResult(response.data);
            setError(null);
        } catch (err) {
            setError('Error calculating elevation.');
            setResult(null);
        }
    };

    return (
        <div className="container mt-5">
            <h1>Calculate Elevation</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="artillery">Artillery</label>
                    <select
                        className="form-control"
                        id="artillery"
                        value={artillery}
                        onChange={(e) => setArtillery(e.target.value)}
                    >
                        <option value="m252">M252</option>
                        <option value="m119">M119</option>
                        <option value="t2s1">2S1</option>
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="mortarEasting">Mortar Easting</label>
                    <input
                        type="number"
                        className="form-control"
                        id="mortarEasting"
                        value={mortarEasting}
                        onChange={(e) => setMortarEasting(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="mortarNorthing">Mortar Northing</label>
                    <input
                        type="number"
                        className="form-control"
                        id="mortarNorthing"
                        value={mortarNorthing}
                        onChange={(e) => setMortarNorthing(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="mortarHeight">Mortar Height</label>
                    <input
                        type="number"
                        className="form-control"
                        id="mortarHeight"
                        value={mortarHeight}
                        onChange={(e) => setMortarHeight(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="observerEasting">Observer Easting</label>
                    <input
                        type="number"
                        className="form-control"
                        id="observerEasting"
                        value={observerEasting}
                        onChange={(e) => setObserverEasting(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="observerNorthing">Observer Northing</label>
                    <input
                        type="number"
                        className="form-control"
                        id="observerNorthing"
                        value={observerNorthing}
                        onChange={(e) => setObserverNorthing(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="observerHeight">Observer Height</label>
                    <input
                        type="number"
                        className="form-control"
                        id="observerHeight"
                        value={observerHeight}
                        onChange={(e) => setObserverHeight(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="observerToEnemyAzimuth">Observer to Enemy Azimuth</label>
                    <input
                        type="number"
                        className="form-control"
                        id="observerToEnemyAzimuth"
                        value={observerToEnemyAzimuth}
                        onChange={(e) => setObserverToEnemyAzimuth(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="observerToEnemyHorizontal">Observer to Enemy Horizontal</label>
                    <input
                        type="number"
                        className="form-control"
                        id="observerToEnemyHorizontal"
                        value={observerToEnemyHorizontal}
                        onChange={(e) => setObserverToEnemyHorizontal(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="observerToEnemyVertical">Observer to Enemy Vertical</label>
                    <input
                        type="number"
                        className="form-control"
                        id="observerToEnemyVertical"
                        value={observerToEnemyVertical}
                        onChange={(e) => setObserverToEnemyVertical(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    Calculate
                </button>
            </form>
            {result && (
                <div className="mt-4">
                    <h2>Result</h2>
                    <p><strong>Azimuth:</strong> {result.azimuth} degrees</p>
                    <p><strong>Elevation:</strong> {result.elevation} degrees</p>
                    <p><strong>Time to Impact:</strong> {result.time_to_impact} seconds</p>
                </div>
            )}
            {error && (
                <div className="alert alert-danger mt-4" role="alert">
                    {error}
                </div>
            )}
        </div>
    );
}

export default CalculateElevationForm;