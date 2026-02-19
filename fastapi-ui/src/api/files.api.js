import api from "./axios";

export const getFiles = () => api.get("/files/", {
  headers: {
    "Cache-Control": "no-cache",
  },
});

export const uploadFile = (file, onProgress) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/files/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress: onProgress,
  });
};

export const deleteFile = (id) =>
  api.delete(`/files/${id}`);
