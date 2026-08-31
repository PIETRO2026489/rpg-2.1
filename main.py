import pygame
import random
import math
import sys

pygame.init()

# ============================================================
# CONFIGURAÇÃO
# ============================================================

WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elementaria RPG")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 34, bold=True)
TITLE_FONT = pygame.font.SysFont("arial", 52, bold=True)

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
RED = (220, 50, 50)
GREEN = (50, 210, 90)
BLUE = (60, 140, 240)
GOLD = (240, 190, 50)
GRAY = (100, 100, 110)

# ============================================================
# ELEMENTOS
# ============================================================

ELEMENTS = {
    "Fogo": {
        "color": (235, 70, 30),
        "attacks": [
            ("Brasa", 20, 25, 10, 15),
            ("Bola de Fogo", 30, 40, 15, 25),
            ("Explosão de Fogo", 45, 55, 30, 45)
        ],
        "weak": "Água",
        "strong": "Planta"
    },

    "Água": {
        "color": (40, 150, 240),
        "attacks": [
            ("Jato d'Água", 20, 25, 10, 15),
            ("Surfar", 30, 40, 15, 25),
            ("Hidro Bomba", 45, 55, 30, 45)
        ],
        "weak": "Elétrico",
        "strong": "Fogo"
    },

    "Elétrico": {
        "color": (245, 220, 40),
        "attacks": [
            ("Faísca", 20, 25, 10, 15),
            ("Raio", 30, 40, 15, 25),
            ("Trovoada", 45, 55, 30, 45)
        ],
        "weak": "Planta",
        "strong": "Água"
    },

    "Planta": {
        "color": (50, 190, 70),
        "attacks": [
            ("Chicote de Vinha", 20, 25, 10, 15),
            ("Folha Navalha", 30, 40, 15, 25),
            ("Bomba de Sementes", 45, 55, 30, 45)
        ],
        "weak": "Fogo",
        "strong": "Elétrico"
    },

    "Sombrio": {
        "color": (75, 45, 95),
        "weak": None,
        "strong": "Todos"
    },

    "Terra": {
        "color": (150, 105, 55),
        "weak": "Voador",
        "strong": "Veneno"
    },

    "Voador": {
        "color": (150, 210, 245),
        "weak": "Gelo",
        "strong": "Terra"
    },

    "Gelo": {
        "color": (150, 230, 255),
        "weak": "Fogo",
        "strong": "Voador"
    },

    "Fantasma": {
        "color": (125, 75, 175),
        "weak": "Veneno",
        "strong": ["Água", "Fogo", "Planta", "Elétrico"]
    },

    "Veneno": {
        "color": (130, 55, 155),
        "weak": "Terra",
        "strong": "Fantasma"
    }
}

ISLANDS = [
    ("Ilha Inicial", "Planta", (75, 170, 90)),
    ("Ilha Vulcânica", "Fogo", (190, 65, 35)),
    ("Ilha Aquática", "Água", (40, 140, 210)),
    ("Ilha Eletrônica", "Elétrico", (75, 75, 110)),
    ("Ilha Sombria", "Sombrio", (40, 35, 55)),
    ("Ilha de Terra", "Terra", (150, 110, 70)),
    ("Ilha Voadora", "Voador", (125, 190, 220)),
    ("Ilha de Gelo", "Gelo", (180, 225, 240)),
    ("Ilha Fantasmagórica", "Fantasma", (80, 65, 100)),
    ("Ilha Venenosa", "Veneno", (90, 125, 65))
]

