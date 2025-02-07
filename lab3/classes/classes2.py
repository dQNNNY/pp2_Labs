class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length * self.length

shape = Shape()
print("Площадь фигуры:", shape.area())

square = Square(2)
print("Площадь квадрата:", square.area())