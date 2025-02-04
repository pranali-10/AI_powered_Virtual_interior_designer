import tkinter as tk
from tkinter import ttk, filedialog, Scrollbar, Canvas
from PIL import Image, ImageTk
import os

class InteriorAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interior AI Simulator")
        #self.root.geometry("1300x700")
        #self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state('zoomed')
        # Title and Subheading
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
        # Sidebar frame
        self.sidebar_canvas = Canvas(self.root, bg="#2c3e50", width=250, height=700)
        self.sidebar_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbar for sidebar
        scrollbar = Scrollbar(self.root, orient=tk.VERTICAL, command=self.sidebar_canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.sidebar_canvas.configure(yscrollcommand=scrollbar.set)
        #self.sidebar_canvas.bind('<Configure>', lambda e: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all")))
        #self.root.bind("<Configure>", self.update_scroll_region)  

        sidebar_frame = tk.Frame(self.sidebar_canvas, bg="#2c3e50")
        self.sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")
        self.root.bind("<Configure>", self.update_scroll_region) 
        self.sidebar_canvas.bind_all("<MouseWheel>", self._on_mouse_scroll)
        self.update_scroll_region()

        # Sidebar content
        title_label = tk.Label(sidebar_frame, text="Settings", bg="#2c3e50", fg="white", font=("Helvetica", 16))
        title_label.pack(pady=20)

        # Room type dropdown
        room_label = tk.Label(sidebar_frame, text="Room Type:", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="white")
        room_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.room_type = ttk.Combobox(sidebar_frame, values=["Living Room", "Bedroom", "Kitchen", "Office"])
        self.room_type.set("Living Room")  # Set default value
        self.room_type.pack(padx=10, pady=5)

        # Room style dropdown
        style_label = tk.Label(sidebar_frame, text="Room Style:", bg="#2c3e50", font=("Helvetica", 12, "bold"), fg="white")
        style_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.room_style = ttk.Combobox(sidebar_frame, values=["Modern", "Classic", "Minimalist", "Industrial"])
        self.room_style.set("Modern")  # Set default value
        self.room_style.pack(padx=10, pady=5)

        # Image Type (Radio Buttons)
        image_type_label = tk.Label(sidebar_frame, text="Image Type:", bg="#2c3e50", font=("Helvetica", 12, "bold"), fg="white")
        image_type_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.image_type_var = tk.StringVar(value="Photo")  # Default selection

        photo_radio = tk.Radiobutton(sidebar_frame, text="Photo", variable=self.image_type_var, value="Photo",
                                     font=("Helvetica", 10, "bold"), bg="#2c3e50", fg="white", selectcolor="#34495e", command=self.set_image_type)
        photo_radio.pack(anchor="w", padx=20)

        drawing_radio = tk.Radiobutton(sidebar_frame, text="Drawing", variable=self.image_type_var, value="Drawing",
                                       font=("Helvetica", 10, "bold"), bg="#2c3e50", fg="white", selectcolor="#34495e", command=self.set_image_type)
        drawing_radio.pack(anchor="w", padx=20)

        # Additional prompt
        prompt_label = tk.Label(sidebar_frame, text="Additional Prompt:", bg="#2c3e50", font=("Helvetica", 12, "bold"), fg="white")
        prompt_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.prompt_textbox = tk.Text(sidebar_frame, height=4, width=25)
        self.prompt_textbox.pack(padx=15, pady=5)

        # Upload image button
        upload_button = tk.Button(sidebar_frame, text="Upload Image", bg="#1abc9c", font=("Helvetica", 12, "bold"), fg="white", command=self.upload_image, height=2)
        upload_button.pack(padx=30, pady=10, fill=tk.X)

        # Display uploaded image below upload button
        self.image_label = tk.Label(sidebar_frame, bg="#2c3e50")
        self.image_label.pack(padx=10, pady=10)

        # Generate button
        generate_button = tk.Button(sidebar_frame, text="Generate Design🪄", bg="#6b2c5d", font=("Helvetica", 12, "bold"),fg="white", command=self.generate_design)
        generate_button.pack(padx=25, pady=20, fill=tk.X)

    def create_content_panel(self):
        # Content Panel
        content_panel = tk.Frame(self.root, bg="#ecf0f1", width=950, height=700)
        content_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Furniture details frame on the right
        self.furniture_frame = tk.Frame(content_panel, bg="#ecf0f1")
        self.furniture_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.details_label = tk.Label(self.furniture_frame, text="Furniture/Product Details", bg="#bdc3c7", font=("Helvetica", 16))
        self.details_label.pack(pady=20)

    def set_image_type(self):
        print(f"Image type set to: {self.image_type_var.get()}")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            # Ensure the directory exists for saving uploaded images
            upload_dir = "uploaded_images"
            os.makedirs(upload_dir, exist_ok=True)
            # Save the uploaded image in the directory
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(upload_dir, file_name)
            with open(file_path, "rb") as file:
                with open(destination_path, "wb") as dest_file:
                    dest_file.write(file.read())
            print(f"Image uploaded and saved at: {destination_path}")
            self.display_uploaded_image(destination_path)

    def display_uploaded_image(self, image_path):
        # Load and display the image in the sidebar below the upload button
        img = Image.open(image_path)
        img = img.resize((200, 150), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def generate_design(self):
        # Placeholder functionality for generating a design preview
        prompt_text = self.prompt_textbox.get("1.0", tk.END).strip()
        self.details_label.config(text="Furniture/Product Details: Example Item 1, Example Item 2")

    def update_scroll_region(self, event=None):
        self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all"))

    def _on_mouse_scroll(self, event):
        if event.delta > 0:  # Scroll up
            self.sidebar_canvas.yview_scroll(-1, "units")
        else:  # Scroll down
            self.sidebar_canvas.yview_scroll(1, "units")



if __name__ == "__main__":
    root = tk.Tk()
    app = InteriorAIApp(root)
    root.mainloop()
