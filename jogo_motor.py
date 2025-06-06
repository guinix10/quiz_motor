# Importa bibliotecas necessárias G
import pygame
import sys

# Verifica se foi enviado o tipo de ligação automaticamente (streamlit) M
if len(sys.argv) > 1:
    choice = sys.argv[1]  # 'estrela' ou 'triangulo'
    menu = False  # pula o menu se estiver usando argumento

# Inicializa o Pygame e configura a janela I
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Conexão Motor: Estrela ou Triângulo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)

# Inicializa variáveis de animação do motor I
motor_frame = 0
motor_frame_timer = 0

# Carrega e redimensiona imagens do motor parado e girando I
motor_img_parado = pygame.image.load("motorparado.png").convert_alpha()
motor_imgs_ligado = [
    pygame.image.load(f"motor{i}.png").convert_alpha() for i in range(1, 4)
]
motor_img_parado = pygame.transform.scale(motor_img_parado, (80, 80))
motor_imgs_ligado = [pygame.transform.scale(img, (80, 80)) for img in motor_imgs_ligado]

# Define cores utilizadas no jogo I
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
YELLOW = (255, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Variáveis de controle do estado do jogo I
menu = True
choice = None
message_game = ""
quiz_mode = False
quiz_message = ""
quiz_correct = False
answer_selected = False

# Botões da interface I
estrela_button = pygame.Rect(165, 250, 270, 80)
triangulo_button = pygame.Rect(465, 250, 270, 80)
button_rect = pygame.Rect(370, 430, 160, 50)
restart_button = pygame.Rect(350, 500, 200, 50)
reset_button = pygame.Rect(700, 500, 180, 50)

# Dados do quiz M
quiz_question = ""
quiz_options = []
correct_option = ""

# Define cores e posições dos fios I
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255)
]
names_left = ["R", "S", "T", "4", "5", "6"]
left_positions = [(150, 100 + i * 70) for i in range(6)]

# Define posições dos buracos da direita para estrela e triângulo G
estrela_right_positions = [(750, 100), (750, 170), (750, 240), (750, 400)]
triangulo_right_positions = [(750, 100), (750, 170), (750, 240)]

# Conexões corretas para estrela I
estrela_conexoes_corretas = {
    0: estrela_right_positions[0],
    1: estrela_right_positions[1],
    2: estrela_right_positions[2],
    3: estrela_right_positions[3],
    4: estrela_right_positions[3],
    5: estrela_right_positions[3],
}

# Conexões corretas para triângulo I
triangulo_conexoes_corretas = {
    0: triangulo_right_positions[0],
    1: triangulo_right_positions[1],
    2: triangulo_right_positions[2],
    3: triangulo_right_positions[1],
    4: triangulo_right_positions[2],
    5: triangulo_right_positions[0],
}

# Variáveis para controle da lógica dos fios M
wires = []
right_holes = {}
selected_wire = None
motor_ligado = False
show_reset_button = False
motor_angle = 0

# Lista para os botões do quiz M
quiz_buttons = []

# Carrega som de clique I
click_sound = pygame.mixer.Sound("somclicker.mp3")

# Inicializa o jogo no modo estrela M
def init_game_estrela():
    global wires, right_holes, selected_wire, motor_ligado, message_game, show_reset_button, motor_angle
    wires = []
    for i in range(6):
        wires.append({
            'color': COLORS[i],
            'left': left_positions[i],
            'connected_to': None,
            'index': i
        })
    right_holes.clear()
    right_holes.update({
        "      1": estrela_right_positions[0],
        "      2": estrela_right_positions[1],
        "      3": estrela_right_positions[2],
        "      Estrela": estrela_right_positions[3]
    })
    selected_wire = None
    motor_ligado = False
    show_reset_button = False
    message_game = ""
    motor_angle = 0

# Inicializa o jogo no modo triângulo I
def init_game_triangulo():
    global wires, right_holes, selected_wire, motor_ligado, message_game, show_reset_button, motor_angle
    wires = []
    for i in range(6):
        wires.append({
            'color': COLORS[i],
            'left': left_positions[i],
            'connected_to': None,
            'index': i
        })
    right_holes.clear()
    right_holes.update({
        "      1": triangulo_right_positions[0],
        "      2": triangulo_right_positions[1],
        "      3": triangulo_right_positions[2],
    })
    selected_wire = None
    motor_ligado = False
    show_reset_button = False
    message_game = ""
    motor_angle = 0

