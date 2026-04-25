import React, { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { ChevronRight, Play, Calendar, Activity, TrendingUp, Plus, MessageSquare } from 'lucide-react'

const colors = {
  primary: '#1E88E5',
  primaryDark: '#0D47A1',
  secondary: '#4CAF50',
  secondaryLight: '#A5D6A7',
  background: '#FFFFFF',
  textPrimary: '#263238',
  textSecondary: '#607D8B',
  border: '#ECEFF1',
  error: '#E53935',
  warning: '#FB8C00',
  success: '#43A047',
  lightGray: '#F5F5F5'
}

const PatientDashboardPage = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  // Mock data for progress chart
  const progressData = [
    { day: 'Mon', score: 70 },
    { day: 'Tue', score: 75 },
    { day: 'Wed', score: 78 },
    { day: 'Thu', score: 82 },
    { day: 'Fri', score: 85 },
    { day: 'Sat', score: 88 },
    { day: 'Sun', score: 85 }
  ]

  // Mock data for exercises
  const exercises = [
    {
      id: 1,
      name: 'Quadriceps Sets',
      duration: '10-15 mins',
      type: 'STRENGTH',
      difficulty: 'LOW IMPACT',
      image: 'https://via.placeholder.com/200x120?text=Quadriceps'
    },
    {
      id: 2,
      name: 'Heel Slides',
      duration: '5-10 mins',
      type: 'MOBILITY',
      difficulty: 'CRITICAL',
      image: 'https://via.placeholder.com/200x120?text=Heel'
    },
    {
      id: 3,
      name: 'Terminal Knee Extension',
      duration: '5 mins',
      type: 'MOBILITY',
      difficulty: 'CRITICAL',
      image: 'https://via.placeholder.com/200x120?text=Terminal'
    }
  ]

  return (
    <div style={{ fontFamily: 'Poppins, sans-serif', display: 'flex', height: '100vh', backgroundColor: colors.lightGray }}>
      {/* Sidebar */}
      <div
        style={{
          width: sidebarOpen ? '240px' : '0',
          backgroundColor: colors.primaryDark,
          color: 'white',
          transition: 'width 0.3s ease',
          overflow: 'hidden',
          padding: sidebarOpen ? '20px 0' : '0',
          boxShadow: '2px 0 8px rgba(0,0,0,0.1)'
        }}
      >
        {/* Logo */}
        <div style={{ padding: '0 20px', marginBottom: '40px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              width: '40px',
              height: '40px',
              backgroundColor: colors.primary,
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px',
              fontWeight: 'bold'
            }}
          >
            DC
          </div>
          <div>
            <div style={{ fontSize: '12px', fontWeight: 'bold' }}>PhysioAI</div>
            <div style={{ fontSize: '10px', opacity: 0.8 }}>CLINICAL EXCELLENCE</div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav>
          {['Dashboard', 'Exercises', 'Sessions', 'Clinician'].map((item, index) => (
            <div
              key={index}
              style={{
                padding: '15px 20px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                borderLeft: index === 0 ? `4px solid ${colors.primary}` : 'none',
                backgroundColor: index === 0 ? 'rgba(30, 136, 229, 0.1)' : 'transparent',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(30, 136, 229, 0.1)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = index === 0 ? 'rgba(30, 136, 229, 0.1)' : 'transparent'
              }}
            >
              <Activity size={18} />
              <span style={{ fontSize: '14px' }}>{item}</span>
            </div>
          ))}
        </nav>

        {/* User Profile Section */}
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
            left: '20px',
            right: '20px',
            padding: '15px',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            textAlign: 'center'
          }}
        >
          <div style={{ width: '50px', height: '50px', borderRadius: '50%', backgroundColor: colors.primary, margin: '0 auto 10px' }}></div>
          <div style={{ fontSize: '12px', fontWeight: 'bold' }}>Dr. Aba Theme</div>
          <div style={{ fontSize: '10px', opacity: 0.8 }}>Physio Trainer</div>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {/* Header */}
        <div
          style={{
            backgroundColor: colors.background,
            padding: '20px 30px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderBottom: `1px solid ${colors.border}`,
            boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
          }}
        >
          <div>
            <span style={{ color: colors.textSecondary, fontSize: '12px' }}>Pages / Dashboard</span>
          </div>
          <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
            <input
              type="text"
              placeholder="Search data..."
              style={{
                padding: '8px 12px',
                border: `1px solid ${colors.border}`,
                borderRadius: '4px',
                fontSize: '13px',
                width: '200px',
                fontFamily: 'Poppins'
              }}
            />
            <Bell size={20} style={{ cursor: 'pointer', color: colors.textSecondary }} />
            <User size={20} style={{ cursor: 'pointer', color: colors.textSecondary }} />
          </div>
        </div>

        {/* Main Dashboard Content */}
        <div style={{ padding: '30px' }}>
          {/* Greeting Section */}
          <div style={{ marginBottom: '40px' }}>
            <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: colors.textPrimary, marginBottom: '8px' }}>
              Good morning, Alex.
            </h1>
            <p style={{ color: colors.textSecondary, fontSize: '14px', lineHeight: '1.6' }}>
              You've reached 85% of your mobility goals this week. Keep up the consistent effort—your knee recovery is showing significant data-driven progress.
            </p>
          </div>

          {/* Overview Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', marginBottom: '30px' }}>
            {/* Recovery Compliance Card */}
            <div
              style={{
                backgroundColor: colors.background,
                padding: '25px',
                borderRadius: '12px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                position: 'relative'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '20px' }}>
                <div>
                  <h2 style={{ fontSize: '16px', fontWeight: 'bold', color: colors.textPrimary, marginBottom: '4px' }}>
                    Recovery Compliance
                  </h2>
                  <p style={{ fontSize: '12px', color: colors.textSecondary }}>Weekly session completion rate</p>
                </div>
                <span
                  style={{
                    backgroundColor: colors.success,
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '11px',
                    fontWeight: 'bold'
                  }}
                >
                  ON TRACK
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '30px' }}>
                {/* Circular Progress */}
                <div style={{ position: 'relative', width: '150px', height: '150px' }}>
                  <svg width="150" height="150" style={{ transform: 'rotate(-90deg)' }}>
                    <circle cx="75" cy="75" r="70" fill="none" stroke={colors.border} strokeWidth="8" />
                    <circle
                      cx="75"
                      cy="75"
                      r="70"
                      fill="none"
                      stroke={colors.primary}
                      strokeWidth="8"
                      strokeDasharray={`${70 * 2 * Math.PI * 0.85} ${70 * 2 * Math.PI}`}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div
                    style={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      transform: 'translate(-50%, -50%)',
                      textAlign: 'center'
                    }}
                  >
                    <div style={{ fontSize: '32px', fontWeight: 'bold', color: colors.primaryDark }}>85%</div>
                  </div>
                </div>

                {/* Stats */}
                <div>
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '11px', color: colors.textSecondary, marginBottom: '4px', textTransform: 'uppercase' }}>
                      CONSISTENCY
                    </div>
                    <div style={{ fontSize: '18px', fontWeight: 'bold', color: colors.textPrimary }}>12 Days</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '11px', color: colors.textSecondary, marginBottom: '4px', textTransform: 'uppercase' }}>
                      MOBILITY SCORE
                    </div>
                    <div style={{ fontSize: '18px', fontWeight: 'bold', color: colors.success }}>+4.2 pts</div>
                  </div>
                  <div style={{ marginTop: '15px', fontSize: '11px', color: colors.textSecondary }}>
                    Daily Average Active Time
                  </div>
                  <div style={{ height: '4px', backgroundColor: colors.border, borderRadius: '2px', marginTop: '8px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', backgroundColor: colors.warning, width: '65%' }}></div>
                  </div>
                  <div style={{ marginTop: '4px', fontSize: '11px', color: colors.textSecondary }}>24.5 min</div>
                </div>
              </div>
            </div>

            {/* Quick Session Card */}
            <div
              style={{
                backgroundColor: colors.primaryDark,
                color: 'white',
                padding: '25px',
                borderRadius: '12px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <span
                  style={{
                    backgroundColor: colors.primary,
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '10px',
                    fontWeight: 'bold',
                    display: 'inline-block',
                    marginBottom: '12px'
                  }}
                >
                  NEXT SESSION
                </span>
                <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '4px' }}>Post-ACL Mobility</h3>
                <p style={{ fontSize: '12px', opacity: 0.8 }}>Starts in 15 mins</p>
              </div>

              <button
                style={{
                  backgroundColor: colors.background,
                  color: colors.primaryDark,
                  border: 'none',
                  padding: '12px 20px',
                  borderRadius: '6px',
                  fontWeight: 'bold',
                  fontSize: '14px',
                  cursor: 'pointer',
                  marginTop: '20px',
                  fontFamily: 'Poppins'
                }}
              >
                Start Routine
              </button>

              {/* Pain Score Data */}
              <div
                style={{
                  marginTop: '20px',
                  paddingTop: '20px',
                  borderTop: '1px solid rgba(255, 255, 255, 0.2)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                  <div
                    style={{
                      width: '30px',
                      height: '30px',
                      borderRadius: '50%',
                      backgroundColor: colors.primary,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}
                  >
                    📊
                  </div>
                  <div>
                    <div style={{ fontSize: '11px', opacity: 0.8 }}>Pain Score Data</div>
                    <div style={{ fontSize: '10px', opacity: 0.7 }}>Last 24 hours</div>
                  </div>
                </div>
                <div style={{ fontSize: '20px', fontWeight: 'bold' }}>2.4</div>
                <div style={{ fontSize: '11px', color: colors.success, marginTop: '4px' }}>↓ 0.2 lower than yesterday</div>
              </div>
            </div>
          </div>

          {/* Exercise Queue */}
          <div style={{ marginBottom: '30px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ fontSize: '18px', fontWeight: 'bold', color: colors.textPrimary }}>Today's Exercise Queue</h2>
              <a href="#" style={{ color: colors.primary, fontSize: '12px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}>
                View all exercises <ChevronRight size={14} />
              </a>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
              {exercises.map((exercise) => (
                <div
                  key={exercise.id}
                  style={{
                    backgroundColor: colors.background,
                    borderRadius: '12px',
                    overflow: 'hidden',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                    transition: 'transform 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-4px)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)'
                  }}
                >
                  <div
                    style={{
                      height: '120px',
                      backgroundColor: colors.border,
                      position: 'relative',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: colors.textSecondary
                    }}
                  >
                    [Exercise Image]
                  </div>
                  <div style={{ padding: '15px' }}>
                    <h3 style={{ fontSize: '14px', fontWeight: 'bold', color: colors.textPrimary, marginBottom: '4px' }}>
                      {exercise.name}
                    </h3>
                    <p style={{ fontSize: '11px', color: colors.textSecondary, marginBottom: '10px' }}>{exercise.duration}</p>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <span
                        style={{
                          padding: '4px 8px',
                          backgroundColor: colors.lightGray,
                          borderRadius: '4px',
                          fontSize: '10px',
                          fontWeight: 'bold',
                          color: colors.textPrimary
                        }}
                      >
                        {exercise.type}
                      </span>
                      <span
                        style={{
                          padding: '4px 8px',
                          backgroundColor: colors.lightGray,
                          borderRadius: '4px',
                          fontSize: '10px',
                          fontWeight: 'bold',
                          color: colors.textPrimary
                        }}
                      >
                        {exercise.difficulty}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* PhysioAI Analysis */}
          <div
            style={{
              backgroundColor: colors.background,
              padding: '25px',
              borderRadius: '12px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '15px' }}>
              <div
                style={{
                  width: '35px',
                  height: '35px',
                  borderRadius: '50%',
                  backgroundColor: colors.primary,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '18px'
                }}
              >
                🤖
              </div>
              <h2 style={{ fontSize: '16px', fontWeight: 'bold', color: colors.textPrimary }}>PhysioAI Analysis</h2>
            </div>

            <p style={{ color: colors.textSecondary, fontSize: '13px', lineHeight: '1.6', marginBottom: '15px' }}>
              Based on your recent knee slide motion data, we noticed a 15% increase in flexion angle compared to last Tuesday. This indicates your joint inflammation is subsiding. Continue with the current intensity, but focus on the slow eccentric (slow lowering) phase of your Quad Sets today.
            </p>

            <button
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                backgroundColor: 'transparent',
                color: colors.primary,
                border: `1px solid ${colors.primary}`,
                padding: '8px 16px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold',
                fontFamily: 'Poppins'
              }}
            >
              💡 Ask about this insight
            </button>
          </div>
        </div>
      </div>

      {/* Floating Action Button */}
      <div
        style={{
          position: 'fixed',
          bottom: '30px',
          right: '30px',
          width: '60px',
          height: '60px',
          backgroundColor: colors.primary,
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(30, 136, 229, 0.4)',
          transition: 'all 0.3s ease'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.boxShadow = '0 6px 16px rgba(30, 136, 229, 0.6)'
          e.currentTarget.style.transform = 'scale(1.05)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.boxShadow = '0 4px 12px rgba(30, 136, 229, 0.4)'
          e.currentTarget.style.transform = 'scale(1)'
        }}
      >
        <Plus size={28} color="white" />
      </div>
    </div>
  )
}

// Placeholder icons
function Bell({ size, style }) {
  return <span style={style}>🔔</span>
}

function User({ size, style }) {
  return <span style={style}>👤</span>
}

export default PatientDashboardPage
