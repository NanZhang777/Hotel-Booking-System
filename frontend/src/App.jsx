import { Route, Routes, NavLink, Navigate, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './AuthContext.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import Rooms from './pages/Rooms.jsx'
import RoomDetail from './pages/RoomDetail.jsx'
import Bookings from './pages/Bookings.jsx'

function Shell(){
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const doLogout = () => { logout(); navigate('/login') }

  return (
    <div>
      <header className="header">
        <div className="brand">🏨 Hotel Booking</div>
        <nav className="nav" style={{display:'flex', gap:10}}>
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/rooms">Rooms</NavLink>
          {user && <NavLink to="/bookings">My Bookings</NavLink>}
          {user ? (
            <button className="btn ghost" onClick={doLogout}>Logout</button>
          ) : (
            <>
              <NavLink to="/login">Login</NavLink>
              <NavLink to="/register">Register</NavLink>
            </>
          )}
        </nav>
      </header>
      <div className="container">
        <Routes>
          <Route index element={<Home/>}/>
          <Route path="login" element={<Login/>}/>
          <Route path="register" element={<Register/>}/>
          <Route path="rooms" element={<Rooms/>}/>
          <Route path="rooms/:id" element={<RoomDetail/>}/>
          <Route path="bookings" element={
            <RequireAuth><Bookings/></RequireAuth>
          }/>
          <Route path="*" element={<Navigate to="/" replace/>}/>
        </Routes>
      </div>
      <footer>Back end → <code>{import.meta.env.VITE_PROXY_TARGET || import.meta.env.VITE_API_BASE || 'http://localhost:5000'}</code></footer>
    </div>
  )
}

function RequireAuth({children}){
  const { user } = useAuth()
  if(!user) return <Navigate to="/login" replace />
  return children
}

export default function App(){
  return (
    <AuthProvider>
      <Shell/>
    </AuthProvider>
  )
}