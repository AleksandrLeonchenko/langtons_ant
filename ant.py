import os
import psutil
import numpy as np
from PIL import Image


def field_init(width: int, height: int) -> np.ndarray:  # Инициализация поля
    """
    Здесь инициализируется поле размером width x height.

    Parameters:
    - width (int): Ширина поля.
    - height (int): Высота поля.

    Returns:
    - np.ndarray: Инициализированное поле.
    """
    return np.zeros((height, width), dtype=np.uint8)


def move_ant(x: int, y: int, direction: int, field: np.ndarray) -> tuple[int, int]:
    """
    Здесь осуществляется перемещение муравья от его текущего положения и направления.

    Parameters:
    - x (int): Текущая координата x муравья.
    - y (int): Текущая координата y муравья.
    - direction (int): Текущее направление муравья (0 - вверх, 1 - вправо, 2 - вниз, 3 - влево).
    - field (np.ndarray): Поле.

    Returns:
    - tuple[int, int]: Новые координаты муравья после изменения положения.
    """
    # if direction == 0:  # Вверх
    #     return (x, (y - 1) % field.shape[0])
    # elif direction == 1:  # Вправо
    #     return ((x + 1) % field.shape[1], y)
    # elif direction == 2:  # Вниз
    #     return (x, (y + 1) % field.shape[0])
    # elif direction == 3:  # Влево
    #     return ((x - 1) % field.shape[1], y)

    if direction == 0:  # Вверх
        return (x, (y - 1) % field.shape[0])
    elif direction == 1:  # Вправо
        return ((x - 1) % field.shape[1], y)
    elif direction == 2:  # Вниз
        return (x, (y + 1) % field.shape[0])
    elif direction == 3:  # Влево
        return ((x + 1) % field.shape[1], y)


def reached_boundary(x: int, y: int, width: int, height: int) -> bool:
    """
    Здесь проверяется, достиг ли муравей границы поля.

    Parameters:
    - x (int): Текущая координата x муравья.
    - y (int): Текущая координата y муравья.
    - width (int): Ширина поля.
    - height (int): Высота поля.

    Returns:
    - bool: True, если муравей достиг границы, False в противном случае.
    """
    return x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1


def main():
    """
    Движение муравья и сохранение результатов.
    """
    width: int = 1024  # Размеры поля
    height: int = 1024
    field: np.ndarray = field_init(width, height)  # Инициализация поля
    ant_x: int = width // 2  # Положение начальное муравья
    ant_y: int = height // 2
    ant_direction: int = 0  # Направление начальное муравья: 0 - вверх (1 - вправо, 2 - вниз, 3 - влево)

    steps: int = 0  # Шаги (для подсчёта)

    # Движение муравья:
    while not reached_boundary(ant_x, ant_y, width, height):  # Пока муравей не достиг границы:
        field[ant_y, ant_x] = 255 - field[ant_y, ant_x]  # Инвертирование цвета текущей клетки
        ant_direction = (ant_direction + (
            1 if field[ant_y, ant_x] == 0 else -1)) % 4  # Поворот муравья (в завис. от цвета)
        ant_x, ant_y = move_ant(ant_x, ant_y, ant_direction, field)  # Перемещение муравья (в завис. от направления)

        steps += 1

    img: Image.Image = Image.fromarray(field, 'L')
    img.save('ant_path.bmp', format='BMP', bits=1)
    black_cells: int = np.sum(field == 0)  # Количество черных клеток
    white_cells: int = np.sum(field == 255)  # Количество белых клеток (для проверки)
    print(f"Всего {steps} шагов. Черных клеток: {black_cells}. Белых клеток: {white_cells}.")

    # Считаем память:
    pid: int = os.getpid()  # Идентификатор процесса
    py: psutil.Process = psutil.Process(pid)
    memory_use: float = py.memory_info()[0] / 2. ** 30  # B > GB
    print(f"Используется памяти: {memory_use:.2f} GB")


if __name__ == "__main__":
    main()