# ============================================================
# JOGADOR
# ============================================================

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.level = 1
        self.xp = 0

        self.element = None
        self.element_level = 1
        self.element_xp = 0

        self.max_hp = 100
        self.hp = 100

        self.max_mana = 100
        self.mana = 100

        self.coins = 100

        self.armor = 0
        self.element_bonus = 0
        self.physical_bonus = 0
        self.dodge = 0

        self.potions_hp = 2
        self.potions_mana = 2

        self.scrolls = []

        self.different_monsters = set()

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= 100 and self.level < 20:
            self.xp -= 100
            self.level += 1

            self.max_hp += 20
            self.max_mana += 20

            self.hp = self.max_hp
            self.mana = self.max_mana

    def gain_element_xp(self, amount):
        self.element_xp += amount

        while self.element_xp >= 100 and self.element_level < 5:
            self.element_xp -= 100
            self.element_level += 1

    def regenerate_mana(self):
        self.mana = min(
            self.max_mana,
            self.mana + random.randint(10, 25)
        )

    def use_hp_potion(self):
        if self.potions_hp > 0 and self.hp < self.max_hp:
            self.potions_hp -= 1
            self.hp = min(
                self.max_hp,
                self.hp + random.randint(20, 35)
            )
            return True
        return False

    def use_mana_potion(self):
        if self.potions_mana > 0 and self.mana < self.max_mana:
            self.potions_mana -= 1
            self.mana = min(
                self.max_mana,
                self.mana + random.randint(20, 35)
            )
            return True
        return False


player = Player()

# ============================================================
# MONSTROS
# ============================================================

class Monster:
    def __init__(self, name, element, level):
        self.name = name
        self.element = element
        self.level = level

        self.max_hp = 70 + level * 30
        self.hp = self.max_hp

        self.max_mana = 50 + level * 15
        self.mana = self.max_mana

        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(120, HEIGHT - 100)

        self.speed = 35 + level * 4

    def move_toward_player(self, dt):
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.hypot(dx, dy)

        if distance > 65:
            if distance:
                self.x += dx / distance * self.speed * dt
                self.y += dy / distance * self.speed * dt


def create_monsters(element, count=3):
    monsters = []

    names = {
        "Fogo": ["Salamandra", "Golem de Lava", "Lagarto Flamejante"],
        "Água": ["Piranha", "Serpente Marinha", "Tubarão Elemental"],
        "Elétrico": ["Drone Vivo", "Rato Elétrico", "Golem Elétrico"],
        "Planta": ["Cogumelo Vivo", "Lobo Planta", "Ent"],
        "Sombrio": ["Demônio Sombrio", "Lobo Negro", "Sombra"],
        "Terra": ["Golem de Terra", "Besouro Rochoso", "Touro de Pedra"],
        "Voador": ["Águia Elemental", "Morcego", "Grifo"],
        "Gelo": ["Pinguim Congelado", "Lobo de Gelo", "Golem de Gelo"],
        "Fantasma": ["Espírito", "Alma Perdida", "Fantasma"],
        "Veneno": ["Cobra", "Escorpião", "Serpente Venenosa"]
    }

    for i in range(count):
        level = random.randint(1, 5)
        monsters.append(
            Monster(names[element][i % 3], element, level)
        )

    return monsters


# ============================================================
# COMBATE
# ============================================================

battle_active = False
current_enemy = None
battle_message = ""

def start_battle(enemy):
    global battle_active, current_enemy, battle_message

    battle_active = True
    current_enemy = enemy
    battle_message = f"{enemy.name} apareceu!"

def calculate_element_damage(base_damage, attack_element, defender_element):
    damage = base_damage

    if player.element_bonus:
        damage += player.element_bonus

    if attack_element == defender_element:
        pass

    data = ELEMENTS.get(attack_element, {})

    weak = data.get("weak")
    strong = data.get("strong")

    if weak == defender_element:
        damage = int(damage * 0.6)

    if strong == defender_element:
        damage = int(damage * 1.5)

    if isinstance(strong, list) and defender_element in strong:
        damage = int(damage * 1.5)

    if defender_element == "Sombrio":
        damage = int(damage * 1.4)

    return damage


def player_attack(index):
    global battle_active, battle_message

    if not current_enemy:
        return

    if index == 0:
        name = "Punho"
        damage = 10 + player.physical_bonus

    else:
        if player.element is None:
            return

        if index == 2 and player.element_level < 2:
            battle_message = "O segundo ataque ainda está bloqueado!"
            return

        if index == 3 and player.element_level < 4:
            battle_message = "O terceiro ataque ainda está bloqueado!"
            return

        attack = ELEMENTS[player.element]["attacks"][index - 1]

        name, min_damage, max_damage, min_mana, max_mana = attack

        mana_cost = random.randint(min_mana, max_mana)

        if player.mana < mana_cost:
            battle_message = "Mana insuficiente!"
            return

        player.mana -= mana_cost

        damage = random.randint(min_damage, max_damage)

        damage = calculate_element_damage(
            damage,
            player.element,
            current_enemy.element
        )

        damage += (player.element_level - 1) * 5

    current_enemy.hp -= damage

    battle_message = f"{name} causou {damage} de dano!"

    if current_enemy.hp <= 0:
        win_battle()
        return

    enemy_turn()


