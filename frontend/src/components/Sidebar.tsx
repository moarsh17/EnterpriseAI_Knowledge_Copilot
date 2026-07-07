"use client";

import React, { useState, useEffect } from "react";
import { api } from "@/services/api";
import { UploadCloud, CheckCircle, AlertCircle, FileText, BookOpen, Trash2, Loader2 } from "lucide-react";

export default function Sidebar() {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  
  const [documents, setDocuments] = useState<any[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(true);

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

  useEffect(() => {
    fetchDocuments();
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

  const handleDeleteDocument = async (documentId: string) => {
    try {
      await api.deleteDocument(documentId);
      fetchDocuments();
    } catch (error) {
      console.error("Failed to delete document:", error);
    }
  };

  return (
    <div className="w-72 h-full flex flex-col bg-white border-r border-slate-200 dark:bg-slate-900 dark:border-slate-800 shadow-sm z-10 transition-colors duration-300">
      {/* Brand Header */}
      <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 shrink-0">
        <div className="w-10 h-10 rounded bg-[#C00F2E] flex items-center justify-center shadow-md shrink-0">
          <BookOpen className="text-[#F3B229] w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-slate-900 dark:text-white leading-tight">ONGC</h1>
          <p className="text-xs text-slate-500 font-medium">Knowledge Copilot</p>
        </div>
      </div>

      {/* Navigation / Upload Area */}
      <div className="flex-1 p-4 flex flex-col gap-6 overflow-y-auto">
        <div>
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Knowledge Base</h2>
          
          <div className="relative group cursor-pointer">
            <input
              type="file"
              multiple
              onChange={handleFileUpload}
              disabled={uploading}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed z-10"
              accept=".pdf,.png,.jpg,.jpeg,.bmp,.tiff,.docx,.xlsx,.xls,.txt,.csv,.pptx"
            />
            <div className={`p-4 rounded-xl border-2 border-dashed flex flex-col items-center justify-center gap-2 text-center transition-all duration-300 ${
              uploading ? "border-slate-300 bg-slate-50 dark:border-slate-700 dark:bg-slate-800" :
              uploadStatus === "success" ? "border-emerald-400 bg-emerald-50 dark:bg-emerald-900/20" :
              uploadStatus === "error" ? "border-rose-400 bg-rose-50 dark:bg-rose-900/20" :
              "border-slate-200 bg-slate-50 group-hover:border-[#F3B229] group-hover:bg-[#F3B229]/5 dark:border-slate-800 dark:bg-slate-900"
            }`}>
              {uploading ? (
                <div className="w-6 h-6 border-2 border-[#C00F2E] border-t-transparent rounded-full animate-spin" />
              ) : uploadStatus === "success" ? (
                <CheckCircle className="w-6 h-6 text-emerald-500" />
              ) : uploadStatus === "error" ? (
                <AlertCircle className="w-6 h-6 text-rose-500" />
              ) : (
                <UploadCloud className="w-6 h-6 text-slate-400 group-hover:text-[#F3B229] transition-colors" />
              )}
              
              <div className="text-sm">
                {uploading ? (
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Ingesting...</span>
                ) : uploadStatus === "success" ? (
                  <span className="text-emerald-600 font-medium">Upload Complete!</span>
                ) : uploadStatus === "error" ? (
                  <span className="text-rose-600 font-medium text-xs">{errorMessage}</span>
                ) : (
                  <>
                    <span className="font-semibold text-slate-700 dark:text-slate-300">Click to upload</span>
                    <p className="text-xs text-slate-400 mt-1">PDF, DOCX, Excel, Images</p>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="flex-1 flex flex-col min-h-0">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Uploaded Documents</h2>
          
          <div className="flex-1 overflow-y-auto pr-1 space-y-2">
            {loadingDocs ? (
              <div className="flex justify-center items-center py-4">
                <Loader2 className="w-5 h-5 animate-spin text-slate-400" />
              </div>
            ) : documents.length === 0 ? (
              <div className="text-sm text-slate-500 text-center py-4">
                No documents uploaded yet.
              </div>
            ) : (
              documents.map((doc, idx) => (
                <div key={idx} className="flex items-center justify-between p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 group">
                  <div className="flex items-center gap-2 overflow-hidden">
                    <FileText className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="text-sm text-slate-700 dark:text-slate-300 truncate" title={doc.filename}>
                      {doc.filename}
                    </span>
                  </div>
                  <button 
                    onClick={() => handleDeleteDocument(doc.document_id)}
                    className="p-1.5 text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/30 rounded-md transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                    title="Remove document"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
      
      {/* Footer */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 text-center shrink-0">
        Powered by AI &bull; Internal Use Only
      </div>
    </div>
  );
}
