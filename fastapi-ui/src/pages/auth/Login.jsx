import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";
import { login, forgotPassword } from "../../api/auth.api";
import logo from "../../assets/logo.png";


export default function Login() {
  const { register, handleSubmit, setValue } = useForm();

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [capsLock, setCapsLock] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  /* ================= REMEMBER ME ================= */

  useEffect(() => {
    const savedEmail = localStorage.getItem("remember_email");
    if (savedEmail) {
      setValue("username", savedEmail);
      setRememberMe(true);
    }
  }, [setValue]);

  /* ================= SUBMIT ================= */

  const onSubmit = async (data) => {
    setError("");
    setLoading(true);

    try {
      await login(data);

      if (rememberMe) {
        localStorage.setItem("remember_email", data.username);
      } else {
        localStorage.removeItem("remember_email");
      }

      window.location.href = "/";
    } catch {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  /* ================= FORGOT PASSWORD ================= */

  const handleForgotPassword = async () => {
    const email = document.querySelector(
      'input[name="username"]'
    )?.value;

    if (!email) {
      setError("Enter your email to reset password");
      return;
    }

    try {
      console.log(JSON.stringify({ email }));

      await forgotPassword({ email });
      setError("Password reset link sent to your email");
    } catch {
      setError("Failed to send reset link");
    }
  };

  /* ================= UI ================= */

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-xl shadow w-96 space-y-5"
      >
        {/* Logo */}
        <div className="flex flex-col items-center gap-2">
          <img
            src={logo}
            alt="FastAPI Logo"
            className="w-10 h-10"
          />
          <h1 className="text-2xl font-bold">
            StarterTemplate
          </h1>
        </div>

        {/* Email */}
        <input
          {...register("username", { required: true })}
          placeholder="Email"
          className="w-full border p-2 rounded"
          disabled={loading}
        />

        {/* Password */}
        <div className="relative">
          <input
            {...register("password", { required: true })}
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            className="w-full border p-2 rounded pr-10"
            disabled={loading}
            onKeyUp={(e) =>
              setCapsLock(e.getModifierState("CapsLock"))
            }
          />

          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-black"
            tabIndex={-1}
          >
            {showPassword ? <EyeOffIcon /> : <EyeIcon />}
          </button>
        </div>

        {/* Caps Lock Warning */}
        {capsLock && (
          <p className="text-xs text-orange-600">
            ⚠ Caps Lock is ON
          </p>
        )}

        {/* Remember Me */}
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) =>
              setRememberMe(e.target.checked)
            }
          />
          Remember me
        </label>

        {/* Error */}
        {error && (
          <p
            className={`text-sm ${
              error.includes("sent")
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            {error}
          </p>
        )}

        {/* Login Button */}
        <button
          type="submit"
          disabled={loading}
          className="
            w-full bg-black text-white py-2 rounded
            hover:bg-gray-900 transition
            flex items-center justify-center
            disabled:opacity-50
          "
        >
          {loading ? (
            <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
          ) : (
            "Login"
          )}
        </button>

        {/* Forgot Password */}
        <button
          type="button"
          onClick={handleForgotPassword}
          className="w-full text-sm text-blue-600 hover:underline"
        >
          Forgot password?
        </button>
      </form>
    </div>
  );
}

/* ================= ICONS ================= */

function EyeIcon() {
  return (
    <svg
      className="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
      />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg
      className="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M3 3l18 18M10.584 10.587A3 3 0 0012 15a3 3 0 002.413-4.413M9.88 9.88A3 3 0 0112 9a3 3 0 013 3"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M2.458 12C3.732 7.943 7.523 5 12 5c1.635 0 3.18.393 4.543 1.093M21.542 12c-.458 1.457-1.275 2.768-2.343 3.82"
      />
    </svg>
  );
}
