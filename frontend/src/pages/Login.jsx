import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { useAuth } from '../AuthContext.jsx'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    setErr(''); setLoading(true)
    try{
      const res = await api.login({ email, password })
const token = res.access_token || res.token || res.accessToken
const user = res.user || res.profile || { email }   //  给 user 一个兜底。如果后端没返回用户信息，那我就自己造一个最基本的用户对象 { email } 来兜底。
if(!token) throw new Error('Login response missing access token')
login(user, token)
      navigate('/rooms')
    }catch(e){
      setErr(e.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{maxWidth:520, margin:'0 auto'}}>
      <h2 className="card-title">Login</h2>
      <form onSubmit={submit} className="row">
        <div style={{gridColumn:'1/-1'}}>
          <label className="small">Email</label>
          <input className="input" type="email" value={email} onChange={e=>setEmail(e.target.value)} required/>
        </div>
        <div style={{gridColumn:'1/-1'}}>
          <label className="small">Password</label>
          <input className="input" type="password" value={password} onChange={e=>setPassword(e.target.value)} required/>
        </div>
        {err && <div style={{color:'var(--danger)'}}>{err}</div>}
        <div style={{gridColumn:'1/-1', display:'flex', gap:10, justifyContent:'flex-end'}}>
          <button className="btn primary" disabled={loading}>{loading ? 'Signing in...' : 'Login'}</button>
        </div>
      </form>
    </div>
  )
}