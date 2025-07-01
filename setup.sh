#!/usr/bin/env bash
set -eux

# Install Homebrew if not present
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install system libraries required for pcsc, cryptography, and build tools
brew update
brew install pkg-config openssl pcsclite python3

# Install Poetry (if not already present)
pip3 install --upgrade pip
pip3 install poetry

# (Optional) Install Swift if not present (macOS usually has Xcode/Swift pre-installed)
if ! command -v swift &>/dev/null; then
    echo "Please install Xcode or Swift toolchain from https://swift.org/download/."
    exit 1
fi

# Install Python dependencies (including dev tools like flake8 and pytest)
poetry install --with dev

# Pre-resolve Swift package dependencies
cd TapTrustSwift
swift package resolve
cd ..

echo "Setup complete."