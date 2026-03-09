import { Link } from 'react-router-dom'

export default function Home(){
  return (
    <div className="card">
      <h2 className="card-title">Welcome to Hotel Booking</h2>
      <p className="small">Search available rooms, book your stay, and manage your reservations.</p>
      <div style={{display:'flex', gap:10, marginTop:10}}>
        <Link to="/rooms" className="btn primary">Find Rooms</Link>
        <Link to="/login" className="btn">Login</Link>
        <Link to="/register" className="btn">Register</Link>
      </div>
    </div>
  )
}