import { Link } from 'react-router-dom'

export default function RoomCard({ room }){
  // 统一容错映射：后端不一定用 id 这个名字
  const id =
    room.id ??
    room.roomTypeId ??
    room.room_type_id ??
    room.room_id

  const name =
    room.name ??
    room.roomType ??
    room.room_name ??
    room.title ??
    (id != null ? `Room #${id}` : 'Room')

  const desc =
    room.description ??
    room.details ??
    ''

  const maxOcc =
    room.max_occupancy ??
    room.maxOccupancy ??
    room.capacity ??
    room.maxGuests

  const amenities =
    room.amenities ??
    room.features ??
    room.tags ??
    ''

  const price =
    room.price_per_night ??
    room.pricePerNight ??
    room.price ??
    room.nightlyRate

  return (
    <div className="card">
      <h3 className="card-title">{name}</h3>
      <div className="small">{desc}</div>
      <div className="separator"></div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          {maxOcc !== undefined && <div><span className="badge">Max</span> {maxOcc}</div>}
          {amenities && <div><span className="badge">Amenities</span> {amenities}</div>}
        </div>
        <div style={{textAlign:'right'}}>
          {price !== undefined && (
            <>
              <div style={{fontSize:24,fontWeight:800}}>${price}</div>
              <div className="small">/ night</div>
            </>
          )}
        </div>
      </div>

      {id !== undefined && (
        <div style={{marginTop:12, display:'flex', gap:10}}>
          <Link className="btn" to={`/rooms/${id}`}>Details</Link>
        </div>
      )}
    </div>
  )
}
