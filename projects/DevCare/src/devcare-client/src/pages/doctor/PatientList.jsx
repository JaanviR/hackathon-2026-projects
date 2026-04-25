import { Link } from 'react-router-dom'
import { Search, UserPlus, Filter, MoreHorizontal, ArrowRight, TrendingUp, Users } from 'lucide-react'

function PatientList() {
  // Mock data
  const patients = [
    { id: 1, name: 'Alice Smith', progress: 75, condition: 'ACL Reconstruction', lastSeen: '2026-04-20', status: 'On Track', risk: 'Low' },
    { id: 2, name: 'Bob Johnson', progress: 45, condition: 'Shoulder Impingement', lastSeen: '2026-04-18', status: 'Falling Behind', risk: 'High' },
    { id: 3, name: 'Charlie Davis', progress: 90, condition: 'Ankle Sprain (Grade II)', lastSeen: '2026-04-24', status: 'Review Ready', risk: 'None' },
    { id: 4, name: 'Diana Prince', progress: 30, condition: 'Lumbar Strain', lastSeen: '2026-04-22', status: 'On Track', risk: 'Medium' },
    { id: 5, name: 'Edward Norton', progress: 60, condition: 'Carpal Tunnel', lastSeen: '2026-04-15', status: 'On Track', risk: 'Low' },
  ]

  const getStatusStyle = (status) => {
    switch (status) {
      case 'Falling Behind': return 'bg-red-50 text-red-600 border-red-100'
      case 'Review Ready': return 'bg-blue-50 text-blue-600 border-blue-100'
      default: return 'bg-emerald-50 text-emerald-600 border-emerald-100'
    }
  }

  return (
    <div className="animate-fade-in">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 mb-12">
        <div>
          <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-primary)] mb-2">
             <Users size={12} />
             Patient Management
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight">Clinical Directory</h1>
          <p className="text-[var(--color-text-muted)] mt-2 text-lg font-medium">Manage and monitor all your connected patients.</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <div className="relative flex-1 min-w-[280px]">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text" 
              placeholder="Search by name, ID or condition..." 
              className="auth-input h-[52px] !pl-14"
            />
          </div>
          <button className="btn-secondary h-[52px]">
            <Filter size={18} />
            <span>Filters</span>
          </button>
          <Link to="/doctor/share" className="btn-primary h-[52px]">
            <UserPlus size={18} />
            <span>New Connection</span>
          </Link>
        </div>
      </div>

      <div className="elevated-card overflow-hidden border-none shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-8 py-5 text-xs font-bold uppercase tracking-widest text-slate-500">Patient Identity</th>
                <th className="px-8 py-5 text-xs font-bold uppercase tracking-widest text-slate-500">Clinical Condition</th>
                <th className="px-8 py-5 text-xs font-bold uppercase tracking-widest text-slate-500">Last Encounter</th>
                <th className="px-8 py-5 text-xs font-bold uppercase tracking-widest text-slate-500">Clinical Status</th>
                <th className="px-8 py-5 text-xs font-bold uppercase tracking-widest text-slate-500 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {patients.map(patient => (
                <tr key={patient.id} className="hover:bg-slate-50/30 transition-all group">
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-4">
                      <div className="h-11 w-11 rounded-2xl bg-slate-100 flex items-center justify-center font-bold text-slate-600 group-hover:bg-[var(--color-primary-soft)] group-hover:text-[var(--color-primary)] transition-colors">
                        {patient.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div>
                         <span className="block font-bold text-slate-800">{patient.name}</span>
                         <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">ID: DC-2024-{patient.id}</span>
                      </div>
                    </div>
                  </td>
                  <td className="px-8 py-6">
                    <span className="text-sm font-semibold text-slate-600">{patient.condition}</span>
                  </td>
                  <td className="px-8 py-6">
                    <span className="text-sm font-medium text-slate-500">{patient.lastSeen}</span>
                  </td>
                  <td className="px-8 py-6">
                    <span className={`inline-flex items-center rounded-lg border px-3 py-1 text-[10px] font-bold uppercase tracking-wider ${getStatusStyle(patient.status)}`}>
                      {patient.status}
                    </span>
                  </td>
                  <td className="px-8 py-6 text-right">
                    <div className="flex items-center justify-end gap-2">
                       <Link 
                        to={`/doctor/patient/${patient.id}`}
                        className="btn-secondary py-2 px-4 text-xs h-9"
                       >
                         Manage
                       </Link>
                       <button className="h-9 w-9 flex items-center justify-center rounded-lg border border-slate-200 text-slate-400 hover:text-slate-600 hover:bg-slate-50">
                         <MoreHorizontal size={18} />
                       </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-8 flex items-center justify-between px-4">
         <p className="text-sm text-slate-500 font-medium">Showing <strong>5</strong> of <strong>24</strong> connected patients</p>
         <div className="flex gap-2">
            <button className="btn-secondary py-2 px-6 text-xs" disabled>Previous</button>
            <button className="btn-secondary py-2 px-6 text-xs">Next Page</button>
         </div>
      </div>
    </div>
  )
}

export default PatientList
