import { useEffect, useState, useRef } from "react";
import {
  getUsers,
  searchUsers,
  createUser,
  updateUser,
  deleteUser,
  getMe,
} from "../../api/users.api";
import { toast } from "sonner";

const PAGE_SIZE = 10;
const SEARCH_DELAY = 400;

export default function UsersList() {
  /* ================= STATE ================= */

  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);

  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [loading, setLoading] = useState(false);

  /* Modals */
  const [modalOpen, setModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  const [deleteOpen, setDeleteOpen] = useState(false);
  const [userToDelete, setUserToDelete] = useState(null);

  /* Form */
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [isActive, setIsActive] = useState(true);

  const firstRender = useRef(true);

  /* ================= FETCH ================= */

  const fetchUsers = async (overridePage) => {
  setLoading(true);

  try {
    let res;
    const currentPage = overridePage ?? page;
    if (search.trim()) {
      // 🔍 Search API (no page-based pagination)
      res = await searchUsers({
        skip: (currentPage - 1) * PAGE_SIZE,
        q: search.trim(),
        limit: PAGE_SIZE,
      });
    } else {
      // ✅ Correct backend pagination
      const currentPage = overridePage ?? page;

      res = await getUsers({
        skip: (currentPage - 1) * PAGE_SIZE,
        limit: PAGE_SIZE,
      });
    }

    const data = res.data || [];

    setUsers(data);
    setHasNextPage(data.length === PAGE_SIZE);
  } catch {
    toast.error("Failed to fetch users");
  } finally {
    setLoading(false);
  }
};


  /* ================= PAGE CHANGE ================= */

  useEffect(() => {
    fetchUsers();

    getMe()
      .then((r) => setCurrentUser(r.data))
      .catch(() => setCurrentUser(null));
  }, [page]);

  /* ================= SEARCH (AUTO LIKE ITEMS) ================= */

  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }

    const timer = setTimeout(() => {
      setPage(1);
      fetchUsers(1); // force refresh
    }, SEARCH_DELAY);

    return () => clearTimeout(timer);
  }, [search]);

  /* ================= MANUAL SEARCH ================= */

  const handleManualSearch = () => {
    setPage(1);
    fetchUsers(1);
  };

  /* ================= CREATE / EDIT ================= */

  const openCreate = () => {
    setEditingUser(null);
    setEmail("");
    setFullName("");
    setPassword("");
    setRole("user");
    setIsActive(true);
    setModalOpen(true);
  };

  const openEdit = (u) => {
    setEditingUser(u);
    setEmail(u.email);
    setFullName(u.full_name || "");
    setPassword("");
    setRole(u.role);
    setIsActive(u.is_active);
    setModalOpen(true);
  };

  const handleSave = async () => {
    if (!email || !fullName) {
      toast.error("Email and Full Name are required");
      return;
    }

    try {
      if (editingUser) {
        await updateUser(editingUser.id, {
          email,
          full_name: fullName,
          role,
          is_active: isActive,
          ...(password ? { password } : {}),
        });
        toast.success("User updated");
      } else {
        await createUser({
          email,
          full_name: fullName,
          password,
          role,
          is_active: isActive,
        });
        toast.success("User created");
      }

      setModalOpen(false);
      setPage(1);
      fetchUsers(1);
    } catch {
      toast.error("Operation failed");
    }
  };

  /* ================= DELETE ================= */

  const handleDelete = async () => {
    try {
      await deleteUser(userToDelete.id);
      toast.success("User deleted");
      setUsers((prev) =>
        prev.filter((u) => u.id !== userToDelete.id)
      );
    } catch {
      toast.error("Delete failed");
    } finally {
      setDeleteOpen(false);
      setUserToDelete(null);
    }
  };
