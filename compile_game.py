# compile_game.py
import subprocess

def main():
    commands = [
        'pyinstaller --onefile main.py',  # Windows
        'pyinstaller --onefile --windowed main.py'  # macOS
    ]

    for command in commands:
        subprocess.run(command, shell=True)

if __name__ == '__main__':
    main()