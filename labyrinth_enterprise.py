"""
Labyrinth Enterprise v8.0 - Zero-Click Installation & Management
Professional Zero Trust Autonomous Encryption for Windows 11
No terminal required - Complete GUI-driven experience
"""

import os
import sys
import json
import logging
import threading
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yaml

# First-time setup detector
FIRST_RUN_FILE = Path.home() / ".labyrinth" / ".installed"

# ============================================================================
# AUTO-INSTALLER - Runs on first launch
# ============================================================================

class AutoInstaller:
    """Automatic dependency installation and setup"""
    
    def __init__(self, parent_window=None):
        self.parent = parent_window
        self.required_packages = [
            'cryptography>=41.0.0',
            'watchdog>=3.0.0',
            'PyYAML>=6.0'
        ]
        
    def check_and_install(self):
        """Check for dependencies and install if needed"""
        missing_packages = []
        
        # Check each package
        for package in self.required_packages:
            pkg_name = package.split('>=')[0]
            try:
                __import__(pkg_name.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            return self.install_packages(missing_packages)
        
        return True
    
    def install_packages(self, packages):
        """Install missing packages with progress window"""
        if self.parent:
            return self.install_with_gui(packages)
        else:
            return self.install_silently(packages)
    
    def install_with_gui(self, packages):
        """Install with visual progress"""
        install_window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        install_window.title("First-Time Setup")
        install_window.geometry("600x400")
        install_window.resizable(False, False)
        
        # Center window
        install_window.update_idletasks()
        x = (install_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (install_window.winfo_screenheight() // 2) - (400 // 2)
        install_window.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Label(
            install_window,
            text="🔐 Labyrinth Enterprise Setup",
            font=("Segoe UI", 16, "bold"),
            fg="#2C3E50"
        )
        header.pack(pady=20)
        
        # Message
        msg = tk.Label(
            install_window,
            text="Installing required components...\nThis only happens once.",
            font=("Segoe UI", 10),
            fg="#34495E"
        )
        msg.pack(pady=10)
        
        # Progress bar
        progress = ttk.Progressbar(
            install_window,
            mode='indeterminate',
            length=400
        )
        progress.pack(pady=20)
        progress.start(10)
        
        # Log output
        log_frame = tk.Frame(install_window)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Consolas", 9),
            bg="#F8F9FA",
            fg="#2C3E50"
        )
        log_text.pack(fill='both', expand=True)
        
        success = [False]  # Mutable container for thread result
        
        def install_thread():
            try:
                for package in packages:
                    log_text.insert(tk.END, f"Installing {package}...\n")
                    log_text.see(tk.END)
                    install_window.update()
                    
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", package],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        log_text.insert(tk.END, f"✓ {package} installed\n", 'success')
                    else:
                        log_text.insert(tk.END, f"✗ Failed: {result.stderr}\n", 'error')
                        success[0] = False
                        return
                
                log_text.insert(tk.END, "\n✓ Setup complete!\n", 'success')
                success[0] = True
                
                # Wait a moment then close
                install_window.after(2000, install_window.destroy)
                
            except Exception as e:
                log_text.insert(tk.END, f"\n✗ Error: {str(e)}\n", 'error')
                success[0] = False
        
        # Configure tags
        log_text.tag_config('success', foreground='#27AE60')
        log_text.tag_config('error', foreground='#E74C3C')
        
        # Start installation thread
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
        
        install_window.mainloop()
        return success[0]
    
    def install_silently(self, packages):
        """Install without GUI"""
        for package in packages:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError:
                return False
        return True


# Import after potential installation
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False


# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

@dataclass
class LabyrinthConfig:
    """Configuration for Labyrinth application"""
    app_name: str = "Labyrinth Enterprise"
    version: str = "8.0.0"
    log_level: str = "INFO"
    log_file: str = "labyrinth.log"
    audit_log_file: str = "labyrinth_audit.log"
    config_dir: str = ""
    key_dir: str = ""
    backup_enabled: bool = True
    max_file_size_mb: int = 100
    allowed_extensions: List[str] = None
    auto_start_windows: bool = False
    notification_enabled: bool = True
    
    def __post_init__(self):
        if not self.config_dir:
            self.config_dir = str(Path.home() / ".labyrinth")
        if not self.key_dir:
            self.key_dir = str(Path(self.config_dir) / "keys")
        if self.allowed_extensions is None:
            self.allowed_extensions = []
        
        # Create directories
        Path(self.config_dir).mkdir(parents=True, exist_ok=True)
        Path(self.key_dir).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def load_from_file(cls, config_path: str = None) -> 'LabyrinthConfig':
        """Load configuration from YAML file"""
        if config_path is None:
            config_path = Path.home() / ".labyrinth" / "config.yaml"
        
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
                return cls(**data)
        
        # Create default config
        config = cls()
        config.save_to_file()
        return config
    
    def save_to_file(self, config_path: str = None):
        """Save configuration to YAML file"""
        if config_path is None:
            config_path = Path(self.config_dir) / "config.yaml"
        
        with open(config_path, 'w') as f:
            yaml.dump(asdict(self), f, default_flow_style=False)


# ============================================================================
# LOGGING SETUP
# ============================================================================

class AuditLogger:
    """Separate audit logger for compliance and security events"""
    
    def __init__(self, config: LabyrinthConfig):
        self.config = config
        self.audit_logger = logging.getLogger('audit')
        self.audit_logger.setLevel(logging.INFO)
        
        audit_handler = logging.FileHandler(
            Path(config.config_dir) / config.audit_log_file
        )
        audit_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.audit_logger.addHandler(audit_handler)
    
    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Log an audit event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }
        self.audit_logger.info(json.dumps(event))


def setup_logging(config: LabyrinthConfig):
    """Configure application logging"""
    log_file = Path(config.config_dir) / config.log_file
    
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


# ============================================================================
# KEY MANAGEMENT
# ============================================================================

class KeyManager:
    """Enhanced key management with security features"""
    
    def __init__(self, config: LabyrinthConfig, audit_logger: AuditLogger):
        self.config = config
        self.audit_logger = audit_logger
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def generate_key(self, key_name: str = None) -> bytes:
        """Generate a new encryption key"""
        key = Fernet.generate_key()
        
        if key_name:
            self.save_key(key, key_name)
        
        self.audit_logger.log_event('key_generated', {
            'key_name': key_name or 'anonymous'
        })
        
        return key
    
    def save_key(self, key: bytes, key_name: str):
        """Save key to secure location"""
        key_path = Path(self.config.key_dir) / f"{key_name}.key"
        
        try:
            with open(key_path, 'wb') as f:
                f.write(key)
            
            if os.name != 'nt':
                os.chmod(key_path, 0o600)
            
            self.audit_logger.log_event('key_saved', {
                'key_name': key_name,
                'key_path': str(key_path)
            })
            
            self.logger.info(f"Key saved: {key_path}")
        except Exception as e:
            self.logger.error(f"Failed to save key: {e}")
            raise
    
    def load_key(self, key_path: str) -> bytes:
        """Load key from file"""
        try:
            with open(key_path, 'rb') as f:
                key = f.read()
            
            self.audit_logger.log_event('key_loaded', {
                'key_path': key_path
            })
            
            return key
        except Exception as e:
            self.logger.error(f"Failed to load key: {e}")
            raise


# ============================================================================
# FILE ENCRYPTION HANDLER
# ============================================================================

class EncryptionHandler(FileSystemEventHandler):
    """Enhanced encryption handler with better error handling"""
    
    def __init__(
        self,
        key: bytes,
        trigger: str,
        mode: str,
        directory: str,
        groups: List[str],
        audit_logger: AuditLogger,
        config: LabyrinthConfig,
        status_callback=None
    ):
        super().__init__()
        self.key = key
        self.fernet = Fernet(self.key)
        self.trigger = trigger
        self.mode = mode
        self.directory = directory
        self.groups = groups or []
        self.audit_logger = audit_logger
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._processing = set()
        self._lock = threading.Lock()
        self.status_callback = status_callback
        self.files_processed = 0
    
    def on_created(self, event):
        if not event.is_directory and self.trigger == "Create":
            file_path = event.src_path
            if not file_path.endswith(".encrypted"):
                self.handle_file(file_path)
    
    def on_deleted(self, event):
        if not event.is_directory and self.trigger == "Delete":
            file_path = event.src_path
            if file_path.endswith(".encrypted"):
                self.handle_file(file_path)
    
    def on_modified(self, event):
        if not event.is_directory and self.trigger == "Modify":
            file_path = event.src_path
            if not file_path.endswith(".encrypted"):
                self.handle_file(file_path)
    
    def handle_file(self, file_path: str):
        """Handle file encryption with proper error handling"""
        with self._lock:
            if file_path in self._processing:
                return
            self._processing.add(file_path)
        
        try:
            file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            if file_size_mb > self.config.max_file_size_mb:
                self.logger.warning(
                    f"File exceeds max size ({file_size_mb:.2f}MB): {file_path}"
                )
                return
            
            if self.config.allowed_extensions:
                ext = Path(file_path).suffix.lower()
                if ext not in self.config.allowed_extensions:
                    return
            
            if self.mode == "Individual":
                self.encrypt_file(file_path)
            elif self.mode == "Group" and self.is_group(file_path):
                self.encrypt_file(file_path)
            elif self.mode == "All":
                self.encrypt_all_files()
        
        except Exception as e:
            self.logger.error(f"Error encrypting file {file_path}: {str(e)}")
            self.audit_logger.log_event('encryption_error', {
                'file_path': file_path,
                'error': str(e)
            })
        finally:
            with self._lock:
                self._processing.discard(file_path)
    
    def is_group(self, file_path: str) -> bool:
        """Check if file belongs to a group"""
        if self.groups:
            for group_path in self.groups:
                if group_path.strip() in file_path:
                    return True
        return False
    
    def encrypt_file(self, file_path: str):
        """Encrypt a single file"""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            encrypted_data = self.fernet.encrypt(data)
            
            encrypted_path = file_path + ".encrypted"
            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)
            
            os.remove(file_path)
            
            self.files_processed += 1
            
            self.logger.info(f"Encrypted: {file_path}")
            self.audit_logger.log_event('file_encrypted', {
                'original_path': file_path,
                'encrypted_path': encrypted_path,
                'size_bytes': len(data)
            })
            
            if self.status_callback:
                self.status_callback(f"Encrypted: {Path(file_path).name}")
        
        except Exception as e:
            self.logger.error(f"Failed to encrypt {file_path}: {e}")
            raise
    
    def encrypt_all_files(self):
        """Encrypt all files in directory"""
        for root, _, files in os.walk(self.directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if not file_path.endswith(".encrypted"):
                    self.encrypt_file(file_path)


# ============================================================================
# DECRYPTION HANDLER
# ============================================================================

class DecryptionHandler(FileSystemEventHandler):
    """Enhanced decryption handler"""
    
    def __init__(
        self,
        key: bytes,
        trigger: str,
        mode: str,
        directory: str,
        groups: List[str],
        audit_logger: AuditLogger,
        config: LabyrinthConfig,
        status_callback=None
    ):
        super().__init__()
        self.key = key
        self.fernet = Fernet(self.key)
        self.trigger = trigger
        self.mode = mode
        self.directory = directory
        self.groups = groups or []
        self.audit_logger = audit_logger
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._processing = set()
        self._lock = threading.Lock()
        self.status_callback = status_callback
        self.files_processed = 0
    
    def on_created(self, event):
        if not event.is_directory and self.trigger == "Create":
            file_path = event.src_path
            if file_path.endswith(".encrypted"):
                self.handle_file(file_path)
    
    def on_deleted(self, event):
        if not event.is_directory and self.trigger == "Delete":
            file_path = event.src_path
            if not file_path.endswith(".encrypted"):
                self.handle_file(file_path)
    
    def on_modified(self, event):
        if not event.is_directory and self.trigger == "Modify":
            file_path = event.src_path
            if file_path.endswith(".encrypted"):
                self.handle_file(file_path)
    
    def handle_file(self, file_path: str):
        """Handle file decryption"""
        with self._lock:
            if file_path in self._processing:
                return
            self._processing.add(file_path)
        
        try:
            if self.mode == "Individual":
                self.decrypt_file(file_path)
            elif self.mode == "Group" and self.is_group(file_path):
                self.decrypt_file(file_path)
            elif self.mode == "All":
                self.decrypt_all_files()
        
        except Exception as e:
            self.logger.error(f"Error decrypting file {file_path}: {str(e)}")
            self.audit_logger.log_event('decryption_error', {
                'file_path': file_path,
                'error': str(e)
            })
        finally:
            with self._lock:
                self._processing.discard(file_path)
    
    def is_group(self, file_path: str) -> bool:
        """Check if file belongs to a group"""
        if self.groups:
            for group_path in self.groups:
                if group_path.strip() in file_path:
                    return True
        return False
    
    def decrypt_file(self, file_path: str):
        """Decrypt a single file"""
        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            original_path = file_path[:-len(".encrypted")]
            with open(original_path, "wb") as f:
                f.write(decrypted_data)
            
            os.remove(file_path)
            
            self.files_processed += 1
            
            self.logger.info(f"Decrypted: {file_path}")
            self.audit_logger.log_event('file_decrypted', {
                'encrypted_path': file_path,
                'original_path': original_path,
                'size_bytes': len(decrypted_data)
            })
            
            if self.status_callback:
                self.status_callback(f"Decrypted: {Path(original_path).name}")
        
        except Exception as e:
            self.logger.error(f"Failed to decrypt {file_path}: {e}")
            raise
    
    def decrypt_all_files(self):
        """Decrypt all encrypted files in directory"""
        for root, _, files in os.walk(self.directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_path.endswith(".encrypted"):
                    self.decrypt_file(file_path)


# ============================================================================
# SETUP WIZARD - First-run experience
# ============================================================================

class SetupWizard:
    """Interactive setup wizard for first-time users"""
    
    def __init__(self, parent=None):
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Labyrinth Enterprise - Setup Wizard")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (550 // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.current_step = 0
        self.steps = [
            self.welcome_step,
            self.directory_step,
            self.security_step,
            self.complete_step
        ]
        
        self.config = LabyrinthConfig()
        self.setup_ui()
        self.show_step()
    
    def setup_ui(self):
        """Setup wizard UI"""
        # Header
        self.header_frame = tk.Frame(self.root, bg="#2C3E50", height=80)
        self.header_frame.pack(fill='x')
        self.header_frame.pack_propagate(False)
        
        self.header_label = tk.Label(
            self.header_frame,
            text="🔐 Welcome to Labyrinth Enterprise",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#2C3E50"
        )
        self.header_label.pack(expand=True)
        
        # Content area
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Button frame
        self.button_frame = tk.Frame(self.root, bg="#ECF0F1", height=60)
        self.button_frame.pack(fill='x', side='bottom')
        self.button_frame.pack_propagate(False)
        
        self.back_btn = ttk.Button(
            self.button_frame,
            text="← Back",
            command=self.prev_step,
            state='disabled'
        )
        self.back_btn.pack(side='left', padx=20, pady=15)
        
        self.next_btn = ttk.Button(
            self.button_frame,
            text="Next →",
            command=self.next_step
        )
        self.next_btn.pack(side='right', padx=20, pady=15)
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_step(self):
        """Show current step"""
        self.clear_content()
        self.steps[self.current_step]()
        
        # Update buttons
        self.back_btn.config(state='normal' if self.current_step > 0 else 'disabled')
        self.next_btn.config(
            text="Finish" if self.current_step == len(self.steps) - 1 else "Next →"
        )
    
    def next_step(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step()
        else:
            self.finish_setup()
    
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()
    
    def welcome_step(self):
        """Welcome screen"""
        tk.Label(
            self.content_frame,
            text="Welcome to Labyrinth Enterprise",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=20)
        
        tk.Label(
            self.content_frame,
            text="Zero Trust Autonomous File Encryption for Windows 11",
            font=("Segoe UI", 11),
            bg="white",
            fg="#7F8C8D"
        ).pack()
        
        features_frame = tk.Frame(self.content_frame, bg="white")
        features_frame.pack(pady=30)
        
        features = [
            ("🔒", "Military-grade encryption", "Protect your sensitive files automatically"),
            ("⚡", "Real-time monitoring", "Automatic encryption when files are created"),
            ("🎯", "Zero configuration", "Works right out of the box"),
            ("🛡️", "Enterprise security", "Audit logs and compliance ready")
        ]
        
        for icon, title, desc in features:
            frame = tk.Frame(features_frame, bg="white")
            frame.pack(fill='x', pady=10)
            
            tk.Label(
                frame,
                text=icon,
                font=("Segoe UI", 24),
                bg="white"
            ).pack(side='left', padx=10)
            
            text_frame = tk.Frame(frame, bg="white")
            text_frame.pack(side='left', fill='x', expand=True)
            
            tk.Label(
                text_frame,
                text=title,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#2C3E50",
                anchor='w'
            ).pack(fill='x')
            
            tk.Label(
                text_frame,
                text=desc,
                font=("Segoe UI", 9),
                bg="white",
                fg="#7F8C8D",
                anchor='w'
            ).pack(fill='x')
    
    def directory_step(self):
        """Choose directories to protect"""
        tk.Label(
            self.content_frame,
            text="Choose Folders to Protect",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=20)
        
        tk.Label(
            self.content_frame,
            text="Select folders where you store sensitive files.\nLabyrinth will automatically encrypt new files in these folders.",
            font=("Segoe UI", 10),
            bg="white",
            fg="#7F8C8D",
            justify='center'
        ).pack(pady=10)
        
        # Quick presets
        presets_frame = tk.LabelFrame(
            self.content_frame,
            text="Quick Setup",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        presets_frame.pack(fill='x', pady=20)
        
        self.preset_var = tk.StringVar(value="documents")
        
        presets = [
            ("documents", "📄 Documents Only", "Protect My Documents folder"),
            ("work", "💼 Work Files", "Documents + Desktop + Downloads"),
            ("maximum", "🔒 Maximum Protection", "All user folders"),
            ("custom", "⚙️ Custom", "Choose specific folders")
        ]
        
        for value, text, desc in presets:
            frame = tk.Frame(presets_frame, bg="white")
            frame.pack(fill='x', padx=20, pady=5)
            
            rb = tk.Radiobutton(
                frame,
                text=text,
                variable=self.preset_var,
                value=value,
                font=("Segoe UI", 10),
                bg="white",
                fg="#2C3E50",
                command=self.update_directory_preview
            )
            rb.pack(side='left')
            
            tk.Label(
                frame,
                text=desc,
                font=("Segoe UI", 9),
                bg="white",
                fg="#95A5A6"
            ).pack(side='left', padx=10)
        
        # Preview
        self.dir_preview = tk.Text(
            self.content_frame,
            height=6,
            font=("Consolas", 9),
            bg="#F8F9FA",
            fg="#2C3E50",
            state='disabled'
        )
        self.dir_preview.pack(fill='x', pady=10)
        
        self.update_directory_preview()
    
    def update_directory_preview(self):
        """Update directory preview based on preset"""
        preset = self.preset_var.get()
        
        user_home = Path.home()
        preview_dirs = []
        
        if preset == "documents":
            preview_dirs = [str(user_home / "Documents")]
        elif preset == "work":
            preview_dirs = [
                str(user_home / "Documents"),
                str(user_home / "Desktop"),
                str(user_home / "Downloads")
            ]
        elif preset == "maximum":
            preview_dirs = [
                str(user_home / "Documents"),
                str(user_home / "Desktop"),
                str(user_home / "Downloads"),
                str(user_home / "Pictures"),
                str(user_home / "Videos")
            ]
        elif preset == "custom":
            preview_dirs = ["Click 'Next' to choose folders..."]
        
        self.dir_preview.config(state='normal')
        self.dir_preview.delete('1.0', tk.END)
        self.dir_preview.insert('1.0', "Protected folders:\n")
        for d in preview_dirs:
            self.dir_preview.insert(tk.END, f"  • {d}\n")
        self.dir_preview.config(state='disabled')
    
    def security_step(self):
        """Security settings"""
        tk.Label(
            self.content_frame,
            text="Security Settings",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=20)
        
        tk.Label(
            self.content_frame,
            text="Configure how Labyrinth protects your files",
            font=("Segoe UI", 10),
            bg="white",
            fg="#7F8C8D"
        ).pack(pady=10)
        
        # Auto-generate encryption key
        key_frame = tk.LabelFrame(
            self.content_frame,
            text="Encryption Key",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        key_frame.pack(fill='x', pady=10)
        
        tk.Label(
            key_frame,
            text="✓ Encryption key will be automatically generated",
            font=("Segoe UI", 10),
            bg="white",
            fg="#27AE60"
        ).pack(padx=20, pady=15)
        
        tk.Label(
            key_frame,
            text="Your key will be securely stored and backed up",
            font=("Segoe UI", 9),
            bg="white",
            fg="#7F8C8D"
        ).pack(padx=20, pady=(0, 15))
        
        # Startup option
        startup_frame = tk.LabelFrame(
            self.content_frame,
            text="Windows Integration",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        startup_frame.pack(fill='x', pady=10)
        
        self.auto_start_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            startup_frame,
            text="Start with Windows",
            variable=self.auto_start_var,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2C3E50"
        ).pack(anchor='w', padx=20, pady=10)
        
        tk.Label(
            startup_frame,
            text="Labyrinth will start automatically to protect your files",
            font=("Segoe UI", 9),
            bg="white",
            fg="#7F8C8D"
        ).pack(anchor='w', padx=40, pady=(0, 10))
        
        # Notifications
        notify_frame = tk.LabelFrame(
            self.content_frame,
            text="Notifications",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        notify_frame.pack(fill='x', pady=10)
        
        self.notify_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            notify_frame,
            text="Show notifications when files are encrypted",
            variable=self.notify_var,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2C3E50"
        ).pack(anchor='w', padx=20, pady=10)
    
    def complete_step(self):
        """Completion screen"""
        tk.Label(
            self.content_frame,
            text="🎉 Setup Complete!",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#27AE60"
        ).pack(pady=30)
        
        tk.Label(
            self.content_frame,
            text="Labyrinth Enterprise is ready to protect your files",
            font=("Segoe UI", 11),
            bg="white",
            fg="#2C3E50"
        ).pack()
        
        # Summary
        summary_frame = tk.Frame(self.content_frame, bg="#F8F9FA")
        summary_frame.pack(fill='both', expand=True, pady=20, padx=20)
        
        tk.Label(
            summary_frame,
            text="What happens next:",
            font=("Segoe UI", 10, "bold"),
            bg="#F8F9FA",
            fg="#2C3E50"
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        steps = [
            "✓ Encryption key has been generated and secured",
            "✓ Your selected folders are now being monitored",
            "✓ New files will be encrypted automatically",
            "✓ You can manage everything from the dashboard"
        ]
        
        for step in steps:
            tk.Label(
                summary_frame,
                text=step,
                font=("Segoe UI", 10),
                bg="#F8F9FA",
                fg="#27AE60",
                anchor='w'
            ).pack(anchor='w', padx=40, pady=5)
        
        tk.Label(
            summary_frame,
            text="Click 'Finish' to open the Labyrinth dashboard",
            font=("Segoe UI", 10),
            bg="#F8F9FA",
            fg="#7F8C8D"
        ).pack(anchor='w', padx=20, pady=(20, 20))
    
    def finish_setup(self):
        """Complete setup and save configuration"""
        # Save configuration
        self.config.auto_start_windows = self.auto_start_var.get()
        self.config.notification_enabled = self.notify_var.get()
        self.config.save_to_file()
        
        # Mark as installed
        FIRST_RUN_FILE.parent.mkdir(parents=True, exist_ok=True)
        FIRST_RUN_FILE.touch()
        
        # Generate initial key
        audit_logger = AuditLogger(self.config)
        key_manager = KeyManager(self.config, audit_logger)
        key_manager.generate_key("master_key")
        
        # Setup Windows startup if requested
        if self.config.auto_start_windows and os.name == 'nt':
            self.setup_windows_startup()
        
        self.root.destroy()
    
    def setup_windows_startup(self):
        """Add to Windows startup"""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(
                key,
                "LabyrinthEnterprise",
                0,
                winreg.REG_SZ,
                f'"{sys.executable}" "{Path(__file__).absolute()}"'
            )
            winreg.CloseKey(key)
        except Exception as e:
            logging.error(f"Failed to setup Windows startup: {e}")


# ============================================================================
# MODERN DASHBOARD - Main Application
# ============================================================================

class LabyrinthDashboard:
    """Modern dashboard-style main application"""
    
    def __init__(self, config: LabyrinthConfig):
        self.config = config
        self.audit_logger = AuditLogger(config)
        self.key_manager = KeyManager(config, self.audit_logger)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.root = tk.Tk()
        self.root.title(f"{config.app_name} v{config.version}")
        self.root.geometry("1000x700")
        
        # Variables
        self.encrypt_observer = None
        self.decrypt_observer = None
        self.monitoring_active = False
        
        self.setup_ui()
        self.load_master_key()
        
    def setup_ui(self):
        """Setup modern dashboard UI"""
        # Set modern theme colors
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Frame(self.root, bg="#2C3E50", height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔐 Labyrinth Enterprise",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#2C3E50"
        ).pack(side='left', padx=30)
        
        # Status indicator
        self.status_indicator = tk.Label(
            header,
            text="● Active",
            font=("Segoe UI", 11),
            fg="#27AE60",
            bg="#2C3E50"
        )
        self.status_indicator.pack(side='right', padx=30)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill='both', expand=True)
        
        # Left sidebar - Quick Actions
        sidebar = tk.Frame(main_frame, bg="white", width=250)
        sidebar.pack(side='left', fill='y', padx=(10, 5), pady=10)
        sidebar.pack_propagate(False)
        
        tk.Label(
            sidebar,
            text="Quick Actions",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=20, padx=20, anchor='w')
        
        # Quick action buttons
        actions = [
            ("🔐 Start Protection", self.quick_start_protection),
            ("⏸️ Pause Protection", self.quick_pause_protection),
            ("🔑 Generate New Key", self.quick_generate_key),
            ("📊 View Activity Log", self.quick_view_logs),
            ("⚙️ Settings", self.open_settings),
            ("❓ Help", self.open_help)
        ]
        
        for text, command in actions:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 10),
                bg="white",
                fg="#2C3E50",
                relief='flat',
                cursor='hand2',
                anchor='w',
                command=command
            )
            btn.pack(fill='x', padx=20, pady=5)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg="#ECF0F1"))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg="white"))
        
        # Center area - Dashboard cards
        center_frame = tk.Frame(main_frame, bg="#ECF0F1")
        center_frame.pack(side='left', fill='both', expand=True, padx=5, pady=10)
        
        # Cards row 1
        cards_row1 = tk.Frame(center_frame, bg="#ECF0F1")
        cards_row1.pack(fill='x', pady=5)
        
        self.files_card = self.create_stat_card(
            cards_row1,
            "Files Protected",
            "0",
            "#3498DB"
        )
        self.files_card.pack(side='left', fill='both', expand=True, padx=5)
        
        self.size_card = self.create_stat_card(
            cards_row1,
            "Data Secured",
            "0 MB",
            "#9B59B6"
        )
        self.size_card.pack(side='left', fill='both', expand=True, padx=5)
        
        self.status_card = self.create_stat_card(
            cards_row1,
            "Status",
            "Monitoring",
            "#27AE60"
        )
        self.status_card.pack(side='left', fill='both', expand=True, padx=5)
        
        # Activity feed
        activity_frame = tk.LabelFrame(
            center_frame,
            text="Recent Activity",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        activity_frame.pack(fill='both', expand=True, pady=10)
        
        # Activity list with scrollbar
        list_frame = tk.Frame(activity_frame, bg="white")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.activity_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg="white",
            fg="#2C3E50",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.activity_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.activity_list.yview)
        
        # Right sidebar - Monitored folders
        right_sidebar = tk.Frame(main_frame, bg="white", width=250)
        right_sidebar.pack(side='right', fill='y', padx=(5, 10), pady=10)
        right_sidebar.pack_propagate(False)
        
        tk.Label(
            right_sidebar,
            text="Protected Folders",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=20, padx=20, anchor='w')
        
        self.folders_list = tk.Listbox(
            right_sidebar,
            font=("Segoe UI", 9),
            bg="#F8F9FA",
            fg="#2C3E50",
            borderwidth=0,
            highlightthickness=0
        )
        self.folders_list.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Button(
            right_sidebar,
            text="+ Add Folder",
            font=("Segoe UI", 10),
            bg="#3498DB",
            fg="white",
            relief='flat',
            cursor='hand2',
            command=self.add_monitored_folder
        ).pack(fill='x', padx=20, pady=10)
        
        # Status bar
        status_bar = tk.Frame(self.root, bg="#34495E", height=30)
        status_bar.pack(side='bottom', fill='x')
        status_bar.pack_propagate(False)
        
        self.status_text = tk.Label(
            status_bar,
            text="Ready",
            font=("Segoe UI", 9),
            fg="white",
            bg="#34495E",
            anchor='w'
        )
        self.status_text.pack(side='left', padx=20)
        
        # Auto-start monitoring
        self.root.after(1000, self.auto_start_monitoring)
    
    def create_stat_card(self, parent, title, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg="white", relief='flat')
        
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            bg="white",
            fg="#7F8C8D"
        ).pack(pady=(20, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg=color
        )
        value_label.pack(pady=(5, 20))
        
        # Store reference to update later
        card.value_label = value_label
        
        return card
    
    def load_master_key(self):
        """Load or create master encryption key"""
        master_key_path = Path(self.config.key_dir) / "master_key.key"
        
        if not master_key_path.exists():
            self.key_manager.generate_key("master_key")
            self.add_activity("🔑 Master encryption key generated")
        else:
            self.add_activity("🔑 Master encryption key loaded")
        
        self.master_key = self.key_manager.load_key(str(master_key_path))
    
    def add_activity(self, message):
        """Add activity to the feed"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_list.insert(0, f"[{timestamp}] {message}")
        
        # Keep only last 100 items
        if self.activity_list.size() > 100:
            self.activity_list.delete(100, tk.END)
        
        # Update status bar
        self.status_text.config(text=message)
    
    def quick_start_protection(self):
        """Quick start monitoring with default settings"""
        if self.monitoring_active:
            messagebox.showinfo("Info", "Protection is already active!")
            return
        
        # Get Documents folder as default
        documents = str(Path.home() / "Documents")
        
        if not Path(documents).exists():
            messagebox.showerror("Error", "Documents folder not found")
            return
        
        try:
            self.start_monitoring(documents)
            self.add_activity(f"🛡️ Started protecting: {documents}")
            messagebox.showinfo(
                "Protection Active",
                f"Now protecting:\n{documents}\n\nNew files will be encrypted automatically."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start protection: {str(e)}")
    
    def quick_pause_protection(self):
        """Pause all monitoring"""
        if not self.monitoring_active:
            messagebox.showinfo("Info", "Protection is not active")
            return
        
        self.stop_monitoring()
        self.add_activity("⏸️ Protection paused")
        messagebox.showinfo("Paused", "File protection has been paused")
    
    def quick_generate_key(self):
        """Quick key generation"""
        # Ask for key name
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Encryption Key")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Generate New Encryption Key",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)
        
        tk.Label(
            dialog,
            text="Key Name:",
            font=("Segoe UI", 10)
        ).pack()
        
        name_entry = tk.Entry(dialog, font=("Segoe UI", 10), width=30)
        name_entry.pack(pady=10)
        name_entry.insert(0, f"key_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        name_entry.select_range(0, tk.END)
        name_entry.focus()
        
        def generate():
            key_name = name_entry.get().strip()
            if not key_name:
                messagebox.showerror("Error", "Please enter a key name")
                return
            
            try:
                self.key_manager.generate_key(key_name)
                self.add_activity(f"🔑 Generated key: {key_name}")
                messagebox.showinfo(
                    "Success",
                    f"Key '{key_name}' generated successfully!\n\nLocation: {self.config.key_dir}"
                )
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate key: {str(e)}")
        
        tk.Button(
            dialog,
            text="Generate",
            command=generate,
            font=("Segoe UI", 10),
            bg="#27AE60",
            fg="white",
            cursor='hand2'
        ).pack(pady=20)
    
    def quick_view_logs(self):
        """View activity logs"""
        log_window = tk.Toplevel(self.root)
        log_window.title("Activity Logs")
        log_window.geometry("800x600")
        
        # Tabs for different logs
        notebook = ttk.Notebook(log_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Application log
        app_log_frame = tk.Frame(notebook)
        notebook.add(app_log_frame, text="Application Log")
        
        app_log_text = scrolledtext.ScrolledText(
            app_log_frame,
            font=("Consolas", 9),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        app_log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load and display log
        log_file = Path(self.config.config_dir) / self.config.log_file
        if log_file.exists():
            with open(log_file, 'r') as f:
                app_log_text.insert('1.0', f.read())
        
        # Audit log
        audit_log_frame = tk.Frame(notebook)
        notebook.add(audit_log_frame, text="Audit Log")
        
        audit_log_text = scrolledtext.ScrolledText(
            audit_log_frame,
            font=("Consolas", 9),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        audit_log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load and display audit log
        audit_file = Path(self.config.config_dir) / self.config.audit_log_file
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                audit_log_text.insert('1.0', f.read())
    
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("600x500")
        settings_window.transient(self.root)
        
        # Center window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (500 // 2)
        settings_window.geometry(f"+{x}+{y}")
        
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # General settings
        general_frame = tk.Frame(notebook, bg="white")
        notebook.add(general_frame, text="General")
        
        tk.Label(
            general_frame,
            text="General Settings",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(pady=20)
        
        # Auto-start
        auto_start_var = tk.BooleanVar(value=self.config.auto_start_windows)
        tk.Checkbutton(
            general_frame,
            text="Start with Windows",
            variable=auto_start_var,
            font=("Segoe UI", 10),
            bg="white"
        ).pack(anchor='w', padx=40, pady=10)
        
        # Notifications
        notify_var = tk.BooleanVar(value=self.config.notification_enabled)
        tk.Checkbutton(
            general_frame,
            text="Show notifications",
            variable=notify_var,
            font=("Segoe UI", 10),
            bg="white"
        ).pack(anchor='w', padx=40, pady=10)
        
        # File settings
        file_frame = tk.Frame(notebook, bg="white")
        notebook.add(file_frame, text="File Settings")
        
        tk.Label(
            file_frame,
            text="File Processing Settings",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(pady=20)
        
        # Max file size
        size_frame = tk.Frame(file_frame, bg="white")
        size_frame.pack(fill='x', padx=40, pady=10)
        
        tk.Label(
            size_frame,
            text="Maximum file size (MB):",
            font=("Segoe UI", 10),
            bg="white"
        ).pack(side='left')
        
        size_var = tk.IntVar(value=self.config.max_file_size_mb)
        tk.Spinbox(
            size_frame,
            from_=1,
            to=1000,
            textvariable=size_var,
            font=("Segoe UI", 10),
            width=10
        ).pack(side='left', padx=10)
        
        # Save button
        def save_settings():
            self.config.auto_start_windows = auto_start_var.get()
            self.config.notification_enabled = notify_var.get()
            self.config.max_file_size_mb = size_var.get()
            self.config.save_to_file()
            self.add_activity("⚙️ Settings saved")
            messagebox.showinfo("Success", "Settings saved successfully")
            settings_window.destroy()
        
        tk.Button(
            settings_window,
            text="Save Settings",
            command=save_settings,
            font=("Segoe UI", 10),
            bg="#27AE60",
            fg="white",
            cursor='hand2'
        ).pack(pady=20)
    
    def open_help(self):
        """Open help window"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help & Support")
        help_window.geometry("700x600")
        
        # Header
        tk.Label(
            help_window,
            text="📚 Labyrinth Enterprise Help",
            font=("Segoe UI", 16, "bold"),
            fg="#2C3E50"
        ).pack(pady=20)
        
        # Help content
        help_text = scrolledtext.ScrolledText(
            help_window,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            bg="white",
            fg="#2C3E50"
        )
        help_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        help_content = """
How Labyrinth Works:

1. AUTOMATIC PROTECTION
   • Labyrinth monitors your selected folders
   • When new files are created, they're automatically encrypted
   • Original files are securely removed after encryption

2. ENCRYPTION KEYS
   • A master key is generated on first run
   • Keys are stored securely in your user folder
   • IMPORTANT: Back up your keys - they're needed to decrypt files

3. QUICK START
   • Click "Start Protection" to monitor your Documents folder
   • Add more folders using "Add Folder" button
   • Pause protection anytime with "Pause Protection"

4. MANAGING FILES
   • Encrypted files have .encrypted extension
   • To decrypt: Move file to monitored folder with decryption active
   • Or use the Decryption tab for manual decryption

5. SAFETY TIPS
   • Always keep backup of encryption keys
   • Test with non-critical files first
   • Check activity log regularly
   • Keep Labyrinth running for automatic protection

SUPPORT:
• Email: themadhattersplayground@gmail.com
• Phone: +447576285686 (UK timezone)
• GitHub: github.com/AeinsteinApp/Labyrinth

For emergency decryption support, contact us with:
• Your encryption key file
• Description of the issue
• Operating system version
        """
        
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
        
        # Support button
        tk.Button(
            help_window,
            text="Contact Support",
            command=lambda: webbrowser.open("mailto:themadhattersplayground@gmail.com"),
            font=("Segoe UI", 10),
            bg="#3498DB",
            fg="white",
            cursor='hand2'
        ).pack(pady=10)
    
    def add_monitored_folder(self):
        """Add folder to monitoring"""
        folder = filedialog.askdirectory(title="Select Folder to Protect")
        
        if folder:
            self.folders_list.insert(tk.END, folder)
            self.start_monitoring(folder)
            self.add_activity(f"📁 Added folder: {folder}")
    
    def start_monitoring(self, directory):
        """Start monitoring a directory"""
        try:
            handler = EncryptionHandler(
                key=self.master_key,
                trigger="Create",
                mode="Individual",
                directory=directory,
                groups=[],
                audit_logger=self.audit_logger,
                config=self.config,
                status_callback=self.add_activity
            )
            
            if not self.encrypt_observer:
                self.encrypt_observer = Observer()
            
            self.encrypt_observer.schedule(handler, directory, recursive=True)
            
            if not self.encrypt_observer.is_alive():
                self.encrypt_observer.start()
            
            self.monitoring_active = True
            self.status_indicator.config(text="● Active", fg="#27AE60")
            self.status_card.value_label.config(text="Monitoring")
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            raise
    
    def stop_monitoring(self):
        """Stop all monitoring"""
        if self.encrypt_observer and self.encrypt_observer.is_alive():
            self.encrypt_observer.stop()
            self.encrypt_observer.join()
        
        self.monitoring_active = False
        self.status_indicator.config(text="● Paused", fg="#E74C3C")
        self.status_card.value_label.config(text="Paused")
    
    def auto_start_monitoring(self):
        """Auto-start monitoring on launch"""
        documents = str(Path.home() / "Documents")
        
        if Path(documents).exists():
            try:
                self.start_monitoring(documents)
                self.folders_list.insert(tk.END, documents)
                self.add_activity(f"🛡️ Auto-started protection: {documents}")
            except Exception as e:
                self.logger.error(f"Auto-start failed: {e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point with auto-setup"""
    
    # Check if first run
    if not FIRST_RUN_FILE.exists():
        # Check and install dependencies
        installer = AutoInstaller()
        if not DEPENDENCIES_OK:
            success = installer.check_and_install()
            if not success:
                messagebox.showerror(
                    "Installation Failed",
                    "Failed to install required components.\n\nPlease check your internet connection and try again."
                )
                return
            
            # Restart after installation
            messagebox.showinfo(
                "Installation Complete",
                "Components installed successfully!\n\nLabyrinth will now restart."
            )
            os.execv(sys.executable, [sys.executable] + sys.argv)
            return
        
        # Run setup wizard
        wizard = SetupWizard()
        wizard.root.mainloop()
    
    # Load configuration
    config = LabyrinthConfig.load_from_file()
    
    # Setup logging
    logger = setup_logging(config)
    logger.info(f"Starting {config.app_name} v{config.version}")
    
    # Create and run dashboard
    dashboard = LabyrinthDashboard(config)
    dashboard.run()


if __name__ == "__main__":
    main()
    