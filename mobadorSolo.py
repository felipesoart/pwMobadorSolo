import pyautogui
import time
from pynput import keyboard

# Flag global para parar com ESC
stop_flag = False

def selecionar_mob():
    pyautogui.press('tab')
    print("[INFO] Procurando mob (TAB)")

def coleta_itens():
    pyautogui.press('4')
    print("[INFO] Coletando itens (4)")

def atacar_mob():
    time.sleep(2)
    
    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")

    # Espera 15 segundos
    time.sleep(3)

    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")      
    
    # Espera 15 segundos
    time.sleep(3)

    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")    
        # Espera 15 segundos
    time.sleep(3)

    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")    

    # Depois coleta itens
    coleta_itens()  

    # Espera 15 segundos
    time.sleep(3)

    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")    

    # Depois coleta itens
    coleta_itens()

def replay_clicks(repeat_count):    

    time.sleep(5)

    global stop_flag4

    for i in range(repeat_count):
        if stop_flag:
            print("[INFO] Encerrado pela tecla ESC.")
            break

        print(f"Repetindo... Rodada {i+1}")
        time.sleep(5)
        selecionar_mob()
        atacar_mob()
        

def on_press(key):
    global stop_flag
    if key == keyboard.Key.esc:
        stop_flag = True
        print("[INFO] Tecla ESC detectada! Encerrando...")

if __name__ == "__main__":
    repeat_times = int(input("Quantas vezes deseja repetir? "))

    # Listener do teclado para ESC
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    replay_clicks(repeat_times)

    listener.stop()
