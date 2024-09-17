import React, { useState } from 'react';
import axios from 'axios';
import { Button, Heading, InputNumber, InputPicker, Stack } from 'rsuite';
import Column from 'rsuite/esm/Table/TableColumn';

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
    const [loading, setLoading] = useState(false);

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

        setLoading(true)
        try {
            const response = await axios.post('/api/calculate_elevation', data);
            console.log(response)
            setResult(response.data);
            setError(null);
        } catch (err) {
            setError('Error calculating elevation.');
            setResult(null);
        } finally {
            setLoading(false)
        }
    };

    const artilleryOptions = [
        { "label": "M252", "value": "m252" },
        { "label": "M119", "value": "m119" },
        { "label": "2S1", "value": "t2s1" }
    ]

    return (
        <>
            <Heading level={1} style={{textAlign: "center"}}>WCS Artillery Calculator</Heading>
            <form onSubmit={handleSubmit}>
                <Stack spacing={10} direction="column">
                    <Stack alignItems="flex-start" direction="column">
                        <label>Artillery</label>
                        <InputPicker size="sm" value={artillery} data={artilleryOptions} onChange={(e) => setArtillery(e)} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Mortar Easting</label>
                        <InputNumber size="sm" onChange={(e) => setMortarEasting(e)} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Morter Northing</label>
                        <InputNumber size="sm" onChange={setMortarNorthing} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Mortar Height</label>
                        <InputNumber size="sm" onChange={setMortarHeight} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Observer Easting</label>
                        <InputNumber osize="sm" nChange={setObserverEasting} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Observer Northing</label>
                        <InputNumber size="sm" onChange={setObserverNorthing} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Observer Height</label>
                        <InputNumber size="sm" onChange={setObserverHeight} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Observer to Enemy Azimuth</label>
                        <InputNumber size="sm" onChange={setObserverToEnemyAzimuth} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Observer to Enemy Horizontal</label>
                        <InputNumber size="sm" onChange={setObserverToEnemyHorizontal} required />
                    </Stack>
                    <Stack alignItems="flex-start" direction="column">
                        <label>Observer to Enemy Vertical</label>
                        <InputNumber size="sm" onChange={setObserverToEnemyVertical} required />
                    </Stack>
                    <Button type="submit" appearance="primary" disabled={loading}>
                        {loading ? 'Calculating...' : 'Calculate'}
                    </Button>
                </Stack>
            </form>
            {result && (
                <div className="mt-4">
                    <h2>Result</h2>
                    <p><strong>Azimuth:</strong> {result.azimuth} degrees</p>
                    <p><strong>Elevation:</strong> {result.elevation} miliradians + offset</p>
                    <p><strong>Time to Impact:</strong> {result.time_to_impact} seconds</p>
                </div>
            )}
            {error && (
                <div className="alert alert-danger mt-4" role="alert">
                    {error}
                </div>
            )}
        </>
    );
}

export default CalculateElevationForm;