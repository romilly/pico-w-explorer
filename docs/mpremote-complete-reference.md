# mpremote: Complete Command Reference

**mpremote** is the official MicroPython CLI tool for interacting with MicroPython devices over serial connections. Maintained by MicroPython creator Damien George and the core team, it has become the standard interface replacing legacy tools like Ampy and largely superseding rshell.

**Current version:** 1.27.0 (December 2025)

---

## Installation

```bash
# Via pip
pip install --user mpremote

# Via pipx (recommended for isolated installation)
pipx install mpremote

# Run directly without installing
pipx run mpremote
```

---

## Basic Usage Patterns

### Simplest invocation
```bash
mpremote
```
Automatically connects to the first available USB serial device and enters the REPL.

### Command chaining
Multiple commands can be chained in a single invocation:
```bash
mpremote connect /dev/ttyUSB0 ls exec "print('Hello')" repl
```

### Implicit connection
If no `connect` command is specified, mpremote automatically connects to the first available device:
```bash
mpremote ls  # Implicitly adds 'connect auto' before 'ls'
```

---

## Connection Management

### connect – Specify device

```bash
mpremote connect <device>
```

**Device specifiers:**

```bash
# List all available devices
mpremote connect list

# Auto-connect to first available (default)
mpremote connect auto

# Connect by USB serial number
mpremote connect id:334D335C3138

# Connect by port path
mpremote connect port:/dev/ttyUSB0

# Connect via RFC2217 (serial over TCP)
mpremote connect rfc2217://192.168.1.100:2217

# Direct device path
mpremote connect /dev/ttyACM0
```

**Note:** Auto-connect only detects USB serial ports (CDC/ACM or FTDI-style devices with USB VID/PID).

**Built-in shortcuts:**
```bash
mpremote devs        # Alias for 'connect list'
mpremote a0          # /dev/ttyACM0 (Linux)
mpremote a1          # /dev/ttyACM1 (Linux)
mpremote u0          # /dev/ttyUSB0 (Linux)
mpremote c1          # COM1 (Windows)
```

### disconnect – Close current connection

```bash
mpremote disconnect
```

Closes the serial connection. Auto-soft-reset is re-enabled after disconnect.

**Example use case:**
```bash
# Work with device 1, then switch to device 2
mpremote a0 ls disconnect a1 ls
```

---

## Interpreter State Control

### resume – Preserve existing state

```bash
mpremote resume
```

Disables auto-soft-reset for subsequent commands. Useful for inspecting program state without clearing it.

**Example:**
```bash
# Inspect variable without resetting
mpremote resume eval "my_sensor_data"
```

### soft-reset – Restart the interpreter

```bash
mpremote soft-reset
```

Clears the Python heap and restarts the interpreter. Also disables auto-soft-reset for subsequent commands.

**Example:**
```bash
# Get clean REPL
mpremote soft-reset repl

# Execute sequence with explicit reset
mpremote resume exec "setup_wifi()" soft-reset exec "import main"
```

**Auto-soft-reset behavior:**
- Automatically triggered on first use of: `mount`, `eval`, `exec`, `run`, or `fs`
- Ensures code runs in a clean environment
- Only happens once per connection unless `disconnect` is called
- Can be bypassed with `resume`

---

## Interactive Development

### repl – Enter the REPL

```bash
mpremote repl [options]
```

Opens an interactive terminal to the device. Exit with `Ctrl-]` or `Ctrl-x`.

**Options:**
```bash
# Capture session output to file
mpremote repl --capture session.log

# Inject code when Ctrl-J is pressed
mpremote repl --inject-code "import demo; demo.run()"

# Inject file contents when Ctrl-K is pressed
mpremote repl --inject-file startup.py

# Display non-printable characters as hex
mpremote repl --escape-non-printable
```

**Important:** The `repl` command does NOT trigger auto-soft-reset. If a program is running, press `Ctrl-C` to interrupt it first.

**Practical workflow:**
```bash
# Mount local directory and inject demo on Ctrl-J
mpremote mount . repl --inject-code "import demo"
# Then: Ctrl-D to soft-reset, Ctrl-J to run demo
```

### eval – Evaluate expression

```bash
mpremote eval <expression>
```

Evaluates a Python expression and prints the result.

