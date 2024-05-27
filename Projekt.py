import tkinter as tk  
from tkinter import filedialog, messagebox 
from PIL import Image, ImageTk, ImageDraw  
import numpy as np  
from scipy.fftpack import fft2, fftshift  
import pyperclip  
import io  
import matplotlib.pyplot as plt  
import math  

def open_file():
    """Otwiera okno do wyboru obrazu"""
    global img, img_path, display_img
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        load_image(file_path)


def load_image(file_path):
    """Ładuje obraz i wyświetla go w oknie."""
    global img, img_path, display_img
    img_path = file_path
    img = Image.open(file_path)
    img.thumbnail((500, 500))  
    display_img = img.copy()
    img_tk = ImageTk.PhotoImage(display_img)
    img_label.config(image=img_tk)
    img_label.image = img_tk  


def save_file():
    """Zapisuje obraz do wybranej ścieżki"""
    global img
    if img:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if save_path:
            img.save(save_path)
            messagebox.showinfo("Info", "Image saved successfully")
    else:
        messagebox.showwarning("Warning", "No image to save")

def copy_image():
    """Kopiuje bieżący obraz do schowka."""
    global img
    if img:
        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        pyperclip.copy(data)
        messagebox.showinfo("Info", "Image copied to clipboard")
    else:
        messagebox.showwarning("Warning", "No image to copy")

def convert_to_8bit():
    """Konwertuje bieżący obraz na skalę szarości (8-bit)."""
    global img, display_img
    if img:
        bw_image = img.convert("L")
        display_img = bw_image.copy()
        img_tk = ImageTk.PhotoImage(display_img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
        img = bw_image
    else:
        messagebox.showwarning("Warning", "No image to convert")

def calculate_fourier():
    """Oblicza i wyświetla transformatę Fouriera obrazu."""
    global img
    if img:
        img_array = np.array(img)
        f_transform = fft2(img_array)
        f_transform_shifted = fftshift(f_transform)
        magnitude_spectrum = np.abs(f_transform_shifted)
        plt.figure()
        plt.imshow(np.log(1 + magnitude_spectrum), cmap="gray")
        plt.title("Fourier Transform")
        plt.show()
    else:
        messagebox.showwarning("Warning", "No image to perform Fourier transform on")

def on_click(event):
    """Obsługuje kliknięcia myszką na obrazie, rejestruje współrzędne punktów i pokazuje zaznaczone punkty."""
    global points, display_img
    x, y = event.x, event.y
    points.append((x, y))
    draw = ImageDraw.Draw(display_img)
    radius = 5
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline="red", width=2)
    img_tk = ImageTk.PhotoImage(display_img)
    img_label.config(image=img_tk)
    img_label.image = img_tk
    if len(points) == 2:
        calculate_distance()

def calculate_distance():
    """Oblicza i wyświetla odległość między dwoma punktami na obrazie."""
    global points, display_img
    (x1, y1), (x2, y2) = points
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    messagebox.showinfo("Distance", f"The distance between the points is {distance:.2f} pixels")
    points = []
    display_img = img.copy()
    img_tk = ImageTk.PhotoImage(display_img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

root = tk.Tk()
root.title("Image Viewer")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy", command=copy_image)
edit_menu.add_command(label="Convert to 8-bit", command=convert_to_8bit)
edit_menu.add_command(label="Calculate Fourier Transform", command=calculate_fourier)

measure_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Measure", menu=measure_menu)
measure_menu.add_command(label="Measure Distance", command=lambda: img_label.bind("<Button-1>", on_click))

img_label = tk.Label(root)
img_label.pack()

points = []

root.mainloop()
