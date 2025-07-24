import pyautogui
import pytesseract
import re
from PIL import Image

# Caminho do Tesseract OCR (ajusta se for diferente)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def responder_antibot():
    # 📸 Screenshot da pergunta
    pergunta = pyautogui.screenshot(region=(28, 782, 382, 189))  # Ajusta X, Y, Largura, Altura
    pergunta.save(r"d:\testefelipe\debug_antibot.png")

    # 🔍 OCR
    texto = pytesseract.image_to_string(pergunta, lang='eng').strip()
    print(f"[OCR] Pergunta detectada: '{texto}'")

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
        return None

if __name__ == "__main__":
    print("[INFO] Iniciando verificação AntiBot...")
    responder_antibot()