const getPasswordStrength = (password) => {
  if (!password) return { label: "", score: 0 };

  let score = 0;

  if (password.length >= 6) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  if (score <= 1) return { label: "Weak", score: 1 };
  if (score === 2 || score === 3)
    return { label: "Medium", score: 2 };
  return { label: "Strong", score: 3 };
};

  /* ================= UI ================= */

  return (
    <div className="space-y-4">
      {/* ===== Top Bar ===== */}
      <div className="flex justify-between items-center">
        <div className="flex gap-2">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by name or email..."
            className="border px-3 py-2 rounded w-72"
          />

          <button
            disabled={loading}
            onClick={handleManualSearch}
            className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
          >
            Search
          </button>
        </div>

        <button
          onClick={openCreate}
          disabled={currentUser?.role === "user"}
          className={`px-4 py-2 rounded-lg text-white ${
            currentUser?.role === "user"
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-green-600 hover:bg-green-700"
          }`}
        >
          + Create User
        </button>
      </div>

      {/* ===== Table ===== */}
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="p-3 text-left">Full Name</th>
              <th className="p-3 text-left">Email</th>
              <th className="p-3 text-center">Role</th>
              <th className="p-3 text-center">Active</th>
              <th className="p-3 text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            {loading && (
              <tr>
                <td colSpan="5" className="p-4 text-center">
                  Loading…
                </td>
              </tr>
            )}

            {!loading && users.length === 0 && (
              <tr>
                <td colSpan="5" className="p-4 text-center">
                  No users found
                </td>
              </tr>
            )}

            {!loading &&
              users.map((u) => {
                const isSelf = currentUser?.id === u.id;

                return (
                  <tr key={u.id} className="border-b">
                    <td className="p-3">{u.full_name || "—"}</td>
                    <td className="p-3">{u.email}</td>
                    <td className="p-3 text-center">{u.role}</td>
                    <td className="p-3 text-center">
                      {u.is_active ? "✅" : "❌"}
                    </td>
                    <td className="p-3 text-center space-x-2">
                      <button
                        onClick={() => openEdit(u)}
                        className="px-3 py-1 bg-blue-600 text-white rounded"
                      >
                        Edit
                      </button>

                      <button
                        disabled={isSelf}
                        onClick={() => {
                          setUserToDelete(u);
                          setDeleteOpen(true);
                        }}
                        className={`px-3 py-1 rounded text-white ${
                          isSelf
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-red-600 hover:bg-red-700"
                        }`}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              })}
          </tbody>
        </table>
      </div>

      {/* ===== Pagination ===== */}
      {(page > 1 || hasNextPage) && (
        <div className="flex gap-2 items-center">
          <button
            disabled={page === 1}
            onClick={() => setPage((p) => p - 1)}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Prev
          </button>

          <span className="px-4 py-2">Page {page}</span>

          <button
            disabled={!hasNextPage}
            onClick={() => setPage((p) => p + 1)}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}

      {/* ===== Delete Modal ===== */}
      {deleteOpen && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">
              Delete User
            </h3>

            <p className="mb-6">
              Are you sure you want to delete{" "}
              <b>{userToDelete?.full_name}</b>?
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setDeleteOpen(false)}
                className="px-4 py-2 border rounded"
              >
                Cancel
              </button>

              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Create / Edit modal stays the same as before */}
      {modalOpen && (
  <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
    <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
      <h3 className="text-lg font-semibold mb-4">
        {editingUser ? "Edit User" : "Create User"}
      </h3>

      <div className="space-y-3">
        {/* Full Name */}
        <input
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Full Name"
          className="w-full border px-3 py-2 rounded"
        />

        {/* Email */}
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="w-full border px-3 py-2 rounded"
        />

        {/* Password (Create only) */}
        {!editingUser && (
          <div className="space-y-1">
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="Password"
              className="w-full border px-3 py-2 rounded"
            />

            {/* 🔐 Strength Meter */}
            {password && (
              <>
                {(() => {
                  const { label, score } =
                    getPasswordStrength(password);

                  const colors = [
                    "bg-red-500",
                    "bg-yellow-500",
                    "bg-green-500",
                  ];

                  return (
                    <div>
                      <div className="w-full h-2 bg-gray-200 rounded overflow-hidden">
                        <div
                          className={`h-2 transition-all ${
                            colors[score - 1]
                          }`}
                          style={{
                            width: `${(score / 3) * 100}%`,
                          }}
                        />
                      </div>

                      <p
                        className={`text-xs mt-1 ${
                          score === 1
                            ? "text-red-600"
                            : score === 2
                            ? "text-yellow-600"
                            : "text-green-600"
                        }`}
                      >
                        Password strength: {label}
                      </p>
                    </div>
                  );
                })()}
              </>
            )}
          </div>
        )}

        {/* Role */}
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>

        {/* Active */}
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={isActive}
            onChange={(e) => setIsActive(e.target.checked)}
          />
          Active
        </label>
      </div>

      {/* Actions */}
      <div className="flex justify-end gap-2 mt-6">
        <button
          onClick={() => setModalOpen(false)}
          className="px-4 py-2 border rounded"
        >
          Cancel
        </button>

        <button
          onClick={handleSave}
          className="px-4 py-2 bg-black text-white rounded hover:bg-gray-900"
        >
          {editingUser ? "Update" : "Create"}
        </button>
      </div>
    </div>
  </div>
)}


    </div>
  );
}
