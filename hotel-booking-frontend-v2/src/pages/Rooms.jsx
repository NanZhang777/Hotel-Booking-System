import { useEffect, useState } from 'react'
import { api } from '../services/api'
import DateField from '../components/DateField.jsx'
import NumberField from '../components/NumberField.jsx'
import RoomCard from '../components/RoomCard.jsx'

function todayISO(){
  const d = new Date(); d.setHours(0,0,0,0)
  return d.toISOString().slice(0,10)
}

export default function Rooms(){
  const [checkIn, setCheckIn] = useState(todayISO())
  const [checkOut, setCheckOut] = useState(()=>{
    const d = new Date(); d.setDate(d.getDate()+1); d.setHours(0,0,0,0)
    return d.toISOString().slice(0,10)
  })
  const [guests, setGuests] = useState(1)
  const [list, setList] = useState([])
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')

  async function search(){
    setErr(''); setLoading(true)
    try{
      const data = await api.listAvailable({ checkIn, checkOut }) // 你的后端不需要人数
const arr =
  Array.isArray(data) ? data :
  data.rooms ??
  data.available ??
  data.availableRooms ??
  data.roomTypes ??
  data.room_types ??
  data.data ??
  data.items ??
  data.results ??
  []
setList(arr)
    }catch(e){ setErr(e.message) }
    finally{ setLoading(false) }
  }

  useEffect(()=>{ search() }, [])

  return (
    <div className="card">
      <h2 className="card-title">Search rooms</h2>
      <div className="form-row" style={{marginBottom:12}}>
        <DateField label="Check-in" value={checkIn} onChange={setCheckIn} min={todayISO()}/>
        <DateField label="Check-out" value={checkOut} onChange={setCheckOut} min={checkIn}/>
        <NumberField label="Guests" value={guests} onChange={setGuests} min={1} max={6}/>
        <div style={{display:'flex', alignItems:'end'}}>
          <button className="btn primary" onClick={search} disabled={loading}>{loading ? 'Searching...' : 'Search'}</button>
        </div>
      </div>
      {err && <div style={{color:'var(--danger)', marginBottom:12}}>{err}</div>}
      <div className="room-grid">
        {list.map(room => <RoomCard key={room.id} room={room} />)}
      </div>
      {!loading && list.length===0 && <div className="small">No rooms found for your filters.</div>}
    </div>
  )
}