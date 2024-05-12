import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk for the styled widgets
import os
import threading
from PIL import Image
import imageio

def convert_and_save_image(dds_image, img_path, img_format, jpg_quality):
    image = Image.fromarray(dds_image)
    if image.mode == 'RGBA':
        image = image.convert("RGB")
    if img_format.upper() == 'JPEG' and jpg_quality is not None:
        image.save(img_path, format=img_format.upper(), quality=jpg_quality)
    else:
        image.save(img_path, format=img_format.upper())

def dds_to_image(dds_path, output_folder, img_format, jpg_quality):
    try:
        img_path = os.path.join(output_folder, os.path.splitext(os.path.basename(dds_path))[0] + f'.{img_format.lower()}')
        dds_image = imageio.imread(dds_path)
        convert_and_save_image(dds_image, img_path, img_format, jpg_quality)
        return True
    except Exception as e:
        return str(e)

def batch_convert_dds_to_images(input_folder, output_folder, img_format, jpg_quality, progress_var, status_var, update_gui_callback):
    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith('.dds')]
    total_files = len(files)
    progress_var.set(0)
    for index, file in enumerate(files):
        result = dds_to_image(file, output_folder, img_format, jpg_quality)
        if isinstance(result, str):
            status_var.set(f"Error: {result}")
        progress_var.set((index + 1) / total_files * 100)
        update_gui_callback()
    status_var.set("Conversion Complete")

class DDSConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title('DDS to Image Converter')

        self.tab_control = ttk.Notebook(self.root)
        self.tab_single = ttk.Frame(self.tab_control)
        self.tab_batch = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_single, text='Single Image Conversion')
        self.tab_control.add(self.tab_batch, text='Batch Conversion')
        self.tab_control.pack(expand=1, fill="both")

        self.setup_single_tab()
        self.setup_batch_tab()

    def setup_single_tab(self):
        # Single Image Tab Setup
        self.single_input_label = ttk.Label(self.tab_single, text="Input DDS File:")
        self.single_input_label.grid(row=0, column=0, sticky='w')
        self.single_input_entry = ttk.Entry(self.tab_single, width=50)
        self.single_input_entry.grid(row=0, column=1)
        self.single_input_button = ttk.Button(self.tab_single, text="Browse", command=self.browse_single_input)
        self.single_input_button.grid(row=0, column=2)

        self.single_output_label = ttk.Label(self.tab_single, text="Output Folder:")
        self.single_output_label.grid(row=1, column=0, sticky='w')
        self.single_output_entry = ttk.Entry(self.tab_single, width=50)
        self.single_output_entry.grid(row=1, column=1)
        self.single_output_button = ttk.Button(self.tab_single, text="Browse", command=self.browse_output)
        self.single_output_button.grid(row=1, column=2)

        self.single_format_label = ttk.Label(self.tab_single, text="Image Format:")
        self.single_format_label.grid(row=2, column=0, sticky='w')
        self.single_format_combobox = ttk.Combobox(self.tab_single, values=['PNG', 'JPG', 'JPEG', 'TIFF', 'BMP'], state="readonly")
        self.single_format_combobox.grid(row=2, column=1, sticky='w')
        self.single_format_combobox.set('PNG')
        self.single_format_combobox.bind('<<ComboboxSelected>>', self.update_quality_state_single)

        self.single_quality_label = ttk.Label(self.tab_single, text="JPEG Quality:")
        self.single_quality_label.grid(row=2, column=2, sticky='w', padx=(10,0))  # Adjusted position
        self.single_quality_scale = tk.Scale(self.tab_single, from_=1, to=100, orient='horizontal', resolution=5)
        self.single_quality_scale.set(100)  # Default quality
        self.single_quality_scale.grid(row=2, column=3, sticky='w')  # Adjusted position
        self.update_quality_state_single()  # Initial call to set visibility

        self.single_convert_button = ttk.Button(self.tab_single, text="Convert", command=self.start_single_conversion)
        self.single_convert_button.grid(row=3, column=1, pady=10)

        self.single_status_var = tk.StringVar(value="Ready")
        self.single_status_label = ttk.Label(self.tab_single, textvariable=self.single_status_var, relief='sunken', anchor='w')
        self.single_status_label.grid(row=4, column=0, columnspan=3, sticky='ew')

    def setup_batch_tab(self):
        # Batch Image Tab Setup
        self.batch_input_label = ttk.Label(self.tab_batch, text="Input Folder:")
        self.batch_input_label.grid(row=0, column=0, sticky='w')
        self.batch_input_entry = ttk.Entry(self.tab_batch, width=50)
        self.batch_input_entry.grid(row=0, column=1)
        self.batch_input_button = ttk.Button(self.tab_batch, text="Browse", command=self.browse_batch_input)
        self.batch_input_button.grid(row=0, column=2)

        self.batch_output_label = ttk.Label(self.tab_batch, text="Output Folder:")
        self.batch_output_label.grid(row=1, column=0, sticky='w')
        self.batch_output_entry = ttk.Entry(self.tab_batch, width=50)
        self.batch_output_entry.grid(row=1, column=1)
        self.batch_output_button = ttk.Button(self.tab_batch, text="Browse", command=self.browse_output)
        self.batch_output_button.grid(row=1, column=2)

        self.batch_format_label = ttk.Label(self.tab_batch, text="Image Format:")
        self.batch_format_label.grid(row=2, column=0, sticky='w')
        self.batch_format_combobox = ttk.Combobox(self.tab_batch, values=['PNG', 'JPG', 'JPEG', 'TIFF', 'BMP'], state="readonly")
        self.batch_format_combobox.grid(row=2, column=1, sticky='w')
        self.batch_format_combobox.set('PNG')
        self.batch_format_combobox.bind('<<ComboboxSelected>>', self.update_quality_state_batch)

        self.batch_quality_label = ttk.Label(self.tab_batch, text="JPEG Quality:")
        self.batch_quality_label.grid(row=2, column=2, sticky='w', padx=(10,0))  # Adjusted position
        self.batch_quality_scale = tk.Scale(self.tab_batch, from_=1, to=100, orient='horizontal', resolution=5)
        self.batch_quality_scale.set(100)  # Default quality
        self.batch_quality_scale.grid(row=2, column=3, sticky='w')  # Adjusted position
        self.update_quality_state_batch()  # Initial call to set visibility

        self.batch_convert_button = ttk.Button(self.tab_batch, text="Convert", command=self.start_batch_conversion)
        self.batch_convert_button.grid(row=3, column=1, pady=10)

        self.batch_progress_var = tk.DoubleVar()
        self.batch_progress = ttk.Progressbar(self.tab_batch, orient='horizontal', length=400, mode='determinate', variable=self.batch_progress_var)
        self.batch_progress.grid(row=4, column=0, columnspan=3, pady=10)
        self.batch_status_var = tk.StringVar(value="Ready")
        self.batch_status_label = ttk.Label(self.tab_batch, textvariable=self.batch_status_var, relief='sunken', anchor='w')
        self.batch_status_label.grid(row=5, column=0, columnspan=3, sticky='ew')

    def browse_single_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("DDS Files", "*.dds")])
        if file_path:
            self.single_input_entry.delete(0, tk.END)
            self.single_input_entry.insert(0, file_path)

    def browse_batch_input(self):
        directory = filedialog.askdirectory()
        if directory:
            self.batch_input_entry.delete(0, tk.END)
            self.batch_input_entry.insert(0, directory)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.single_output_entry.delete(0, tk.END)
            self.single_output_entry.insert(0, directory)
            self.batch_output_entry.delete(0, tk.END)
            self.batch_output_entry.insert(0, directory)

    def start_single_conversion(self):
        input_file = self.single_input_entry.get()
        output_folder = self.single_output_entry.get()
        img_format = self.single_format_combobox.get()
        jpg_quality = int(self.single_quality_scale.get()) if self.single_quality_scale.winfo_viewable() else None

        if not input_file or not output_folder:
            messagebox.showerror("Error", "Please specify both input file and output directory.")
            return

        threading.Thread(target=dds_to_image, args=(
            input_file, output_folder, img_format, jpg_quality
        )).start()

    def start_batch_conversion(self):
        input_folder = self.batch_input_entry.get()
        output_folder = self.batch_output_entry.get()
        img_format = self.batch_format_combobox.get()
        jpg_quality = int(self.batch_quality_scale.get()) if self.batch_quality_scale.winfo_viewable() else None

        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please specify both input and output directories.")
            return

        threading.Thread(target=batch_convert_dds_to_images, args=(
            input_folder, output_folder, img_format, jpg_quality,
            self.batch_progress_var, self.batch_status_var, self.update_gui_batch
        )).start()

    def update_quality_state_single(self, event=None):
        if self.single_format_combobox.get() in ['JPG', 'JPEG']:
            self.single_quality_label.grid()
            self.single_quality_scale.grid()
        else:
            self.single_quality_label.grid_remove()
            self.single_quality_scale.grid_remove()

    def update_quality_state_batch(self, event=None):
        if self.batch_format_combobox.get() in ['JPG', 'JPEG']:
            self.batch_quality_label.grid()
            self.batch_quality_scale.grid()
        else:
            self.batch_quality_label.grid_remove()
            self.batch_quality_scale.grid_remove()

    def update_gui_single(self):
        self.single_status_label.update_idletasks()

    def update_gui_batch(self):
        self.batch_progress.update_idletasks()
        self.batch_status_label.update_idletasks()

if __name__ == '__main__':
    root = tk.Tk()
    app = DDSConverterApp(root)
    root.mainloop()
