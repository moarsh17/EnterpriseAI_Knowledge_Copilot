const BASE_URL = "http://127.0.0.1:8000/api/v1";

export interface Source {
  filename: string;
  page: number;
  chunk_index: number;
  text?: string;
  original_filename?: string;
  source_type?: string;
  repository_name?: string;
  file_path?: string;
  repository_url?: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
  sources: Source[];
}

export const api = {
  uploadFiles: async (files: File[]): Promise<any[]> => {
    const results = [];
    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${BASE_URL}/upload/`, {
        method: "POST",
        body: formData,
      });

      const json = await res.json().catch(() => ({}));
      results.push(json);
    }
    return results;
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

  ingestGithub: async (repoUrl: string): Promise<any> => {
    const res = await fetch(`${BASE_URL}/github/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repo_url: repoUrl }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to ingest repository");
    }
    return res.json();
  },

  getGithubRepos: async (): Promise<any> => {
    const res = await fetch(`${BASE_URL}/github/`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to fetch repositories");
    }
    return res.json();
  },

  deleteGithubRepo: async (repoId: string): Promise<any> => {
    const res = await fetch(`${BASE_URL}/github/${repoId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to delete repository");
    }
    return res.json();
  },
};