def enemy_turn():
    global battle_message

    if random.random() < player.dodge:
        battle_message = "Você desviou do ataque!"
        player.regenerate_mana()
        return

    base = random.randint(10, 18) + current_enemy.level * 5

    # Cada equipamento comprado aumenta o ataque dos monstros.
    equipment_count = 0

    if player.armor > 0:
        equipment_count += 1

    if player.element_bonus > 0:
        equipment_count += 1

    if player.physical_bonus > 0:
        equipment_count += 1

    if player.dodge > 0:
        equipment_count += 1

    base += equipment_count * 15

    damage = int(base * (1 - player.armor))

    player.hp -= damage

    battle_message += f" O inimigo causou {damage} de dano."

    player.regenerate_mana()

    if player.hp <= 0:
        player.hp = 0
        battle_message = "Você foi derrotado!"
        game_state["screen"] = "game_over"


def win_battle():
    global battle_active, current_enemy, battle_message

    level_rewards = {
        1: ((24, 50), (30, 50)),
        2: ((45, 75), (45, 50)),
        3: ((70, 100), (50, 60)),
        4: ((100, 125), (55, 65)),
        5: ((120, 150), (65, 80))
    }

    coin_range, xp_range = level_rewards[current_enemy.level]

    coins = random.randint(*coin_range)
    xp = random.randint(*xp_range)
    element_xp = random.randint(10, 35)

    player.coins += coins
    player.gain_xp(xp)
    player.gain_element_xp(element_xp)

    player.different_monsters.add(current_enemy.name)

    battle_message = (
        f"Vitória! +{coins} moedas, "
        f"+{xp} XP e +{element_xp} XP elemental."
    )

    battle_active = False
    current_enemy = None

    check_quests()


# ============================================================
# MISSÕES
# ============================================================

quests = {
    "first_monster": False,
    "five_monsters": False,
    "boss": False
}

def check_quests():
    if not quests["first_monster"] and len(player.different_monsters) >= 1:
        quests["first_monster"] = True
        player.coins += 25
        player.gain_xp(15)

    if not quests["five_monsters"] and len(player.different_monsters) >= 5:
        quests["five_monsters"] = True
        player.coins += 50
        player.gain_xp(30)


# ============================================================
# LOJA
# ============================================================

SHOP_ITEMS = {
    "Armadura de Ferro": 250,
    "Armadura de Escamas": 350,
    "Cajado Arcano": 150,
    "Espada de Ferro": 200,
    "Escudo Elemental": 300,
    "Poção de Regeneração": 15,
    "Poção de Mana": 20
}

def buy_item(item):
    if player.coins < SHOP_ITEMS[item]:
        return

    player.coins -= SHOP_ITEMS[item]

    if item == "Armadura de Ferro":
        player.armor = max(player.armor, 0.10)

    elif item == "Armadura de Escamas":
        player.armor = max(player.armor, 0.25)

    elif item == "Cajado Arcano":
        player.element_bonus += 15

    elif item == "Espada de Ferro":
        player.physical_bonus += 20

    elif item == "Escudo Elemental":
        player.dodge = 0.30

    elif item == "Poção de Regeneração":
        player.potions_hp += 1

    elif item == "Poção de Mana":
        player.potions_mana += 1


# ============================================================
# ESTADO DO JOGO
# ============================================================

game_state = {
    "screen": "element_select",
    "island": 0,
    "shop": False,
    "inventory": False
}

completed_dungeons = set()

# ============================================================
# DESENHO
# ============================================================

def draw_text(text, x, y, color=WHITE, font=FONT):
    surface = font.render(str(text), True, color)
    screen.blit(surface, (x, y))


def draw_bar(x, y, width, height, value, maximum, color):
    pygame.draw.rect(
        screen,
        (35, 35, 40),
        (x, y, width, height)
    )

    if maximum > 0:
        current_width = int(width * value / maximum)

        pygame.draw.rect(
            screen,
            color,
            (x, y, current_width, height)
        )

    pygame.draw.rect(
        screen,
        WHITE,
        (x, y, width, height),
        2
    )


