import tkinter as tk
from tkinter import filedialog
import binary_data_handler
import huffman_coding
from tkinter import ttk

def compress_image():
    image_path = image_path_entry.get()
    image_bit_string = binary_data_handler.read_image_bit_string(image_path)
    compressed_image_bit_string = huffman_coding.compress(image_bit_string)
    compressed_path = "IO/Outputs/compressed_image.bin"
    binary_data_handler.save_data(compressed_image_bit_string, compressed_path, 'image')
    compression_ratio = len(image_bit_string) / len(compressed_image_bit_string)
    compression_ratio_label.config(text=f"Compression Ratio (CR): {compression_ratio:.2f}")

def decompress_image():
    compressed_path = "IO/Outputs/compressed_image.bin"
    compressed_image_bit_string = binary_data_handler.read_image_bit_string(compressed_path)
    decompressed_image_bit_string = huffman_coding.decompress(compressed_image_bit_string)
    decompressed_path = "IO/Outputs/decompressed_image.jpg"
    binary_data_handler.save_data(decompressed_image_bit_string, decompressed_path, 'image')
    decompression_complete_label.config(text="Decompression Complete!")

def browse_image_path():
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bin")])
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, image_path)

# Create the main window
root = tk.Tk()
root.title("Image Compression Tool")

# Create and set a custom style
style = ttk.Style()
style.theme_use("clam")  # Choose a style theme (options: "default", "alt", "classic", "clam")

# Create and place widgets
image_path_label = ttk.Label(root, text="Image Path:")
image_path_label.pack(pady=10)

image_path_entry = ttk.Entry(root)
image_path_entry.pack(pady=5, fill=tk.X)

browse_button = ttk.Button(root, text="Browse", command=browse_image_path)
browse_button.pack(pady=5)

compress_button = ttk.Button(root, text="Compress Image", command=compress_image)
compress_button.pack(pady=5)

decompress_button = ttk.Button(root, text="Decompress Image", command=decompress_image)
decompress_button.pack(pady=5)

compression_ratio_label = ttk.Label(root, text="Compression Ratio (CR):")
compression_ratio_label.pack(pady=5)

decompression_complete_label = ttk.Label(root, text="")
decompression_complete_label.pack(pady=10)

root.mainloop()