**Examples:**
```bash
# Simple math
mpremote eval "1/2"

# Check variable
mpremote eval "machine.freq()"

# Multiple evaluations in sequence
mpremote eval "1+1" eval "2+2" eval "3+3"

# Use with different devices
mpremote a0 eval "machine.unique_id()" a1 eval "machine.unique_id()"
```

### exec – Execute Python code

```bash
mpremote exec <code>
```

Executes Python statements (does not print return value like `eval`).

**Examples:**
```bash
# Single line
mpremote exec "import machine; machine.freq(240_000_000)"

# Multi-line with proper quoting
mpremote exec "
import micropython
micropython.mem_info()
"

# Run in background with --no-follow
mpremote exec --no-follow "
import time
while True:
    print('heartbeat')
    time.sleep(1)
"

# Memory info
mpremote exec "import micropython; micropython.mem_info()"
```

### run – Execute local script

```bash
mpremote run <file.py>
```

Executes a local Python file **directly from RAM** on the device without copying it to the filesystem. This is the fastest iteration method for single-file development.

**Examples:**
```bash
# Run local script
mpremote run test.py

# Run and leave executing in background
mpremote run --no-follow server.py

# Run after updating a dependency
mpremote cp driver.py : + run test.py
```

**Workflow comparison:**
```bash
# OLD WORKFLOW: Copy then run
mpremote cp test.py :test.py + exec "import test"

# NEW WORKFLOW: Run directly
mpremote run test.py
```

---

## Filesystem Operations

### fs – Filesystem commands

All filesystem operations use the `:` prefix convention to indicate remote paths (similar to `scp`).

```bash
mpremote fs <subcommand>
```

**Subcommands:**

#### cat – Display file contents
```bash
# Show single file
mpremote cat :boot.py

# Show multiple files
mpremote cat :boot.py :main.py

# Shortcut (without 'fs')
mpremote cat :boot.py
```

#### ls – List directory
```bash
# List root
mpremote ls

# List specific directories
mpremote ls :lib :utils

# Shortcut
mpremote ls
```

#### cp – Copy files
```bash
# Local to remote
mpremote cp main.py :main.py
mpremote cp main.py :              # Same as above (: means root)

# Remote to local
mpremote cp :main.py main.py
mpremote cp :main.py .             # Copy to current directory

# Remote to remote
mpremote cp :a.py :b.py

# Multiple files to directory
mpremote cp *.py :lib/

# Recursive copy
mpremote cp -r src/ :src/

# Force copy (ignore SHA256 hash check)
mpremote cp -f main.py :

# Copy then continue with other commands
mpremote cp driver.py :utils/driver.py + repl
```

**Note:** By default, `cp` skips copying if the SHA256 hash matches between source and destination. Use `-f` to force.

#### rm – Remove files/directories
```bash
# Remove single file
mpremote rm :old_file.py

# Remove multiple files
mpremote rm :a.py :b.py :c.py

# Remove directory recursively
mpremote rm -r :old_lib

# Remove with verbose output
mpremote rm -rv :temp

# Remove from current remote directory
mpremote rm -r :libs

# Remove everything (DESTRUCTIVE!)
mpremote rm -rv :/
```

**Warning:** There is no way to recover files deleted with `mpremote rm -r`. Use with extreme caution.

#### mkdir – Create directories
```bash
mpremote mkdir :lib
mpremote mkdir :data :logs :config
```

#### rmdir – Remove empty directories
```bash
mpremote rmdir :empty_folder
mpremote rmdir :old_dir1 :old_dir2
```

#### touch – Create empty files
```bash
mpremote touch :marker.txt
mpremote touch :log1.txt :log2.txt
```

#### sha256sum – Calculate file hash
```bash
mpremote sha256sum :boot.py
mpremote sha256sum :*.py
```

#### tree – Display directory tree
```bash
# Basic tree
mpremote tree

# Show file sizes
mpremote tree --size
mpremote tree -s

# Human-readable sizes
mpremote tree --human
mpremote tree -h

# Include device name in output
mpremote tree -v

# Tree of specific directories
mpremote tree :lib :utils
```

### df – Show filesystem statistics

```bash
mpremote df
```

Displays filesystem size, used space, and free space (similar to Unix `df`).

**Example output:**
```
Filesystem         Size      Used     Avail Use%
/flash           1408K      384K     1024K  27%
```

---

## Advanced Development Features

### mount – Mount local directory on device

```bash
mpremote mount [options] <local-dir>
```

Mounts a local directory as `/remote` on the device. The device reads files **directly from your host** over the serial connection — no copying required.

