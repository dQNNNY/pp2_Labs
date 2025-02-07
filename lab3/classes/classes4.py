import math
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f'x={self.x}  y={self.y}')

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        return math.sqrt((other_point.x - self.x)**2 + (other_point.y - self.y)**2)

p1 = Point(1, 4)
p2 = Point(4, 6)

p1.show()
p2.show()

p1.move(2, 6)
p1.show()

print(f'dist: {p1.dist(p2)}')