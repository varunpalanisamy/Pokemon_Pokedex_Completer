// frontend/src/App.jsx
import { useEffect, useState } from 'react';
import './index.css';

export default function App() {
  const [data, setData] = useState([]);
  const [region, setRegion] = useState('Obsidian Fieldlands');
  const [regions, setRegions] = useState([]);

  useEffect(() => {
    fetch('/uncaught_pokedex.json')
      .then((res) => res.json())
      .then((json) => {
        setData(json);

        const allRegions = new Set();
        json.forEach((pokemon) => {
          const locations = pokemon.location.split('\n');
          for (let i = 0; i < locations.length; i += 2) {
            if (locations[i]) allRegions.add(locations[i]);
          }
        });
        setRegions([...allRegions]);
      });
  }, []);

  const groupedBySublocation = {};
  data.forEach((pokemon) => {
    const locations = pokemon.location.split('\n');
    for (let i = 0; i < locations.length; i += 2) {
      const loc = locations[i];
      const sub = locations[i + 1];

      if (loc === region && sub) {
        sub.split(',').forEach((subarea) => {
          const trimmed = subarea.trim();
          if (!groupedBySublocation[trimmed]) {
            groupedBySublocation[trimmed] = [];
          }
          groupedBySublocation[trimmed].push(pokemon);
        });
      }
    }
  });

  return (
    <div className="p-6 font-sans">
      <h1 className="text-3xl font-bold mb-4">Uncaught Pokémon by Location</h1>

      <select
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        className="mb-6 p-2 border rounded"
      >
        {regions.map((r) => (
          <option key={r} value={r}>{r}</option>
        ))}
      </select>

      <div className="space-y-6">
        {Object.entries(groupedBySublocation).map(([sub, mons]) => (
          <div key={sub}>
            <h2 className="text-xl font-semibold mb-2">{sub}</h2>
            <ul className="list-disc list-inside">
              {mons.map((mon) => (
                <li key={mon.number}>{mon.number.toUpperCase()} - {mon.name}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