**This is the killer feature for iterative development.**

**Examples:**
```bash
# Mount current directory
mpremote mount .

# Mount and import a module
mpremote mount . exec "import main"

# Mount and stay in REPL (implicit)
mpremote mount .  # Automatically adds 'repl' at end

# Mount specific directory
mpremote mount src/

# Mount with symbolic link access outside directory
mpremote mount --unsafe-links .
mpremote mount -l .
```

**Behavior:**
- Mounted as `/remote` on device
- Device `cwd` changed to `/remote`
- All imports/file access occur from mounted directory
- Mount persists through soft-reset (`Ctrl-D`)
- To remount after hard reset: `Ctrl-A Ctrl-D` then `Ctrl-B`

**Development workflow:**
```bash
# Terminal 1: Mount and enter REPL
mpremote mount .

# Terminal 2: Edit main.py in your editor

# Back in Terminal 1 REPL:
>>> import main         # First run
>>> # Edit code in editor
>>> # In REPL:
>>> import sys
>>> del sys.modules['main']
>>> import main         # Reload changes
```

**Even better with inject:**
```bash
mpremote mount . repl --inject-code "import sys; [sys.modules.pop(k) for k in list(sys.modules.keys()) if not k.startswith('_')]; import main"
# Now Ctrl-D (soft reset), then Ctrl-J (re-import main)
```

### unmount – Unmount directory

```bash
mpremote umount
```

Explicitly unmounts the previously mounted directory. Happens automatically when mpremote exits.

### edit – Edit remote file locally

```bash
mpremote edit <file...>
```

Copies file(s) from device to local temp directory, opens your `$EDITOR`, and copies back if editor exits successfully.

**Examples:**
```bash
# Edit single file
mpremote edit :main.py

# Edit multiple files
mpremote edit :boot.py :main.py :config.py
```

**Requirements:**
- `$EDITOR` environment variable must be set
- Editor must exit with success code (0) for changes to be copied back

---

## Package Management

### mip – Install packages

```bash
mpremote mip install <package...> [options]
```

Installs packages from micropython-lib or external sources using the `mip` package manager.

**Examples:**
```bash
# Install from micropython-lib
mpremote mip install aioble
mpremote mip install unittest unittest-discover

# Install from GitHub
mpremote mip install github:org/repo
mpremote mip install github:org/repo@branch

# Install from GitLab
mpremote mip install gitlab:org/repo@branch

# Install to specific directory
mpremote mip install --target /flash/third-party functools

# Install without .mpy compilation
mpremote mip install --no-mpy requests

# Install from custom index
mpremote mip install --index https://custom.org/index.json package_name
```

**How it works:**
- Fetches packages from micropython-lib (default) or specified source
- Automatically uses pre-compiled `.mpy` files when available (unless `--no-mpy`)
- Works on network-capable boards via device's WiFi
- On non-WiFi boards, mpremote handles download via host

---

## ROMFS Management

### romfs – Manage read-only filesystem partitions

```bash
mpremote romfs <subcommand>
```

Creates and deploys read-only filesystem images (useful for bundling assets and libraries).

**Subcommands:**

#### query – List ROMFS partitions
```bash
mpremote romfs query
```

#### build – Create ROMFS image
```bash
# Build from directory
mpremote romfs build assets/

# Build with custom output name
mpremote romfs -o custom.romfs build assets/

# Auto-compile .py to .mpy (default)
mpremote romfs build src/

# Don't compile to .mpy
mpremote romfs --no-mpy build src/
```

#### deploy – Deploy ROMFS image
```bash
# Deploy pre-built image
mpremote romfs deploy assets.romfs

# Deploy from directory (builds automatically)
mpremote romfs deploy assets/

# Deploy to specific partition
mpremote romfs -p data deploy data/
```

**Note:** Auto-compilation to `.mpy` requires the `mpy_cross` Python package:
```bash
pip install mpy_cross
```

---

## System Control

### rtc – Real-time clock control

```bash
# Get current device time
mpremote rtc

# Set device time to host PC time
mpremote rtc --set
```

**Example output:**
```
(2025, 2, 12, 3, 14, 35, 46, 0)
```

### sleep – Pause execution

```bash
mpremote sleep <seconds>
```

Delays execution in a command chain (useful for waiting on device operations).

