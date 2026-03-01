# 🎬 Video to WebM Converter

A simple, easy-to-use GUI application for converting video files (AVI, MP4, MKV, MOV, etc.) to WebM format.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)

## Features

- 🎨 **Clean GUI Interface** - Easy to use graphical interface
- 🖱️ **Simple File Selection** - Click to browse and select video files
- ⚙️ **Quality Control** - Adjustable quality settings (CRF 20-40)
- 🔄 **Codec Selection** - Choose between VP9 (better compression) or VP8 (faster)
- 📊 **Progress Indicator** - See conversion progress in real-time
- ✅ **File Size Comparison** - Compare original and converted file sizes
- 🔒 **Local Processing** - Everything runs on your computer, no uploads
- 💻 **Cross-Platform** - Works on Windows, macOS, and Linux

## Screenshots
<img width="599" height="499" alt="image" src="https://github.com/user-attachments/assets/78c678b9-73d5-4d56-ad30-f37ac595874f" />


## Installation

### Prerequisites

This project has **no pip packages** — see [requirements.txt](../requirements.txt) for details. You only need to install the following system-level dependencies:

1. **Python 3.6 or higher**
   - Check version: `python3 --version`
   - Download from: https://www.python.org/downloads/

2. **FFmpeg** (required for video conversion)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Windows:**
   - Download from: https://ffmpeg.org/download.html
   - Or use Chocolatey: `choco install ffmpeg`
   - Make sure FFmpeg is added to your system PATH

3. **Tkinter** (usually included with Python)
   
   If you get an error about tkinter, install it:
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install python3-tk
   ```
   
   **Fedora:**
   ```bash
   sudo dnf install python3-tkinter
   ```
   
   **macOS/Windows:** Already included with Python

### Quick Start

No pip installation needed! Just run:

```bash
python3 video-converter-gui.py
```

Or on Windows:
```bash
python video-converter-gui.py
```

## Usage

1. **Launch the application**
   ```bash
   python3 video-converter-gui.py
   ```

2. **Select a video file**
   - Click anywhere in the file selection area
   - Or click the "Browse Files" button
   - Choose your video file (MP4, AVI, MKV, MOV, etc.)

3. **Adjust settings (optional)**
   - **Quality Slider**: Lower CRF = higher quality (larger file)
     - CRF 20-25: High quality
     - CRF 26-32: Medium quality (recommended)
     - CRF 33-40: Lower quality (smaller file)
   - **Codec**: 
     - VP9: Better compression, smaller files (recommended)
     - VP8: Faster encoding, larger files

4. **Convert**
   - Click "Convert to WebM"
   - Choose where to save the output file
   - Wait for conversion to complete
   - Download/use your WebM file!

## Supported Input Formats

- MP4 (.mp4, .m4v)
- AVI (.avi)
- MKV (.mkv)
- MOV (.mov)
- FLV (.flv)
- WMV (.wmv)
- And many more video formats supported by FFmpeg

## Understanding Quality Settings

### CRF (Constant Rate Factor)
- **Lower values** (20-25) = Higher quality, larger file size
- **Medium values** (26-32) = Balanced quality and size (recommended)
- **Higher values** (33-40) = Lower quality, smaller file size

### Codec Comparison
| Feature | VP9 | VP8 |
|---------|-----|-----|
| Compression | Better | Good |
| File Size | Smaller | Larger |
| Encoding Speed | Slower | Faster |
| Quality | Better | Good |
| **Recommended** | ✅ Yes | For quick conversions |

## Troubleshooting

### "FFmpeg Not Found" Error
The application checks for FFmpeg on startup. If you see this error:
1. Make sure FFmpeg is installed
2. Verify it's in your system PATH:
   ```bash
   ffmpeg -version
   ```
3. If the command above doesn't work, reinstall FFmpeg and ensure it's added to PATH

### "Conversion Failed" Error
- Check that the input file is a valid video
- Ensure you have write permissions for the output location
- Check the console/terminal for detailed error messages
- Try a different quality setting or codec

### Tkinter Not Found
If you get "No module named tkinter":
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **Windows/macOS**: Reinstall Python from python.org

### Slow Conversion
VP9 encoding can be slow, especially for:
- Large video files
- High resolution videos (4K, 1080p)
- Lower CRF values (higher quality)

**Solutions:**
- Use VP8 codec for faster encoding
- Increase CRF value (lower quality, faster encoding)
- Be patient - quality encoding takes time!

## FAQ

**Q: Is my video uploaded anywhere?**  
A: No! Everything happens locally on your computer. Your videos never leave your machine.

**Q: What's WebM and why use it?**  
A: WebM is an open, royalty-free video format designed for the web. It offers:
- Excellent compression (smaller file sizes)
- High quality
- Wide browser support
- Open source and free

**Q: Can I convert multiple files at once?**  
A: Currently, the app converts one file at a time. You can convert another file immediately after finishing one.

**Q: How long does conversion take?**  
A: Depends on:
- File size and resolution
- Codec choice (VP8 is faster)
- Quality settings (higher CRF is faster)
- Your computer's CPU
  
Typical times: 1-5 minutes for a 100MB video on modern hardware.

**Q: Can I cancel a conversion?**  
A: Not in the current version. You can close the application, but this may leave an incomplete output file.

## Technical Details

### Built With
- **Python 3** - Core language
- **Tkinter** - GUI framework (included with Python)
- **FFmpeg** - Video conversion engine

### How It Works
1. User selects input video file
2. Application spawns FFmpeg subprocess with specified parameters
3. FFmpeg converts video to WebM format
4. Progress is displayed in the GUI
5. Upon completion, output file is ready to use

### FFmpeg Command
The application runs FFmpeg with these parameters:
```bash
ffmpeg -i input.mp4 \
  -c:v libvpx-vp9 \
  -crf 30 \
  -b:v 0 \
  -c:a libopus \
  -b:a 128k \
  -vf scale=trunc(iw/2)*2:trunc(ih/2)*2 \
  -y output.webm
```

## License

This project is free and open source. Use it however you like!

## Contributing

Found a bug? Have a feature request? Feel free to open an issue or submit a pull request!

## Credits

- Uses [FFmpeg](https://ffmpeg.org/) for video conversion
- Built with Python's tkinter library

## Support

If you encounter issues:
1. Check the Troubleshooting section
2. Ensure FFmpeg is properly installed
3. Verify your Python version is 3.6+
4. Check that input video is valid and not corrupted

---

**Made with ❤️ for easy video conversion**
