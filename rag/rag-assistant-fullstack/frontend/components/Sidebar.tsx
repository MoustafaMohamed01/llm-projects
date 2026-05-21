"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, Upload, Info, Zap } from "lucide-react";
import clsx from "clsx";

const links = [
  { href: "/chat",   label: "Chat",   icon: MessageSquare },
  { href: "/upload", label: "Upload", icon: Upload },
  { href: "/about",  label: "About",  icon: Info },
];

export default function Sidebar() {
  const path = usePathname();
  return (
    <aside className="w-52 shrink-0 flex flex-col h-screen bg-panel border-r border-border">
      {/* Logo */}
      <div className="px-4 py-5 border-b border-border">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-accent flex items-center justify-center shrink-0">
            <Zap size={15} className="text-white" />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-100 leading-tight">RAG Assistant</p>
            <p className="text-[10px] font-mono text-muted">Hybrid · Gemini</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-1">
        {links.map(({ href, label, icon: Icon }) => {
          const active = path.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all",
                active
                  ? "bg-accent/10 text-accent border border-accent/20 font-medium"
                  : "text-muted hover:text-slate-200 hover:bg-card"
              )}
            >
              <Icon size={15} />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-border">
        <p className="text-[10px] font-mono text-dim leading-relaxed">
          FAISS + BM25 + CrossEncoder<br />Gemini 2.5 Flash
        </p>
      </div>
    </aside>
  );
}
