import { createContext, useContext, useEffect, useState } from 'react'

const AuthCtx = createContext(null)

export function AuthProvider({ children }){
  const [user, setUser] = useState(()=>{
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  })
  const [token, setToken] = useState(()=> localStorage.getItem('token'))

  useEffect(()=>{
    if(user) localStorage.setItem('user', JSON.stringify(user))
    else localStorage.removeItem('user')
  }, [user])
  useEffect(()=>{
    if(token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  const login = (user, token) => { setUser(user); setToken(token) }
  const logout = () => { setUser(null); setToken(null) }

  return <AuthCtx.Provider value={{ user, token, login, logout }}>{children}</AuthCtx.Provider>
}

export const useAuth = () => useContext(AuthCtx)