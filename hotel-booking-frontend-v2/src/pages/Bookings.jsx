import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function Bookings(){
  const [list, setList] = useState([])
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')

  async function load(){
    setErr(''); setLoading(true)
    try{
      // const data = await api.myBookings()
      // setList(Array.isArray(data) ? data : (data.reservations || []))
      const data = await api.myBookings()
// 兼容常见后端键名：reservations / bookings / myBookings / data / items / results / my_bookings / reservation_list ...
const arr =
Array.isArray(data) ? data :
data.reservations ??
data.bookings ??
data.myBookings ??
data.my_bookings ??
data.reservation_list ??
data.data ??
data.items ??
data.results ??
[]
setList(arr)
    }catch(e){ setErr(e.message) }
    finally{ setLoading(false) }
  }
  useEffect(()=>{ load() }, [])

  async function cancel(id){
    if(!confirm('Cancel this reservation?')) return
    try{
      await api.cancelReservation(id)
      await load()
    }catch(e){ alert(e.message) }
  }

  return (
    <div className="card">
      <h2 className="card-title">My reservations</h2>
      {err && <div style={{color:'var(--danger)'}}>{err}</div>}
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Room Type</th>
            <th>Check-in</th>
            <th>Check-out</th>
            <th>Guests</th>
            <th>Total</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map(r => (
            <tr key={r.reservationId || r.id}>
              <td>{r.reservationId || r.id}</td>
              <td>{r.roomType || r.room_type || r.roomName}</td>
              <td>{r.checkInDate || r.check_in_date}</td>
              <td>{r.checkOutDate || r.check_out_date}</td>
              <td>{r.numberOfGuests || r.guests}</td>
              <td>${r.totalPrice || r.total_price}</td>
              <td className={"status " + (r.status || '')}>{r.status}</td>
              <td>
                {(r.status === 'Confirmed' || !r.status) && (
                  <button className="btn danger" onClick={()=>cancel(r.reservationId || r.id)}>Cancel</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {!loading && list.length===0 && <div className="small">No reservations yet.</div>}
    </div>
  )
}