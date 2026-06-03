// Updated to match the FastAPI prefix pattern (API_V1_STR)
const BASE_URL = 'http://localhost:8000/api/v1';

export const projectApi = {
  async getAll() {
    // 🔴 DYNAMIC HEADERS EXTRACTION
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    const response = await fetch(`${BASE_URL}/projects/`, { // 🔴 Target mapped to /projects/ resource prefix string cleanly
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
      }
    });
    if (!response.ok) throw new Error('Failed to fetch projects');
    return response.json();
  },

  async create(title, description = "") {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    // Backend expects Form data per your Python snippet
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);

    const response = await fetch(`${BASE_URL}/projects/`, { // 🔴 Route correctly targets project base
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
        // Note: Do not manually define Content-Type for FormData, browser sets it with boundary context automatically
      },
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to create project');
    return response.json();
  },

  async update(id, title, description) {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    const formData = new FormData();
    if (title) formData.append('title', title);
    if (description) formData.append('description', description);

    // 🔴 FIXED: Changed method to PATCH to perfectly map to the new @router.patch logic
    const response = await fetch(`${BASE_URL}/projects/${id}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
      },
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to update project');
    return response.json();
  },

  async delete(id) {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    const response = await fetch(`${BASE_URL}/projects/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
      }
    });
    if (!response.ok) throw new Error('Failed to delete project');
    return response.json(); // 🔴 Captures the 200 OK success message body string we created
  },

  async getOne(id) {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    const response = await fetch(`${BASE_URL}/projects/${id}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
      }
    });
    return response.json();
  },

  // ---------------------------------------------------------
  // AI SERVICES CONNECTIONS
  // ---------------------------------------------------------

  async generateAIObjectives(projectId, contentSource, contentText) {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    const formData = new FormData();
    formData.append('project_id', projectId);
    formData.append('content_source', contentSource); // e.g., "raw_text"
    formData.append('content', contentText); // e.g., "Learn how to build a REST API using FastAPI."

    const response = await fetch(`${BASE_URL}/ai/objectives/generate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
      },
      body: formData,
    });
    if (!response.ok) throw new Error('AI Objectives generation failed');
    return response.json();
  },

  async generateAIInteractivity(projectId, contentSource, contentText) {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("organization_id");

    const formData = new FormData();
    formData.append('project_id', projectId);
    formData.append('content_source', contentSource);
    formData.append('content', contentText);

    const response = await fetch(`${BASE_URL}/ai/interactivity-suggestions/generate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Organization-ID': orgId
      },
      body: formData,
    });
    if (!response.ok) throw new Error('AI Interactivity suggestions failed');
    return response.json();
  }
};