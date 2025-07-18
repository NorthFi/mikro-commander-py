# 🚀 Mikro Commander

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/NorthFi/mikro-commander-py)

A powerful, multi-threaded GUI tool for executing commands across multiple MikroTik devices simultaneously. Perfect for network administrators who need to manage large-scale RouterOS deployments efficiently.

![Mikro Commander Screenshot](https://via.placeholder.com/800x500/2c3e50/ffffff?text=Mikro+Commander+Interface)

## ✨ Features

- **Multi-threaded Execution**: Run commands on multiple devices concurrently
- **Intuitive GUI**: Clean, modern interface built with Tkinter
- **Flexible Target Input**: Load device lists from files or enter manually
- **Real-time Progress**: Visual progress bar and colored output logging
- **Session Logging**: Automatic logging of all operations with timestamps
- **Host Key Verification**: Optional SSH host key verification for security
- **Command Validation**: Built-in validation and error handling
- **Configurable Settings**: Customizable SSH ports, thread counts, and user preferences
- **Export Capabilities**: Save output logs for documentation and analysis

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Required Dependencies

```bash
pip install paramiko tkinter
```

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/NorthFi/mikro-commander-py.git
cd mikro-commander-py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python mikro-commander-py.py
```

## 🎯 Usage

### Basic Operation

1. **Enter Commands**: Type RouterOS commands in the Commands box (one per line)
2. **Specify Targets**: Add device IP addresses in the Targets box
   - Separate with commas, spaces, or newlines
   - Or load from a text file using the "Load Targets" button
3. **Configure Settings**: Set SSH port (default: 22) and thread count
4. **Execute**: Click "Execute" to run commands on all devices

### Advanced Features

#### Loading Targets from File
Create a text file with one IP address per line:
```
192.168.1.1
192.168.1.2
192.168.1.3
```

#### Example Commands
```bash
# System information
/system identity print
/system resource print

# Interface status
/interface print brief

# IP address configuration
/ip address print

# Firewall rules
/ip firewall filter print
```

#### Configuration File
The application automatically saves settings to `mikrotikmcp.cfg`:
```ini
[DEFAULT]
username = admin
port = 22
threads = 5
verify_host = false
```

## 🔧 Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| Username | SSH username for device access | admin |
| SSH Port | Port number for SSH connections | 22 |
| Threads | Number of concurrent connections | 5 |
| Host Verification | Enable SSH host key verification | false |

## 📊 Output Format

The application provides color-coded output:
- 🔵 **Info**: General information and progress updates
- 🟢 **Success**: Successful command execution
- 🟡 **Warning**: Non-critical warnings
- 🔴 **Error**: Connection failures and command errors

## 🔒 Security Features

- **Host Key Verification**: Optional SSH host key validation
- **Secure Password Input**: Hidden password entry dialog
- **Connection Logging**: Automatic logging to device system logs
- **Timeout Protection**: Configurable connection timeouts

## 📁 File Structure

```
mikro-commander-py/
├── mikro-commander-py.py      # Main application file
├── requirements.txt           # Python dependencies
├── mikrotikmcp.cfg           # Configuration file (auto-generated)
├── known_hosts               # SSH known hosts file
├── session_*.log             # Session log files
├── mikrotik-banner.png       # Optional banner image
└── mikrotik-icon.png         # Optional window icon
```

## 🚀 Performance

- **Concurrent Execution**: Default 5 threads (configurable up to 20)
- **Connection Timeout**: 10 seconds with 20-second banner timeout
- **Memory Efficient**: Minimal resource usage even with large device lists
- **Error Recovery**: Robust error handling and connection retry logic

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- Large device lists (>100) may require increased timeout values
- Some RouterOS versions may have compatibility issues with certain commands
- Host key verification requires manual key management

## 🔮 Roadmap

- [ ] Command templates and favorites
- [ ] Device grouping and filtering
- [ ] Real-time command output streaming
- [ ] Dark mode theme support
- [ ] Export to CSV/Excel formats
- [ ] API integration for automated workflows
- [ ] Plugin system for custom commands

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/NorthFi/mikro-commander-py/issues) page
2. Create a new issue with detailed information
3. Include your Python version and operating system

## 👨‍💻 Author

**NorthFi** - [GitHub Profile](https://github.com/NorthFi)

## 🙏 Acknowledgments

- MikroTik for their excellent RouterOS platform
- The Paramiko team for SSH connectivity
- The Python community for continuous support

---

⭐ **Star this repository if you find it helpful!** ⭐
