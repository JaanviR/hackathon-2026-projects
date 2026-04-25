import { useState } from 'react'
import { 
  ClipboardList, 
  Search, 
  Plus, 
  Trash2, 
  CheckCircle2, 
  Info, 
  ArrowRight,
  SendHorizontal,
  UserCheck
} from 'lucide-react'

function AssignTherapy() {
  const [selectedPatient, setSelectedPatient] = useState('')
  const [exercises, setExercises] = useState([]) // Array of { id, reps, sets }
  const [tasks, setTasks] = useState([])
  const [newTask, setNewTask] = useState('')

  const availableExercises = [
    { id: 'ex1', name: 'Bicep Curl', description: 'Elbow flexion with resistance', icon: '💪' },
    { id: 'ex2', name: 'Squat', description: 'Functional lower body movement', icon: '🦵' },
    { id: 'ex3', name: 'Shoulder Raise', description: 'Lateral arm elevation', icon: '🏋️' },
    { id: 'ex4', name: 'Knee Extension', description: 'Terminal knee straightening', icon: '🦵' },
    { id: 'ex5', name: 'Hip Abduction', description: 'Lateral leg movement', icon: '🦿' },
  ]

  const toggleExercise = (id) => {
    const exists = exercises.find(e => e.id === id)
    if (exists) {
      setExercises(exercises.filter(e => e.id !== id))
    } else {
      setExercises([...exercises, { id, reps: 10, sets: 3 }])
    }
  }

  const updateExerciseParams = (id, field, value) => {
    setExercises(exercises.map(ex => 
      ex.id === id ? { ...ex, [field]: parseInt(value) || 0 } : ex
    ))
  }

  const addTask = () => {
    if (newTask.trim()) {
      setTasks([...tasks, newTask.trim()])
      setNewTask('')
    }
  }

  const removeTask = (index) => {
    setTasks(tasks.filter((_, i) => i !== index))
  }

  return (
    <div className="animate-fade-in pb-12">
      <header className="mb-12">
        <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-primary)] mb-2">
           <ClipboardList size={12} />
           Plan Configuration
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight">Assign Recovery Plan</h1>
        <p className="text-lg text-[var(--color-text-muted)] mt-2 font-medium">Create a personalized combination of exercises and daily tasks.</p>
      </header>

      <div className="grid gap-8 lg:grid-cols-12">
        <div className="lg:col-span-8 space-y-8">
          
          {/* Step 1: Select Patient */}
          <section className="elevated-card p-8 border-none shadow-lg">
            <div className="flex items-center gap-3 mb-8">
              <div className="h-8 w-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm">01</div>
              <h2 className="text-xl font-bold">Select Target Patient</h2>
            </div>
            <div className="relative">
               <select 
                className="auth-input h-[56px] appearance-none font-semibold text-slate-700"
                value={selectedPatient}
                onChange={(e) => setSelectedPatient(e.target.value)}
               >
                <option value="">Choose a patient from your directory...</option>
                <option value="1">Sarah Chen (ACL Reconstruction)</option>
                <option value="2">Bob Johnson (Shoulder Impingement)</option>
                <option value="3">Charlie Davis (Ankle Sprain)</option>
               </select>
               <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                  <ArrowRight size={18} className="rotate-90" />
               </div>
            </div>
          </section>

          {/* Step 2: Physical Exercises */}
          <section className="elevated-card p-8 border-none shadow-lg">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm">02</div>
                <h2 className="text-xl font-bold">Physical Therapy Library</h2>
              </div>
              <div className="relative hidden sm:block">
                 <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={14} />
                 <input type="text" placeholder="Search exercises..." className="bg-slate-50 border border-slate-100 rounded-lg py-2 pl-9 pr-4 text-xs font-medium outline-none focus:border-blue-200" />
              </div>
            </div>
            
            <div className="grid gap-4 sm:grid-cols-2">
              {availableExercises.map(ex => {
                const selected = exercises.find(e => e.id === ex.id)
                return (
                  <div 
                    key={ex.id}
                    onClick={() => toggleExercise(ex.id)}
                    className={`group cursor-pointer rounded-[1.5rem] border-2 p-5 transition-all flex flex-col gap-4 ${
                      selected 
                        ? 'border-[var(--color-primary)] bg-[var(--color-primary-soft)]' 
                        : 'border-slate-100 hover:border-slate-200 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <div className={`h-12 w-12 rounded-2xl flex items-center justify-center text-xl transition-all shadow-sm ${selected ? 'bg-white' : 'bg-slate-50'}`}>
                        {ex.icon}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h4 className={`font-bold transition-colors ${selected ? 'text-[var(--color-primary)]' : 'text-slate-800'}`}>{ex.name}</h4>
                          {selected && <CheckCircle2 size={18} className="text-[var(--color-primary)] animate-in zoom-in duration-300" />}
                        </div>
                        <p className={`text-xs mt-1.5 font-medium leading-relaxed transition-colors ${selected ? 'text-blue-600/80' : 'text-slate-500'}`}>{ex.description}</p>
                      </div>
                    </div>

                    {selected && (
                      <div className="flex items-center gap-4 pt-4 border-t border-blue-100 animate-in slide-in-from-top-2 duration-300" onClick={(e) => e.stopPropagation()}>
                        <div className="flex-1">
                          <label className="text-[9px] font-black uppercase tracking-widest text-blue-400 block mb-1.5">No. of Reps</label>
                          <input 
                            type="number" 
                            value={selected.reps}
                            onChange={(e) => updateExerciseParams(ex.id, 'reps', e.target.value)}
                            className="w-full bg-white border border-blue-100 rounded-xl px-3 py-2 text-xs font-bold text-slate-700 focus:border-blue-300 outline-none"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </section>

          {/* Step 3: Daily Tasks */}
          <section className="elevated-card p-8 border-none shadow-lg">
            <div className="flex items-center gap-3 mb-8">
              <div className="h-8 w-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm">03</div>
              <h2 className="text-xl font-bold">Daily Recovery Roadmap</h2>
            </div>
            
            <div className="flex gap-3 mb-8">
              <input 
                type="text" 
                className="auth-input flex-1 h-[56px] border-slate-200" 
                placeholder="e.g., Apply ice compression for 15 mins..."
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addTask()}
              />
              <button 
                onClick={addTask}
                className="btn-dark px-8 rounded-2xl h-[56px] hover:scale-105 transition-transform"
              >
                <Plus size={20} />
                <span>Add Task</span>
              </button>
            </div>

            <div className="space-y-3">
              {tasks.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 px-6 bg-slate-50/50 border-2 border-dashed border-slate-100 rounded-[2rem]">
                   <div className="h-12 w-12 rounded-full bg-white flex items-center justify-center text-slate-300 mb-4 shadow-sm">
                      <Info size={24} />
                   </div>
                   <p className="text-sm font-bold text-slate-400">No supplemental tasks added yet</p>
                   <p className="text-xs text-slate-400 mt-1">Add items like nutrition, rest, or cold therapy.</p>
                </div>
              ) : (
                tasks.map((task, index) => (
                  <div key={index} className="group flex items-center justify-between p-5 rounded-2xl bg-white border border-slate-100 shadow-sm hover:shadow-md hover:border-blue-100 transition-all">
                    <div className="flex items-center gap-4">
                       <div className="h-6 w-6 rounded-full bg-blue-50 text-blue-500 flex items-center justify-center text-[10px] font-black">
                         {index + 1}
                       </div>
                       <span className="text-sm font-semibold text-slate-700">{task}</span>
                    </div>
                    <button 
                      onClick={() => removeTask(index)}
                      className="h-8 w-8 rounded-lg flex items-center justify-center text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>

        {/* Action Sidebar */}
        <div className="lg:col-span-4">
          <div className="sticky top-8 space-y-6">
            <div className="elevated-card p-8 border-none shadow-xl bg-white relative overflow-hidden">
               <div className="absolute top-0 left-0 w-full h-1 bg-[var(--color-primary)]"></div>
               <h2 className="text-xl font-bold mb-8">Plan Summary</h2>
               
               <div className="space-y-6">
                 <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100">
                   <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-2">Recipient</p>
                   <p className="text-sm font-bold text-slate-900">
                     {selectedPatient ? (selectedPatient === '1' ? 'Sarah Chen' : selectedPatient === '2' ? 'Bob Johnson' : 'Charlie Davis') : '---'}
                   </p>
                 </div>

                 <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100">
                      <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Exercises</p>
                      <p className="text-2xl font-black text-slate-900">{exercises.length}</p>
                    </div>
                    <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100">
                      <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Tasks</p>
                      <p className="text-2xl font-black text-slate-900">{tasks.length}</p>
                    </div>
                 </div>
               </div>

               <button 
                 disabled={!selectedPatient || (exercises.length === 0 && tasks.length === 0)}
                 className="btn-primary w-full mt-10 py-4 rounded-2xl flex items-center justify-center gap-3 shadow-blue-200"
                 onClick={() => alert('Plan has been securely transmitted to patient dashboard.')}
               >
                 <SendHorizontal size={20} />
                 <span>Deploy Plan</span>
               </button>
               
            </div>

            <div className="p-6 rounded-[2rem] bg-emerald-50 border border-emerald-100">
               <div className="flex gap-4">
                  <div className="h-10 w-10 rounded-xl bg-white flex items-center justify-center text-emerald-500 shadow-sm">
                     <CheckCircle2 size={20} />
                  </div>
                  <div>
                     <p className="text-sm font-bold text-emerald-800 leading-tight">Patient Connected</p>
                     <p className="text-xs text-emerald-600 mt-1 font-medium">Real-time telemetry will activate once plan is assigned.</p>
                  </div>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AssignTherapy
