#!/usr/bin/env python

import os

# Update apt
os.system("sudo apt update")

# Install gitleaks
os.system("sudo apt install gitleaks")

# Install latest version of VS Code
os.system("curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg")
os.system("sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/")
os.system("sudo sh -c 'echo \"deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list'")
os.system("sudo apt update")
os.system("sudo apt install code")

# Install OpenAI library
os.system("sudo pip install openai")