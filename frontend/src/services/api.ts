const BASE_URL = "http://127.0.0.1:8000/api/v1";

export interface Source {
  filename: string;
  page: number;
  chunk_index: number;
}

export interface ChatResponse {
  question: string;
  answer: string;
  sources: Source[];
}

export const api = {
  uploadFiles: async (files: File[]): Promise<any> => {
    const formData = new FormData();
    files.forEach(file => formData.append("files", file));

    const res = await fetch(`${BASE_URL}/upload/`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Upload failed");
    }

    return res.json();
  },

  chat: async (
    question: string,
    filters?: { domain?: string; department?: string; document_type?: string }
  ): Promise<ChatResponse> => {
    const params = new URLSearchParams();
    params.append("question", question);

    if (filters?.domain) params.append("domain", filters.domain);
    if (filters?.department) params.append("department", filters.department);
    if (filters?.document_type) params.append("document_type", filters.document_type);

    const res = await fetch(`${BASE_URL}/chat/?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Chat failed");
    }

    return res.json();
  },

  getDocuments: async (): Promise<any> => {
    const res = await fetch(`${BASE_URL}/documents/`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to fetch documents");
    }
    return res.json();
  },

  deleteDocument: async (documentId: string): Promise<any> => {
    const res = await fetch(`${BASE_URL}/documents/${documentId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to delete document");
    }
    return res.json();
  },
};
