"""
Example: Simple GUI application using tkinter.

This demonstrates how to integrate the converter into a desktop GUI application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from io import BytesIO
from smiles_to_image import smiles_to_image


class SmilesConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SMILES to Image Converter")
        self.root.geometry("600x700")

        # Current image
        self.current_image = None

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Input", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="SMILES:").grid(row=0, column=0, sticky="w")
        self.smiles_entry = ttk.Entry(input_frame, width=50)
        self.smiles_entry.grid(row=0, column=1, padx=5)
        self.smiles_entry.insert(0, "CCO")  # Default example

        # Options frame
        options_frame = ttk.LabelFrame(self.root, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, sticky="w")
        self.format_var = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var,
                                     values=["PNG", "JPEG", "SVG"], state="readonly", width=10)
        format_combo.grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(options_frame, text="Size:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.size_var = tk.StringVar(value="400")
        size_combo = ttk.Combobox(options_frame, textvariable=self.size_var,
                                   values=["200", "300", "400", "500", "800"], width=10)
        size_combo.grid(row=0, column=3, padx=5, sticky="w")

        # Buttons frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Generate Image", command=self.generate_image).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save As...", command=self.save_image).pack(side="left", padx=5)

        # Image display frame
        display_frame = ttk.LabelFrame(self.root, text="Preview", padding=10)
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.image_label = ttk.Label(display_frame, text="Click 'Generate Image' to start",
                                     background="white", anchor="center")
        self.image_label.pack(fill="both", expand=True)

    def generate_image(self):
        smiles = self.smiles_entry.get().strip()
        if not smiles:
            messagebox.showerror("Error", "Please enter a SMILES string")
            return

        try:
            img_format = self.format_var.get()
            size = int(self.size_var.get())

            # Generate image
            self.current_image = smiles_to_image(smiles, img_format, (size, size), return_pil=True)

            # Display in GUI
            # Resize for display if too large
            display_size = min(size, 500)
            if size > display_size:
                display_img = self.current_image.copy()
                display_img.thumbnail((display_size, display_size), Image.Resampling.LANCZOS)
            else:
                display_img = self.current_image

            photo = ImageTk.PhotoImage(display_img)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep reference

        except ValueError as e:
            messagebox.showerror("Invalid SMILES", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate image: {e}")

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save. Generate an image first.")
            return

        img_format = self.format_var.get().lower()
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{img_format}",
            filetypes=[
                (f"{img_format.upper()} Image", f"*.{img_format}"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            try:
                self.current_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SmilesConverterGUI(root)
    root.mainloop()
