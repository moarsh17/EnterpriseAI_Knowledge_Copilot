"use client";

import React, { useState, useRef, useEffect } from "react";
import { api, ChatResponse } from "@/services/api";
import { Send, User, Bot, FileText, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatResponse["sources"];
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello! I am your ONGC Knowledge Copilot. How can I assist you with your documents today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const res = await api.chat(userMessage);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.answer, sources: res.sources },
      ]);
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error while processing your request: " + (error.message || "Unknown error"),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-background relative overflow-hidden">
      {/* Decorative background blob */}
      <div className="absolute top-[-10%] left-[10%] w-[40rem] h-[40rem] bg-[#C00F2E]/5 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[10%] w-[40rem] h-[40rem] bg-[#F3B229]/5 rounded-full blur-[100px] pointer-events-none" />

      {/* Header */}
      <header className="px-8 py-5 border-b border-border/50 glass z-10 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-medium text-foreground tracking-tight">Assistant Chat</h2>
          <p className="text-[11px] text-muted-foreground uppercase tracking-widest mt-1">Query the ONGC knowledge base</p>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-8 z-10 flex flex-col gap-8 scroll-smooth">
        <AnimatePresence initial={false}>
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
              className={`flex gap-4 max-w-3xl ${
                msg.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 shadow-sm ${
                  msg.role === "user"
                    ? "bg-foreground text-background"
                    : "bg-[#C00F2E] text-white"
                }`}
              >
                {msg.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Content box */}
              <div className={`flex flex-col gap-3 ${msg.role === "user" ? "items-end" : "items-start"}`}>
                <div
                  className={`px-5 py-4 rounded-2xl shadow-sm text-[15px] leading-relaxed ${
                    msg.role === "user"
                      ? "bg-foreground text-background rounded-tr-sm"
                      : "bg-muted/50 text-foreground rounded-tl-sm border border-border/50 backdrop-blur-md"
                  }`}
                >
                  {msg.content}
                </div>

                {/* Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <motion.div 
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
                    className="flex flex-wrap gap-2 mt-1"
                  >
                    {msg.sources.map((source, sIdx) => (
                      <div
                        key={sIdx}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-background/50 border border-border/80 text-muted-foreground rounded-full text-[11px] font-medium shadow-sm hover:border-[#F3B229]/50 hover:text-foreground transition-all cursor-default"
                      >
                        <FileText className="w-3 h-3 text-[#F3B229]" />
                        <span className="truncate max-w-[150px]" title={source.filename}>
                          {source.filename}
                        </span>
                        <span className="opacity-50 mx-1">•</span>
                        <span className="text-muted-foreground font-mono text-[10px]">pg {source.page}</span>
                      </div>
                    ))}
                  </motion.div>
                )}
              </div>
            </motion.div>
          ))}
          {loading && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-4 max-w-3xl mr-auto"
            >
              <div className="w-9 h-9 rounded-full bg-[#C00F2E] text-white flex items-center justify-center shrink-0 shadow-sm">
                <Loader2 className="w-4 h-4 animate-spin" />
              </div>
              <div className="flex items-center bg-muted/50 border border-border/50 backdrop-blur-md px-5 py-4 rounded-2xl rounded-tl-sm shadow-sm h-[56px]">
                <div className="flex gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50 animate-bounce" />
                  <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:0.2s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:0.4s]" />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} className="h-4" />
      </div>

      {/* Input Area */}
      <div className="p-6 bg-gradient-to-t from-background via-background/95 to-transparent z-10">
        <div className="max-w-3xl mx-auto relative">
          <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 p-1.5 bg-background/80 backdrop-blur-xl border border-border/80 rounded-full shadow-lg focus-within:ring-1 focus-within:ring-[#C00F2E]/30 focus-within:border-[#C00F2E]/50 transition-all"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about the documents..."
              className="flex-1 bg-transparent px-5 py-2.5 outline-none text-[15px] text-foreground placeholder:text-muted-foreground/70"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="w-11 h-11 rounded-full bg-foreground hover:bg-foreground/90 text-background flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
            >
              <Send className="w-4 h-4 ml-0.5" />
            </button>
          </form>
          <div className="text-center mt-4 text-[10px] text-muted-foreground uppercase tracking-widest font-medium">
            AI can make mistakes. Verify critical ONGC information.
          </div>
        </div>
      </div>
    </div>
  );
}
