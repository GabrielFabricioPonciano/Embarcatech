import time
import board
import digitalio
import analogio
import usb_hid
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)

joystick_x = analogio.AnalogIn(board.GP27)
joystick_y = analogio.AnalogIn(board.GP26)

botao_a = digitalio.DigitalInOut(board.GP5)
botao_a.direction = digitalio.Direction.INPUT
botao_a.pull = digitalio.Pull.UP

botao_b = digitalio.DigitalInOut(board.GP6)
botao_b.direction = digitalio.Direction.INPUT
botao_b.pull = digitalio.Pull.UP

# Novos parâmetros de ajuste
DEADZONE = 2000       # Zona morta para evitar drift
SENSIBILIDADE = 550  # Reduzida a sensibilidade para 150
INVERTER_Y = True     # Inverte o eixo vertical
INVERTER_X = False    # Inverte o eixo horizontal (adicionei essa variável)

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

while True:
    mov_x = ajustar_eixo(joystick_x.value, inverter=INVERTER_X)
    mov_y = ajustar_eixo(joystick_y.value, inverter=INVERTER_Y)

    if mov_x != 0 or mov_y != 0:
        mouse.move(x=mov_x, y=mov_y)

    if not botao_a.value:
        mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.1)
    if not botao_b.value:
        mouse.click(Mouse.RIGHT_BUTTON)
        time.sleep(0.1)

    time.sleep(0.01)
