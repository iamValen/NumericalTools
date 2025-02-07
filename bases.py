import customtkinter as ctk
import tkinter as tk

def charToInt(char):
    if '0' <= char <= '9':
        return int(char)
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A') + 10
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 36
    return None

def intToChar(i):
    if 0 <= i < 10:
        return chr(i + ord('0'))
    if 10 <= i < 36:
        return chr(i + ord('A') - 10)
    if 36 <= i < 62:
        return chr(i + ord('a') - 36)
    return '?'

def transformaEmDecimal(numero, base):
    """Converte um número (lista [parte_inteira, parte_fracionária]) da base 'base' para decimal."""
    output = 0
    # Processa a parte fracionária (se houver)
    if numero[1] != "":
        lastAlgPos = len(numero[1]) - 1
        i = 0
        while i <= lastAlgPos:
            val = charToInt(numero[1][lastAlgPos - i])
            if val is None:
                raise ValueError("Dígito inválido na parte fracionária")
            output += val * (base ** i)
            i += 1
        output /= (base ** len(numero[1]))
    # Processa a parte inteira
    lastAlgPos = len(numero[0]) - 1
    i = 0
    while i <= lastAlgPos:
        if numero[0][lastAlgPos - i] == '-':
            output *= -1
            return output
        val = charToInt(numero[0][lastAlgPos - i])
        if val is None:
            raise ValueError("Dígito inválido na parte inteira")
        output += val * (base ** i)
        i += 1
    return output

def transformaNoutraBase(numero, base):
    """Converte um número decimal para a base alvo.
       Retorna uma lista [parte_inteira, parte_fracionária]."""
    negativeFlag = False
    if numero < 0:
        negativeFlag = True
        numero = -numero
    intPart = int(numero)
    fracPart = numero - intPart
    outInt = []
    outFrac = []
    if intPart == 0:
        outInt.append('0')
    while intPart != 0:
        outInt.insert(0, intToChar(intPart % base))
        intPart = int(intPart / base)
    i = 0
    while fracPart != 0 and i < 8:
        temp = fracPart * base
        tempInt = int(temp)
        outFrac.append(intToChar(tempInt))
        fracPart = temp - tempInt
        i += 1
    if negativeFlag:
        outInt.insert(0, '-')
    return [''.join(outInt), ''.join(outFrac)]

def tranformaUmaBaseNoutra(numero, baseIn, baseOut):
    """Converte um número (lista [parte_inteira, parte_fracionária])
       da baseIn para a baseOut."""
    dec = transformaEmDecimal(numero, baseIn)
    return transformaNoutraBase(dec, baseOut)

def formatOutput(numero):
    """Formata a saída, garantindo que haja parte inteira e fracionária."""
    if numero[0] == "":
        numero[0] = "0"
    if numero[1] == "":
        numero[1] = "0"
    return numero[0] + "." + numero[1]

def getAllowedDigits(base):
    """Retorna uma string com todos os algarismos permitidos para a base informada."""
    digits = ""
    for i in range(base):
        digits += intToChar(i) + " "
    return digits.strip()

# --------------------------
# Aplicação GUI
# --------------------------

class BaseConversionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Conversão de Bases")
        self.geometry("800x600")
        self.configure(fg_color="#131313")

        # Base de entrada
        self.label_base_in = ctk.CTkLabel(self, text="Base de entrada:", text_color="white", font=("Arial", 14))
        self.label_base_in.pack(pady=(20, 5))
        self.entry_base_in = ctk.CTkEntry(self, placeholder_text="Ex: 10", width=200)
        self.entry_base_in.pack(pady=5)

        # Label para mostrar os algarismos permitidos
        self.label_allowed = ctk.CTkLabel(self, text="", text_color="white")
        self.label_allowed.pack(pady=5)

        # Número a converter
        self.label_number = ctk.CTkLabel(self, text="Número a converter:", text_color="white", font=("Arial", 14))
        self.label_number.pack(pady=5)
        self.entry_number = ctk.CTkEntry(self, placeholder_text="Ex: 123.45", width=200)
        self.entry_number.pack(pady=5)

        # Base de saída
        self.label_base_out = ctk.CTkLabel(self, text="Base de saída:", text_color="white", font=("Arial", 14))
        self.label_base_out.pack(pady=5)
        self.entry_base_out = ctk.CTkEntry(self, placeholder_text="Ex: 2", width=200)
        self.entry_base_out.pack(pady=5)

        # Botão Converter
        self.button_convert = ctk.CTkButton(self, text="Converter", command=self.convert)
        self.button_convert.pack(pady=20)

        # Label para o resultado
        self.label_result = ctk.CTkLabel(self, text="", text_color="white", font=("Arial", 16))
        self.label_result.pack(pady=20)

        # Atualiza os dígitos permitidos quando o foco sai da entrada de base de entrada
        self.entry_base_in.bind("<FocusOut>", self.updateAllowedDigits)

    def updateAllowedDigits(self, event=None):
        try:
            base_in = int(self.entry_base_in.get())
            if base_in < 2 or base_in > 62:
                self.label_allowed.configure(text="A base deve estar entre 2 e 62.")
            else:
                digits = getAllowedDigits(base_in)
                self.label_allowed.configure(text=f"Algarismos permitidos: {digits}")
        except:
            self.label_allowed.configure(text="")

    def convert(self):
        try:
            base_in = int(self.entry_base_in.get())
            base_out = int(self.entry_base_out.get())
            number_str = self.entry_number.get().strip()

            # Validação das bases
            if not (2 <= base_in <= 62):
                self.label_result.configure(text="Base de entrada inválida (deve estar entre 2 e 62).")
                return
            if not (2 <= base_out <= 62):
                self.label_result.configure(text="Base de saída inválida (deve estar entre 2 e 62).")
                return

            # Separa a parte inteira da fracionária
            if "." in number_str:
                parts = number_str.split(".")
                if len(parts) != 2:
                    self.label_result.configure(text="Número inválido.")
                    return
                numero = [parts[0], parts[1]]
            else:
                numero = [number_str, ""]

            # Valida os dígitos para a base de entrada
            for ch in numero[0]:
                if ch == '-' and numero[0].index(ch) == 0:
                    continue
                val = charToInt(ch)
                if val is None or val >= base_in:
                    self.label_result.configure(text="Número de entrada inválido para a base.")
                    return
            for ch in numero[1]:
                val = charToInt(ch)
                if val is None or val >= base_in:
                    self.label_result.configure(text="Número de entrada inválido para a base.")
                    return

            # Realiza a conversão
            result = tranformaUmaBaseNoutra(numero, base_in, base_out)
            formatted = formatOutput(result)
            self.label_result.configure(text=f"Número convertido: {formatted}")
        except Exception as e:
            self.label_result.configure(text=f"Erro: {str(e)}")


def run():
    app = BaseConversionApp()
    app.mainloop()

def main():
    run()

if __name__ == "__main__":
    main()
