# main.py

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
from interior_design import InteriorDesignGenerator

class InteriorAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interior AI Simulator")
        self.root.state('zoomed')  # Fullscreen

        # Create a backend object for image generation
        self.design_generator = InteriorDesignGenerator()

        # Title Section
        self.create_title_section()

        # Main layout: Sidebar and Content Panel
        self.create_sidebar()
        self.create_content_panel()

    def create_title_section(self):
        title_frame = tk.Frame(self.root, bg="#3498db", height=80)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(title_frame, text="Experience the Magic of AI Remodelling🪄", bg="#3498db", fg="white", font=("Helvetica", 24))
        title_label.pack(pady=10)

        subtitle_label = tk.Label(title_frame, text="Transform your space in clicks", bg="#3498db", fg="white", font=("Helvetica", 14))
        subtitle_label.pack()

    def create_sidebar(self):
        self.sidebar_canvas = tk.Canvas(self.root, bg="#2c3e50", width=250, height=700)
        self.sidebar_canvas.pack(side=tk.LEFT, fill=tk.Y)

        scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.sidebar_canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_canvas.configure(yscrollcommand=scrollbar.set)

        sidebar_frame = tk.Frame(self.sidebar_canvas, bg="#2c3e50")
        self.sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")

        title_label = tk.Label(sidebar_frame, text="Settings", bg="#2c3e50", fg="white", font=("Helvetica", 16))
        title_label.pack(pady=20)

        room_label = tk.Label(sidebar_frame, text="Room Type:", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="white")
        room_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.room_type = ttk.Combobox(sidebar_frame, values=["Living Room", "Bedroom", "Kitchen", "Office"])
        self.room_type.set("Living Room")
        self.room_type.pack(padx=10, pady=5)

        style_label = tk.Label(sidebar_frame, text="Room Style:", bg="#2c3e50", font=("Helvetica", 12, "bold"), fg="white")
        style_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.room_style = ttk.Combobox(sidebar_frame, values=["Modern", "Classic", "Minimalist", "Industrial"])
        self.room_style.set("Modern")
        self.room_style.pack(padx=10, pady=5)

        image_type_label = tk.Label(sidebar_frame, text="Image Type:", bg="#2c3e50", font=("Helvetica", 12, "bold"), fg="white")
        image_type_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.image_type_var = tk.StringVar(value="Photo")
        photo_radio = tk.Radiobutton(sidebar_frame, text="Photo", variable=self.image_type_var, value="Photo", bg="#2c3e50", fg="white", command=self.set_image_type)
        photo_radio.pack(anchor="w", padx=20)

        drawing_radio = tk.Radiobutton(sidebar_frame, text="Drawing", variable=self.image_type_var, value="Drawing", bg="#2c3e50", fg="white", command=self.set_image_type)
        drawing_radio.pack(anchor="w", padx=20)

        prompt_label = tk.Label(sidebar_frame, text="Additional Prompt:", bg="#2c3e50", font=("Helvetica", 12, "bold"), fg="white")
        prompt_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.prompt_textbox = tk.Text(sidebar_frame, height=4, width=25)
        self.prompt_textbox.pack(padx=15, pady=5)

        upload_button = tk.Button(sidebar_frame, text="Upload Image", bg="#1abc9c", font=("Helvetica", 12, "bold"), fg="white", command=self.upload_image)
        upload_button.pack(padx=30, pady=10, fill=tk.X)

        self.image_label = tk.Label(sidebar_frame, bg="#2c3e50")
        self.image_label.pack(padx=10, pady=10)

        generate_button = tk.Button(sidebar_frame, text="Generate Design🪄", bg="#6b2c5d", font=("Helvetica", 12, "bold"), fg="white", command=self.generate_design)
        generate_button.pack(padx=25, pady=20, fill=tk.X)

    def create_content_panel(self):
        content_panel = tk.Frame(self.root, bg="#ecf0f1", width=950, height=700)
        content_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.furniture_frame = tk.Frame(content_panel, bg="#ecf0f1")
        self.furniture_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.details_label = tk.Label(self.furniture_frame, text="Furniture/Product Details", bg="#bdc3c7", font=("Helvetica", 16))
        self.details_label.pack(pady=20)

    def set_image_type(self):
        print(f"Image type set to: {self.image_type_var.get()}")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            self.uploaded_image_path = file_path
            print(f"Image uploaded and saved at: {file_path}")
            self.display_uploaded_image(file_path)

    def display_uploaded_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((100, 50), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def generate_design(self):
        room_type = self.room_type.get()
        room_style = self.room_style.get()
        image_type = self.image_type_var.get()
        additional_prompt = self.prompt_textbox.get("1.0", tk.END).strip()

        prompt = f"A {room_style} {room_type} interior, {additional_prompt}, high quality, ultra-detailed, {image_type} image"
        print(f"Prompt: {prompt}")

        # Generate the new design using the backend
        if hasattr(self, 'uploaded_image_path'):
            generated_image_path = self.design_generator.generate_redesigned_image(prompt, self.uploaded_image_path)
            self.display_generated_image(generated_image_path)

    def display_generated_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((400, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        if hasattr(self, 'generated_image_label'):
            self.generated_image_label.config(image=img_tk)
            self.generated_image_label.image = img_tk
        else:
            self.generated_image_label = tk.Label(self.root, image=img_tk)
            self.generated_image_label.image = img_tk
            self.generated_image_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = InteriorAIApp(root)
    root.mainloop()
