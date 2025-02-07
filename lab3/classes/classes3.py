class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length * self.length

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

shape = Shape()
print("Площадь фигуры:", shape.area())

square = Square(2)
print("Площадь квадрата:", square.area())

rectangle = Rectangle(2, 4)
print("Площадь прямоугольника:", rectangle.area())