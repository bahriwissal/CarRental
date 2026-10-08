import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'

export default function CarList() {
  const [cars, setCars] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    api.listCars().then(setCars).catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="error">{error}</p>

  return (
    <>
      <h1>Available cars</h1>
      <div className="grid">
        {cars.map((car) => (
          <div key={car.id} className="card">
            <h2>{car.brand} {car.model}</h2>
            <p className="muted">{car.year}</p>
            <p className="price">{car.daily_price.toFixed(2)} € / day</p>
            {car.available ? (
              <Link className="button" to={`/cars/${car.id}/book`}>Book</Link>
            ) : (
              <span className="muted">Unavailable</span>
            )}
          </div>
        ))}
      </div>
    </>
  )
}
