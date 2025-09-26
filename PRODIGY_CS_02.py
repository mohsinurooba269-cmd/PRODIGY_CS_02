
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


BG_MAIN = "#0f0f1a"     # Dark navy
BG_FRAME = "#1a1a2e"    # Dark violet
FG_TEXT = "#e0e0e0"     # Soft white
BTN_ENCRYPT = "#ff2e63" # Neon pink
BTN_DECRYPT = "#08d9d6" # Neon cyan


input_img = None
output_img = None

def encrypt_decrypt_image(input_path, output_path, key):
    try:
        img = Image.open(input_path)
        pixels = img.load()

        for i in range(img.size[0]):  # width
            for j in range(img.size[1]):  # height
                pixel = pixels[i, j]

                if len(pixel) == 3:  # RGB
                    r, g, b = pixel
                    pixels[i, j] = (r ^ key, g ^ key, b ^ key)

                elif len(pixel) == 4:  # RGBA
                    r, g, b, a = pixel
                    pixels[i, j] = (r ^ key, g ^ key, b ^ key, a)

        img.save(output_path)
        return img
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
        return None

def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, filepath)
        show_input_preview(filepath)

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
    if filepath:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, filepath)

def run_task(mode):
    input_path = entry_input.get()
    output_path = entry_output.get()
    try:
        key = int(entry_key.get())
        if not (0 <= key <= 255):
            raise ValueError("Key must be between 0 and 255.")
    except ValueError as ve:
        messagebox.showerror("Invalid Key", str(ve))
        return

    if not input_path or not output_path:
        messagebox.showwarning("Missing Info", "Please select both input and output paths.")
        return

    img = encrypt_decrypt_image(input_path, output_path, key)
    if img:
        messagebox.showinfo("Success", f"Image {mode}ed successfully!\nSaved at: {output_path}")
        show_output_preview(output_path)

def show_input_preview(image_path):
    global input_img
    img = Image.open(image_path)
    img.thumbnail((250, 250))
    input_img = ImageTk.PhotoImage(img)
    preview_input.config(image=input_img)
    preview_input.image = input_img

def show_output_preview(image_path):
    global output_img
    img = Image.open(image_path)
    img.thumbnail((250, 250))
    output_img = ImageTk.PhotoImage(img)
    preview_output.config(image=output_img)
    preview_output.image = output_img

# ========== GUI Setup ==========
root = tk.Tk()
root.title("🔐 Image Encryption & Decryption Tool")
root.geometry("900x650")
root.config(bg=BG_MAIN)


title_label = tk.Label(root, text="🔒 Image Encryption Tool", 
                       font=("Arial", 20, "bold"), fg=FG_TEXT, bg=BG_MAIN)
title_label.pack(pady=15)


frame_top = tk.Frame(root, bg=BG_FRAME, padx=15, pady=15, relief="ridge", bd=2)
frame_top.pack(pady=10, fill="x")

tk.Label(frame_top, text="Input Image:", font=("Arial", 12, "bold"), fg=FG_TEXT, bg=BG_FRAME).grid(row=0, column=0, sticky="w")
entry_input = tk.Entry(frame_top, width=60)
entry_input.grid(row=0, column=1, padx=5)
tk.Button(frame_top, text="📂 Browse", command=select_file, bg=BTN_ENCRYPT, fg="white").grid(row=0, column=2, padx=5)

tk.Label(frame_top, text="Output Image:", font=("Arial", 12, "bold"), fg=FG_TEXT, bg=BG_FRAME).grid(row=1, column=0, sticky="w")
entry_output = tk.Entry(frame_top, width=60)
entry_output.grid(row=1, column=1, padx=5)
tk.Button(frame_top, text="💾 Save As", command=save_file, bg=BTN_DECRYPT, fg="black").grid(row=1, column=2, padx=5)

tk.Label(frame_top, text="Key (0-255):", font=("Arial", 12, "bold"), fg=FG_TEXT, bg=BG_FRAME).grid(row=2, column=0, sticky="w", pady=10)
entry_key = tk.Entry(frame_top, width=15, font=("Arial", 12))
entry_key.grid(row=2, column=1, sticky="w")


frame_buttons = tk.Frame(root, bg=BG_MAIN)
frame_buttons.pack(pady=15)

tk.Button(frame_buttons, text="🔑 Encrypt", command=lambda: run_task("Encrypt"),
          font=("Arial", 12, "bold"), bg=BTN_ENCRYPT, fg="white", width=15).grid(row=0, column=0, padx=20)

tk.Button(frame_buttons, text="🔓 Decrypt", command=lambda: run_task("Decrypt"),
          font=("Arial", 12, "bold"), bg=BTN_DECRYPT, fg="black", width=15).grid(row=0, column=1, padx=20)


preview_frame = tk.Frame(root, bg=BG_MAIN)
preview_frame.pack(pady=20)

tk.Label(preview_frame, text="Original Image", font=("Arial", 12, "bold"), fg=FG_TEXT, bg=BG_MAIN).grid(row=0, column=0, padx=40)
tk.Label(preview_frame, text="Processed Image", font=("Arial", 12, "bold"), fg=FG_TEXT, bg=BG_MAIN).grid(row=0, column=1, padx=40)

preview_input = tk.Label(preview_frame, bg=BG_FRAME, width=250, height=250)
preview_input.grid(row=1, column=0, padx=20, pady=10)

preview_output = tk.Label(preview_frame, bg=BG_FRAME, width=250, height=250)
preview_output.grid(row=1, column=1, padx=20, pady=10)

root.mainloop()

