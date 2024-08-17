import os
import subprocess
import shutil
import glob

# Define the target directory for dotfiles
DOTFILES_DIR = os.path.expanduser("~/.dotfiles")

# Configuration for different applications
CONFIGS = {
    "kde": [
        "~/.config/kdeglobals",
        "~/.config/plasma-org.kde.plasma.desktop-appletsrc",
        "~/.config/kglobalshortcutsrc",  # KDE keyboard shortcuts
        # Add more KDE-specific config files here
    ],
    "vscode": [
        "~/.config/Code/User/settings.json",
        "~/.config/Code/User/keybindings.json"
    ],
    "vscodium": [
        "~/.config/VSCodium/User/settings.json",
        "~/.config/VSCodium/User/keybindings.json"
    ],
    "pycharm": [
        "~/.config/JetBrains/PyCharm*/options",  # Use * for different versions
        # Add more PyCharm-specific config files here
    ],
    "konsole": ["~/.config/konsolerc"],
    "yaquake": ["~/.config/yakuakerc"],
    "dolphin": ["~/.config/dolphinrc"],
    "cool-retro-term": ["~/.config/cool-retro-term"],  # This might be a directory
    "bash": [
        "~/.bashrc",  # Bash configuration
        "~/.bash_aliases",  # Bash aliases
    ],
}

# Function to handle copying/restoring files or directories
def handle_config(source, destination, mode):
    source = os.path.expanduser(source)
    if not os.path.exists(source):
        print(f"Warning: Configuration not found: {source}")
        return  # Skip if the source doesn't exist

    try:
        if os.path.isdir(source):
            if mode == "copy":
                shutil.copytree(source, destination, dirs_exist_ok=True)
                print(f"Copied directory {source} to {destination}")
            elif mode == "restore":
                shutil.copytree(os.path.join(DOTFILES_DIR, source), destination, dirs_exist_ok=True)
                print(f"Restored directory {source} to {destination}")
        else:
            if mode == "copy":
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.copy2(source, destination)
                print(f"Copied file {source} to {destination}")
            elif mode == "restore":
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.copy2(os.path.join(DOTFILES_DIR, source), destination)
                print(f"Restored file {source} to {destination}")
    except FileNotFoundError:
        print(f"Warning: File or directory not found: {source}")

# Create the dotfiles directory if it doesn't exist
if not os.path.exists(DOTFILES_DIR):
    os.makedirs(DOTFILES_DIR)

# Iterate through each application's configuration
for app, config_files in CONFIGS.items():
    # Copy/restore each configuration file for the current application
    for config_file in config_files:
        source_path = os.path.expanduser(config_file)
        for expanded_source in glob.glob(source_path):
            if not os.path.exists(expanded_source):
                print(f"Warning: Configuration not found: {expanded_source}")
                continue  # Skip to the next configuration file

            app_dir = os.path.join(DOTFILES_DIR, app)
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)  # Create the app directory only if the config exists

            destination_path = os.path.join(app_dir, os.path.basename(expanded_source))
            handle_config(expanded_source, destination_path, mode="copy")

print("Dotfiles collection complete! Files can be found in " + DOTFILES_DIR)


# # --- Restore Functionality ---
# restore = input("Do you want to restore the dotfiles? (y/n): ")
# if restore.lower() == "y":
#     for app, config_files in CONFIGS.items():
#         for config_file in config_files:
#             source_path = os.path.join(app, os.path.basename(config_file))
#             for expanded_source in glob.glob(os.path.join(DOTFILES_DIR, source_path)):
#                 destination_path = os.path.expanduser(config_file)
#                 handle_config(expanded_source, destination_path, mode="restore")

#     print("Dotfiles restoration complete!")