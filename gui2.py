import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os

def on_generate():
    print("Generate button clicked")

def on_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize((250, 200), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        uploaded_image_label.config(image=img_tk)
        uploaded_image_label.image = img_tk
        
        # Save the uploaded image to the current directory
        save_path = os.path.join(os.getcwd(), os.path.basename(file_path))
        img.save(save_path)
        print(f"Image saved to: {save_path}")

root = tk.Tk()
root.title("Virtual interior designer")
root.geometry("1200x700")
root.configure(bg="#f0f8ff")

# Main Heading
tk.Label(root, text="Experience the Magic of AI Remodeling🪄", font=("Arial", 24, "bold"), bg="#f0f8ff").pack(pady=10)

# Sub Heading
tk.Label(root, text="Personalized, smart designs that bring your dream space to life", font=("Arial", 12), bg="#f0f8ff").pack(pady=10)

# Left panel with buttons and inputs
left_canvas = tk.Canvas(root, bg="#f0f8ff", bd=2, width=320)  # No border for the canvas
left_canvas.pack(side=tk.LEFT, fill=tk.Y, padx=1, pady=10)

scrollbar = tk.Scrollbar(root, orient="vertical", command=left_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

left_canvas.configure(yscrollcommand=scrollbar.set)
left_canvas.bind('<Configure>', lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))

# Left frame with a visible border
left_frame = tk.Frame(left_canvas, bg="#f0f8ff", padx=15, pady=15, relief=tk.GROOVE, borderwidth=0, width=320)
left_canvas.create_window((0, 0), window=left_frame, anchor="nw")


tk.Label(left_frame, text="Image Type", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(anchor="w")
tk.Label(left_frame, text="Choose the type of your input image", font=("Arial", 10), bg="#f0f8ff").pack(anchor="w", pady=2)

image_type_frame = tk.Frame(left_frame, bg="#f0f8ff")
image_type_frame.pack(pady=5)

image_types = ["Photo", "Drawing"]
for img_type in image_types:
    btn = tk.Button(image_type_frame, text=img_type, bg="#e6e6e6", relief=tk.RAISED, width=12)
    btn.pack(side=tk.LEFT, padx=2, pady=2)

# Room Type
room_type_label = tk.Label(left_frame, text="Room Type", font=("Arial", 12, "bold"), bg="#f0f8ff")
room_type_label.pack(anchor="w", pady=5)
room_type = ttk.Combobox(left_frame, values=["Living Room", "Bedroom", "Office"], width=27)
room_type.pack(pady=10)

# Room Style
tk.Label(left_frame, text="Room Style", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(anchor="w", pady=5)
room_style = ttk.Combobox(left_frame, values=["Modern", "Western", "Luxurious", "Minimalist"], width=27)
room_style.pack(pady=10)

# Additional Prompt
tk.Label(left_frame, text="Additional Prompt", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(anchor="w", pady=5)
additional_prompt = tk.Text(left_frame, width=30, height=3)  # Using Text widget for height
additional_prompt.pack(pady=10)

# Upload Button
tk.Button(left_frame, text="Upload Image", command=on_upload, bg="#6fa3ef", fg="white", font=("Arial", 10, "bold"), width=22, relief=tk.RAISED, height=2).pack(pady=10)

uploaded_image_label = tk.Label(left_frame, text="No Image Uploaded", font=("Arial", 10), bg="#f0f8ff")
uploaded_image_label.pack(pady=10)

# Generate Button
tk.Button(left_frame, text="Generate🪄", command=on_generate, bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=22, relief=tk.RAISED).pack(pady=10)

# Center frame for generated image
generated_frame = tk.Frame(root, height=500, width=600, relief=tk.GROOVE, borderwidth=2, bg="#f0f8ff")
generated_frame.pack(side=tk.LEFT, padx=20, pady=10, expand=True, fill=tk.BOTH)
image_label = tk.Label(generated_frame, text="Generated Image", font=("Arial", 18, "bold"), bg="#f0f8ff")
image_label.pack(expand=True)

# Divider line
# divider_line = tk.Frame(root, height=700, width=2, bg="#b0c4de")
# divider_line.pack(side=tk.LEFT, fill=tk.Y)

# Right panel for furniture details
right_frame = tk.Frame(root, width=300, bg="#f0f8ff", padx=15, pady=10, relief=tk.GROOVE, borderwidth=2)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=10)

tk.Label(right_frame, text="Furniture Details", font=("Arial", 18, "bold"), bg="#f0f8ff").pack()
tk.Label(right_frame, text="Price of the product will be displayed here.", wraplength=250, bg="#f0f8ff", font=("Arial", 10)).pack(pady=10)

root.mainloop()