**Examples:**
```bash
# Wait for device to initialize
mpremote reset sleep 0.5 exec "import main"

# Wait between operations
mpremote exec "sensor.start()" sleep 1.0 eval "sensor.read()"
```

### reset – Hard reset device

```bash
mpremote reset
```

Equivalent to `machine.reset()` — performs a hardware reset.

**Example:**
```bash
mpremote reset sleep 0.5 bootloader
```

### bootloader – Enter bootloader mode

```bash
mpremote bootloader
```

Enters the device bootloader (port-specific: DFU on STM32, UF2 on RP2040).

**Example use case:**
```bash
# Enter UF2 bootloader on Pico
mpremote bootloader
# Device now appears as USB mass storage drive
```

---

## Shortcuts and Configuration

### Built-in shortcuts

```bash
devs          # connect list
a0, a1...     # /dev/ttyACM0, /dev/ttyACM1... (Linux)
u0, u1...     # /dev/ttyUSB0, /dev/ttyUSB1... (Linux)
c0, c1...     # COM0, COM1... (Windows)
cat, ls, cp, rm, mkdir, rmdir, touch  # Aliases for fs <subcmd>
```

### Custom shortcuts – config.py

Location: `~/.config/mpremote/config.py` (Linux/macOS) or `%LOCALAPPDATA%\mpremote\config.py` (Windows)

**Example config.py:**
```python
commands = {
    # Simple connection shortcut
    "c33": "connect id:334D335C3138",
    
    # Shorter bootloader command
    "bl": "bootloader",
    
    # Shortcut with argument and default
    "double x=4": "eval x*2",
    
    # Multi-step macro
    "wl_scan": [
        "exec",
        """
import network
wl = network.WLAN()
wl.active(1)
for ap in wl.scan():
    print(ap)
"""
    ],
    
    # Common development workflow
    "test": ["mount", ".", "exec", "import test"],
    
    # Deploy and run
    "deploy": [
        "cp", "-r", "src/", ":",
        "soft-reset",
        "exec", "import main",
    ],
    
    # Get WiFi IP address
    "wl_ip": [
        "exec",
        "import network; sta=network.WLAN(network.WLAN.IF_STA); print(sta.ipconfig('addr4'))"
    ],
    
    # Multiple-parameter command
    "multiply x=4 y=7": "eval x*y",
}
```

**Usage:**
```bash
mpremote c33                    # Uses "c33" shortcut
mpremote test                   # Runs test macro
mpremote double                 # Uses default: eval 4*2
mpremote double 10              # eval 10*2
mpremote multiply 3 5           # eval 3*5
```

---

## Real-World Workflows

### 1. Fast single-file iteration
```bash
# Edit test.py locally, run on device from RAM (no filesystem writes)
mpremote run test.py
```

### 2. Multi-file development with mount
```bash
# Mount current directory, import module
mpremote mount . exec "import main"

# Or with REPL for debugging
mpremote mount .
# Now edit files locally; changes visible immediately on next import
```

### 3. Deploy library then test
```bash
mpremote cp -r mylib/ :lib/mylib + run tests/test_mylib.py
```

### 4. Update driver and restart application
```bash
mpremote cp drivers/sensor.py :lib/sensor.py + soft-reset repl
```

### 5. Full deployment workflow
```bash
# Copy all source, install dependencies, restart
mpremote cp -r src/ : + \
         mip install aioble + \
         soft-reset + \
         exec "import main"
```

### 6. Development with auto-reload inject
```bash
mpremote mount . repl --inject-file dev/reload.py
# Press Ctrl-K to reload, Ctrl-D then Ctrl-K for full reset+reload
```

**reload.py:**
```python
import sys
# Remove all user modules
for k in list(sys.modules.keys()):
    if not k.startswith('_'):
        del sys.modules[k]
import main
```

### 7. Multi-device development
```bash
# Compare behavior across two devices
mpremote a0 eval "machine.freq()" a1 eval "machine.freq()"

# Deploy to multiple devices
mpremote a0 cp main.py : + disconnect a1 cp main.py :
```

### 8. Debugging with state inspection
```bash
# Run program, then inspect without resetting
mpremote exec "import main; main.setup()" + \
         resume + \
         eval "main.sensor_readings"
```

### 9. Create ROMFS bundle of assets
```bash
# Build assets into ROMFS, deploy to device
mpremote romfs build assets/ + romfs deploy assets.romfs
```

