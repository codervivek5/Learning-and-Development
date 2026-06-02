// Updated to match the FastAPI prefix pattern (API_V1_STR)
const BASE_URL = 'http://localhost:8000/api/v1/projects'; 

export const projectApi = {
  async getAll() {
    const response = await fetch(`${BASE_URL}/`);
    if (!response.ok) throw new Error('Failed to fetch projects');
    return response.json();
  },

  async create(title, description = "") {
    // Backend expects Form data per your Python snippet
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);

    const response = await fetch(`${BASE_URL}/`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to create project');
    return response.json();
  },

  async update(id, title, description) {
    const formData = new FormData();
    if (title) formData.append('title', title);
    if (description) formData.append('description', description);

    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to update project');
    return response.json();
  },

  async delete(id) {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete project');
    return true;
  },

  async getOne(id) {
    const response = await fetch(`${BASE_URL}/${id}`);
    return response.json();
  }
};