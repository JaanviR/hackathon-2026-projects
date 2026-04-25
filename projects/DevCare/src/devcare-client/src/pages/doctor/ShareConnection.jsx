import { useState } from 'react'
import { 
  UserPlus, 
  QrCode, 
  Copy, 
  MessageCircle, 
  Smartphone, 
  Mail, 
  Clock, 
  CheckCircle2,
  ShieldCheck,
  Zap,
  ArrowRight
} from 'lucide-react'

function ShareConnection() {
  const [copied, setCopied] = useState(false)
  const shareLink = "devcare.app/connect/dr-robert-8219"

  const handleCopy = () => {
    navigator.clipboard.writeText("https://devcare.app/connect/dr-robert-8219")
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="animate-fade-in pb-12">
      <header className="mb-12">
        <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--color-primary)] mb-2">
           <UserPlus size={12} />
           Onboarding Center
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight">Expand Your Network</h1>
        <p className="mt-2 text-lg text-[var(--color-text-muted)] max-w-2xl font-medium">
          Securely onboard new patients by sharing a unique connection gateway.
        </p>
      </header>

      <div className="grid gap-10 lg:grid-cols-12">
        {/* Left Column: QR Code Gateway */}
        <div className="lg:col-span-4">
          <div className="elevated-card rounded-[2.5rem] border-none bg-white p-10 text-center h-full flex flex-col justify-center shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 h-32 w-32 bg-slate-50 rounded-full blur-3xl -mr-16 -mt-16"></div>
            
            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-400 mb-10">Instant QR Gateway</h3>
            
            <div className="mx-auto bg-white p-6 rounded-[2.5rem] shadow-xl border border-slate-50 mb-10 relative group">
              <div className="absolute inset-0 bg-[var(--color-primary)] opacity-0 group-hover:opacity-5 transition-opacity rounded-[2.5rem]"></div>
              <img 
                src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://devcare.app/connect/dr-robert-8219" 
                alt="Secure QR Code" 
                className="w-full h-auto relative z-10"
              />
            </div>
            
            <div className="space-y-4 px-2">
               <div className="flex items-center gap-3 text-left p-4 rounded-2xl bg-slate-50 border border-slate-100">
                  <Smartphone className="text-blue-500 shrink-0" size={18} />
                  <p className="text-[11px] font-semibold text-slate-600 leading-tight">Patient scans via DevCare app to establish clinical link.</p>
               </div>
            </div>
          </div>
        </div>

        {/* Middle Column: Digital Invitations */}
        <div className="lg:col-span-8 space-y-8">
           <div className="grid gap-8 md:grid-cols-2">
              {/* Share Link Card */}
              <div className="elevated-card rounded-[2.5rem] border-none bg-white p-10 shadow-lg">
                 <div className="h-12 w-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-6 shadow-sm">
                    <Copy size={24} />
                 </div>
                 <h3 className="text-xl font-bold mb-3">Invite Link</h3>
                 <p className="text-sm text-slate-500 font-medium mb-8 leading-relaxed">
                   Perfect for email invitations or telehealth onboarding sessions.
                 </p>
                 
                 <div className="relative group">
                    <input 
                      readOnly
                      value={shareLink}
                      className="auth-input pr-12 h-[56px] bg-slate-50 border-slate-100 font-bold text-slate-800 cursor-default"
                    />
                    <button 
                      onClick={handleCopy}
                      className={`absolute right-2 top-1/2 -translate-y-1/2 h-10 w-10 flex items-center justify-center rounded-xl transition-all ${
                        copied ? 'bg-emerald-500 text-white' : 'bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-dark)]'
                      }`}
                    >
                      {copied ? <CheckCircle2 size={18} /> : <Copy size={18} />}
                    </button>
                 </div>
                 {copied && <p className="text-[10px] font-black text-emerald-600 mt-3 text-center uppercase tracking-widest animate-in fade-in slide-in-from-top-1">Copied to Clipboard</p>}
              </div>

              {/* Multi-channel Share */}
              <div className="elevated-card rounded-[2.5rem] border-none bg-white p-10 shadow-lg">
                 <div className="h-12 w-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-6 shadow-sm">
                    <MessageCircle size={24} />
                 </div>
                 <h3 className="text-xl font-bold mb-3">One-Click Share</h3>
                 <p className="text-sm text-slate-500 font-medium mb-8 leading-relaxed">
                    Directly send invitations through preferred messaging platforms.
                 </p>
                 
                 <div className="grid grid-cols-3 gap-3">
                    {[
                      { icon: MessageCircle, label: 'WhatsApp', color: 'bg-[#25D366]/10 text-[#25D366] hover:bg-[#25D366]/20' },
                      { icon: Mail, label: 'Email', color: 'bg-blue-50 text-blue-600 hover:bg-blue-100' },
                      { icon: Smartphone, label: 'SMS', color: 'bg-slate-100 text-slate-600 hover:bg-slate-200' }
                    ].map((btn, i) => (
                      <button key={i} className={`flex flex-col items-center justify-center gap-3 p-4 rounded-2xl transition-all border border-transparent hover:border-current/10 ${btn.color}`}>
                         <btn.icon size={24} />
                         <span className="text-[9px] font-black uppercase tracking-widest">{btn.label}</span>
                      </button>
                    ))}
                 </div>
              </div>
           </div>

           {/* Activity & Logs */}
           <div className="elevated-card rounded-[2.5rem] border-none bg-white shadow-xl overflow-hidden">
              <div className="px-10 py-8 border-b border-slate-50 flex items-center justify-between bg-slate-50/30">
                 <div>
                    <h3 className="text-lg font-bold text-slate-900">Recent Onboarding Activity</h3>
                    <p className="text-xs text-slate-400 font-bold uppercase tracking-widest mt-1">Status Tracking</p>
                 </div>
                 <button className="text-xs font-bold text-blue-600 hover:underline flex items-center gap-1">
                   Full History <ArrowRight size={14} />
                 </button>
              </div>
              <div className="divide-y divide-slate-50">
                 {[
                   { name: 'Sarah Chen', status: 'Connected', time: 'Today, 10:24 AM', color: 'bg-emerald-50 text-emerald-600' },
                   { name: 'Marcus Thompson', status: 'Pending', time: 'Yesterday, 04:15 PM', color: 'bg-amber-50 text-amber-600' }
                 ].map((conn, i) => (
                   <div key={i} className="px-10 py-6 flex items-center justify-between group hover:bg-slate-50/50 transition-colors cursor-pointer">
                     <div className="flex items-center gap-5">
                       <div className="h-12 w-12 rounded-2xl bg-slate-100 flex items-center justify-center font-black text-slate-400 group-hover:bg-white group-hover:text-blue-600 group-hover:shadow-sm transition-all">
                         {conn.name.split(' ').map(n => n[0]).join('')}
                       </div>
                       <div>
                         <h4 className="font-bold text-slate-900 leading-tight">{conn.name}</h4>
                         <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1 flex items-center gap-1.5">
                            <Clock size={10} /> {conn.time}
                         </p>
                       </div>
                     </div>
                     <span className={`px-4 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-[0.15em] border border-current/10 ${conn.color}`}>
                       {conn.status}
                     </span>
                   </div>
                 ))}
              </div>
           </div>
        </div>
      </div>
    </div>
  )
}

export default ShareConnection
