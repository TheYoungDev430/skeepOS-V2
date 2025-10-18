import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import os  # ✅ Added missing import

# --- Context Menu Creation ---
def create_context_menu(app_name, app_function, description):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label=f"Open {app_name}", command=app_function)
    menu.add_command(label="Properties", command=lambda: messagebox.showinfo("Properties", description))
    return menu

# --- Desktop Icon Launcher with Labels and Context Menu ---
def create_desktop_icon(label_text, app_function, description, x, y):
    icon_button = tk.Button(root, text=label_text, command=app_function, width=10, height=2, bg="white")
    icon_button.place(x=x, y=y)

    label = tk.Label(root, text=label_text, font=("Comic Sans", 10), bg="white")
    label.place(x=x + 50, y=y + 45, anchor="center")

    context_menu = create_context_menu(label_text, app_function, description)
    icon_button.bind("<Button-3>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))

# --- Main OS Interface ---
def show_main_os():
    root.configure(bg="lightblue")

    global taskbar
    start_menu = tk.Frame(root, bg="gray", width=200, height=250)
    start_menu.place(x=0, y=350)
    start_menu.place_forget()

    def toggle_start_menu():
        if start_menu.winfo_ismapped():
            start_menu.place_forget()
        else:
            start_menu.place(x=0, y=350)

    taskbar = tk.Frame(root, bg="black", height=30)
    taskbar.pack(side="bottom", fill="x")

    time_label = tk.Label(taskbar, fg="white", bg="black", font=("Comic Sans", 10))
    time_label.pack(side="right", padx=10)

    def update_time():
        current_time = time.strftime("%I:%M:%S %p")
        current_date = time.strftime("%d-%b-%Y")
        time_label.config(text=f"{current_time} | {current_date}")
        root.after(1000, update_time)

    update_time()

    battery_label = tk.Label(taskbar, fg="white", bg="black", font=("Comic Sans", 10), text="🔋 87%")
    battery_label.pack(side="right", padx=10)

    start_button = tk.Button(taskbar, text="Start", command=toggle_start_menu, bg="gray", fg="white")
    start_button.pack(side="left", padx=5)

    def open_notepad():
        subprocess.Popen(["notepad.exe"])

    def open_paint():
        subprocess.Popen(["mspaint.exe"])

    def open_cmd():
        subprocess.Popen(["cmd.exe"])

    def open_regedit():
        subprocess.Popen(["regedit.exe"])

    def open_edge():
        edge_path = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        if os.path.exists(edge_path):
            subprocess.Popen([edge_path])
        else:
            messagebox.showerror("Error", "Edge not found!")

    def shutdown_os():
        for widget in root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        shutdown_label = tk.Label(root, text="Exiting safely...", font=("Comic Sans", 24), bg="black", fg="white")
        shutdown_label.place(relx=0.5, rely=0.5, anchor="center")
        root.after(4000, root.destroy)

    def open_file_explorer():
        explorer = tk.Toplevel(root)
        explorer.title("File Explorer")
        explorer.geometry("400x300")
        explorer.configure(bg="white")

        files = ["Documents", "Pictures", "Music", "Videos", "file1.txt", "file2.docx"]
        for f in files:
            icon = "📁" if "." not in f else "📄"
            tk.Label(explorer, text=f"{icon} {f}", font=("Comic Sans", 12), bg="white").pack(anchor="w", padx=10, pady=5)

    apps = [
        ("Notepad", open_notepad),
        ("Paint", open_paint),
        ("CMD", open_cmd),
        ("Registry Editor", open_regedit),
        ("Microsoft Edge", open_edge),
        ("File Explorer", open_file_explorer),
        ("Shutdown", shutdown_os)
    ]

    for name, cmd in apps:
        btn = tk.Button(start_menu, text=name, command=cmd, width=25)
        btn.pack(pady=5)

    # Desktop Icons with Labels and Context Menus
    create_desktop_icon("Notepad", open_notepad, "Notepad for skeepOS", 50, 50)
    create_desktop_icon("Registry Editor", open_regedit, "Registry Editor for skeepOS", 150, 50)
    create_desktop_icon("Edge", open_edge, "Edge browser for skeepOS", 250, 50)
    create_desktop_icon("CMD", open_cmd, "Command Prompt for skeepOS", 350, 50)

# --- Login Screen ---
def show_login_screen():
    login_frame = tk.Frame(root, bg="black")
    login_frame.place(relwidth=1, relheight=1)

    time_label = tk.Label(login_frame, fg="white", bg="black", font=("Comic Sans", 24))
    time_label.pack(pady=20)

    def update_login_time():
        if time_label.winfo_exists():
            current_time = time.strftime("%I:%M:%S %p")
            current_date = time.strftime("%d-%b-%Y")
            time_label.config(text=f"{current_time}\n{current_date}")
            root.after(1000, update_login_time)

    def show_password_entry(event=None):
        root.unbind_all("<Key>")
        time_label.destroy()
        for widget in login_frame.winfo_children():
            widget.destroy()
        tk.Label(login_frame, text="Enter Password:", font=("Comic Sans", 16), bg="black", fg="white").pack(pady=10)
        password_entry = tk.Entry(login_frame, show="*", font=("Comic Sans", 16))
        password_entry.pack(pady=10)
        def check_password():
            if password_entry.get() == "4":
                login_frame.destroy()
                show_main_os()
            else:
                messagebox.showerror("Error", "Incorrect Password")
        tk.Button(login_frame, text="Login", command=check_password).pack(pady=10)

    root.bind_all("<Key>", show_password_entry)
    update_login_time()

# Create main window
root = tk.Tk()
root.title("skeepOS Simulator")
root.geometry("800x600")
root.resizable(False, False)

# Show login screen first
show_login_screen()

# Run the app
root.mainloop()
