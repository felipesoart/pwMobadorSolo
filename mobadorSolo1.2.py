import pyautogui
import time
from pynput import keyboard
import pytesseract
from PIL import Image
from PIL import ImageOps, ImageFilter
import re

# Caminho do Tesseract no Windows (AJUSTE!)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flag global para parar com ESC
stop_flag = False

def selecionar_mob():
    pyautogui.press('tab')
    print("[INFO] Procurando mob (TAB)")

def coleta_itens():
    pyautogui.press('4')
    print("[INFO] Coletando itens (4)")

def buff():
    pyautogui.press('8')
    print("[INFO] Buffar (8)")


def verificar_mob3(nomes_esperados):
    # Flag de retorno
    ret = False

    # Screenshot
    screenshot = pyautogui.screenshot(region=(903, 62, 190, 20))
    screenshot.save(r"d:\testefelipe\debug_original.png")

    gray = screenshot.convert('L')
    gray.save(r"d:\testefelipe\debug_gray.png")

    # Lista de thresholds (label, valor)
    thresholds = [
        ("Branco", 175),
        ("Meio termo", 125),
        ("Verde escuro", 72)
    ]

    nomes = [n.strip().lower() for n in nomes_esperados.split(';')]

    for label, limiar in thresholds:
        threshold = gray.point(lambda x: 255 if x > limiar else 0)
        path = fr"d:\testefelipe\debug_{label.replace(' ', '_').lower()}.png"
        threshold.save(path)

        print(f"[DEBUG] {label} - Salvo {path}")

        texto = pytesseract.image_to_string(threshold, lang='eng')
        print(f"[OCR] Texto detectado: '{texto.strip()}'")

        texto_detectado = texto.lower()

        for nome in nomes:
            if nome in texto_detectado:
                print(f"[INFO] MOB '{nome}' ENCONTRADO!")
                return True

    print("[INFO] MOB NÃO ENCONTRADO!")
    return False


def verificar_mob2(nomes_esperados):

    ret = False
    # 1️⃣ Screenshot
    screenshot = pyautogui.screenshot(region=(903, 62, 190, 20))
    screenshot.save(r"d:\testefelipe\debug_original.png")

    # 2️⃣ Cinza + filtro
    gray = screenshot.convert('L')
    gray.save(r"d:\testefelipe\debug_gray.png")

    if ret == False:#branco
        # 3️⃣ Threshold invertido: força texto claro pra branco
        #    Tudo acima de 50~100 vira branco (texto), resto fica preto (fundo)
        threshold = gray.point(lambda x: 255 if x > 175 else 0)#branco
        #threshold = gray.point(lambda x: 255 if x > 75 else 0)#verde escuro
        threshold.save(r"d:\testefelipe\debug_threshold_invertedlogic.png")

        print("[DEBUG] Branco - Salvo debug_threshold_invertedlogic.png")

        # 4️⃣ OCR
        texto = pytesseract.image_to_string(threshold, lang='eng')#qnd o mobs tiver com o nome de outra cor
        #texto = pytesseract.image_to_string(gray, lang='eng')#qnd o mobs tiver com o nome branco
        print(f"[OCR] Texto detectado: '{texto.strip()}'")

    # 🔑 Verificar todos os nomes separados por ';'
        nomes = [n.strip().lower() for n in nomes_esperados.split(';')]
        texto_detectado = texto.lower()

        for nome in nomes:
            if nome in texto_detectado:
                print(f"[INFO] MOB '{nome}' ENCONTRADO!")
                ret = True
                return ret

    if ret == False:#meio termo
         # 3️⃣ Threshold invertido: força texto claro pra branco
        #    Tudo acima de 50~100 vira branco (texto), resto fica preto (fundo)
        threshold = gray.point(lambda x: 255 if x > 125 else 0)
        threshold.save(r"d:\testefelipe\debug_threshold_invertedlogic.png")

        print("[DEBUG] Meio termo - Salvo debug_threshold_invertedlogic.png")

        # 4️⃣ OCR
        texto = pytesseract.image_to_string(threshold, lang='eng')#qnd o mobs tiver com o nome de outra cor
        #texto = pytesseract.image_to_string(gray, lang='eng')#qnd o mobs tiver com o nome branco
        print(f"[OCR] Texto detectado: '{texto.strip()}'")

        # 🔑 Verificar todos os nomes separados por ';'
        nomes = [n.strip().lower() for n in nomes_esperados.split(';')]
        texto_detectado = texto.lower()

        for nome in nomes:
            if nome in texto_detectado:
                print(f"[INFO] MOB '{nome}' ENCONTRADO!")
                ret = True
                return ret

    if ret == False:#verde escuro
         # 3️⃣ Threshold invertido: força texto claro pra branco
        #    Tudo acima de 50~100 vira branco (texto), resto fica preto (fundo)
        threshold = gray.point(lambda x: 255 if x > 72 else 0)
        threshold.save(r"d:\testefelipe\debug_threshold_invertedlogic.png")

        print("[DEBUG] Verde escuro - Salvo debug_threshold_invertedlogic.png")

        # 4️⃣ OCR
        texto = pytesseract.image_to_string(threshold, lang='eng')#qnd o mobs tiver com o nome de outra cor
        #texto = pytesseract.image_to_string(gray, lang='eng')#qnd o mobs tiver com o nome branco
        print(f"[OCR] Texto detectado: '{texto.strip()}'")

        # 🔑 Verificar todos os nomes separados por ';'
        nomes = [n.strip().lower() for n in nomes_esperados.split(';')]
        texto_detectado = texto.lower()

        for nome in nomes:
            if nome in texto_detectado:
                print(f"[INFO] MOB '{nome}' ENCONTRADO!")
                ret = True
                return ret


    print("[INFO] MOB NÃO ENCONTRADO!")
    return ret


