import { useRef, useState } from "react";
import { uploadFile } from "../../api/files.api";
import { toast } from "sonner";

/* ================= CONFIG ================= */

const MAX_FILE_SIZE_MB = 10;
const ALLOWED_TYPES = [
  "image/png",
  "image/jpeg",
  "application/pdf",
];

export default function UploadFile({ onSuccess, onClose }) {
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [dragOver, setDragOver] = useState(false);

  /* ================= VALIDATION ================= */

  const validateFile = (file) => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      toast.error("Invalid file type (PNG, JPG, PDF only)");
      return false;
    }

    if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      toast.error(`File size must be under ${MAX_FILE_SIZE_MB}MB`);
      return false;
    }

    return true;
  };

  /* ================= FILE SELECT ================= */

  const handleFileSelect = (file) => {
    if (!file) return;
    if (!validateFile(file)) return;

    setFile(file);
    setProgress(0);
  };

  const handleInputChange = (e) => {
    handleFileSelect(e.target.files[0]);
    e.target.value = "";
  };

  /* ================= DRAG & DROP ================= */

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFileSelect(e.dataTransfer.files[0]);
  };

  /* ================= UPLOAD ================= */

  const startUpload = async () => {
    if (!file || uploading) return;

    setUploading(true);

    try {
      await uploadFile(file, (event) => {
        const percent = Math.round(
          (event.loaded * 100) / event.total
        );
        setProgress(percent);
      });

      toast.success("File uploaded successfully 📁");

      setFile(null);
      setProgress(0);

      onSuccess?.(); // refresh files list
      onClose?.();   // close modal
    } catch (err) {
      console.error(err);
      toast.error("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  /* ================= UI ================= */

  return (
    <div className="space-y-4">
      {/* Drag & Drop Area */}
      <div
        onClick={() => fileInputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-xl p-6
          cursor-pointer text-center
          transition
          ${
            dragOver
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-blue-400"
          }
        `}
      >
        <UploadIcon />

        <p className="mt-2 text-sm text-gray-600">
          Drag & drop a file here, or click to browse
        </p>

        <p className="text-xs text-gray-400 mt-1">
          PNG, JPG, PDF up to {MAX_FILE_SIZE_MB}MB
        </p>

        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={handleInputChange}
        />
      </div>

      {/* File Preview */}
      {file && (
        <div className="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
          <div>
            <p className="text-sm font-medium">{file.name}</p>
            <p className="text-xs text-gray-500">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>

          <button
            onClick={() => setFile(null)}
            className="text-sm text-red-600 hover:underline"
          >
            Remove
          </button>
        </div>
      )}

      {/* Progress Bar */}
      {uploading && (
        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className="bg-blue-600 h-2 transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={startUpload}
        disabled={!file || uploading}
        className="
          w-full
          bg-gradient-to-r from-blue-600 to-indigo-600
          text-white font-medium
          py-2.5 rounded-lg
          shadow
          hover:from-blue-700 hover:to-indigo-700
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-all
        "
      >
        {uploading ? "Uploading…" : "Upload File"}
      </button>
    </div>
  );
}

/* ================= SVG ICON ================= */

function UploadIcon() {
  return (
    <svg
      className="mx-auto h-10 w-10 text-blue-500"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M7 16V12M7 12l-2 2m2-2l2 2m6-6V4m0 0l-2 2m2-2l2 2M3 20h18"
      />
    </svg>
  );
}
