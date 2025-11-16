"""
Labyrinth Enterprise - One-Click Windows Installer
Double-click to install - No terminal needed!
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
import threading
import shutil
import winreg

class LabyrinthInstaller:
    """One-click installer for Windows"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Labyrinth Enterprise - Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.install_dir = Path.home() / "AppData" / "Local" / "LabyrinthEnterprise"
        self.start_menu_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Labyrinth Enterprise"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup installer UI"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2C3E50", height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔐 Labyrinth Enterprise",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#2C3E50"
        ).pack(pady=10)
        
        tk.Label(
            header_frame,
            text="Zero Trust File Encryption for Windows 11",
            font=("Segoe UI", 11),
            fg="#ECF0F1",
            bg="#2C3E50"
        ).pack()
        
        # Content
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        tk.Label(
            content_frame,
            text="Welcome to Labyrinth Enterprise Setup",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=20)
        
        tk.Label(
            content_frame,
            text="This wizard will install Labyrinth Enterprise on your computer.\n\n" +
                 "Features:\n" +
                 "  • Automatic file encryption\n" +
                 "  • Zero-configuration setup\n" +
                 "  • Windows 11 integration\n" +
                 "  • Enterprise-grade security",
            font=("Segoe UI", 10),
            bg="white",
            fg="#34495E",
            justify='left'
        ).pack(pady=10)
        
        # Installation location
        location_frame = tk.LabelFrame(
            content_frame,
            text="Installation Location",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        location_frame.pack(fill='x', pady=20)
        
        tk.Label(
            location_frame,
            text=str(self.install_dir),
            font=("Segoe UI", 9),
            bg="white",
            fg="#7F8C8D"
        ).pack(pady=10)
        
        # Options
        options_frame = tk.LabelFrame(
            content_frame,
            text="Options",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        options_frame.pack(fill='x', pady=10)
        
        self.desktop_shortcut_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Create desktop shortcut",
            variable=self.desktop_shortcut_var,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2C3E50"
        ).pack(anchor='w', padx=20, pady=5)
        
        self.start_menu_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Create Start Menu entry",
            variable=self.start_menu_var,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2C3E50"
        ).pack(anchor='w', padx=20, pady=5)
        
        self.auto_start_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Start with Windows",
            variable=self.auto_start_var,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2C3E50"
        ).pack(anchor='w', padx=20, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#ECF0F1", height=60)
        button_frame.pack(fill='x', side='bottom')
        button_frame.pack_propagate(False)
        
        self.install_btn = tk.Button(
            button_frame,
            text="Install",
            font=("Segoe UI", 11, "bold"),
            bg="#27AE60",
            fg="white",
            cursor='hand2',
            command=self.start_installation,
            width=15
        )
        self.install_btn.pack(side='right', padx=20, pady=15)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 10),
            bg="#95A5A6",
            fg="white",
            cursor='hand2',
            command=self.root.quit,
            width=12
        ).pack(side='right', padx=5, pady=15)
    
    def start_installation(self):
        """Begin installation process"""
        self.install_btn.config(state='disabled')
        
        # Show progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Installing...")
        progress_window.geometry("500x300")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Center progress window
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (300 // 2)
        progress_window.geometry(f"+{x}+{y}")
        
        tk.Label(
            progress_window,
            text="Installing Labyrinth Enterprise",
            font=("Segoe UI", 14, "bold"),
            fg="#2C3E50"
        ).pack(pady=20)
        
        progress = ttk.Progressbar(
            progress_window,
            mode='indeterminate',
            length=400
        )
        progress.pack(pady=20)
        progress.start(10)
        
        status_label = tk.Label(
            progress_window,
            text="Preparing installation...",
            font=("Segoe UI", 10),
            fg="#7F8C8D"
        )
        status_label.pack(pady=10)
        
        # Log area
        from tkinter import scrolledtext
        log_text = scrolledtext.ScrolledText(
            progress_window,
            height=8,
            font=("Consolas", 8),
            bg="#F8F9FA",
            fg="#2C3E50"
        )
        log_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        def log(message):
            log_text.insert(tk.END, f"{message}\n")
            log_text.see(tk.END)
            progress_window.update()
        
        def install_thread():
            try:
                # Step 1: Create directories
                status_label.config(text="Creating directories...")
                log("Creating installation directory...")
                self.install_dir.mkdir(parents=True, exist_ok=True)
                log(f"✓ Created: {self.install_dir}")
                
                # Step 2: Copy files
                status_label.config(text="Copying files...")
                log("Copying application files...")
                
                # Get script directory
                script_dir = Path(__file__).parent
                
                # Copy main application
                app_file = script_dir / "labyrinth_enterprise.py"
                if app_file.exists():
                    shutil.copy2(app_file, self.install_dir / "labyrinth_enterprise.py")
                    log("✓ Copied: labyrinth_enterprise.py")
                
                # Copy config template
                config_file = script_dir / "config.yaml"
                if config_file.exists():
                    shutil.copy2(config_file, self.install_dir / "config.yaml")
                    log("✓ Copied: config.yaml")
                
                # Step 3: Install Python dependencies
                status_label.config(text="Installing dependencies...")
                log("Installing required packages...")
                
                packages = ['cryptography', 'watchdog', 'PyYAML']
                for package in packages:
                    log(f"Installing {package}...")
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", package],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        log(f"✓ {package} installed")
                    else:
                        log(f"⚠ {package} installation warning (may already exist)")
                
                # Step 4: Create Start Menu shortcut
                if self.start_menu_var.get():
                    status_label.config(text="Creating Start Menu entry...")
                    log("Creating Start Menu shortcut...")
                    self.create_start_menu_shortcut()
                    log("✓ Start Menu entry created")
                
                # Step 5: Create Desktop shortcut
                if self.desktop_shortcut_var.get():
                    status_label.config(text="Creating desktop shortcut...")
                    log("Creating desktop shortcut...")
                    self.create_desktop_shortcut()
                    log("✓ Desktop shortcut created")
                
                # Step 6: Setup auto-start
                if self.auto_start_var.get():
                    status_label.config(text="Configuring auto-start...")
                    log("Setting up Windows auto-start...")
                    self.setup_autostart()
                    log("✓ Auto-start configured")
                
                # Step 7: Create uninstaller
                status_label.config(text="Creating uninstaller...")
                log("Creating uninstaller...")
                self.create_uninstaller()
                log("✓ Uninstaller created")
                
                # Complete
                progress.stop()
                status_label.config(text="Installation complete!")
                log("\n✓ Installation completed successfully!")
                
                # Wait and close
                self.root.after(2000, lambda: self.installation_complete(progress_window))
                
            except Exception as e:
                progress.stop()
                log(f"\n✗ Error: {str(e)}")
                status_label.config(text="Installation failed!")
                messagebox.showerror("Installation Error", f"Installation failed:\n{str(e)}")
        
        # Start installation in thread
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
    
    def create_start_menu_shortcut(self):
        """Create Start Menu shortcut"""
        self.start_menu_dir.mkdir(parents=True, exist_ok=True)
        
        shortcut_path = self.start_menu_dir / "Labyrinth Enterprise.lnk"
        target = str(self.install_dir / "labyrinth_enterprise.py")
        
        self.create_shortcut(str(shortcut_path), target)
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Labyrinth Enterprise.lnk"
        target = str(self.install_dir / "labyrinth_enterprise.py")
        
        self.create_shortcut(str(shortcut_path), target)
    
    def create_shortcut(self, shortcut_path, target):
        """Create Windows shortcut using VBScript"""
        vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{sys.executable}"
oLink.Arguments = "{target}"
oLink.WorkingDirectory = "{self.install_dir}"
oLink.Description = "Zero Trust File Encryption"
oLink.Save
'''
        
        vbs_file = self.install_dir / "create_shortcut.vbs"
        with open(vbs_file, 'w') as f:
            f.write(vbs_script)
        
        subprocess.run(['cscript', '//nologo', str(vbs_file)], check=True)
        vbs_file.unlink()
    
    def setup_autostart(self):
        """Add to Windows startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            value = f'"{sys.executable}" "{self.install_dir / "labyrinth_enterprise.py"}"'
            winreg.SetValueEx(key, "LabyrinthEnterprise", 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Failed to setup autostart: {e}")
    
    def create_uninstaller(self):
        """Create uninstaller script"""
        uninstaller_script = f'''
import os
import shutil
import winreg
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def uninstall():
    try:
        # Remove installation directory
        install_dir = Path(r"{self.install_dir}")
        if install_dir.exists():
            shutil.rmtree(install_dir)
        
        # Remove Start Menu entry
        start_menu = Path(r"{self.start_menu_dir}")
        if start_menu.exists():
            shutil.rmtree(start_menu)
        
        # Remove desktop shortcut
        desktop_shortcut = Path.home() / "Desktop" / "Labyrinth Enterprise.lnk"
        if desktop_shortcut.exists():
            desktop_shortcut.unlink()
        
        # Remove from startup
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, "LabyrinthEnterprise")
            winreg.CloseKey(key)
        except:
            pass
        
        messagebox.showinfo("Uninstall Complete", "Labyrinth Enterprise has been uninstalled.")
    except Exception as e:
        messagebox.showerror("Uninstall Error", f"Error during uninstall: {{str(e)}}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    result = messagebox.askyesno(
        "Uninstall Labyrinth Enterprise",
        "Are you sure you want to uninstall Labyrinth Enterprise?\\n\\n" +
        "Note: Your encryption keys will NOT be deleted."
    )
    
    if result:
        uninstall()
'''
        
        uninstaller_path = self.install_dir / "uninstall.py"
        with open(uninstaller_path, 'w') as f:
            f.write(uninstaller_script)
        
        # Create uninstaller shortcut in Start Menu
        if self.start_menu_var.get():
            shortcut_path = self.start_menu_dir / "Uninstall Labyrinth Enterprise.lnk"
            self.create_shortcut(str(shortcut_path), str(uninstaller_path))
    
    def installation_complete(self, progress_window):
        """Show completion message and launch app"""
        progress_window.destroy()
        
        result = messagebox.askyesno(
            "Installation Complete",
            "Labyrinth Enterprise has been installed successfully!\n\n" +
            "Would you like to launch it now?",
            icon='info'
        )
        
        if result:
            # Launch the application
            subprocess.Popen([
                sys.executable,
                str(self.install_dir / "labyrinth_enterprise.py")
            ])
        
        self.root.quit()
    
    def run(self):
        """Start the installer"""
        self.root.mainloop()


if __name__ == "__main__":
    installer = LabyrinthInstaller()
    installer.run()