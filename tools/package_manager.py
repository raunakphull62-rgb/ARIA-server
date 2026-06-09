# tools/package_manager.py
import subprocess
import sys
import os
import json
import requests
import tempfile
import zipfile
from pathlib import Path

ARIA_REGISTRY = "https://your-render-url.com"  # Replace with actual Render URL

SYSTEM_TOOLS = {
    'git', 'curl', 'wget', 'vim', 'nano',
    'python', 'node', 'npm', 'ruby', 'go',
    'ffmpeg', 'imagemagick', 'sqlite'
}

HEAVY_PACKAGES = {
    'numpy', 'scipy', 'pandas', 'matplotlib',
    'pillow', 'opencv', 'tensorflow', 'torch'
}

def smart_install(package):
    print(f"Looking up {package}...")
    # 1. Check ARIA registry
    try:
        r = requests.get(f"{ARIA_REGISTRY}/packages/{package}", timeout=5)
        if r.status_code == 200:
            pkg = r.json()
            print(f"Found in ARIA registry: {pkg['description']}")
            install_aria_plugin(pkg)
            requests.post(f"{ARIA_REGISTRY}/packages/{package}/install")
            return
    except Exception:
        pass

    # 2. System tools
    if package in SYSTEM_TOOLS:
        print(f"Installing system tool: {package}")
        os.system(f"pkg install {package} -y")
        return

    # 3. Heavy packages via pkg
    if package in HEAVY_PACKAGES:
        print(f"Installing heavy package {package} via pkg...")
        os.system(f"pkg install python-{package} -y")
        return

    # 4. PyPI fallback
    print(f"Installing Python package: {package}")
    os.system(f"pip install {package}")

def install_aria_plugin(pkg):
    download_url = pkg['download_url']
    name = pkg['name']
    print(f"Downloading {name}...")
    resp = requests.get(download_url)
    plugin_dir = os.path.expanduser(f"~/.aria/plugins/{name}")
    os.makedirs(plugin_dir, exist_ok=True)
    tmp = tempfile.mktemp(suffix='.zip')
    with open(tmp, 'wb') as f:
        f.write(resp.content)
    with zipfile.ZipFile(tmp, 'r') as z:
        z.extractall(plugin_dir)
    os.remove(tmp)
    print(f"{name} installed to ~/.aria/plugins/ ✅")

def aria_search(query):
    try:
        r = requests.get(f"{ARIA_REGISTRY}/packages?search={query}", timeout=5)
        packages = r.json()
        if not packages:
            print("No packages found.")
            return
        print(f"Found {len(packages)} packages:")
        for p in packages:
            print(f"  {p['name']} v{p['version']} — {p['description']}")
    except Exception:
        print("Could not reach ARIA registry.")

def list_plugins():
    plugin_dir = os.path.expanduser("~/.aria/plugins")
    if not os.path.exists(plugin_dir):
        print("No plugins installed.")
        return
    plugins = [d for d in os.listdir(plugin_dir) if os.path.isdir(os.path.join(plugin_dir, d))]
    if not plugins:
        print("No plugins found.")
    else:
        print("Installed plugins:")
        for p in plugins:
            print(f"  {p}")