def draw_player():
    color = ELEMENTS.get(
        player.element,
        {"color": (230, 230, 240)}
    )["color"]

    # Corpo
    pygame.draw.circle(
        screen,
        color,
        (int(player.x), int(player.y)),
        22
    )

    # Chapéu de mago
    pygame.draw.polygon(
        screen,
        (55, 35, 100),
        [
            (player.x - 20, player.y - 15),
            (player.x + 20, player.y - 15),
            (player.x, player.y - 55)
        ]
    )


def draw_enemy(enemy):
    color = ELEMENTS[enemy.element]["color"]

    pygame.draw.circle(
        screen,
        color,
        (int(enemy.x), int(enemy.y)),
        27
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (int(enemy.x - 8), int(enemy.y - 5)),
        4
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (int(enemy.x + 8), int(enemy.y - 5)),
        4
    )


def draw_world():
    island_name, island_element, bg_color = ISLANDS[game_state["island"]]

    screen.fill(bg_color)

    # Água ao redor
    pygame.draw.rect(
        screen,
        (35, 105, 170),
        (0, 0, WIDTH, 70)
    )

    # Decoração simples
    for i in range(20):
        x = (i * 71 + 40) % WIDTH
        y = 100 + ((i * 113) % (HEIGHT - 130))

        if island_element == "Fogo":
            pygame.draw.polygon(
                screen,
                (90, 50, 35),
                [(x, y + 25), (x + 15, y - 15), (x + 30, y + 25)]
            )

        elif island_element == "Água":
            pygame.draw.circle(
                screen,
                (100, 220, 235),
                (x, y),
                8
            )

        elif island_element == "Planta":
            pygame.draw.rect(
                screen,
                (75, 105, 45),
                (x, y, 8, 30)
            )
            pygame.draw.circle(
                screen,
                (40, 130, 60),
                (x + 4, y - 5),
                15
            )

        elif island_element == "Gelo":
            pygame.draw.polygon(
                screen,
                WHITE,
                [(x, y + 30), (x + 15, y - 15), (x + 30, y + 30)]
            )

        elif island_element == "Sombrio" or island_element == "Fantasma":
            pygame.draw.rect(
                screen,
                (30, 25, 35),
                (x, y, 35, 40)
            )

        else:
            pygame.draw.circle(
                screen,
                (100, 90, 70),
                (x, y),
                14
            )

    draw_player()

    draw_text(
        island_name,
        20,
        20,
        WHITE,
        BIG_FONT
    )

    draw_text(
        f"Nível {player.level} | XP {player.xp}/100",
        20,
        80
    )

    draw_text(
        f"{player.element} Nv. {player.element_level} | "
        f"XP Elemental {player.element_xp}/100",
        20,
        105
    )

    draw_bar(
        20, 135,
        250, 22,
        player.hp,
        player.max_hp,
        RED
    )

    draw_text(
        f"Vida: {player.hp}/{player.max_hp}",
        30, 137
    )

    draw_bar(
        20, 165,
        250, 22,
        player.mana,
        player.max_mana,
        BLUE
    )

    draw_text(
        f"Mana: {player.mana}/{player.max_mana}",
        30, 167
    )

    draw_text(
        f"💰 {player.coins}",
        WIDTH - 160,
        20,
        GOLD,
        BIG_FONT
    )


def draw_inventory():
    screen.fill((25, 25, 35))

    draw_text(
        "INVENTÁRIO",
        40,
        30,
        GOLD,
        TITLE_FONT
    )

    draw_text(
        f"Elemento: {player.element}",
        50, 110
    )

    draw_text(
        f"Nível: {player.level}",
        50, 145
    )

    draw_text(
        f"Nível elemental: {player.element_level}",
        50, 180
    )

    draw_text(
        f"Moedas: {player.coins}",
        50, 215,
        GOLD
    )

    draw_text(
        f"Poções de vida: {player.potions_hp}",
        50, 260
    )

    draw_text(
        f"Poções de mana: {player.potions_mana}",
        50, 295
    )

    draw_text(
        f"Defesa: {int(player.armor * 100)}%",
        50, 340
    )

    draw_text(
        f"Dano elemental extra: +{player.element_bonus}",
        50, 375
    )

    draw_text(
        f"Dano físico extra: +{player.physical_bonus}",
        50, 410
    )

    draw_text(
        f"Esquiva: {int(player.dodge * 100)}%",
        50, 445
    )

    draw_text(
        "Pergaminhos:",
        50, 495,
        GOLD
    )

    if player.scrolls:
        draw_text(
            ", ".join(player.scrolls),
            50, 530
        )
    else:
        draw_text(
            "Nenhum",
            50, 530
        )

    draw_text(
        "Pressione I para voltar",
        50, HEIGHT - 50,
        GRAY
    )


