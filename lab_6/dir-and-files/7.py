import os 

path1 = r"C:\Users\Daniyar\Desktop\labs\lab_6\dir-and-files\tst.txt"
path2 = r"C:\Users\Daniyar\Desktop\labs\lab_6\dir-and-files\test.txt"

if not os.path.exists(path2):
    print(f"Error: Source file '{path2}' not found.")
else:
    with open(path2, 'r', encoding='utf-8') as file:
        content = file.read()

    with open(path1, 'w', encoding='utf-8') as gg:
        gg.write(content)

    print(f"Content copied from '{path2}' to '{path1}' successfully.")
