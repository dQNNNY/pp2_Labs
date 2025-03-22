import os 

path = r"C:\vscode\labs\.vscode\.vscode\lab_6\dir-and-files\gg.txt"

if os.path.exists(path):
    if os.access(path, os.R_OK) and os.access(path, os.W_OK):
        os.remove(path)
        print(f"'{path}' has been removed.")
    else:
        print(f"Insufficient permissions to delete '{path}'.")
else:
    print("Sorry bro, here nothing.")
