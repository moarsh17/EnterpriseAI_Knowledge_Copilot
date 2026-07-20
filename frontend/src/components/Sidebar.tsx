"use client";

import React, { useState, useEffect } from "react";
import { api } from "@/services/api";
import { UploadCloud, CheckCircle, AlertCircle, FileText, BookOpen, Trash2, Loader2, Sun, Moon, Globe, RefreshCw } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "next-themes";

export default function Sidebar() {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  
  const [documents, setDocuments] = useState<any[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(true);

  const [githubUrl, setGithubUrl] = useState("");
  const [ingestingGithub, setIngestingGithub] = useState(false);
  const [githubRepos, setGithubRepos] = useState<any[]>([]);
  const [loadingRepos, setLoadingRepos] = useState(true);
  const [syncingRepoId, setSyncingRepoId] = useState<string | null>(null);

  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const fetchDocuments = async () => {
    setLoadingDocs(true);
    try {
      const docs = await api.getDocuments();
      setDocuments(docs);
    } catch (error) {
      console.error("Failed to fetch documents:", error);
    } finally {
      setLoadingDocs(false);
    }
  };

  const fetchGithubRepos = async () => {
    setLoadingRepos(true);
    try {
      const repos = await api.getGithubRepos();
      setGithubRepos(repos);
    } catch (error) {
      console.error("Failed to fetch github repos:", error);
    } finally {
      setLoadingRepos(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    fetchGithubRepos();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    setUploading(true);
    setUploadStatus("idle");
    setErrorMessage("");

    try {
      await api.uploadFiles(files);
      setUploadStatus("success");
      fetchDocuments();
    } catch (error: any) {
      setUploadStatus("error");
      setErrorMessage(error.message || "Failed to upload files");
    } finally {
      setUploading(false);
      e.target.value = "";
      setTimeout(() => setUploadStatus("idle"), 3000);
    }
  };

  const handleGithubIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!githubUrl.trim()) return;

    setIngestingGithub(true);
    try {
      await api.ingestGithub(githubUrl.trim());
      setGithubUrl("");
      fetchGithubRepos();
    } catch (error: any) {
      alert(error.message || "Failed to ingest repository");
    } finally {
      setIngestingGithub(false);
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    try {
      await api.deleteDocument(documentId);
      fetchDocuments();
    } catch (error) {
      console.error("Failed to delete document:", error);
    }
  };

  const handleDeleteRepo = async (repoId: string) => {
    try {
      await api.deleteGithubRepo(repoId);
      fetchGithubRepos();
    } catch (error) {
      console.error("Failed to delete repo:", error);
    }
  };

  const handleSyncRepo = async (repoId: string) => {
    setSyncingRepoId(repoId);
    try {
      await api.syncGithubRepo(repoId);
      fetchGithubRepos();
    } catch (error: any) {
      alert(error.message || "Failed to sync repository");
    } finally {
      setSyncingRepoId(null);
    }
  };

  return (
    <div className="w-80 h-full flex flex-col bg-background border-r border-border shadow-none z-10 transition-colors duration-300">
      {/* Brand Header */}
      <div className="p-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#C00F2E] flex items-center justify-center shadow-lg shrink-0">
            <BookOpen className="text-[#F3B229] w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-foreground tracking-tight leading-none">ONGC</h1>
            <p className="text-[10px] text-muted-foreground uppercase tracking-widest mt-1">Copilot</p>
          </div>
        </div>
        {mounted && (
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 rounded-full hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
        )}
      </div>

      {/* Navigation / Upload Area */}
      <div className="flex-1 px-6 pb-6 flex flex-col gap-8 overflow-y-auto">
        <div>
          <h2 className="text-[10px] font-semibold text-muted-foreground uppercase tracking-widest mb-3">Knowledge Base</h2>
          
          <div className="relative group cursor-pointer mb-4">
            <input
              type="file"
              multiple
              onChange={handleFileUpload}
              disabled={uploading}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed z-10"
              accept=".pdf,.png,.jpg,.jpeg,.bmp,.tiff,.docx,.xlsx,.xls,.txt,.csv,.pptx"
            />
            <div className={`p-4 rounded-xl border border-dashed flex flex-col items-center justify-center gap-2 text-center transition-all duration-300 ${
              uploading ? "border-muted bg-muted/50" :
              uploadStatus === "success" ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400" :
              uploadStatus === "error" ? "border-rose-500/50 bg-rose-500/10 text-rose-600 dark:text-rose-400" :
              "border-border bg-muted/30 group-hover:border-[#F3B229]/50 group-hover:bg-[#F3B229]/5"
            }`}>
              {uploading ? (
                <div className="w-5 h-5 border-2 border-[#C00F2E] border-t-transparent rounded-full animate-spin" />
              ) : uploadStatus === "success" ? (
                <CheckCircle className="w-5 h-5" />
              ) : uploadStatus === "error" ? (
                <AlertCircle className="w-5 h-5" />
              ) : (
                <UploadCloud className="w-5 h-5 text-muted-foreground group-hover:text-[#F3B229] transition-colors" />
              )}
              
              <div className="text-xs">
                {uploading ? (
                  <span className="text-muted-foreground font-medium">Ingesting...</span>
                ) : uploadStatus === "success" ? (
                  <span className="font-medium">Upload Complete!</span>
                ) : uploadStatus === "error" ? (
                  <span className="font-medium">{errorMessage}</span>
                ) : (
                  <>
                    <span className="font-medium text-foreground">Click to upload</span>
                    <p className="text-[10px] text-muted-foreground mt-1">PDF, DOCX, Excel, Images</p>
                  </>
                )}
              </div>
            </div>
          </div>
          
          <form onSubmit={handleGithubIngest} className="flex flex-col gap-2">
            <div className="relative">
              <Globe className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <input 
                type="url" 
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="https://github.com/..." 
                className="w-full pl-9 pr-3 py-2 text-xs bg-muted/30 border border-border rounded-lg focus:outline-none focus:border-[#C00F2E] transition-colors"
                disabled={ingestingGithub}
              />
            </div>
            <button 
              type="submit" 
              disabled={ingestingGithub || !githubUrl.trim()}
              className="w-full py-2 bg-[#C00F2E] hover:bg-[#A00B24] text-white rounded-lg text-xs font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {ingestingGithub ? (
                <><Loader2 className="w-3.5 h-3.5 animate-spin" /> Indexing Repo...</>
              ) : (
                <> Index Repository</>
              )}
            </button>
          </form>
        </div>

        <div className="flex-1 flex flex-col min-h-0">
          <h2 className="text-[10px] font-semibold text-muted-foreground uppercase tracking-widest mb-3">Indexed Sources</h2>
          
          <div className="flex-1 overflow-y-auto pr-1 space-y-1">
            {loadingDocs || loadingRepos ? (
              <div className="flex justify-center items-center py-4">
                <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
              </div>
            ) : documents.length === 0 && githubRepos.length === 0 ? (
              <div className="text-xs text-muted-foreground text-center py-4">
                No sources indexed yet.
              </div>
            ) : (
              <AnimatePresence>
                {documents.map((doc, idx) => (
                  <motion.div 
                    key={doc.document_id}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.2, delay: idx * 0.05 }}
                    className="flex items-center justify-between p-2 rounded-lg hover:bg-muted group transition-colors"
                  >
                    <div className="flex items-center gap-2 overflow-hidden">
                      <FileText className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                      <span className="text-xs text-foreground truncate font-medium" title={doc.original_filename || doc.filename}>
                        {doc.original_filename || doc.filename}
                      </span>
                    </div>
                    <button 
                      onClick={() => handleDeleteDocument(doc.document_id)}
                      className="p-1.5 text-muted-foreground hover:text-rose-500 hover:bg-rose-500/10 rounded-md transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                      title="Remove document"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </motion.div>
                ))}
                {githubRepos.map((repo, idx) => (
                  <motion.div 
                    key={repo.document_id}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.2, delay: (documents.length + idx) * 0.05 }}
                    className="flex items-center justify-between p-2 rounded-lg hover:bg-muted group transition-colors"
                  >
                    <div className="flex items-center gap-2 overflow-hidden">
                      <Globe className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                      <span className="text-xs text-foreground truncate font-medium" title={repo.repository_name}>
                        {repo.repository_name}
                      </span>
                    </div>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 focus-within:opacity-100 transition-opacity">
                      <button 
                        onClick={() => handleSyncRepo(repo.document_id)}
                        disabled={syncingRepoId === repo.document_id}
                        className="p-1.5 text-muted-foreground hover:text-emerald-500 hover:bg-emerald-500/10 rounded-md transition-colors disabled:opacity-50"
                        title="Sync repository"
                      >
                        {syncingRepoId === repo.document_id ? (
                          <Loader2 className="w-3 h-3 animate-spin text-emerald-500" />
                        ) : (
                          <RefreshCw className="w-3 h-3" />
                        )}
                      </button>
                      <button 
                        onClick={() => handleDeleteRepo(repo.document_id)}
                        className="p-1.5 text-muted-foreground hover:text-rose-500 hover:bg-rose-500/10 rounded-md transition-colors"
                        title="Remove repository"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            )}
          </div>
        </div>
      </div>
      
      {/* Footer */}
      <div className="p-6 text-[10px] text-muted-foreground text-center shrink-0 uppercase tracking-widest font-medium">
        Internal Use Only
      </div>
    </div>
  );
}
