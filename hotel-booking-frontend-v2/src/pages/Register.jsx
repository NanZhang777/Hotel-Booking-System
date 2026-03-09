import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'

export default function Register(){
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    setErr(''); setLoading(true)
    try{
      await api.register({ firstName, lastName, email, password })
      navigate('/login')
    }catch(e){ setErr(e.message) }
    finally{ setLoading(false) }
  }

  return (
    <div className="card" style={{maxWidth:640, margin:'0 auto'}}>
      <h2 className="card-title">Create account</h2>
      <form onSubmit={submit} className="row">
        <div><label className="small">First Name</label><input className="input" value={firstName} onChange={e=>setFirstName(e.target.value)} required/></div>
        <div><label className="small">Last Name</label><input className="input" value={lastName} onChange={e=>setLastName(e.target.value)} required/></div>
        <div style={{gridColumn:'1/-1'}}><label className="small">Email</label><input className="input" type="email" value={email} onChange={e=>setEmail(e.target.value)} required/></div>
        <div style={{gridColumn:'1/-1'}}><label className="small">Password</label><input className="input" type="password" value={password} onChange={e=>setPassword(e.target.value)} required/></div>
        {err && <div style={{color:'var(--danger)'}}>{err}</div>}
        <div style={{gridColumn:'1/-1', display:'flex', gap:10, justifyContent:'flex-end'}}>
          <button className="btn primary" disabled={loading}>{loading ? 'Submitting...' : 'Register'}</button>
        </div>
      </form>
    </div>
  )
}