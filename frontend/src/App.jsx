import { NavLink, Route, Routes } from 'react-router-dom'
import CarList from './components/CarList.jsx'
import BookingForm from './components/BookingForm.jsx'
import BookingList from './components/BookingList.jsx'

export default function App() {
  return (
    <>
      <header className="navbar">
        <span className="logo">CarRental</span>
        <nav>
          <NavLink to="/" end>Cars</NavLink>
          <NavLink to="/bookings">Bookings</NavLink>
        </nav>
      </header>
      <main className="container">
        <Routes>
          <Route path="/" element={<CarList />} />
          <Route path="/cars/:id/book" element={<BookingForm />} />
          <Route path="/bookings" element={<BookingList />} />
        </Routes>
      </main>
    </>
  )
}
