# 🔐 Labyrinth Enterprise v8.0 - Zero-Click Edition

![Logo](https://raw.githubusercontent.com/aeinsteinapp/User_Friendly_LabyrinthV8/main/

**Professional Zero Trust Autonomous File Encryption for Windows 11**

> No terminal. No configuration. Just double-click and you're protected.

[![Windows 11](https://img.shields.io/badge/Windows-11-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue?style=for-the-badge)](LICENSE)

---

## 🎯 What's New in v8.0 - Zero-Click Edition

### **Complete GUI Experience** - No Terminal Needed!
- ✅ **One-Click Installer** - Double-click `setup_windows.py` and you're done
- ✅ **Auto-Setup Wizard** - Guides you through first-time setup
- ✅ **Auto-Dependency Installation** - Installs everything automatically
- ✅ **Modern Dashboard** - Professional interface with real-time monitoring
- ✅ **Windows Integration** - Start Menu, Desktop shortcuts, Auto-start
- ✅ **Zero Configuration** - Works out of the box

### **Enterprise-Ready Features**
- 🔒 Military-grade encryption (Fernet/AES-256)
- ⚡ Real-time file monitoring
- 📊 Activity dashboard with statistics
- 🛡️ Automatic key generation and secure storage
- 📝 Comprehensive audit logging
- 🎯 Quick-start templates (Documents, Work Files, Maximum Protection)
- 🔔 Windows notifications
- ⚙️ Simple settings management

---

## 🚀 Installation (3 Easy Steps)

### Method 1: One-Click Installer (Recommended)

1. **Download** the repository
2. **Double-click** `setup_windows.py`
3. **Click** "Install"

That's it! No terminal, no commands, no configuration.

### Method 2: Direct Launch

1. **Double-click** `labyrinth_enterprise.py`
2. Follow the **Setup Wizard**
3. Start protecting your files!

The application will automatically:
- ✓ Check for required components
- ✓ Install missing dependencies
- ✓ Generate encryption keys
- ✓ Configure Windows integration
- ✓ Start monitoring your files

---

## 📖 Quick Start Guide

### First Launch - Setup Wizard

When you first run Labyrinth, the Setup Wizard guides you through:

#### Step 1: Welcome
Learn about Labyrinth's features and capabilities

#### Step 2: Choose Protection Level
Select from quick presets:
- **📄 Documents Only** - Protect My Documents folder
- **💼 Work Files** - Documents + Desktop + Downloads
- **🔒 Maximum Protection** - All user folders
- **⚙️ Custom** - Choose specific folders

#### Step 3: Security Settings
- ✓ Automatic encryption key generation
- ✓ Windows startup integration
- ✓ Notification preferences

#### Step 4: Complete!
Start protecting your files immediately

### Using the Dashboard

Once setup is complete, you'll see the **Labyrinth Dashboard**:

```
┌─────────────────────────────────────────────────────────┐
│  🔐 Labyrinth Enterprise              ● Active          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Quick Actions          Dashboard          Protected    │
│  ├ Start Protection    ┌────────┐         Folders       │
│  ├ Pause Protection    │  0     │         ├ Documents   │
│  ├ Generate Key        │ Files  │         ├ Desktop     │
│  ├ View Logs           └────────┘         └ Downloads   │
│  ├ Settings                                              │
│  └ Help                Recent Activity                   │
│                        ├ [12:30] File encrypted...       │
│                        ├ [12:29] Monitoring started      │
│                        └ [12:28] Key generated           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎮 Using Labyrinth

### Protection is Automatic

Once Labyrinth is running:

1. **Create a file** in a protected folder
2. **It's automatically encrypted** within seconds
3. **Original file removed** securely
4. **Encrypted file** has `.encrypted` extension

### Quick Actions

#### Start Protection
Click **"Start Protection"** to:
- Monitor your Documents folder
- Encrypt new files automatically
- See real-time activity

#### Pause Protection
Click **"Pause Protection"** to:
- Temporarily stop monitoring
- Make changes without encryption
- Resume anytime

#### Generate New Key
Click **"Generate New Key"** to:
- Create additional encryption keys
- Organize keys by project/purpose
- Store securely automatically

#### View Activity Log
Click **"View Activity Log"** to:
- See all encryption events
- Review audit trail
- Check for issues

---

## 🔐 How It Works

### Encryption Process

```
┌──────────────┐
│  New File    │
│  Created     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Labyrinth   │ ──► Detects file creation
│  Monitoring  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Encrypt     │ ──► Uses master key
│  with        │     (AES-256)
│  Fernet      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Save as     │ ──► filename.txt
│  .encrypted  │     → filename.txt.encrypted
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Remove      │ ──► Securely delete original
│  Original    │
└──────────────┘
```

### Security Features

- **AES-256 Encryption** - Military-grade security
- **Unique Keys** - Each installation generates unique keys
- **Secure Storage** - Keys stored in user's protected folder
- **Audit Logging** - Complete trail of all operations
- **No Cloud** - Everything stays on your computer

---

## ⚙️ Settings & Configuration

### Access Settings
Dashboard → **Quick Actions** → **Settings**

### Available Settings

#### General
- ✅ **Start with Windows** - Launch on system startup
- ✅ **Show Notifications** - Get alerts for encrypted files

#### File Settings
- 📏 **Maximum File Size** - Set file size limits (default: 100MB)
- 📑 **File Type Filtering** - Choose which file types to encrypt
- 🔄 **Backup Settings** - Configure backup options

#### Advanced
- 🔧 **Log Level** - Control logging detail
- 📁 **Key Location** - View/manage encryption keys
- 🛡️ **Security Options** - Additional security settings

---

## 📊 Understanding the Dashboard

### Statistics Cards

**Files Protected**
- Shows total number of encrypted files
- Updates in real-time

**Data Secured**
- Total size of encrypted data
- Displayed in MB/GB

**Status**
- Current monitoring state
- Active / Paused / Stopped

### Activity Feed

Shows recent events:
- `🔑 Key generated` - New encryption key created
- `🛡️ Started protecting` - Monitoring activated
- `🔐 Encrypted: filename.txt` - File encrypted
- `📁 Added folder` - New folder monitored

### Protected Folders

Lists all monitored folders:
- Click **"+ Add Folder"** to protect more locations
- Remove folders by right-clicking (future update)

---

## 🛡️ Security Best Practices

### Keep Your Keys Safe

**Encryption keys are stored at:**
```
C:\Users\[YourName]\.labyrinth\keys\
```

**Important:**
- ✅ Back up your keys to external drive
- ✅ Store backup in secure location
- ✅ Never share keys via email
- ✅ Test decryption periodically

### Backup Strategy

1. **Weekly** - Copy keys to external drive
2. **Monthly** - Copy keys to second location
3. **Before Updates** - Always backup before system updates
4. **Document** - Keep list of what you've encrypted

### What If I Lose My Keys?

**⚠️ Critical:** Without keys, files CANNOT be decrypted!

If keys are lost:
1. Contact support immediately: +447576285686
2. Cryptographic recovery possible (on-site visit required)
3. Keep copies of audit logs
4. Estimated recovery time: 24-48 hours

---

## 🔧 Troubleshooting

### Installation Issues

**"Failed to install components"**
- Check internet connection
- Run as Administrator
- Disable antivirus temporarily
- Check Windows Defender settings

**"Python not found"**
- Download Python from python.org
- Check "Add to PATH" during installation
- Restart computer

### Operation Issues

**"Files not being encrypted"**
- Check monitoring is Active (green indicator)
- Verify folder is in "Protected Folders" list
- Check file size doesn't exceed limit
- View Activity Log for errors

**"Can't start monitoring"**
- Ensure folder exists and is accessible
- Check you have write permissions
- Try different folder
- Check logs for specific error

**"Encrypted files too large"**
- Increase file size limit in Settings
- Or filter by file type
- Consider encrypting folders separately

### Recovery Issues

**"Can't decrypt files"**
- Ensure using correct encryption key
- Check file has `.encrypted` extension
- Verify key file hasn't been corrupted
- Contact support if issues persist

---

## 📞 Support & Help

### In-App Help
Dashboard → **Quick Actions** → **Help**

### Email Support
📧 themadhattersplayground@gmail.com

### Emergency Decryption
☎️ +447576285686 (UK timezone - GMT)

**When contacting support, include:**
- Windows version
- Python version
- Error messages from logs
- Screenshots if applicable

### GitHub Issues
🐛 [Report a Bug](https://github.com/AeinsteinApp/Labyrinth/issues)

---

## 🎓 Training & Best Practices

### For Individual Users

**First Week:**
- Day 1: Install and complete setup wizard
- Day 2: Test with non-critical files
- Day 3: Add important folders
- Day 4: Backup encryption keys
- Day 7: Review activity logs

**Monthly Tasks:**
- Backup encryption keys
- Review protected folders
- Check for updates
- Test file recovery

### For IT Administrators

**Deployment:**
1. Test in isolated environment
2. Create deployment package
3. Backup all encryption keys centrally
4. Train end users
5. Monitor audit logs

**Best Practices:**
- Central key backup storage
- Regular audit log reviews
- User training documentation
- Incident response procedures

---

## 🚦 System Requirements

### Minimum Requirements
- **OS:** Windows 10 (1809+) or Windows 11
- **Python:** 3.8 or higher
- **RAM:** 2 GB
- **Disk:** 100 MB free space
- **Processor:** Any modern CPU

### Recommended
- **OS:** Windows 11 (latest)
- **Python:** 3.11+
- **RAM:** 4 GB or more
- **Disk:** 500 MB free space
- **Processor:** Multi-core CPU

---

## 📋 Feature Comparison

| Feature | v6.x | v7.0 | v8.0 (Current) |
|---------|------|------|----------------|
| Terminal Required | ❌ Yes | ❌ Yes | ✅ No |
| Auto-Setup | ❌ No | ⚠️ Partial | ✅ Yes |
| GUI Installer | ❌ No | ❌ No | ✅ Yes |
| Dashboard | ❌ No | ⚠️ Basic | ✅ Modern |
| One-Click Start | ❌ No | ❌ No | ✅ Yes |
| Windows Integration | ⚠️ Manual | ⚠️ Manual | ✅ Automatic |
| Auto-Dependencies | ❌ No | ❌ No | ✅ Yes |
| Setup Wizard | ❌ No | ❌ No | ✅ Yes |
| Quick Actions | ❌ No | ⚠️ Limited | ✅ Full |
| Activity Feed | ❌ No | ❌ No | ✅ Yes |
| Statistics | ❌ No | ⚠️ Basic | ✅ Real-time |

---

## 🗺️ Roadmap

### v8.1 (Next Release)
- [ ] Cloud backup integration
- [ ] Mobile app (iOS/Android)
- [ ] Team/Enterprise features
- [ ] Remote management dashboard

### v8.2
- [ ] AI-powered file classification
- [ ] Automatic backup scheduling
- [ ] Multi-user key management
- [ ] Advanced analytics

### v9.0 (Future)
- [ ] Zero-knowledge cloud sync
- [ ] Blockchain key verification
- [ ] Hardware security key support
- [ ] Compliance reporting (SOC2, GDPR)

---

## 📄 License

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)

See [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Blu Corbel**
- 🌐 GitHub: [@AeinsteinApp](https://github.com/AeinsteinApp)
- 📧 Email: themadhattersplayground@gmail.com
- ☎️ Phone: +447576285686 (UK)

---

## 🙏 Acknowledgments

- Cryptography library developers
- Watchdog monitoring library
- Windows 11 design guidelines
- Open source community
- Early testers and contributors

---

## ⚠️ Important Notice

**This tool is designed for legitimate data protection purposes.**

- Always ensure you have proper authorization before encrypting files
- Keep secure backups of all encryption keys
- Test with non-critical files first
- Understand that without keys, files cannot be recovered
- Use for legal and ethical purposes only

**Encryption keys are unique per generation. If lost, recovery requires cryptographic analysis and may necessitate an on-site visit.**

---

## 🎉 Ready to Get Started?

1. **Download** Labyrinth Enterprise
2. **Double-click** `setup_windows.py`
3. **Follow** the Setup Wizard
4. **Protect** your sensitive files!

**No terminal. No configuration. Just security.**

---

*Built with 💙 for Windows 11*