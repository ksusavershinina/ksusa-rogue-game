# отвечает за процедурную генерацию уровней (комнат и туннелей)
from __future__ import annotations
import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
import entity_factories
import tcod

max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]
item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 80)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}


def get_max_value_for_floor(

    max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    """goes through they keys (floor numbers) and values (list of weighted entities),
    stopping when the key is higher than the given floor number."""
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities
# нужен для создания комнат
class RectangularRoom:
    """создание прямоугольной комнаты"""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """координаты центра комнаты"""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Возвращает внутреннюю часть нашей комнаты"""
        # +1 надо для того, чтобы были двойные стенки.
        # Поможет избежать случайного отсуствият стены между комнатами рядом
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    # проверяет комнаты на пересечения
    def intersects(self, other: RectangularRoom) -> bool:
        # other - другая комната, с которой чекаем пересечение
        """Возвращает истину, если наша комната пересекается с другой комнатой"""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )

def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Возращает туннель между двумя точками в форме L"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50 процентов шанс
        # сначала горизонтально, потом вертикально
        corner_x, corner_y = x2, y1
    else:
        # сначала вертикально, потом горизонтально
        corner_x, corner_y = x1, y2

    # генерирует координаты для этого туннеля
    # использует алгоритм брезенхема - определяет, какие точки
    # двумерного пространства нужно закрасить, чтобы получить близкое
    # приближение прямой линии между двумя заданными точками.
    # los - алгоритмы прямой
    #
    # видимости, которые определяют, какие объекты
    # или области находятся в непосредственной "видимости" друг от друга
    # в двумерном или трехмерном пространстве
    # поток конвертируем в numpy list - в линию

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
        # По сути, вместо того, чтобы возвращать значения и полностью выходить
        # из функции, мы возвращаем значения, но сохраняем локальное состояние.
        # позволяет функции при повторном вызове продолжить отсюда, а не сначала
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

# yield - испольщуется для создания генераторов. Позволяют создавать
# последовательности значений, которые могут быть получены по одному
# элементу за раз. при вызове возращает обьект-итератор, который можно использовать
# для получения значений полседовательности

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Создание нового подземелья"""
    player = engine.player
    # создаем начальную карту
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" класс делает проще работу с комнатами
        new_room = RectangularRoom(x, y, room_width, room_height)

        # чекаем на пересечения
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # пересекается, так что скипаем

        # Создаем внутреннюю часть этой комнаты
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # первая комната, где начинаем
            player.place(*new_room.center, dungeon)
        else:  # все комнаты после первой
            # делаем туннель между этой комнатой и предыдущей
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
            center_of_last_room = new_room.center
        # помещает сущности в комнаты
        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # добавляем новую комнату в листик
        rooms.append(new_room)

    return dungeon



