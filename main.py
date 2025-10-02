import tkinter as tk
from parse_characters import parse_characters
from build_groups import build_groups


# Global character list
characters = []

# ---------------------------
# Helper function to populate scrollable content
# ---------------------------
def display_characters():
    # Remove the placeholder if it exists
    global placeholder_label, characters
    if placeholder_label:
        placeholder_label.destroy()

    # Clear previous content if any
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Optionally filter outliers based on checkbox
    include_outliers = include_outlier_var.get()

    # Parse characters
    characters = parse_characters("characters.txt", include_outliers)

    for char in characters:

        tk.Label(content_frame, text=str(char), anchor="w", justify="left").pack(fill="x", pady=5)

    # Change button text and behavior
    map_button.config(text="Develop Groups", command=develop_groups)

# ---------------------------
# Function to run build_groups.py
# ---------------------------
def develop_groups():

    global characters
    if not characters:
        return  # safety check

    groups = build_groups(characters)

    # Clear current content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Display groups
    for group in groups:
        tk.Label(content_frame, text=str(group), anchor="w", justify="left", bd=1, relief="solid", padx=5, pady=5).pack(fill="x", pady=5)


# Create main window
root = tk.Tk()
root.title("Terraria NPC Relationship Viewer")
root.geometry("600x900")

# Top label
label = tk.Label(root, text="Welcome!", font=("Arial", 16))
label.pack(pady=20)

# Frame to hold button and checkbox
top_frame = tk.Frame(root)
top_frame.pack(pady=20)

# Left: Button
map_button = tk.Button(top_frame, text="Import Characters", width=20, height=2, command=display_characters)
map_button.pack(side="left", padx=20)

# Right: Checkbox
include_outlier_var = tk.BooleanVar()
include_outlier_cb = tk.Checkbutton(top_frame, text="Include outlier characters",
                                    variable=include_outlier_var)
include_outlier_cb.pack(side="left", padx=20)

# --------------------------------------
# Scrollable Data Section
# --------------------------------------
# Create a frame to contain the canvas and scrollbar
data_frame = tk.Frame(root, bd=2, relief="sunken")
data_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Canvas for scrolling
canvas = tk.Canvas(data_frame)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(data_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Another frame inside the canvas to hold actual content
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Function to update scrollregion when widgets are added
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", on_configure)

# Example: populate some data
placeholder_label = tk.Label(content_frame, text="Awaiting user input...", font=("Arial", 10), fg="gray")
placeholder_label.pack(pady=10, anchor="center")

# Start the app
root.mainloop()