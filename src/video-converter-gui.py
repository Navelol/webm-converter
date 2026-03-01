#!/usr/bin/env python3
"""
Video to WebM Converter - GUI Application
Simple drag-and-drop video converter with tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
from pathlib import Path

class VideoConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to WebM Converter")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Check if ffmpeg is installed
        if not self.check_ffmpeg():
            messagebox.showerror(
                "FFmpeg Not Found",
                "FFmpeg is not installed or not in PATH.\n\n"
                "Install it with:\n"
                "- Ubuntu/Debian: sudo apt install ffmpeg\n"
                "- Mac: brew install ffmpeg\n"
                "- Windows: Download from ffmpeg.org"
            )
            self.root.destroy()
            return
        
        self.input_file = None
        self.output_file = None
        self.converting = False
        
        self.setup_ui()
    
    def check_ffmpeg(self):
        """Check if ffmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title_frame = tk.Frame(self.root, bg="#667eea", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎬 Video to WebM Converter",
            font=("Arial", 20, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection section
        file_frame = tk.LabelFrame(content_frame, text="Input Video", padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            wraplength=500,
            justify=tk.LEFT,
            fg="gray"
        )
        self.file_label.pack(fill=tk.X, pady=(0, 10))
        
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack()
        
        tk.Button(
            btn_frame,
            text="Browse Files",
            command=self.browse_file,
            bg="#667eea",
            fg="white",
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Settings section
        settings_frame = tk.LabelFrame(content_frame, text="Conversion Settings", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Quality slider
        quality_frame = tk.Frame(settings_frame)
        quality_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT)
        
        self.quality_var = tk.IntVar(value=30)
        self.quality_label = tk.Label(quality_frame, text="Medium (CRF 30)", fg="#667eea", font=("Arial", 9, "bold"))
        self.quality_label.pack(side=tk.RIGHT)
        
        self.quality_slider = tk.Scale(
            settings_frame,
            from_=20,
            to=40,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            command=self.update_quality_label,
            showvalue=False,
            length=500
        )
        self.quality_slider.pack(fill=tk.X, pady=(0, 5))
        
        quality_hint = tk.Frame(settings_frame)
        quality_hint.pack(fill=tk.X)
        tk.Label(quality_hint, text="← Higher Quality", font=("Arial", 8), fg="gray").pack(side=tk.LEFT)
        tk.Label(quality_hint, text="Smaller File →", font=("Arial", 8), fg="gray").pack(side=tk.RIGHT)
        
        # Codec selection
        codec_frame = tk.Frame(settings_frame)
        codec_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(codec_frame, text="Codec:").pack(side=tk.LEFT)
        
        self.codec_var = tk.StringVar(value="vp9")
        codec_combo = ttk.Combobox(
            codec_frame,
            textvariable=self.codec_var,
            values=["vp9", "vp8"],
            state="readonly",
            width=30
        )
        codec_combo.pack(side=tk.LEFT, padx=10)
        codec_combo.set("vp9 (Recommended)")
        
        # Progress section
        progress_frame = tk.Frame(content_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=500
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to convert",
            fg="gray",
            font=("Arial", 9)
        )
        self.status_label.pack()
        
        # Convert button
        self.convert_btn = tk.Button(
            content_frame,
            text="Convert to WebM",
            command=self.convert_video,
            bg="#667eea",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.convert_btn.pack(fill=tk.X)
        
        # Info box
        info_frame = tk.Frame(content_frame, bg="#e3f2fd", relief=tk.FLAT)
        info_frame.pack(fill=tk.X, pady=(15, 0))
        
        info_text = tk.Label(
            info_frame,
            text="💡 Tip: Lower CRF values = higher quality & larger files\n"
                 "VP9 provides better compression than VP8",
            bg="#e3f2fd",
            fg="#1565c0",
            font=("Arial", 9),
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        info_text.pack()
    
    def update_quality_label(self, value):
        """Update the quality label based on slider value"""
        crf = int(float(value))
        if crf <= 25:
            label = "High"
        elif crf <= 32:
            label = "Medium"
        else:
            label = "Lower"
        self.quality_label.config(text=f"{label} (CRF {crf})")
    
    def browse_file(self):
        """Open file dialog to select video"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.input_file = filename
            self.file_label.config(
                text=f"📁 {os.path.basename(filename)}\n{filename}",
                fg="black"
            )
            self.convert_btn.config(state=tk.NORMAL)
            
            # Suggest output filename
            base = os.path.splitext(filename)[0]
            self.output_file = base + ".webm"
    
    def convert_video(self):
        """Start video conversion in a separate thread"""
        if not self.input_file or self.converting:
            return
        
        # Ask for output location
        output = filedialog.asksaveasfilename(
            title="Save WebM As",
            defaultextension=".webm",
            initialfile=os.path.basename(self.output_file),
            filetypes=[("WebM files", "*.webm"), ("All files", "*.*")]
        )
        
        if not output:
            return
        
        self.output_file = output
        self.converting = True
        
        # Update UI
        self.convert_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Converting... Please wait", fg="orange")
        self.progress_bar.start(10)
        
        # Run conversion in thread
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()
    
    def run_conversion(self):
        """Run the actual ffmpeg conversion"""
        try:
            # Get settings
            crf = self.quality_var.get()
            codec_text = self.codec_var.get()
            codec = "libvpx-vp9" if "vp9" in codec_text else "libvpx"
            
            # Build ffmpeg command
            cmd = [
                'ffmpeg',
                '-i', self.input_file,
                '-c:v', codec,
                '-pix_fmt', 'yuva420p',  # ADD THIS for alpha transparency
                '-crf', str(crf),
                '-b:v', '0',
                '-c:a', 'libopus',
                '-b:a', '128k',
                '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                '-auto-alt-ref', '0',  # ADD THIS to prevent VP9 errors with alpha
                '-y',
                self.output_file
            ]
            
            # Run conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            # Check result
            if result.returncode == 0:
                self.root.after(0, self.conversion_success)
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.root.after(0, lambda: self.conversion_failed(error_msg))
                
        except Exception as e:
            self.root.after(0, lambda: self.conversion_failed(str(e)))
    
    def conversion_success(self):
        """Handle successful conversion"""
        self.converting = False
        self.progress_bar.stop()
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="✅ Conversion complete!", fg="green")
        
        # Get file sizes
        input_size = os.path.getsize(self.input_file) / (1024 * 1024)
        output_size = os.path.getsize(self.output_file) / (1024 * 1024)
        
        message = (
            f"Conversion successful!\n\n"
            f"Input: {input_size:.2f} MB\n"
            f"Output: {output_size:.2f} MB\n"
            f"Saved to: {self.output_file}"
        )
        
        messagebox.showinfo("Success", message)
    
    def conversion_failed(self, error):
        """Handle failed conversion"""
        self.converting = False
        self.progress_bar.stop()
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="❌ Conversion failed", fg="red")
        
        messagebox.showerror(
            "Conversion Failed",
            f"An error occurred during conversion:\n\n{error[:500]}"
        )


def main():
    root = tk.Tk()
    app = VideoConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()