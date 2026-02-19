import { useEffect, useState } from "react";
import api from "../../api/axios";
import { getFiles, deleteFile } from "../../api/files.api";
import UploadFile from "./UploadFile";
import { toast } from "sonner";

export default function FilesList() {
  const [files, setFiles] = useState([]);
  const [uploadOpen, setUploadOpen] = useState(false);

  const [deleteOpen, setDeleteOpen] = useState(false);
  const [fileToDelete, setFileToDelete] = useState(null);

  const fetchFiles = async () => {
    const res = await getFiles();
    setFiles(res.data || []);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  /* ================= DOWNLOAD ================= */
  const handleDownload = async (file) => {
    try {
      const res = await api.get("/files/download", {
        params: { file_id: file.id },
        responseType: "blob",
      });

      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = file.original_filename || "download";
      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch {
      toast.error("Download failed");
    }
  };

  /* ================= DELETE ================= */

  const confirmDelete = (file) => {
    setFileToDelete(file);
    setDeleteOpen(true);
  };

  const handleDelete = async () => {
    if (!fileToDelete) return;

    try {
      await deleteFile(fileToDelete.id);
      setFiles((prev) =>
        prev.filter((f) => f.id !== fileToDelete.id)
      );
      toast.success("File deleted");
    } catch {
      toast.error("Delete failed");
    } finally {
      setDeleteOpen(false);
      setFileToDelete(null);
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes && bytes !== 0) return "—";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024)
      return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="space-y-4">
      {/* Top Bar */}
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">Files</h2>

        <button
          onClick={() => setUploadOpen(true)}
          className="
            bg-gradient-to-r from-blue-600 to-indigo-600
            text-white px-4 py-2 rounded-lg
            shadow hover:from-blue-700 hover:to-indigo-700
          "
        >
          + Upload File
        </button>
      </div>

      {/* Files List */}
      <ul className="bg-white rounded-xl shadow divide-y">
        {files.length === 0 && (
          <li className="p-4 text-center text-gray-500">
            No files uploaded
          </li>
        )}

        {files.map((f) => (
          <li
            key={f.id}
            className="p-4 flex justify-between items-center"
          >
            <div>
              <p className="font-medium">
                {f.original_filename}
              </p>

              <p className="text-xs text-gray-500">
                {formatFileSize(f.file_size)}
              </p>
            </div>

            <div className="flex gap-2">
              {/* Download Button */}
              <button
                onClick={() => handleDownload(f)}
                className="
                  px-3 py-1.5
                  text-sm font-medium
                  text-white
                  bg-green-600
                  rounded-md
                  hover:bg-green-700
                  transition
                "
              >
                Download
              </button>

              {/* Delete Button */}
              <button
                onClick={() => confirmDelete(f)}
                className="
                  px-3 py-1.5
                  text-sm font-medium
                  text-white
                  bg-red-600
                  rounded-md
                  hover:bg-red-700
                  transition
                "
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      {/* Upload Modal */}
      {uploadOpen && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-lg relative">
            <button
              onClick={() => setUploadOpen(false)}
              className="absolute top-3 right-3 text-gray-500 hover:text-black"
            >
              ✕
            </button>

            <h3 className="text-lg font-semibold mb-4">
              Upload File
            </h3>

            <UploadFile
              onSuccess={fetchFiles}
              onClose={() => setUploadOpen(false)}
            />
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteOpen && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-2">
              Delete File
            </h3>

            <p className="text-sm text-gray-600 mb-6">
              Are you sure you want to delete{" "}
              <span className="font-medium">
                {fileToDelete?.original_filename}
              </span>
              ?
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setDeleteOpen(false);
                  setFileToDelete(null);
                }}
                className="px-4 py-2 border rounded-md"
              >
                Cancel
              </button>

              <button
                onClick={handleDelete}
                className="
                  px-4 py-2
                  bg-red-600 text-white
                  rounded-md
                  hover:bg-red-700
                "
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
