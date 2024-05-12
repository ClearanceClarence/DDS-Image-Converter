## DDS Image Converter

### Description
**Convert DDS files to multiple image formats using an easy-to-use GUI.**

### Key Features
- **Single File Conversion**: Convert individual DDS files effortlessly.
- **Batch Processing**: Transform multiple DDS files in one go.
- **Dynamic Quality Settings**: Adjust JPEG quality settings dynamically when JPG/JPEG is selected.

### Requirements
To run this script, you'll need the following:
- *Python 3.x* - A powerful, expressive scripting language.
- *Pillow* - The Python Imaging Library adds image processing capabilities.
- *imageio* - Provides an easy interface to read and write a wide range of image data.
- *Tkinter* - Standard GUI toolkit in Python.

*Before running the script, ensure you have the necessary libraries installed:*
```shell
pip install Pillow imageio
```

### Installation
1. Clone this repository or download the ZIP file.
2. Extract the files to a directory of your choice.
3. Open your command line interface (CLI) and navigate to the script directory.

### Usage
1. Start the application:
   ```shell
   python dds_converter.py
   ```
2. Once the GUI opens, follow these steps:
   - For single file conversion, click "Browse" to select your DDS file and set the output directory.
   - For batch processing, select the folder containing your DDS files.
   - Choose the desired output image format from the dropdown menu.
   - If converting to JPEG, adjust the quality using the slider that appears.
   - Click "Convert" to start the conversion process.
3. Check the output directory for your converted images.

### Contributing
Feel free to fork this project and submit pull requests. You can also open issues to discuss potential improvements or report bugs.

### License
This project is open-sourced under the GNU General Public License v3.0. For more details, see the full license at [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
