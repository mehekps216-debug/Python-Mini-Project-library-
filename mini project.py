import tkinter as tk
from tkinter import ttk, messagebox
import csv

book_list = []

def add_book():
    data = (
        len(book_list) + 1,
        title_entry.get().strip(),
        isbn_entry.get().strip(),
        genre_combo.get(),
        status_combo.get()
    )
    if not all(data[1:]):
        return messagebox.showwarning("Warning", "Please complete all fields!")
        
    book_list.append(data)
    insert_row(data)
    
    with open("library_inventory.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(data)
        
    messagebox.showinfo("Success", "Record successfully added!")
    clear_fields()

def insert_row(book):
    tag = "available" if book[4] == "Available" else "borrowed"
    table.insert("", "end", values=book, tags=(tag,))

def search_book():
    query = isbn_entry.get().strip().lower()
    table.delete(*table.get_children())
    
    if query in ("", "all"):
        matches = book_list
    else:
        matches = [b for b in book_list if str(b[0]) == query or query in b[1].lower() or query in b[2].lower()]
        
    if not matches:
        return messagebox.showerror("Not Found", "No matching book found!")
        
    for b in matches:
        insert_row(b)

def delete_book():
    selected = table.selection()
    if not selected:
        return messagebox.showwarning("Warning", "Please select a record to delete!")
        
    for item in selected:
        table.delete(item)
    messagebox.showinfo("Success", "Selected record deleted!")

def clear_fields():
    title_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    genre_combo.set("")
    status_combo.set("")

# ---------------- Warm Amber & Espresso Theme ----------------
COLOR_BG = "#181825"         # Dark Espresso Base
COLOR_LEFT_PANEL = "#1e1e2e" # Form Box Background
COLOR_RIGHT_PANEL = "#181825"# Table Box Background
COLOR_CARD = "#27272a"       # Form Input Container
COLOR_TEXT = "#f4f4f5"       # Warm Off-White Text
COLOR_MUTED = "#a1a1aa"      # Muted Label Text

# Accent Action Colors
COLOR_AMBER = "#d97706"      # Primary Gold/Amber Accent (Add)
COLOR_TEAL = "#0d9488"       # Search Accent
COLOR_CORAL = "#e11d48"      # Delete Accent
COLOR_STONE = "#52525b"      # Clear Accent

window = tk.Tk()
window.title("Athenaeum — Catalog Register")
window.geometry("920x550")
window.configure(bg=COLOR_BG)

# Root Split Layout (Left Form, Right Register)
main_frame = tk.Frame(window, bg=COLOR_BG)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

# ---------------- LEFT SIDE: Delivery / Admission Details Form ----------------
left_panel = tk.Frame(main_frame, bg=COLOR_LEFT_PANEL, width=330, padx=18, pady=18, highlightbackground="#3f3f46", highlightthickness=1)
left_panel.pack(side="left", fill="y", expand=False)
left_panel.pack_propagate(False)

# Form Section Title
tk.Label(
    left_panel, 
    text="📥 Book Admission Box", 
    bg=COLOR_LEFT_PANEL, 
    fg=COLOR_AMBER, 
    font=("Georgia", 15, "bold")
).pack(anchor="w", pady=(0, 2))

tk.Label(
    left_panel, 
    text="Enter details to register or search item", 
    bg=COLOR_LEFT_PANEL, 
    fg=COLOR_MUTED, 
    font=("Trebuchet MS", 9)
).pack(anchor="w", pady=(0, 15))

# Input Container Card
form_card = tk.Frame(left_panel, bg=COLOR_CARD, padx=12, pady=12, highlightbackground="#3f3f46", highlightthickness=1)
form_card.pack(fill="x", pady=(0, 15))

def create_field_label(parent, text):
    tk.Label(parent, text=text, bg=COLOR_CARD, fg=COLOR_TEXT, font=("Trebuchet MS", 9, "bold")).pack(anchor="w", pady=(4, 2))

# Title Entry
create_field_label(form_card, "BOOK TITLE")
title_entry = tk.Entry(form_card, font=("Trebuchet MS", 10), bg="#18181b", fg=COLOR_TEXT, insertbackground=COLOR_TEXT, relief="flat", bd=4)
title_entry.pack(fill="x", pady=(0, 8))

# ISBN / ID Entry
create_field_label(form_card, "ISBN / BOOK ID")
isbn_entry = tk.Entry(form_card, font=("Trebuchet MS", 10), bg="#18181b", fg=COLOR_TEXT, insertbackground=COLOR_TEXT, relief="flat", bd=4)
isbn_entry.pack(fill="x", pady=(0, 8))

# Genre Dropdown
create_field_label(form_card, "GENRE")
genre_combo = ttk.Combobox(form_card, values=["Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Technology"], font=("Trebuchet MS", 10), state="readonly")
genre_combo.pack(fill="x", pady=(0, 8))

# Status Dropdown
create_field_label(form_card, "STATUS")
status_combo = ttk.Combobox(form_card, values=["Available", "Borrowed"], font=("Trebuchet MS", 10), state="readonly")
status_combo.pack(fill="x", pady=(0, 4))

# Left Actions Grid
actions_frame = tk.Frame(left_panel, bg=COLOR_LEFT_PANEL)
actions_frame.pack(fill="x")

def create_action_btn(parent, text, bg_color, command, row, col):
    btn = tk.Button(
        parent, 
        text=text, 
        bg=bg_color, 
        fg="#ffffff", 
        font=("Trebuchet MS", 9, "bold"), 
        relief="flat", 
        activebackground=bg_color, 
        activeforeground="#ffffff",
        cursor="hand2", 
        command=command,
        pady=8
    )
    btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

actions_frame.columnconfigure(0, weight=1)
actions_frame.columnconfigure(1, weight=1)

create_action_btn(actions_frame, "➕ Add Record", COLOR_AMBER, add_book, 0, 0)
create_action_btn(actions_frame, "🔍 Search", COLOR_TEAL, search_book, 0, 1)
create_action_btn(actions_frame, "🧹 Clear Form", COLOR_STONE, clear_fields, 1, 0)
create_action_btn(actions_frame, "🗑 Delete", COLOR_CORAL, delete_book, 1, 1)

# ---------------- RIGHT SIDE: Output Register Box ----------------
right_panel = tk.Frame(main_frame, bg=COLOR_RIGHT_PANEL, padx=15, pady=5)
right_panel.pack(side="right", fill="both", expand=True)

# Register Header
tk.Label(
    right_panel, 
    text="📋 Output Register Box", 
    bg=COLOR_RIGHT_PANEL, 
    fg=COLOR_TEXT, 
    font=("Georgia", 14, "bold")
).pack(anchor="w", pady=(0, 12))

# Styling Treeview
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview", 
    background="#1e1e2e", 
    fieldbackground="#1e1e2e", 
    foreground=COLOR_TEXT, 
    rowheight=32, 
    font=("Trebuchet MS", 9), 
    borderwidth=0
)

style.configure(
    "Treeview.Heading", 
    background="#27272a", 
    foreground=COLOR_AMBER, 
    font=("Georgia", 10, "bold"), 
    borderwidth=0
)

style.map("Treeview", background=[("selected", "#d97706")], foreground=[("selected", "#ffffff")])

# Output Table
cols = ("ID", "Title", "ISBN", "Genre", "Status")
table = ttk.Treeview(right_panel, columns=cols, show="headings")

col_widths = {"ID": 40, "Title": 190, "ISBN": 100, "Genre": 100, "Status": 90}
for col, width in col_widths.items():
    table.heading(col, text=col)
    table.column(col, anchor="center" if col != "Title" else "w", width=width)

table.pack(fill="both", expand=True)

# Status Highlights
table.tag_configure("available", background="#064e3b", foreground="#a7f3d0") # Emerald tint
table.tag_configure("borrowed", background="#881337", foreground="#fecdd3")  # Crimson tint

window.mainloop()
