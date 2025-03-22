import os

path = r"C:\Users\Daniyar\Desktop\labs\lab_6\dir-and-files"

if not os.path.exists(path):
    os.makedirs(path)

alpha = [chr(i) for i in range(65, 91)]

for letter in alpha:
    file_path = os.path.join(path, letter + ".txt")
    with open(file_path, 'x') as file:
        pass
