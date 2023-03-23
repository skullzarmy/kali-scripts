#!/usr/bin/env python
import os
from tqdm import tqdm

# wrap everything in a tqdm progress bar so I can see overall progress of the script
with tqdm(total=100, desc="Overall Progress") as pbar:
    
    # Update apt
    os.system("sudo apt update")
    pbar.update(10)
    
    # Install gitleaks
    os.system("sudo apt install gitleaks")
    pbar.update(10)
    
    # Install latest version of VS Code
    # if microsoft.gpg does not exists on disk
    if not os.path.exists("microsoft.gpg"):
        os.system("curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg")
        os.system("sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/")
        os.system("sudo sh -c 'echo \"deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list'")
    os.system("sudo apt update")
    os.system("sudo apt install code")
    pbar.update(20)
    
    # Install VS Code extensions
    os.system("code --install-extension akamud.vscode-theme-onedark")
    os.system("code --install-extension formulahendry.auto-rename-tag")
    os.system("code --install-extension ms-azuretools.vscode-docker")
    os.system("code --install-extension github.copilot")
    os.system("code --install-extension davidanson.vscode-markdownlint")
    os.system("code --install-extension ms-python.python")
    os.system("code --install-extension chakrounAnas.turbo-console-log")
    pbar.update(30)
    
    # Install OpenAI library
    os.system("sudo pip install openai")
    pbar.update(10)
    
pbar.close()
