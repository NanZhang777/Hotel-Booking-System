import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../services/api'
import { useAuth } from '../AuthContext.jsx'

export default function RoomDetail(){
  const { id } = useParams()
  const [room, setRoom] = useState(null)
  const [checkInDate, setCheckInDate] = useState('')
  const [checkOutDate, setCheckOutDate] = useState('')
  const [numberOfGuests, setNumberOfGuests] = useState(1)
  const [err, setErr] = useState('')
  const [ok, setOk] = useState('')
  const navigate = useNavigate()
  const { user } = useAuth()

  useEffect(()=>{
    api.getRoom(id).then(setRoom).catch(e=> setErr(e.message))
  }, [id])

  async function book(){
    setErr(''); setOk('')
    try{
      await api.createReservation({ roomTypeId: Number(id), checkInDate, checkOutDate, numberOfGuests })
      setOk('Reservation created!')
      navigate('/bookings')
    }catch(e){ setErr(e.message) }
  }

  if(!room) return <div className="card">Loading...</div>

  return (
    <div className="card">
      <h2 className="card-title">{room.name}</h2>
      <p className="small">{room.description}</p>
      <div className="separator"></div>
      <div style={{display:'flex', justifyContent:'space-between'}}>
        <div>
          <div><span className="badge">Max</span> {room.max_occupancy || room.maxOccupancy}</div>
          <div><span className="badge">Amenities</span> {room.amenities}</div>
        </div>
        <div style={{textAlign:'right'}}>
          <div style={{fontSize:24,fontWeight:800}}>${room.price_per_night || room.pricePerNight}</div>
          <div className="small">/ night</div>
        </div>
      </div>

      <div className="separator"></div>
      {user ? (
        <div className="row">
          <div>
            <label className="small">Check-in</label>
            <input className="input" type="date" value={checkInDate} onChange={e=>setCheckInDate(e.target.value)}/>
          </div>
          <div>
            <label className="small">Check-out</label>
            <input className="input" type="date" value={checkOutDate} onChange={e=>setCheckOutDate(e.target.value)}/>
          </div>
          <div>
            <label className="small">Guests</label>
            <input className="input" type="number" min="1" max="6" value={numberOfGuests} onChange={e=>setNumberOfGuests(parseInt(e.target.value||'0',10))}/>
          </div>
          <div style={{display:'flex',alignItems:'end'}}>
            <button className="btn primary" onClick={book}>Book this room</button>
          </div>
        </div>
      ) : (
        <div className="small">Please login to book this room.</div>
      )}
      {err && <div style={{color:'var(--danger)'}}>{err}</div>}
      {ok && <div style={{color:'var(--success)'}}>{ok}</div>}
    </div>
  )
}