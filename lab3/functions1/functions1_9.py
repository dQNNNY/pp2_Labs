import math

def sphere_volume(radius):
    return (4 / 3) * math.pi * radius**3

radius = float(input("Enter the radius: "))
print("The volume of the sphere is:", sphere_volume(radius))
