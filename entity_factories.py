# файл для определения всех сущностей, которые есть в игре
# тут находятся все их перки, так что для подрубления читов надо заходить сюда, гы
from components.ai import HostileEnemy
from components import consumable, equippable
from components.fighter import Fighter
from components.equipment import Equipment
from components.inventory import Inventory
from components.cash import Cash
from entity import Actor, Item
from components.level import Level

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=300, base_defense=1, base_power=50),
    inventory=Inventory(capacity=26), # каждая буква алфавита соответствует слоту, так что их 26
    money=Cash(current_cash=0),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    money=Cash(money_given=10),
    level=Level(xp_given=35),
)
troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    money=Cash(money_given=20),
    level=Level(xp_given=100),
)
confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=2),
)
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=5),
)
lightning_scroll = Item(
    char="~",
    color=(139, 135, 119),
    name="Mjolnir Scroll",
    consumable=consumable.LightningDamageConsumable(damage=30, maximum_range=5),
)
dagger = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger()
)

sword = Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail()
)