# Desenha a imagem do motor (parado ou animado) I
def draw_motor():
    global motor_frame, motor_frame_timer
    pos = (60, 460)
    if motor_ligado:
        motor_frame_timer += 1
        if motor_frame_timer >= 5:
            motor_frame = (motor_frame + 1) % len(motor_imgs_ligado)
            motor_frame_timer = 0
        screen.blit(motor_imgs_ligado[motor_frame], pos)
    else:
        screen.blit(motor_img_parado, pos)

# Desenha fios e buracos de conexão G
def draw_wires():
    for i, wire in enumerate(wires):
        pygame.draw.circle(screen, wire['color'], wire['left'], 15)
        left_label = font.render(names_left[i], True, WHITE)
        screen.blit(left_label, (wire['left'][0] - 20, wire['left'][1] - 30))
        if wire['connected_to']:
            pygame.draw.line(screen, wire['color'], wire['left'], wire['connected_to'], 5)

    for name, pos in right_holes.items():
        pygame.draw.circle(screen, GRAY, pos, 20)
        right_label = font.render(name, True, WHITE)
        screen.blit(right_label, (pos[0] - 15, pos[1] - 30))

# Verifica se todos os fios estão conectados M
def all_connected():
    return all(wire['connected_to'] is not None for wire in wires)

# Verifica se todas as conexões estão corretas no modo estrela M
def check_estrela():
    for i, wire in enumerate(wires):
        correto = estrela_conexoes_corretas[i]
        if wire['connected_to'] != correto:
            return False
    return True

# Verifica se todas as conexões estão corretas no modo triângulo I
def check_triangulo():
    for i, wire in enumerate(wires):
        correto = triangulo_conexoes_corretas[i]
        if wire['connected_to'] != correto:
            return False
    return True

# Desenha um botão com texto em geral M
def draw_button(rect, text, color_bg=(0, 150, 0)):
    pygame.draw.rect(screen, color_bg, rect)
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# Desenha a tela de menu com botões de escolha I
def draw_menu():
    screen.fill(DARK_GRAY)
    title = big_font.render("Escolha o tipo de fechamento", True, WHITE)
    screen.blit(title, (190, 150))

    pygame.draw.rect(screen, (0, 120, 200), estrela_button)
    estrela_text = font.render("Fechamento Estrela", True, WHITE)
    screen.blit(estrela_text, estrela_text.get_rect(center=estrela_button.center))

    pygame.draw.rect(screen, (200, 120, 0), triangulo_button)
    triangulo_text = font.render("Fechamento Triângulo", True, WHITE)
    screen.blit(triangulo_text, triangulo_text.get_rect(center=triangulo_button.center))

    # Muda o cursor do mouse G
    mouse_pos = pygame.mouse.get_pos()
    if estrela_button.collidepoint(mouse_pos) or triangulo_button.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Exibe uma pergunta de quiz com opções de resposta M
def show_quiz(question, options, correct):
    global quiz_mode, quiz_question, quiz_options, correct_option, quiz_buttons, answer_selected
    quiz_mode = True
    quiz_question = question
    quiz_options = options
    correct_option = correct
    quiz_buttons = [pygame.Rect(300, 250 + i * 80, 300, 60) for i in range(len(options))]
    answer_selected = False

