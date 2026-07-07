"use client";

import React, { useState, useRef, useEffect } from "react";
import { api, ChatResponse } from "@/services/api";
import { Send, User, Bot, FileText, ChevronDown, Loader2 } from "lucide-react";

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
    <div className="flex-1 flex flex-col h-full bg-slate-50 dark:bg-[#020617] relative">
      {/* Decorative background blob */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-[#C00F2E]/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#F3B229]/5 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <header className="px-8 py-4 border-b border-slate-200 dark:border-slate-800 glass z-10 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Assistant Chat</h2>
          <p className="text-sm text-slate-500">Query the ingested ONGC knowledge base</p>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-8 z-10 flex flex-col gap-6">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-4 max-w-4xl ${
              msg.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            {/* Avatar */}
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-sm ${
                msg.role === "user"
                  ? "bg-slate-800 text-white dark:bg-slate-100 dark:text-slate-900"
                  : "bg-[#C00F2E] text-white"
              }`}
            >
              {msg.role === "user" ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>

            {/* Content box */}
            <div className={`flex flex-col gap-2 ${msg.role === "user" ? "items-end" : "items-start"}`}>
              <div
                className={`p-4 rounded-2xl shadow-sm text-sm sm:text-base leading-relaxed ${
                  msg.role === "user"
                    ? "bg-slate-800 text-white dark:bg-slate-200 dark:text-slate-900 rounded-tr-none"
                    : "bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-tl-none border border-slate-200 dark:border-slate-800"
                }`}
              >
                {msg.content}
              </div>

              {/* Sources */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  <div className="w-full text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                    Sources
                  </div>
                  {msg.sources.map((source, sIdx) => (
                    <div
                      key={sIdx}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-white dark:bg-slate-900 border border-[#F3B229]/30 text-slate-600 dark:text-slate-300 rounded-full text-xs shadow-sm hover:border-[#F3B229] transition-colors cursor-default"
                    >
                      <FileText className="w-3.5 h-3.5 text-[#F3B229]" />
                      <span className="truncate max-w-[150px]" title={source.filename}>
                        {source.filename}
                      </span>
                      <span className="text-slate-400">pg {source.page}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-4 max-w-4xl mr-auto">
            <div className="w-10 h-10 rounded-full bg-[#C00F2E] text-white flex items-center justify-center shrink-0 shadow-sm">
              <Loader2 className="w-5 h-5 animate-spin" />
            </div>
            <div className="flex items-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl rounded-tl-none shadow-sm">
              <div className="flex gap-1">
                <div className="w-2 h-2 rounded-full bg-slate-300 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-slate-300 animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-slate-300 animate-bounce [animation-delay:0.4s]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-transparent z-10">
        <div className="max-w-4xl mx-auto relative">
          <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 p-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-full shadow-lg focus-within:ring-2 focus-within:ring-[#C00F2E]/20 focus-within:border-[#C00F2E] transition-all"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 bg-transparent px-4 py-2 outline-none text-slate-800 dark:text-slate-200"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="w-10 h-10 rounded-full bg-[#C00F2E] hover:bg-[#910B23] text-white flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
            >
              <Send className="w-4 h-4 ml-0.5" />
            </button>
          </form>
          <div className="text-center mt-3 text-xs text-slate-400">
            Copilot can make mistakes. Verify critical ONGC information.
          </div>
        </div>
      </div>
    </div>
  );
}