def responder_antibot():
    # 📸 Screenshot da pergunta
    pergunta = pyautogui.screenshot(region=(28, 782, 382, 189))  # Ajusta X, Y, Largura, Altura
    pergunta.save(r"d:\testefelipe\debug_antibot.png")

    # 🔍 OCR
    texto = pytesseract.image_to_string(pergunta, lang='eng').strip()
    print(f"[OCR] Pergunta detectada: '{texto}'")

    nome_esperado = "AntiBot"

    if nome_esperado.lower() in texto.lower():
        print("[INFO] AntiBot detecter!")            
    
        # 🗂️ Localiza o '?'
        pos_interrogacao = texto.find('?')

        if pos_interrogacao != -1:
            inicio = max(0, pos_interrogacao - 9)  # Pegando mais pra garantir
            conta = texto[inicio:pos_interrogacao]

            # 🧹 Remove espaços
            conta_sem_espaco = conta.replace(' ', '')
            print(f"[INFO] Trecho da conta (sem espaços): '{conta_sem_espaco}'")       

            # 🧮 Filtra números e +
            expressao = re.findall(r'\d+|\+', conta_sem_espaco)
            print(f"[DEBUG] Expressão filtrada: {expressao}")

            # 🧮 Calcula
            resultado = 0
            for item in expressao:
                if item != '+':
                    resultado += int(item)
            print(f"[INFO] Resposta do AntiBot: {resultado}")

            # Simula digitar (descomenta se quiser)
            # pyautogui.typewrite(str(resultado))
            # pyautogui.press('enter')

            return resultado
        else:
            print("[WARN] Não encontrou '?' no texto.")
            return -1
    else:
        print("[INFO] AntiBot Não detecter!")
        return -1

def atacar_mob():
    print("[INFO] Atacando mob...")

    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")
    
    time.sleep(5)
    
    pyautogui.press('1')
    print("[INFO] Ataque disparado (1)")
    
    time.sleep(5)

    pyautogui.press('3')
    print("[INFO] Usar porção de hp (3)")

    time.sleep(2)
    coleta_itens()
    time.sleep(2)
    coleta_itens()
    time.sleep(2)
    coleta_itens()
    time.sleep(2)
    coleta_itens()


def replay_clicks(repeat_count, nome_mob):

    time.sleep(10)
    buff()
    time.sleep(5)
    global stop_flag
    nbuff = 0
    for i in range(repeat_count):
        #if stop_flag:
            #print("[INFO] Encerrado pela tecla ESC.")
            #break
        nbuff+1
        print(f"Rodada {i+1} - Procurando mob...")

        while True:
            #if stop_flag:
                #print("[INFO] Encerrado pela tecla ESC durante tentativa.")
                #return
            
            antBot = responder_antibot()
            print(f"[antBot] '{antBot}'")

            if antBot != -1:
                pyautogui.press('enter')  # abre o chat ou ativa campo de resposta

                # Transforma em string e percorre cada dígito
                for digito in str(antBot):
                    pyautogui.press(digito)
                    print(f"[INFO] Digitou: {digito}")

                pyautogui.press('enter')  # envia resposta
                time.sleep(15)
                


            verificaMobs= True

            if nbuff==50:
                nbuff=0
                print("[INFO] BUFFAR")
                buff()
                time.sleep(15)

            if verificaMobs:
                
                verificaMobs_metodo = verificar_mob3(nome_mob)

                if verificaMobs_metodo:
                    print("[INFO] Mob com hp continuar a atacar!")
                else:
                    selecionar_mob()

                if verificaMobs_metodo:
                    atacar_mob()
                    print("[INFO] Mob atacado com sucesso!")
                    break  # Sai do while e vai pra próxima rodada
                else:
                    print("[INFO] Mob errado, tentando de novo em 3s...")
                    time.sleep(3)  # Espera antes de tentar de novo

            else:
                selecionar_mob()

                atacar_mob()
                print("[INFO] Mob atacado com sucesso!")
                break  # Sai do while e vai pra próxima rodada


def on_press(key):
    global stop_flag
    #if key == keyboard.Key.esc:
       # stop_flag = True
       # print("[INFO] Tecla ESC detectada! Encerrando...")

if __name__ == "__main__":
    repeat_times = int(input("Quantas vezes deseja repetir? "))
    nome_mob = input("Digite o nome do mob que quer atacar: ")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    replay_clicks(repeat_times, nome_mob)

    listener.stop()

#instalar
#https://github.com/UB-Mannheim/tesseract/wiki
