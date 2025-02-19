import time
import board
import digitalio
import analogio
import usb_hid
from adafruit_hid.mouse import Mouse

# --- Configuração do Mouse ---
mouse = Mouse(usb_hid.devices)

# --- Configuração do Joystick ---
joystick_x = analogio.AnalogIn(board.GP27)
joystick_y = analogio.AnalogIn(board.GP26)

# --- Configuração dos Botões ---
botao_a = digitalio.DigitalInOut(board.GP5)  # Botão esquerdo
botao_a.direction = digitalio.Direction.INPUT
botao_a.pull = digitalio.Pull.UP

botao_b = digitalio.DigitalInOut(board.GP6)  # Botão direito
botao_b.direction = digitalio.Direction.INPUT
botao_b.pull = digitalio.Pull.UP

botao_scroll = digitalio.DigitalInOut(board.GP22)  # Botão para scroll
botao_scroll.direction = digitalio.Direction.INPUT
botao_scroll.pull = digitalio.Pull.UP

# --- Parâmetros de Ajuste ---
DEADZONE = 2000       # Zona morta para evitar drift
SENSIBILIDADE = 550   # Sensibilidade do joystick (movimento do cursor)
SENSIBILIDADE_SCROLL = 2500  # Sensibilidade do scroll (quanto maior, mais lento)
INVERTER_Y = True     # Inverte o eixo vertical
INVERTER_X = False    # Inverte o eixo horizontal

# --- Variáveis de Estado ---
botao_a_pressionado = False
botao_b_pressionado = False
modo_scroll = False

def ajustar_eixo(valor, centro=32768, inverter=False):
    valor_ajustado = valor - centro
    
    # Aplica zona morta
    if abs(valor_ajustado) < DEADZONE:
        return 0
        
    # Aplica inversão se necessário
    if inverter:
        valor_ajustado = -valor_ajustado
    
    # Ajusta a sensibilidade e limita a faixa
    movimento = valor_ajustado / SENSIBILIDADE
    return int(max(-127, min(movimento, 127)))

# --- Loop Principal ---
while True:
    # Leitura e processamento do joystick
    mov_x = ajustar_eixo(joystick_x.value, inverter=INVERTER_X)
    mov_y = ajustar_eixo(joystick_y.value, inverter=INVERTER_Y)

    # Verificação do botão de scroll
    if not botao_scroll.value:
        if not modo_scroll:
            modo_scroll = True
        # Scroll com o eixo Y (ajustado pela sensibilidade do scroll)
        scroll_y = mov_y / (SENSIBILIDADE_SCROLL / 100)  # Ajuste fino
        mouse.move(wheel=-int(scroll_y))  # Invertido para direção natural
    else:
        if modo_scroll:
            modo_scroll = False
        # Movimento normal do mouse
        if mov_x != 0 or mov_y != 0:
            mouse.move(x=mov_x, y=mov_y)

    # Verificação do botão A (clique esquerdo)
    if not botao_a.value:
        if not botao_a_pressionado:
            mouse.press(Mouse.LEFT_BUTTON)
            botao_a_pressionado = True
    else:
        if botao_a_pressionado:
            mouse.release(Mouse.LEFT_BUTTON)
            botao_a_pressionado = False

    # Verificação do botão B (clique direito)
    if not botao_b.value:
        if not botao_b_pressionado:
            mouse.press(Mouse.RIGHT_BUTTON)
            botao_b_pressionado = True
    else:
        if botao_b_pressionado:
            mouse.release(Mouse.RIGHT_BUTTON)
            botao_b_pressionado = False

    time.sleep(0.01)  # Pequeno delay para evitar sobrecarga
