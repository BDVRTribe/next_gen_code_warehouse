import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

UNDO_DIR = "undo_logs"

class UndoBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 Undo Snapshot Browser")
        self.root.geometry("800x600")

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        # Listbox for log files
        self.listbox = tk.Listbox(self.root, height=10, font=("Helvetica", 12))
        self.listbox.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.display_log_details)

        # Text area for details
        self.preview = tk.Text(self.root, wrap=tk.WORD, font=("Courier", 10))
        self.preview.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        self.preview.configure(state=tk.DISABLED)

        # Restore button
        self.restore_button = ttk.Button(self.root, text="🔁 Restore Snapshot", command=self.restore_snapshot)
        self.restore_button.pack(side=tk.BOTTOM, pady=10)

        # Load logs
        self.logs = self.load_logs()
        self.populate_listbox()

    def load_logs(self):
        logs = []
        if not os.path.exists(UNDO_DIR):
            os.makedirs(UNDO_DIR)
            return logs

        for filename in sorted(os.listdir(UNDO_DIR)):
            if not filename.endswith(".json"):
                continue

            full_path = os.path.join(UNDO_DIR, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)

                # Normalize
                normalized = []
                if isinstance(raw_data, list):
                    for entry in raw_data:
                        if isinstance(entry, dict):
                            normalized.append(entry)
                elif isinstance(raw_data, dict):
                    normalized.append(raw_data)
                else:
                    print(f"⚠️ Ignored {filename}: not a list or dict")
                    continue

                logs.append((filename, normalized))

            except Exception as e:
                print(f"⚠️ Failed to load {filename}: {e}")
        return logs

    def populate_listbox(self):
        for filename, data in self.logs:
            if isinstance(data, list):
                entry = f"{filename} – {len(data)} change(s)"
            else:
                entry = f"{filename} – ⚠️ Invalid format"
            self.listbox.insert(tk.END, entry)

    def display_log_details(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        filename, data = self.logs[index]

        self.preview.configure(state=tk.NORMAL)
        self.preview.delete("1.0", tk.END)

        for i, entry in enumerate(data, 1):
            if not isinstance(entry, dict):
                self.preview.insert(tk.END, f"{i}. ⚠️ Invalid entry\n")
                continue

            emoji = {
                "add": "🟢",
                "edit": "📝",
                "delete": "🗑"
            }.get(entry.get("action_type", "").lower(), "❔")

            line = (
                f"{i}. {emoji} [{entry.get('action_type', '?').upper()}]\n"
                f"   File: {entry.get('filename', 'unknown')}\n"
                f"   Lang: {entry.get('language', 'unknown')}\n"
                f"   Path: {entry.get('path', 'N/A')}\n"
                f"   Time: {entry.get('timestamp', 'N/A')}\n"
                f"\n"
            )
            self.preview.insert(tk.END, line)

        self.preview.configure(state=tk.DISABLED)

    def restore_snapshot(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Restore", "Please select a snapshot first.")
            return

        index = selection[0]
        _, data = self.logs[index]

        restored_count = 0
        for entry in data:
            if isinstance(entry, dict) and entry.get("path") and entry.get("code"):
                try:
                    with open(entry["path"], "w", encoding="utf-8") as f:
                        f.write(entry["code"])
                    restored_count += 1
                except Exception as e:
                    print(f"❌ Failed to restore {entry['path']}: {e}")

        messagebox.showinfo("Restore Complete", f"✅ Restored {restored_count} file(s).")

if __name__ == "__main__":
    UndoBrowser()

