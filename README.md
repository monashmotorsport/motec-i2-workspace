# MMS Motec i2 Workspace

Welcome to the centralized repository for the Monash Motorsport's MoTeC i2 Pro workspaces, Math Channels, and Aliases.

To ensure everyone on the team is analyzing data using the exact same math functions, we use a custom automated sync script. **You do not need to know how to use Git to keep your workspace up to date.**

## Setup

To get started, you only need to download the updater script and place it in the correct folder on your computer.

1. Download the `update.bat` file directly from this repository.
2. Open File Explorer and navigate to your MoTeC workspace folder. This is typically located at:
   `Documents\MoTeC\i2\Workspaces\[Your Workspace Name]`
3. Move the `update.bat` file into this workspace folder. It **must** sit in the exact same directory as your `Channels` and `Maths` folders.

## How to Update Your Files

If you just want to ensure you have the latest versions of our math channels and aliases

1. **Close MoTeC i2 Pro.** (The script will intentionally block you if MoTeC is open to prevent file corruption).
2. Double-click `update.bat`.
3. The script will automatically connect to GitHub, download the latest files, safely merge the new math channels, and clean up after itself. 
4. *Bonus:* The script is self-updating. If we push a bug fix for the script itself, it will automatically install the new version when you run it!

> [!WARNING]
> **Alias Overwrites:** This script forces your `Channels/Aliases.xml` file to perfectly match the team's master file. **If you have created local, custom aliases on your laptop, they will be deleted.** If you make a good alias, submit it to us to be added to the repo!