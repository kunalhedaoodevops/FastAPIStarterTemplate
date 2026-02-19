import api from "../../api/axios";
import { useEffect, useState } from "react";

export default function Health() {
  const [status, setStatus] = useState("checking"); // checking | healthy | unhealthy
  const [message, setMessage] = useState("");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await api.get("/health/");
        setStatus("healthy");
        setMessage("All systems operational");
      } catch (error) {
        const msg =
          error.response?.data?.detail ||
          error.response?.statusText ||
          error.message ||
          "Unknown error";

        setStatus("unhealthy");
        setMessage(msg);
      }
    };

    checkHealth();
  }, []);

  const statusStyles = {
    checking:
      "bg-gray-50 border-gray-300 text-gray-700",
    healthy:
      "bg-green-50 border-green-400 text-green-700",
    unhealthy:
      "bg-red-50 border-red-400 text-red-700",
  };

  const statusIcon = {
    checking: "⏳",
    healthy: "✅",
    unhealthy: "❌",
  };

  const statusText = {
    checking: "Checking API health…",
    healthy: "API is Healthy",
    unhealthy: "API is Unhealthy",
  };

  return (
    <div className="flex justify-center">
      <div
        className={`
          w-full max-w-lg
          border-l-4 rounded-xl shadow
          p-6 transition-all duration-500
          ${statusStyles[status]}
        `}
      >
        {/* Header */}
        <div className="flex items-center gap-3">
          <span
            className={`
              text-2xl
              ${status === "checking" ? "animate-spin" : ""}
            `}
          >
            {statusIcon[status]}
          </span>

          <h2 className="text-xl font-bold">
            API Health Status
          </h2>
        </div>

        {/* Status Text */}
        <p
          className={`
            mt-4 text-lg font-medium
            transition-opacity duration-500
            ${status === "checking" ? "animate-pulse" : ""}
          `}
        >
          {statusText[status]}
        </p>

        {/* Extra Message */}
        {status !== "checking" && (
          <p className="mt-2 text-sm opacity-80">
            {message}
          </p>
        )}

        {/* Footer */}
        <div className="mt-6 text-xs text-gray-500">
          Last checked just now
        </div>
      </div>
    </div>
  );
}
