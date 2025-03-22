import os

path = r"C:\Users\Daniyar\Desktop\labs\lab_6\dir-and-files\test.txt"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        print(f"Number of lines in the file: {len(lines)}")
else:
    print(f"Error: File not found at {path}. Please check the path and try again.")
