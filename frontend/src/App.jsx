import React, { useState } from 'react';
import { Shield, Terminal, Send, ShieldAlert, Database, Lock } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Système CyberGuard IA en ligne. Prêt pour l\'analyse de menace.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  // Fonction pour envoyer le message au Backend Python
  const handleSend = async () => {
    if (!input.trim()) return;

    // Ajouter le message de l'utilisateur à l'interface
    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setLoading(true);
    const currentInput = input;
    setInput('');

    try {
      // Connexion avec le Backend FastAPI
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput }),
      });
      
      const data = await response.json();
      
      // Ajouter la réponse de l'IA Agent
      setMessages([...newMessages, { sender: 'bot', text: data.response }]);
    } catch (error) {
      setMessages([...newMessages, { sender: 'bot', text: 'Erreur: Le serveur Backend est-il lancé ?' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* HEADER : Look Professionnel Cyber */}
      <header className="border-b border-emerald-500/20 bg-slate-900/50 p-4 flex items-center justify-between backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
            <Shield className="text-emerald-400 w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-emerald-400">CYBERGUARD <span className="text-slate-500">//</span> AI AGENT</h1>
            <p className="text-[10px] text-emerald-500/60 font-mono uppercase tracking-[0.2em]">Security Operations Center v1.0</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-2 text-xs bg-slate-800 px-3 py-1.5 rounded-full border border-slate-700">
            <Database size={14} className="text-blue-400" />
            <span className="text-slate-300">RAG: Actif</span>
          </div>
          <div className="flex items-center gap-2 text-xs bg-emerald-500/10 text-emerald-400 px-3 py-1.5 rounded-full border border-emerald-500/20">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping"></div>
            EN LIGNE
          </div>
        </div>
      </header>

      {/* MAIN LAYOUT */}
      <main className="flex-1 flex overflow-hidden">
        
        {/* SIDEBAR GAUCHE : État de la Cyber-Sécurité */}
        <aside className="w-64 border-r border-slate-800 bg-slate-900/30 p-6 hidden lg:flex flex-col gap-8">
          <div>
            <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-4">Modules IA</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-sm text-slate-300 bg-slate-800/50 p-2 rounded-md border border-slate-700">
                <Lock size={16} className="text-emerald-400" />
                <span>Anonymiseur PII</span>
              </div>
              <div className="flex items-center gap-3 text-sm text-slate-300 bg-slate-800/50 p-2 rounded-md border border-slate-700">
                <Terminal size={16} className="text-blue-400" />
                <span>Analyseur de Logs</span>
              </div>
            </div>
          </div>

          <div className="mt-auto border-t border-slate-800 pt-6">
            <div className="p-4 bg-amber-500/5 border border-amber-500/10 rounded-xl">
              <div className="flex items-center gap-2 text-amber-500 mb-2">
                <ShieldAlert size={16} />
                <span className="text-xs font-bold uppercase">Alerte IA</span>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                L'agent surveille actuellement les tentatives d'injection SQL et les scans de ports.
              </p>
            </div>
          </div>
        </aside>

        {/* CHAT AREA */}
        <section className="flex-1 flex flex-col bg-slate-950 relative">
          
          {/* Grille de fond "Cyber" */}
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

          <div className="flex-1 p-6 overflow-y-auto space-y-6 relative z-0">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-4 rounded-2xl shadow-2xl ${
                  msg.sender === 'user' 
                    ? 'bg-emerald-600 text-white rounded-tr-none' 
                    : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none'
                }`}>
                  <p className="text-sm leading-relaxed whitespace-pre-line">{msg.text}</p>
                  <span className="text-[9px] opacity-40 mt-2 block uppercase tracking-tighter">
                    {msg.sender === 'user' ? 'Utilisateur' : 'Cyber-Agent'}
                  </span>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex gap-2 items-center text-emerald-500 text-xs font-mono italic">
                <span className="animate-bounce">.</span><span className="animate-bounce delay-100">.</span><span className="animate-bounce delay-200">.</span>
                Analyse RAG en cours
              </div>
            )}
          </div>

          {/* INPUT AREA */}
          <div className="p-6 bg-slate-900/80 backdrop-blur-md border-t border-slate-800 relative z-10">
            <div className="max-w-4xl mx-auto flex gap-3 bg-slate-950 p-2 rounded-xl border border-slate-700 focus-within:border-emerald-500/50 transition-all shadow-inner">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Décrivez une menace ou collez un log suspect..."
                className="flex-1 bg-transparent border-none p-3 text-sm text-emerald-400 focus:outline-none placeholder:text-slate-600"
              />
              <button 
                onClick={handleSend} 
                className="bg-emerald-600 hover:bg-emerald-500 text-white px-5 rounded-lg transition-all flex items-center gap-2 group"
              >
                <span className="text-xs font-bold uppercase tracking-wider">Analyser</span>
                <Send size={16} className="group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
            <p className="text-[10px] text-center text-slate-500 mt-3 italic">
              Propulsé par RAG (Retrieval-Augmented Generation) & LangChain Agent
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;