# Desenha a tela do quiz M
def draw_quiz():
    screen.fill(BLACK)
    title = big_font.render(quiz_question, True, WHITE)
    screen.blit(title, (100, 100))

    for i, rect in enumerate(quiz_buttons):
        pygame.draw.rect(screen, DARK_GRAY, rect)
        text = font.render(quiz_options[i], True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

    if quiz_message:
        msg = big_font.render(quiz_message, True, GREEN if quiz_correct else RED)
        screen.blit(msg, (150, 450))

    if answer_selected:
        draw_button(restart_button, "Reiniciar", (0, 120, 200) if quiz_correct else (200, 0, 0))

# Função principal de jogo para cada modo. T
def game_loop(logic_check, right_conns):
    global selected_wire, motor_ligado, message_game, show_reset_button

    screen.fill((10, 10, 30) if logic_check == check_estrela else (30, 10, 10))
    draw_motor()
    draw_wires()

    if selected_wire:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, selected_wire['color'], selected_wire['left'], mouse_pos, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Inicia quiz ao clicar no botão quando motor estiver ligado G
            if motor_ligado and button_rect.collidepoint(pos):
                if logic_check == check_triangulo:
                    show_quiz("Qual tensão do fechamento em triângulo?", ["220V", "380V"], "380V")
                    return True
                elif logic_check == check_estrela:
                    show_quiz("Qual tensão do fechamento em estrela?", ["220V", "380V"], "220V")
                    return True

            # Reinicia o jogo ao clicar em "Reiniciar" G
            if show_reset_button and reset_button.collidepoint(pos):
                if choice == "estrela":
                    init_game_estrela()
                elif choice == "triangulo":
                    init_game_triangulo()
                return True

            # Seleciona e conecta fios com cliques. I M
            if not motor_ligado:
                if not selected_wire:
                    for wire in wires:
                        if not wire['connected_to']:
                            dx = pos[0] - wire['left'][0]
                            dy = pos[1] - wire['left'][1]
                            if dx * dx + dy * dy <= 225:
                                selected_wire = wire
                                break
                else:
                    for _, hole_pos in right_holes.items():
                        dx = pos[0] - hole_pos[0]
                        dy = pos[1] - hole_pos[1]
                        if dx * dx + dy * dy <= 400:
                            selected_wire['connected_to'] = hole_pos
                            pygame.mixer.Sound.play(click_sound)
                            selected_wire = None
                            break
                    selected_wire = None

    # Verifica conexões e atualiza estado do motor M
    if not motor_ligado:
        if all_connected():
            if logic_check():
                message_game = "Motor Ligado!"
                motor_ligado = True
                show_reset_button = False
            else:
                message_game = "Curto ou erro de ligação!"
                show_reset_button = True
        else:
            message_game = ""

    # Exibe modo atual do jogo I
    if choice:
        modo = font.render(f"Modo: {choice.capitalize()}", True, WHITE)
        screen.blit(modo, (10, 10))

    # Exibe mensagem do jogo (ligado ou erro) G
    if message_game:
        color_msg = GREEN if "Ligado" in message_game else YELLOW
        msg = big_font.render(message_game, True, color_msg)
        screen.blit(msg, (200, 490))

    # Mostra botões conforme estado do jogo I
    if motor_ligado:
        draw_button(button_rect, "Próxima fase")

    if show_reset_button:
        draw_button(reset_button, "Reiniciar", (200, 0, 0))

    pygame.display.flip()
    clock.tick(60)
    return True

# Loop principal do jogo G
running = True
while running:
    if quiz_mode:
        draw_quiz()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not answer_selected:
                    for i, rect in enumerate(quiz_buttons):
                        if rect.collidepoint(pos):
                            selected = quiz_options[i]
                            quiz_correct = selected == correct_option
                            quiz_message = "Parabéns! Seu motor não queimou" if quiz_correct else "*Explosão!* Motor queimado"
                            answer_selected = True
                if restart_button.collidepoint(pos):
                    quiz_mode = False
                    menu = True
                    quiz_message = ""
                    quiz_correct = False
                    answer_selected = False
        pygame.display.flip()
        clock.tick(60)

    elif menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if estrela_button.collidepoint(pos):
                    menu = False
                    choice = "estrela"
                    init_game_estrela()
                elif triangulo_button.collidepoint(pos):
                    menu = False
                    choice = "triangulo"
                    init_game_triangulo()
        pygame.display.flip()
        clock.tick(60)

    else:
        if choice == "estrela":
            running = game_loop(check_estrela, estrela_conexoes_corretas)
        elif choice == "triangulo":
            running = game_loop(check_triangulo, triangulo_conexoes_corretas)


pygame.quit()