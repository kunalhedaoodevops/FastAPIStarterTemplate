import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Dashboard() {
    const [stats, setStats] = useState({
        users: "—",
        items: "—",
        files: "—",
        uptime: "OFF",
    });

    useEffect(() => {
        const loadStats = async () => {
            try {
                // Users
                let usersCount = 0;

                try {
                    const usersCountRes = await api.get("/users/count",{
                         headers: {
                        "Cache-Control": "no-cache",
                    },
                    });
                    usersCount = usersCountRes.data ?? 0;
                } catch (error) {
                    if (error.response?.status === 403) {
                        usersCount = 0; // explicitly for forbidden
                    } else {
                        console.error("Failed to fetch users count", error);
                        usersCount = "N/A";
                    }
                }

                // Items
                const itemsRes = await api.get("/items/count", {
                    headers: {
                        "Cache-Control": "no-cache",
                    },
                });
                const itemsCount = itemsRes.data ?? 0;

                // Files
                const filesRes = await api.get("/files/", {
                    headers: {
                        "Cache-Control": "no-cache",
                    },
                });
                const filesCount = filesRes.data?.length ?? 0;

                // Health
                await api.get("/health/");

                setStats({
                    users: usersCount,
                    items: itemsCount,
                    files: filesCount,
                    uptime: "OK",
                });
            } catch (err) {
                console.error("Failed to load dashboard stats", err);
            }
        };

        loadStats();
    }, []);

    const cards = [
        { label: "Users", value: stats.users },
        { label: "Items", value: stats.items },
        { label: "Files", value: stats.files },
        { label: "Uptime", value: stats.uptime },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {cards.map((c) => (
                <div
                    key={c.label}
                    className="bg-white p-6 rounded-xl shadow"
                >
                    <p className="text-gray-500">{c.label}</p>
                    <h2 className="text-3xl font-bold mt-2">
                        {c.value}
                    </h2>
                </div>
            ))}
        </div>
    );
}
