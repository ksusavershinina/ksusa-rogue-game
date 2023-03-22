# показывает, в каком порядке будут рендериться трупы и живые существа
from enum import auto, Enum
# enum - сет переменных, которые не меняются
class RenderOrder(Enum):
    CORPSE = auto() # труп. низжий порядок рендера
    ITEM = auto()
    ACTOR = auto()