### 10. WiFi scanning utility
```bash
mpremote exec "
import network
wl = network.WLAN()
wl.active(1)
for ap in wl.scan():
    ssid = ap[0].decode()
    rssi = ap[3]
    print(f'{ssid:32s} {rssi:>4d} dBm')
"
```

---

## Command Termination with `+`

When filesystem commands take variable arguments and you want to chain more commands, use `+` to terminate the argument list:

```bash
# Wrong - "repl" interpreted as a path
mpremote cp file1.py file2.py : repl

# Correct - + terminates cp arguments
mpremote cp file1.py file2.py : + repl

# Also applies to other multi-arg commands
mpremote rm :a.py :b.py :c.py + soft-reset
mpremote cat :boot.py :main.py + ls
```

---

## Troubleshooting

### Device not found
```bash
# List available devices
mpremote devs

# Explicitly specify device
mpremote connect /dev/ttyUSB0 repl
```

### Permission denied (Linux)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and back in

# Or use sudo (not recommended)
sudo mpremote
```

### Mount doesn't work after hard reset
```bash
# Remount requires raw repl access
# Press: Ctrl-A (raw repl) Ctrl-D (soft reset) Ctrl-B (normal repl)
# Mount will then reconnect automatically
```

### REPL appears unresponsive
```bash
# Device may be in paste mode or raw REPL
# Try: Ctrl-C (interrupt) Ctrl-B (normal REPL)
```

### File copy fails despite different content
```bash
# SHA256 hash collision (unlikely) or cached hash
mpremote cp -f file.py :file.py  # Force copy
```

---

## Comparison with Legacy Tools

| Feature | mpremote | ampy | rshell |
|---------|----------|------|--------|
| Maintained | ✅ Active | ❌ Abandoned (2018) | ⚠️ Low maintenance |
| Directory mounting | ✅ Yes | ❌ No | ❌ No |
| Package management | ✅ mip built-in | ❌ No | ❌ No |
| Command chaining | ✅ Yes | ❌ No | ⚠️ Limited |
| File hash checking | ✅ Yes | ❌ No | ❌ No |
| Bootloader access | ✅ Yes | ❌ No | ❌ No |
| ROMFS support | ✅ Yes | ❌ No | ❌ No |
| Speed (file transfers) | ✅ Fast | ⚠️ Slow | ⚠️ Slow |

**Verdict:** Use mpremote for everything. Other tools exist only for legacy compatibility.

---

## Integration with Other Tools

### Use with MicroPico VS Code extension
MicroPico uses mpremote internally. You can use both simultaneously:
- MicroPico: Upload project, manage device
- mpremote: Quick CLI operations, automation

### Use with mpr wrapper
[mpr](https://github.com/bulletmark/mpr) provides conventional CLI interface:
```bash
# mpremote style
mpremote cp main.py :

# mpr style  
mpr put main.py /
mpr get main.py .
```

### Use in CI/CD scripts
```bash
# GitHub Actions example
- name: Deploy to device
  run: |
    mpremote connect ${{ secrets.DEVICE_PORT }} \
             cp -r src/ : + \
             soft-reset
```

---

## Version History Notes

- **v1.27.0** (Dec 2025): Current version
- **v1.26.1** (Dec 2025): Mentioned in ecosystem documentation
- **v1.22+**: Added ROMFS support
- **v1.21+**: Improved `mip` integration
- **v1.20+**: Added `tree` command
- Earlier versions deprecated

Always use the latest version: `pip install --upgrade mpremote`

---

## Summary: Essential Commands

**Quick reference for daily use:**

```bash
# Basic
mpremote                          # Connect and enter REPL
mpremote ls                       # List files
mpremote cat :main.py            # Show file

# Fast iteration
mpremote run test.py             # Run local file from RAM
mpremote mount .                 # Mount for multi-file dev
mpremote mount . exec "import main"  # Mount and run

# File management
mpremote cp main.py :            # Copy to device
mpremote cp :main.py .           # Copy from device
mpremote cp -r src/ :            # Recursive copy
mpremote rm -r :old/             # Remove directory

# Development
mpremote exec "import sys; sys.path"     # Execute code
mpremote eval "machine.freq()"           # Evaluate expression
mpremote mip install aioble              # Install package

# Workflow
mpremote cp driver.py : + soft-reset + exec "import main"
```

This is your modern MicroPython CLI toolkit. Master these patterns and iterative development becomes seamless.
