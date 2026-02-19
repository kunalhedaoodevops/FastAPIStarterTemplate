import { useEffect, useState, useRef } from "react";
import {
  getItems,
  deleteItem,
  createItem,
  updateItem,
  searchItems,
} from "../../api/items.api";
import { getMe } from "../../api/users.api";
import ItemModal from "./ItemModal";
// import {getUsers, searchUsers} from "../../api/users.api.js";
import {toast} from "sonner";

const PAGE_SIZE = 10;
const SEARCH_DELAY = 400; // ms

export default function ItemsList() {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasNextPage, setHasNextPage] = useState(false);

  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);

  // 🔥 delete confirmation state
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState(null);

  const firstRender = useRef(true);

  /* ================= FETCH ================= */

//   const fetchItems = async (overridePage) => {
//     setLoading(true);
//     try {
//       const res = await getItems({
//         page: overridePage ?? page,
//         size: PAGE_SIZE,
//         search: search.trim() || undefined,
//         _t: Date.now(),
//       });

//       const data = res.data || [];
//       setItems(data);
//       setHasNextPage(data.length === PAGE_SIZE);
//     } catch (err) {
//       console.error("Failed to fetch items", err);
//     } finally {
//       setLoading(false);
//     }
//   };
const fetchItems = async (overridePage) => {
  setLoading(true);

  try {
    const currentPage = overridePage ?? page;
    // 🔐 get current user once
const meRes = await getMe();
const me = meRes.data;

const baseParams = {
  skip: (currentPage - 1) * PAGE_SIZE,
  limit: PAGE_SIZE,
};

// 👇 only attach owner_id if NOT admin
if (me.role !== "admin") {
  baseParams.owner_id = me.id;
}

let res;

    if (search.trim()) {
      // 🔍 Search API (no page-based pagination)
      res = await searchItems({
        ...baseParams,
        q: search.trim()
      });
    } else {
      // ✅ Correct backend pagination
      res = await getItems({
        ...baseParams
      });
    }

    const data = res.data || [];

    setItems(data);
    setHasNextPage(data.length === PAGE_SIZE);
  } catch (err) {
    toast.error("Failed to fetch items");
  } finally {
    setLoading(false);
  }
};
  /* ================= AUTO SEARCH ================= */

  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }

    const timer = setTimeout(() => {
      setPage(1);
      fetchItems(1); // force refresh
    }, SEARCH_DELAY);

    return () => clearTimeout(timer);
  }, [search]);
  /* ================= MANUAL SEARCH ================= */

  const handleManualSearch = () => {
    setPage(1);
    fetchItems(1);
  };
  /* ================= PAGE CHANGE ================= */

  useEffect(() => {
    fetchItems();
  }, [page]);

  /* ================= CREATE ================= */

  const handleCreate = async (data) => {
    try {
      await createItem(data);
      setModalOpen(false);
      setPage(1);
      fetchItems(1);
    } catch {
      alert("Create failed");
    }
  };

  /* ================= EDIT ================= */

  const handleEdit = async (data) => {
    const id = editingItem.id;

    setItems((prev) =>
      prev.map((i) =>
        i.id === id ? { ...i, ...data } : i
      )
    );

    try {
      await updateItem(id, data);
      setModalOpen(false);
      setEditingItem(null);
    } catch {
      alert("Update failed");
      fetchItems();
    }
  };

  /* ================= DELETE ================= */

  const openDeleteConfirm = (item) => {
    setItemToDelete(item);
    setDeleteOpen(true);
  };

  const handleDelete = async () => {
    if (!itemToDelete) return;

    const backup = items;
    setItems((prev) =>
      prev.filter((i) => i.id !== itemToDelete.id)
    );

    try {
      await deleteItem(itemToDelete.id);
    } catch {
      alert("Delete failed, restoring item");
      setItems(backup);
    } finally {
      setDeleteOpen(false);
      setItemToDelete(null);
    }
  };

  /* ================= UI ================= */

  return (
    <div className="space-y-4">
      {/* Top Bar */}
      <div className="flex justify-between items-center">
        <div className="flex gap-2">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search items..."
            className="border px-3 py-2 rounded w-64"
          />

          <button
            disabled={loading}
            onClick={() => {
              setPage(1);
              fetchItems(1);
            }}
            className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
          >
            Search
          </button>
        </div>

        <button
          onClick={() => {
            setEditingItem(null);
            setModalOpen(true);
          }}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Create Item
        </button>
      </div>

      {/* Table */}
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="p-3 text-left">Title</th>
              <th className="p-3 text-left">Description</th>
              <th className="p-3 text-center">Price</th>
              <th className="p-3 text-center">Owner</th>
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

            {!loading && items.length === 0 && (
              <tr>
                <td colSpan="5" className="p-4 text-center">
                  No items found
                </td>
              </tr>
            )}

            {!loading &&
              items.map((item) => (
                <tr key={item.id} className="border-b">
                  <td className="p-3 font-medium">
                    {item.title}
                  </td>

                  <td className="p-3 max-w-xs">
                    <span
                      title={item.description}
                      className="block truncate text-gray-600 cursor-help"
                    >
                      {item.description || "—"}
                    </span>
                  </td>

                  <td className="p-3 text-center">
                    ₹ {item.price}
                  </td>

                  <td className="p-3 text-center">
                    {item.owner_id}
                  </td>

                  <td className="p-3 text-center space-x-2">
                    <button
                      onClick={() => {
                        setEditingItem(item);
                        setModalOpen(true);
                      }}
                      className="px-3 py-1 bg-blue-600 text-white rounded"
                    >
                      Edit
                    </button>

                    <button
                      onClick={() => openDeleteConfirm(item)}
                      className="px-3 py-1 bg-red-600 text-white rounded"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {(page > 1 || hasNextPage) && (
        <div className="flex gap-2 items-center">
          {page > 1 && (
            <button
              disabled={loading}
              onClick={() => setPage((p) => p - 1)}
              className="px-4 py-2 border rounded disabled:opacity-50"
            >
              Prev
            </button>
          )}

          <span className="px-4 py-2">Page {page}</span>

          {hasNextPage && (
            <button
              disabled={loading}
              onClick={() => setPage((p) => p + 1)}
              className="px-4 py-2 border rounded disabled:opacity-50"
            >
              Next
            </button>
          )}
        </div>
      )}

      {/* Create / Edit Modal */}
      <ItemModal
        open={modalOpen}
        initialData={editingItem}
        onClose={() => {
          setModalOpen(false);
          setEditingItem(null);
        }}
        onSubmit={editingItem ? handleEdit : handleCreate}
      />

      {/* Delete Confirmation Modal */}
      {deleteOpen && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-2">
              Delete Item
            </h3>

            <p className="text-sm text-gray-600 mb-6">
              Are you sure you want to delete{" "}
              <span className="font-medium">
                {itemToDelete?.title}
              </span>
              ?
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setDeleteOpen(false);
                  setItemToDelete(null);
                }}
                className="px-4 py-2 border rounded-md"
              >
                Cancel
              </button>

              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
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
