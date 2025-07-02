import time
import json
from pynput import mouse, keyboard
from pynput.mouse import Controller, Button
import pyautogui

# Arquivo onde vamos salvar os cliques
FILENAME = "clicks.json"

recorded_clicks = []
mouse_controller = Controller()
start_time = None
MAX_DURATION = 180  # 3 minutos em segundos

# Flag pra parar tudo com ESC
stop_flag = False

def on_click(x, y, button, pressed):
    global start_time, stop_flag

    if pressed:
        if start_time is None:
            start_time = time.time()

        elapsed = time.time() - start_time
        click_time = elapsed
        recorded_clicks.append((x, y, click_time))
        print(f"Clique gravado em ({x}, {y}) no t={click_time:.2f}s")

        if elapsed >= MAX_DURATION:
            print("Tempo máximo atingido! Gravação encerrada.")
            stop_flag = True
            return False

        if stop_flag:
            print("Gravação encerrada pela tecla ESC.")
            return False

def on_press(key):
    global stop_flag
    try:
        if key == keyboard.Key.esc:
            stop_flag = True
            print("ESC pressionado! Encerrando execução...")
            return False  # Para o listener do teclado também
    except:
        pass

def save_clicks():
    with open(FILENAME, "w") as f:
        json.dump(recorded_clicks, f)
    print(f"Cliques salvos em {FILENAME}")

def load_clicks():
    with open(FILENAME, "r") as f:
        clicks = json.load(f)
    return clicks

def replay_clicks(clicks, repeat_count):
    global stop_flag

    for i in range(repeat_count):
        if stop_flag:
            print("Execução interrompida pelo ESC.")
            break

        print(f"Repetindo... Rodada {i+1}")
        last_time = 0

        for x, y, click_time in clicks:
            if stop_flag:
                print("Execução interrompida pelo ESC durante cliques.")
                break

            time.sleep(click_time - last_time)
            mouse_controller.position = (x, y)
            mouse_controller.click(Button.left)
            print(f"Clique em ({x}, {y})")
            last_time = click_time

    print("Repetição finalizada!")

def atacar_mob():
    pyautogui.press('f1')
    print("[INFO] Ataque disparado (F1)")

def selecionar_mob():
    pyautogui.press('tab')
    print("[INFO] Procurando mob (TAB)")

def main():
    global stop_flag

    choice = input("Digite [R] para gravar ou [P] para reproduzir: ").strip().upper()

    if choice == "R":
        print("Gravando por até 3 minutos... Pressione ESC para parar antes.")
        mouse_listener = mouse.Listener(on_click=on_click)
        keyboard_listener = keyboard.Listener(on_press=on_press)

        mouse_listener.start()
        keyboard_listener.start()

        mouse_listener.join()
        keyboard_listener.stop()

        save_clicks()

    elif choice == "P":
        clicks = load_clicks()
        repeat_times = int(input("Quantas vezes deseja repetir? "))

        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.start()

        replay_clicks(clicks, repeat_times)

        keyboard_listener.stop()

    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
