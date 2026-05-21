"use client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import clsx from "clsx";
import type { Message } from "@/lib/api";

export function TypingDots() {
  return (
    <div className="flex items-start gap-3 animate-fade-in">
      <Avatar role="assistant" />
      <div className="bg-card border border-border rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="flex gap-1.5 items-center h-4">
          <span className="dot" />
          <span className="dot" />
          <span className="dot" />
        </div>
      </div>
    </div>
  );
}

function Avatar({ role }: { role: "user" | "assistant" }) {
  return (
    <div className={clsx(
      "w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-[11px] font-mono font-bold",
      role === "user"
        ? "bg-accent text-white"
        : "bg-accent/15 border border-accent/25 text-accent"
    )}>
      {role === "user" ? "You" : "AI"}
    </div>
  );
}

interface Props {
  message: Message & { sources?: string[] };
}

export default function ChatBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={clsx("flex items-start gap-3 animate-fade-up", isUser && "flex-row-reverse")}>
      <Avatar role={message.role} />
      <div className={clsx(
        "max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
        isUser
          ? "bg-accent/12 border border-accent/20 rounded-tr-sm text-slate-100"
          : "bg-card border border-border rounded-tl-sm text-slate-200"
      )}>
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{

              code({ className, children, ...props }: any) {
                const lang = /language-(\w+)/.exec(className || "")?.[1];
                return lang ? (
                  <SyntaxHighlighter style={oneDark as any} language={lang} PreTag="div" className="rounded-lg text-xs my-2">
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                ) : (
                  <code className="bg-input text-accent px-1.5 py-0.5 rounded text-xs font-mono" {...props}>
                    {children}
                  </code>
                );
              },
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-0.5">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-0.5">{children}</ol>,
              li: ({ children }) => <li>{children}</li>,
              strong: ({ children }) => <strong className="font-semibold text-slate-100">{children}</strong>,
              h1: ({ children }) => <h1 className="text-base font-semibold mb-2">{children}</h1>,
              h2: ({ children }) => <h2 className="text-sm font-semibold mb-1.5">{children}</h2>,
              h3: ({ children }) => <h3 className="text-sm font-medium mb-1">{children}</h3>,
              blockquote: ({ children }) => (
                <blockquote className="border-l-2 border-accent pl-3 italic text-muted my-2">{children}</blockquote>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}

        {/* Source file badges */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3 pt-2.5 border-t border-border">
            {message.sources.map((s) => (
              <span key={s} className="text-[10px] font-mono bg-input text-muted px-2 py-0.5 rounded-full border border-border">
                📄 {s}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
