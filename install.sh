#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define paths
VENV_PATH="$HOME/.serial_monitor"
LAUNCHER_PATH="$HOME/.local/bin/serial_monitor"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"
pip install -e "$SCRIPT_DIR"

# Create bin directory if it doesn't exist
mkdir -p "$HOME/.local/bin"

# Create launcher script
echo "Creating launcher script..."
cat > "$LAUNCHER_PATH" << EOL
#!/bin/bash
source "$VENV_PATH/bin/activate"
python -m arduino_serial_monitor "\$@"
deactivate
EOL

# Make launcher executable
chmod +x "$LAUNCHER_PATH"

# Add ~/.local/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding ~/.local/bin to PATH..."
    
    # Determine shell configuration file
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    # Add PATH update to shell configuration
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    echo "Please restart your terminal or run: source $SHELL_RC"
else
    echo "~/.local/bin already in PATH"
fi

echo "Installation complete! You can now run 'serial_monitor' from anywhere."
echo "Example usage:"
echo "  serial_monitor                    # Auto-detect device"
echo "  serial_monitor --port COM3        # Specify port"
echo "  serial_monitor --baud 115200      # Custom baud rate" 