def draw_shop():
    screen.fill((35, 28, 20))

    draw_text(
        "🏪 LOJA",
        40,
        30,
        GOLD,
        TITLE_FONT
    )

    y = 110

    for i, (item, price) in enumerate(SHOP_ITEMS.items()):
        color = WHITE

        if player.coins < price:
            color = GRAY

        draw_text(
            f"{i + 1}. {item} - {price} moedas",
            70,
            y,
            color
        )

        y += 55

    draw_text(
        "Pressione 1-7 para comprar | ESC para sair",
        70,
        HEIGHT - 50,
        GRAY
    )


def draw_element_selection():
    screen.fill((15, 20, 35))

    draw_text(
        "ELEMENTARIA",
        WIDTH // 2 - 180,
        60,
        GOLD,
        TITLE_FONT
    )

    draw_text(
        "Escolha seu elemento",
        WIDTH // 2 - 140,
        130,
        WHITE,
        BIG_FONT
    )

    names = [
        ("1", "Fogo", "🔥"),
        ("2", "Água", "💧"),
        ("3", "Elétrico", "⚡"),
        ("4", "Planta", "🌿")
    ]

    y = 230

    for key, element, emoji in names:
        color = ELEMENTS[element]["color"]

        pygame.draw.rect(
            screen,
            color,
            (WIDTH // 2 - 180, y, 360, 65),
            border_radius=12
        )

        draw_text(
            f"{key} - {emoji} {element}",
            WIDTH // 2 - 130,
            y + 18,
            WHITE,
            BIG_FONT
        )

        y += 85

    draw_text(
        "ATENÇÃO: esta escolha é permanente!",
        WIDTH // 2 - 180,
        600,
        RED
    )


def draw_battle():
    screen.fill((25, 25, 40))

    draw_text(
        "⚔️ BATALHA",
        40,
        25,
        GOLD,
        TITLE_FONT
    )

    # Jogador
    pygame.draw.circle(
        screen,
        ELEMENTS[player.element]["color"],
        (250, 250),
        65
    )

    draw_text(
        "Mago",
        215,
        330,
        WHITE,
        BIG_FONT
    )

    draw_bar(
        120, 370,
        260, 25,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        120, 405,
        260, 25,
        player.mana,
        player.max_mana,
        BLUE
    )

    # Inimigo
    draw_enemy(current_enemy)

    draw_text(
        current_enemy.name,
        820,
        330,
        WHITE,
        BIG_FONT
    )

    draw_text(
        f"Nível {current_enemy.level}",
        850,
        370
    )

    draw_bar(
        760, 405,
        300, 25,
        current_enemy.hp,
        current_enemy.max_hp,
        RED
    )

    draw_bar(
        760, 440,
        300, 25,
        current_enemy.mana,
        current_enemy.max_mana,
        BLUE
    )

    # Menu
    buttons = [
        "0 - Punho",
        "1 - Ataque Elemental 1",
        "2 - Ataque Elemental 2",
        "3 - Ataque Elemental 3",
        "4 - Poção Vida",
        "5 - Poção Mana"
    ]

    y = 510

    for text in buttons:
        draw_text(
            text,
            60,
            y
        )
        y += 28

    draw_text(
        battle_message,
        500,
        570,
        GOLD
    )


# ============================================================
# ESCOLHA DE ELEMENTO
# ============================================================

def select_element(element):
    player.element = element
    game_state["screen"] = "world"


# ============================================================
# EVENTOS
# ============================================================

def handle_event(event):

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # --------------------------------------------------------
    # ESCOLHA DE ELEMENTO
    # --------------------------------------------------------

    if game_state["screen"] == "element_select":

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                select_element("Fogo")

            elif event.key == pygame.K_2:
                select_element("Água")

            elif event.key == pygame.K_3:
                select_element("Elétrico")

            elif event.key == pygame.K_4:
                select_element("Planta")

        return

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    if game_state["screen"] == "game_over":

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

        return

    # --------------------------------------------------------
    # INVENTÁRIO
    # --------------------------------------------------------

    if game_state["screen"] == "inventory":

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                game_state["screen"] = "world"

        return

    # --------------------------------------------------------
    # LOJA
    # --------------------------------------------------------

    if game_state["screen"] == "shop":

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                game_state["screen"] = "world"

            keys = {
                pygame.K_1: "Armadura de Ferro",
                pygame.K_2: "Armadura de Escamas",
                pygame.K_3: "Cajado Arcano",
                pygame.K_4: "Espada de Ferro",
                pygame.K_5: "Escudo Elemental",
                pygame.K_6: "Poção de Regeneração",
                pygame.K_7: "Poção de Mana"
            }

            if event.key in keys:
                buy_item(keys[event.key])

        return

    # --------------------------------------------------------
    # BATALHA
    # --------------------------------------------------------

    if game_state["screen"] == "battle":

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_0:
                player_attack(0)

            elif event.key == pygame.K_1:
                player_attack(1)

            elif event.key == pygame.K_2:
                player_attack(2)

            elif event.key == pygame.K_3:
                player_attack(3)

            elif event.key == pygame.K_4:
                if player.use_hp_potion():
                    enemy_turn()

            elif event.key == pygame.K_5:
                if player.use_mana_potion():
                    enemy_turn()

        return

    # --------------------------------------------------------
    # MUNDO
    # --------------------------------------------------------

    if game_state["screen"] == "world":

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_i:
                game_state["screen"] = "inventory"

            elif event.key == pygame.K_e:
                # Loja simples
                game_state["screen"] = "shop"


# ============================================================
# RESET
# ============================================================

def reset_game():
    global player
    global completed_dungeons

    player = Player()

    completed_dungeons = set()

    game_state["screen"] = "element_select"
    game_state["island"] = 0


# ============================================================
# MOVIMENTO E MONSTROS
# ============================================================

monsters = create_monsters("Planta")

def update_world(dt):

    global monsters

    keys = pygame.key.get_pressed()

    speed = 250

    if keys[pygame.K_w]:
        player.y -= speed * dt

    if keys[pygame.K_s]:
        player.y += speed * dt

    if keys[pygame.K_a]:
        player.x -= speed * dt

    if keys[pygame.K_d]:
        player.x += speed * dt

    player.x = max(30, min(WIDTH - 30, player.x))
    player.y = max(100, min(HEIGHT - 30, player.y))

    for monster in monsters:
        monster.move_toward_player(dt)

        distance = math.hypot(
            player.x - monster.x,
            player.y - monster.y
        )

        if distance < 55 and not battle_active:
            start_battle(monster)
            game_state["screen"] = "battle"
            break


# ============================================================
# DESENHO GAME OVER
# ============================================================

def draw_game_over():
    screen.fill((15, 10, 20))

    draw_text(
        "VOCÊ FOI DERROTADO",
        WIDTH // 2 - 230,
        250,
        RED,
        TITLE_FONT
    )

    draw_text(
        "Pressione R para reiniciar",
        WIDTH // 2 - 150,
        340,
        WHITE
    )


# ============================================================
# LOOP PRINCIPAL
# ============================================================

running = True

while running:

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        handle_event(event)

    if game_state["screen"] == "world":
        update_world(dt)

    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    if game_state["screen"] == "element_select":

        draw_element_selection()

    elif game_state["screen"] == "world":

        draw_world()

        for monster in monsters:
            draw_enemy(monster)

        draw_text(
            "WASD: mover | E: loja | I: inventário",
            20,
            HEIGHT - 35,
            WHITE
        )

    elif game_state["screen"] == "inventory":

        draw_inventory()

    elif game_state["screen"] == "shop":

        draw_shop()

    elif game_state["screen"] == "battle":

        draw_battle()

    elif game_state["screen"] == "game_over":

        draw_game_over()

    pygame.display.flip()

pygame.quit()
