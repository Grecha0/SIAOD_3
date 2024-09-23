import random
import matplotlib.pyplot as plt
import math

# Класс для представления точки
class Point:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

# Класс для представления прямоугольной области
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x  # Центр по оси X
        self.y = y  # Центр по оси Y
        self.width = width
        self.height = height

    # Проверка, содержит ли прямоугольник точку
    def contains(self, point):
        return (self.x - self.width / 2 <= point.x <= self.x + self.width / 2 and
                self.y - self.height / 2 <= point.y <= self.y + self.height / 2)

    # Проверка, пересекается ли прямоугольник с другим прямоугольником
    def intersects(self, range):
        return not (range.x - range.width / 2 > self.x + self.width / 2 or
                    range.x + range.width / 2 < self.x - self.width / 2 or
                    range.y - range.height / 2 > self.y + self.height / 2 or
                    range.y + range.height / 2 < self.y - self.height / 2)

# Класс квадродерева
class Quadtree:
    def __init__(self, boundary, capacity, depth=0, max_depth=10):
        self.boundary = boundary  # Область этого узла
        self.capacity = capacity  # Максимальное количество точек перед разделением
        self.points = []          # Точки в этом узле
        self.divided = False      # Флаг разделения
        self.depth = depth        # Текущая глубина
        self.max_depth = max_depth  # Максимальная глубина

    # Метод для вставки точки в квадродерево
    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity or self.depth >= self.max_depth:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            return (self.northeast.insert(point) or
                    self.northwest.insert(point) or
                    self.southeast.insert(point) or
                    self.southwest.insert(point))

    # Метод для разделения текущего узла на 4 дочерних
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2

        ne = Rectangle(x + w / 2, y + h / 2, w, h)
        nw = Rectangle(x - w / 2, y + h / 2, w, h)
        se = Rectangle(x + w / 2, y - h / 2, w, h)
        sw = Rectangle(x - w / 2, y - h / 2, w, h)

        self.northeast = Quadtree(ne, self.capacity, self.depth + 1, self.max_depth)
        self.northwest = Quadtree(nw, self.capacity, self.depth + 1, self.max_depth)
        self.southeast = Quadtree(se, self.capacity, self.depth + 1, self.max_depth)
        self.southwest = Quadtree(sw, self.capacity, self.depth + 1, self.max_depth)

        self.divided = True

    # Метод для поиска всех точек внутри заданного диапазона
    def query_range(self, range, found=None):
        if found is None:
            found = []

        if not self.boundary.intersects(range):
            return found
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
            if self.divided:
                self.northwest.query_range(range, found)
                self.northeast.query_range(range, found)
                self.southwest.query_range(range, found)
                self.southeast.query_range(range, found)
        return found

    # Метод для поиска точки по ID
    def find_point_by_id(self, id):
        for p in self.points:
            if p.id == id:
                return p
        if self.divided:
            found = (self.northwest.find_point_by_id(id) or
                     self.northeast.find_point_by_id(id) or
                     self.southwest.find_point_by_id(id) or
                     self.southeast.find_point_by_id(id))
            return found
        return None

# Функция для генерации случайных точек
def generate_random_points(num_points, x_range, y_range):
    points = []
    for i in range(1, num_points + 1):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        points.append(Point(x, y, i))
    return points

# Функция для поиска ближайших соседей
def find_nearest_neighbors(quadtree, target_point, k=5):
    # Используем простой подход: обходим все точки и выбираем k ближайших
    # Для больших наборов данных рекомендуется использовать более эффективные алгоритмы
    all_points = []
    def traverse(node):
        all_points.extend(node.points)
        if node.divided:
            traverse(node.northwest)
            traverse(node.northeast)
            traverse(node.southwest)
            traverse(node.southeast)
    traverse(quadtree)
    all_points.remove(target_point)  # Исключаем саму точку
    sorted_points = sorted(all_points, key=lambda p: p.distance_to(target_point))
    return sorted_points[:k]

# Функция для визуализации
def visualize(quadtree, target_point=None, neighbors=None):
    plt.figure(figsize=(10, 10))
    all_points = []
    def collect_points(node):
        all_points.extend(node.points)
        if node.divided:
            collect_points(node.northwest)
            collect_points(node.northeast)
            collect_points(node.southwest)
            collect_points(node.southeast)
    collect_points(quadtree)

    x = [p.x for p in all_points]
    y = [p.y for p in all_points]
    ids = [p.id for p in all_points]

    plt.scatter(x, y, c='blue', label='Преподаватели')

    if target_point:
        plt.scatter(target_point.x, target_point.y, c='red', label=f'Выбранный ID: {target_point.id}')
    if neighbors:
        nx = [p.x for p in neighbors]
        ny = [p.y for p in neighbors]
        plt.scatter(nx, ny, c='green', label='Ближайшие соседи')

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Распределение преподавателей и их ближайшие соседи на сессии')
    plt.grid(True)
    plt.show()

# Основная функция
def main():
    # Настройки
    NUM_POINTS = 100  # Количество объектов
    X_RANGE = (0, 100)
    Y_RANGE = (0, 100)
    CAPACITY = 4      # Вместимость узла перед разделением
    MAX_DEPTH = 10    # Максимальная глубина квадродерева

    # Генерация случайных точек
    points = generate_random_points(NUM_POINTS, X_RANGE, Y_RANGE)

    # Создание квадродерева
    boundary = Rectangle((X_RANGE[0] + X_RANGE[1])/2, (Y_RANGE[0] + Y_RANGE[1])/2, X_RANGE[1]-X_RANGE[0], Y_RANGE[1]-Y_RANGE[0])
    quadtree = Quadtree(boundary, CAPACITY, depth=0, max_depth=MAX_DEPTH)

    # Вставка точек в квадродерево
    for p in points:
        quadtree.insert(p)

    while True:
        try:
            user_input = input("Введите ID преподавателя (или 'exit' для выхода): ")
            if user_input.lower() == 'exit':
                break
            target_id = int(user_input)
            target_point = quadtree.find_point_by_id(target_id)
            if not target_point:
                print(f"Преподаватель с ID {target_id} не найден.")
                continue
            neighbors = find_nearest_neighbors(quadtree, target_point, k=5)
            print(f"Ближайшие соседи для ID {target_id}:")
            for neighbor in neighbors:
                print(f"ID: {neighbor.id}, Координаты: ({neighbor.x:.2f}, {neighbor.y:.2f}), Расстояние: {target_point.distance_to(neighbor):.2f}")
            visualize(quadtree, target_point, neighbors)
        except ValueError:
            print("Пожалуйста, введите корректный числовой ID.")
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break

if __name__ == "__main__":
    main()
