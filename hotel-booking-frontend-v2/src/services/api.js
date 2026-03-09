const BASE = '' // use relative path; Vite proxy forwards /api to backend

function authHeaders() {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function http(path, { method='GET', body, headers={} }={}){
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...headers
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  const text = await res.text()
  let data
  try { data = text ? JSON.parse(text) : {} } catch { data = { message: text } }
  if(!res.ok){
    throw new Error(data?.message || data?.error || `HTTP ${res.status}`)
  }
  return data
}

export const api = {
  // Auth
  register(payload){ return http('/api/register', { method:'POST', body: payload }) },
  login(payload){ return http('/api/login', { method:'POST', body: payload }) },
  // Rooms
  listAvailable({ checkIn, checkOut }){
  const q = new URLSearchParams({ checkInDate: checkIn, checkOutDate: checkOut }).toString()
  return http(`/api/rooms/available?${q}`)
},
  getRoom(id){ return http(`/api/rooms/${id}`) },
  // Reservations (auth)
  createReservation(payload){ return http('/api/reservations', { method:'POST', body: payload }) },
  myBookings(){ return http('/api/my-bookings') },
  cancelReservation(id){ return http(`/api/reservations/${id}/cancel`, { method:'POST' }) },
}