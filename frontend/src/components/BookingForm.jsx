import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../api.js'

export default function BookingForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [car, setCar] = useState(null)
  const [form, setForm] = useState({ customer_name: '', customer_email: '', start_date: '', end_date: '' })
  const [error, setError] = useState(null)

  useEffect(() => {
    api.getCar(id).then(setCar).catch((e) => setError(e.message))
  }, [id])

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      await api.createBooking({ ...form, car_id: Number(id) })
      navigate('/bookings')
    } catch (err) {
      setError(err.message)
    }
  }

  if (!car) return error ? <p className="error">{error}</p> : <p>Loading…</p>

  return (
    <>
      <h1>Book {car.brand} {car.model}</h1>
      <form className="form" onSubmit={submit}>
        <label>Full name<input name="customer_name" value={form.customer_name} onChange={update} required /></label>
        <label>Email<input type="email" name="customer_email" value={form.customer_email} onChange={update} required /></label>
        <label>Start date<input type="date" name="start_date" value={form.start_date} onChange={update} required /></label>
        <label>End date<input type="date" name="end_date" value={form.end_date} onChange={update} required /></label>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="button">Confirm booking</button>
      </form>
    </>
  )
}
