import pygame
import random
import sys

# Inicializando o pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo das Linguagens de Programação")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Carregar imagens das linguagens de programação
IMAGES = {
    "Python": pygame.image.load("Debug Premiado/python.png"),
    "Java": pygame.image.load("Debug Premiado/java.png"),
    "C++": pygame.image.load("Debug Premiado/cpp.png"),
    "Ruby": pygame.image.load("Debug Premiado/ruby.png"),
}

# Redimensionar as imagens
for key in IMAGES:
    IMAGES[key] = pygame.transform.scale(IMAGES[key], (100, 100))

# Função para desenhar o texto centralizado na tela
font = pygame.font.Font(None, 36)
def draw_text_centered(text, y, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(text_surface, text_rect)

# Função para desenhar texto centralizado em um botão
def draw_button_text(text, button_rect, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

# Configuração inicial do jogo
clock = pygame.time.Clock()
running = True
selected_language = ""
bet_amount = 0
player_balance = 1000
symbols = ["Python", "Java", "C++", "Ruby"]
roll_results = ["", "", ""]
rolling = False
animation_counters = [0, 0, 0]
roll_speeds = [0, 0, 0]
start_time = 0
ROLL_DURATION = 3000  # Duração da rotação em milissegundos
show_confetti = False
confetti_particles = []

# Botões
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
SPACING = 30

# Posicionamento dos botões de linguagem no centro da tela
button_start_x = (SCREEN_WIDTH - (len(symbols) * (BUTTON_WIDTH + SPACING) - SPACING)) // 2
select_buttons = {
    lang: pygame.Rect(
        button_start_x + i * (BUTTON_WIDTH + SPACING),
        SCREEN_HEIGHT - 150,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    ) for i, lang in enumerate(symbols)
}

# Botão de girar centralizado abaixo dos botões de linguagem
roll_button_rect = pygame.Rect(
    (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
    SCREEN_HEIGHT - 80,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Função para iniciar os rolos
def start_roll():
    global rolling, roll_results, animation_counters, roll_speeds, start_time, show_confetti, confetti_particles
    rolling = True
    roll_results = [random.choice(symbols) for _ in range(3)]
    animation_counters = [0, 0, 0]
    roll_speeds = [random.randint(10, 20), random.randint(20, 30), random.randint(30, 40)]
    start_time = pygame.time.get_ticks()
    show_confetti = False
    confetti_particles = []

# Função para verificar o resultado
def check_results():
    if roll_results[0] == roll_results[1] == roll_results[2] == selected_language:
        return True
    return False

# Função para gerar confetes
def generate_confetti():
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        color = random.choice([RED, GREEN, BLACK, GRAY])
        confetti_particles.append({"x": x, "y": y, "color": color, "speed": random.randint(1, 5)})

# Atualizar confetes
def update_confetti():
    for particle in confetti_particles:
        particle["y"] += particle["speed"]
        if particle["y"] > SCREEN_HEIGHT:
            particle["y"] = 0
            particle["x"] = random.randint(0, SCREEN_WIDTH)

# Desenhar confetes
def draw_confetti():
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle["color"], (particle["x"], particle["y"]), 5)

# Loop principal do jogo
while running:
    screen.fill(WHITE)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if roll_button_rect.collidepoint(x, y) and not rolling and player_balance >= bet_amount > 0 and selected_language:
                player_balance -= bet_amount
                start_roll()
            for lang, rect in select_buttons.items():
                if rect.collidepoint(x, y):
                    selected_language = lang

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bet_amount += 10
            if event.key == pygame.K_DOWN and bet_amount > 0:
                bet_amount -= 10

    # Atualizar a animação dos rolos
    if rolling:
        current_time = pygame.time.get_ticks()
        if current_time - start_time < ROLL_DURATION:
            for i in range(3):
                animation_counters[i] += roll_speeds[i]
                if animation_counters[i] >= len(symbols) * 100:
                    animation_counters[i] = 0
        else:
            rolling = False
            if check_results():
                winnings = bet_amount * 100
                player_balance += winnings
                show_confetti = True
                generate_confetti()

    # Desenhar texto e interface
    draw_text_centered("Debug Premiado", 30)
    draw_text_centered(f"Saldo: R$ {player_balance}", 80)
    draw_text_centered(f"Aposta: R$ {bet_amount}", 120)
    draw_text_centered(f"Linguagem escolhida: {selected_language}", 160)

    # Mostrar resultados do rolo (com animação)
    slot_start_x = (SCREEN_WIDTH - (3 * 150)) // 2
    for i in range(3):
        if rolling:
            index = (animation_counters[i] // 100) % len(symbols)
            screen.blit(IMAGES[symbols[index]], (slot_start_x + i * 150, 250))
        else:
            # Se o resultado for vazio, mostra o primeiro símbolo
            symbol_to_show = roll_results[i] if roll_results[i] else symbols[0]
            screen.blit(IMAGES[symbol_to_show], (slot_start_x + i * 150, 250))

    # Desenhar confetes
    if show_confetti:
        update_confetti()
        draw_confetti()

    # Desenhar botões de seleção de linguagem
    for lang, rect in select_buttons.items():
        color = GREEN if lang == selected_language else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=5)
        draw_button_text(lang, rect)

    # Desenhar botão de girar
    button_color = RED if not selected_language or bet_amount <= 0 or player_balance < bet_amount else GREEN
    pygame.draw.rect(screen, button_color, roll_button_rect, border_radius=5)
    draw_button_text("GIRAR", roll_button_rect)

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()