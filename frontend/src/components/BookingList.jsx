import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function BookingList() {
  const [bookings, setBookings] = useState([])
  const [error, setError] = useState(null)

  const load = () => api.listBookings().then(setBookings).catch((e) => setError(e.message))

  useEffect(() => {
    load()
  }, [])

  const cancel = async (bookingId) => {
    await api.cancelBooking(bookingId).catch((e) => setError(e.message))
    load()
  }

  return (
    <>
      <h1>Bookings</h1>
      {error && <p className="error">{error}</p>}
      {bookings.length === 0 ? (
        <p className="muted">No bookings yet.</p>
      ) : (
        <table>
          <thead>
            <tr><th>Customer</th><th>Car #</th><th>From</th><th>To</th><th>Total</th><th></th></tr>
          </thead>
          <tbody>
            {bookings.map((b) => (
              <tr key={b.id}>
                <td>{b.customer_name}<br /><span className="muted">{b.customer_email}</span></td>
                <td>{b.car_id}</td>
                <td>{b.start_date}</td>
                <td>{b.end_date}</td>
                <td>{b.total_price.toFixed(2)} €</td>
                <td><button className="link" onClick={() => cancel(b.id)}>Cancel</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  )
}
