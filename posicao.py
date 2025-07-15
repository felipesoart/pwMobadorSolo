import pyautogui
import time

print("Posicione o mouse onde quiser. Em 5 segundos vai mostrar a posição a cada segundo.\nCTRL+C pra parar!")

time.sleep(5)


try:
    while True:
        x, y = pyautogui.position()
        print(f"Posição atual: x={x}, y={y}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nEncerrado.")


