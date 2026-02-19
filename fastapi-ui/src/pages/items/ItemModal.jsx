import { useEffect, useState } from "react";

export default function ItemModal({
  open,
  onClose,
  onSubmit,
  initialData,
}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || "");
      setDescription(initialData.description || "");
      setPrice(initialData.price || "");
    } else {
      setTitle("");
      setDescription("");
      setPrice("");
    }
  }, [initialData]);

  if (!open) return null;

  const isValid =
    title.trim() && Number(price) > 0;

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6 space-y-4">
        <h2 className="text-xl font-bold">
          {initialData ? "Edit Item" : "Create Item"}
        </h2>

        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Title"
          className="w-full border px-3 py-2 rounded"
        />

        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description"
          rows={4}
          className="w-full border px-3 py-2 rounded resize-none"
        />

        <input
          type="number"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          placeholder="Price"
          className="w-full border px-3 py-2 rounded"
        />

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded"
          >
            Cancel
          </button>

          <button
            disabled={!isValid}
            onClick={() =>
              onSubmit({
                title: title.trim(),
                description: description.trim(),
                price: Number(price),
              })
            }
            className="px-4 py-2 bg-black text-white rounded disabled:opacity-50"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
