import subprocess
import glob
import shutil
import os
from sys import stderr

def find_panda3d_location():
    result = subprocess.run(["pip", "show", "panda3d"], stdout=subprocess.PIPE, text=True)
    pip_text = result.stdout.splitlines(keepends=False)

    for line in pip_text:
        if line.startswith("Location: "):
            return line[len("Location: "):]
    return None


def main():
    if os.path.exists("./dist"):
        shutil.rmtree("./dist")
    result = os.system("pyinstaller --onefile --windowed .\\run_game.py")
    if result != 0:
        print("could not create exe", file=stderr)
    panda3d_location = find_panda3d_location()
    for f in glob.glob(f"{panda3d_location}/bin/*.dll"):
        shutil.copy(f, "dist/")
    
    shutil.copytree("art/", "dist/art")
    shutil.copytree("etc/", "dist/etc")
    shutil.copytree("models/", "dist/models")
    shutil.copytree("scenes/", "dist/scenes")
    shutil.copytree("sound/", "dist/sound")

if __name__ == '__main__':
    main()

