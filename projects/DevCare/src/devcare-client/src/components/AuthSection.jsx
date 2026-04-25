import { useState } from 'react'

import { loginUser, registerUser } from '../api/authApi'

const ACCESS_TOKEN_KEY = 'devcare_access_token'
const REFRESH_TOKEN_KEY = 'devcare_refresh_token'
const USERNAME_KEY = 'devcare_username'
const ROLE_KEY = 'devcare_role'

function AuthSection({ onAuthSuccess }) {
  const [mode, setMode] = useState('login')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [form, setForm] = useState({
    username: '',
    email: '',
    role: 'patient',
    password: '',
    confirmPassword: '',
  })

  function storeAuth(access, refresh, username, role) {
    const normalizedRole = (role || 'patient').toLowerCase()
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
    localStorage.setItem(USERNAME_KEY, username)
    localStorage.setItem(ROLE_KEY, normalizedRole)
  }

  function updateField(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      if (mode === 'register') {
        const registerData = await registerUser({
          username: form.username,
          email: form.email,
          role: form.role.toLowerCase(),
          password: form.password,
          password_confirm: form.confirmPassword,
        })

        storeAuth(
          registerData.access,
          registerData.refresh,
          registerData.user.username,
          registerData.user.role
        )
        setSuccess('Registration successful. Redirecting to dashboard...')
        setForm({
          username: '',
          email: '',
          role: 'patient',
          password: '',
          confirmPassword: '',
        })
        onAuthSuccess?.(
          registerData.access,
          registerData.refresh,
          registerData.user.username,
          registerData.user.role
        )
      } else {
        const loginData = await loginUser({
          email: form.email,
          password: form.password,
        })

        storeAuth(
          loginData.access,
          loginData.refresh,
          loginData.user?.username || form.username,
          loginData.user?.role
        )

        setSuccess('Login successful. Redirecting to dashboard...')
        setForm({
          username: '',
          email: '',
          role: 'patient',
          password: '',
          confirmPassword: '',
        })
        onAuthSuccess?.(
          loginData.access,
          loginData.refresh,
          loginData.user?.username || form.username,
          loginData.user?.role
        )
      }
    } catch (submitError) {
      setError(submitError.message)
    } finally {
      setLoading(false)
    }
  }

  function switchMode(nextMode) {
    setMode(nextMode)
    setError('')
    setSuccess('')
  }

  return (
    <section id="contact" className="site-container pb-20">
      <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <article className="elevated-card rounded-3xl border border-[var(--color-border)] bg-[var(--color-surface)] px-6 py-10 sm:px-9">
          <p className="text-sm font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
            {mode === 'register' ? 'Create Account' : 'Welcome Back'}
          </p>
          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            {mode === 'register'
              ? 'Register your healthcare demo account'
              : 'Login to your dashboard'}
          </h2>
          <p className="mt-4 max-w-2xl text-base text-[var(--color-text-muted)] sm:text-lg">
            {mode === 'register'
              ? 'Create a simple JWT-backed account for your hackathon demo.'
              : 'Use your JWT credentials to access the dashboard page.'}
          </p>
        </article>

        <article className="elevated-card rounded-3xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 sm:p-8">
          <div className="mb-5 flex items-center gap-2 rounded-full bg-[var(--color-surface-soft)] p-1">
            <button
              type="button"
              className={`auth-tab ${mode === 'login' ? 'auth-tab-active' : ''}`}
              onClick={() => switchMode('login')}
            >
              Login
            </button>
            <button
              type="button"
              className={`auth-tab ${mode === 'register' ? 'auth-tab-active' : ''}`}
              onClick={() => switchMode('register')}
            >
              Register
            </button>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
                <label className="auth-label" htmlFor={mode === 'register' ? 'username' : 'email'}>
                  {mode === 'register' ? 'Username' : 'Email'}
                </label>
                <input
                  id={mode === 'register' ? 'username' : 'email'}
                  name={mode === 'register' ? 'username' : 'email'}
                  type={mode === 'register' ? 'text' : 'email'}
                  value={mode === 'register' ? form.username : form.email}
                  onChange={updateField}
                  className="auth-input"
                  placeholder={mode === 'register' ? 'Enter username' : 'name@example.com'}
                  autoComplete={mode === 'register' ? 'username' : 'email'}
                  required
                />


                {mode === 'register' && (
                  <>
                    <label className="auth-label" htmlFor="email">
                      Email
                    </label>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      value={form.email}
                      onChange={updateField}
                      className="auth-input"
                      placeholder="name@example.com"
                      autoComplete="email"
                      required
                    />

                    <label className="auth-label" htmlFor="role">
                      Register as
                    </label>
                    <select
                      id="role"
                      name="role"
                      value={form.role}
                      onChange={updateField}
                      className="auth-input"
                      required
                    >
                      <option value="patient">Patient</option>
                      <option value="doctor">Doctor</option>
                    </select>
                  </>
                )}

                <label className="auth-label" htmlFor="password">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  value={form.password}
                  onChange={updateField}
                  className="auth-input"
                  placeholder="Enter password"
                  autoComplete={
                    mode === 'register' ? 'new-password' : 'current-password'
                  }
                  required
                />

                {mode === 'register' && (
                  <>
                    <label className="auth-label" htmlFor="confirmPassword">
                      Confirm Password
                    </label>
                    <input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      value={form.confirmPassword}
                      onChange={updateField}
                      className="auth-input"
                      placeholder="Re-enter password"
                      autoComplete="new-password"
                      required
                    />
                  </>
                )}

                {error && <p className="auth-message auth-message-error">{error}</p>}
                {success && (
                  <p className="auth-message auth-message-success">{success}</p>
                )}

                <button type="submit" className="btn-primary w-full" disabled={loading}>
                  {loading
                    ? 'Please wait...'
                    : mode === 'register'
                      ? 'Create account'
                      : 'Login'}
                </button>
              </form>
        </article>
      </div>
    </section>
  )
}

export default AuthSection