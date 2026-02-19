import { useState, useEffect, useRef } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import api from "../../api/axios";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  const passwordRef = useRef(null);

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [expired, setExpired] = useState(false);

  /* ================= AUTO FOCUS ================= */
  useEffect(() => {
    passwordRef.current?.focus();
  }, []);

  /* ================= PASSWORD STRENGTH ================= */

  const calculateStrength = (password) => {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    return score;
  };

  const strength = calculateStrength(newPassword);

  const strengthLabel = ["Weak", "Fair", "Good", "Strong"];
  const strengthColor = [
    "bg-red-500",
    "bg-orange-400",
    "bg-yellow-400",
    "bg-green-500",
  ];

  /* ================= SUBMIT ================= */

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!token) {
      setExpired(true);
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await api.post("/auth/reset-password", {
        token,
        new_password: newPassword,
      });

      setSuccess(true);

      setTimeout(() => {
        navigate("/login");
      }, 2500);
    } catch (err) {
      setExpired(true);
    } finally {
      setLoading(false);
    }
  };

  /* ================= EXPIRED SCREEN ================= */

  if (expired) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-xl shadow w-96 text-center space-y-4">
          <h2 className="text-xl font-bold text-red-600">
            Reset Link Expired 🔒
          </h2>
          <p className="text-sm text-gray-600">
            Your reset link is invalid or expired.
          </p>
          <button
            onClick={() => navigate("/login")}
            className="w-full bg-black text-white py-2 rounded"
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  /* ================= SUCCESS ANIMATION ================= */

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-xl shadow w-96 text-center space-y-4 animate-fade-in">
          <div className="text-5xl animate-bounce">✅</div>
          <h2 className="text-xl font-bold text-green-600">
            Password Updated!
          </h2>
          <p className="text-sm text-gray-600">
            Redirecting to login...
          </p>
        </div>
      </div>
    );
  }

  /* ================= MAIN UI ================= */

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow w-96 space-y-5"
      >
        {/* Logo */}
        <div className="flex flex-col items-center gap-2">
          <img
            src="https://assets.streamlinehq.com/image/private/w_300,h_300,ar_1/f_auto/v1/icons/logos/fastapi-91dvq8q5ewijkczjmd9bcb.png/fastapi-ggmxtn5w3qqwks1i5jnx2p.png?_a=DATAiZAAZAA0"
            alt="Logo"
            className="w-10 h-10"
          />
          <h1 className="text-2xl font-bold">
            Reset Password
          </h1>
        </div>

        {/* Password */}
        <div className="relative">
          <input
            ref={passwordRef}
            type={showPassword ? "text" : "password"}
            placeholder="New Password"
            value={newPassword}
            onChange={(e) =>
              setNewPassword(e.target.value)
            }
            className="w-full border p-2 rounded pr-10"
          />

          <button
            type="button"
            onClick={() =>
              setShowPassword((prev) => !prev)
            }
            className="absolute right-2 top-2"
          >
            <EyeIcon open={showPassword} />
          </button>
        </div>

        {/* Strength Meter */}
        {newPassword && (
          <div className="space-y-1">
            <div className="w-full h-2 bg-gray-200 rounded overflow-hidden">
              <div
                className={`h-2 transition-all duration-300 ${
                  strengthColor[strength - 1] ||
                  "bg-gray-300"
                }`}
                style={{
                  width: `${(strength / 4) * 100}%`,
                }}
              />
            </div>
            <p className="text-xs text-gray-600">
              Strength:{" "}
              {strengthLabel[strength - 1] || "Too weak"}
            </p>
          </div>
        )}

        {/* Confirm Password */}
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) =>
            setConfirmPassword(e.target.value)
          }
          className="w-full border p-2 rounded"
        />

        {/* Error */}
        {error && (
          <p className="text-sm text-red-600">
            {error}
          </p>
        )}

        {/* Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-black text-white py-2 rounded hover:bg-gray-900 transition flex justify-center disabled:opacity-50"
        >
          {loading ? (
            <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
          ) : (
            "Reset Password"
          )}
        </button>
      </form>
    </div>
  );
}

/* ================= SVG EYE ICON ================= */

function EyeIcon({ open }) {
  return open ? (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-5 w-5 text-gray-500"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path d="M17.94 17.94A10.94 10.94 0 0112 19C7 19 2.73 15.11 1 12c.73-1.32 1.73-2.5 2.94-3.44M9.88 9.88a3 3 0 104.24 4.24" />
      <path d="M1 1l22 22" />
    </svg>
  ) : (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-5 w-5 text-gray-500"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path d="M1 12C2.73 8.89 7 5 12 5s9.27 3.89 11 7c-1.73 3.11-6 7-11 7S2.73 15.11 1 12z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}
