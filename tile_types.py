# плиточки в игре - цвета, видимость и все такое
from typing import Tuple

import numpy as np  # type: ignore

# Структурированный тип графики, совместимый с Console.tiles_rgb.
# dtype - +-как struct в си
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # в Unicode из целых чисел
        ("fg", "3B"),  # 3 байта для RGB цветов
        ("bg", "3B"), # задник
    ]
)

# Структура плитки, используемая для статически определенных данных плитки
tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  # истина, если можно пройти
        ("transparent", np.bool_),  # и, если не блокирует поле зрения
        ("dark", graphic_dt),  # графика для открытых плиток вне поля зрения
        ("light", graphic_dt),  # плиточка в поле зрения
    ]
)

#Он создает массив Numpy только из одного элемента tile_dt и возвращает его.
def new_tile(
    *,  # Принудительно используйте ключевые слова, чтобы порядок параметров не имел значения
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Вспомогательная функция для придания индивидуальности плитке"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD представляет неоткрытые, невидимые плитки
# вообще это библиотека для сокрытия кода программы от прямого чтения
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


# ord - из юникода в целое число
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
    # dark=(ord("."), (100, 100, 100), (0, 0, 0)),
    # light=(ord("."), (200, 200, 200), (0, 0, 0)),

)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
    # dark=(ord("#"), (100, 100, 100), (0, 0, 0)),
    # light=(ord("#"), (200, 200, 200), (0, 0, 0)),
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),
    # dark=(ord(">"), (100, 100, 100), (0, 0, 0)),
    # light=(ord(">"), (200, 200, 200), (0, 0, 0)),
)