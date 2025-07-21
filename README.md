# 🗄️ SQLite Editor

Your **intuitive desktop companion** for exploring, editing, and managing SQLite databases in a clean, responsive Qt-powered interface.

Ideal for developers, data analysts, or anyone who works hands-on with `.db` files.

---

## 🚀 Features

- 📂 **Open SQLite Databases**: Load `.db` files and browse schema effortlessly.
- 📋 **View Tables & Records**: Clean, scrollable views with sortable columns.
- ➕ **Add Tables & Records**: Custom dialogs for structured creation of tables and data.
- 🖱️ **Right-Click Context Menus**: Fast actions for opening, editing, or deleting.
- 🗑️ **Delete Safely**: Remove tables or rows with confirmation and error handling.
- 🔄 **Auto-Refresh**: UI updates dynamically after changes (via `AutoReload`).
- 🚨 **Robust Error Reporting**: Clear messages on malformed queries or data issues.
- 🎨 **StyleDefine Support**: Theme your editor with Qt styles and palettes.
- 🖼️ **Icon Sets**: Resource-based icons for UI polish and instant recognition.
- 🧪 **Unit Tested**: Core functionality and JSON export paths are fully covered.

---

## 🖼️ Preview

<p>
   <img src="assets/photo-1.jpg.jpg" alt="Photo 1" width="400" />
</p>
<p>
   <img src="assets/photo-2.jpg.jpg" alt="Photo 2" width="400" />
</p>

---

## ⚙️ Technologies Used

| Tool         | Purpose                                      |
|--------------|----------------------------------------------|
| 🐍 `Python`   | Core scripting language                      |
| 🖥️ `PySide6`  | Qt-based desktop UI framework               |
| 🧪 `pytest`   | Unit testing and validation                  |
| 🗃️ `SQLite3`  | Native DB engine                            |

---

## 📦 Installation

Make sure you have a working Python environment and that [`uv`](https://docs.astral.sh/uv) is installed for dependency management.

---

## ▶️ How to Run

```bash
uv run sqlite_editor.py
```

---

## ✅ Testing

Run validation tests with:

```bash
pytest
```

Tests include checks for JSON format, content structure, and error handling.

---

## 📚 License

LGPLv3 — Free for personal or commercial use. Contributions welcome!
