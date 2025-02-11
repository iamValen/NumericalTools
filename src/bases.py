"""
This program implements base conversion.
It allows users to convert numbers between different bases (from base 2 to base 62).
"""

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

def convertToDecimal(number, base):
    """Convert a number (list [integer_part, fractional_part]) from the given base to decimal."""
    output = 0
    if number[1] != "":
        lastIndex = len(number[1]) - 1
        i = 0
        while i <= lastIndex:
            val = charToInt(number[1][lastIndex - i])
            if val is None:
                raise ValueError("Invalid digit in fractional part")
            output += val * (base ** i)
            i += 1
        output /= (base ** len(number[1]))
    lastIndex = len(number[0]) - 1
    i = 0
    while i <= lastIndex:
        if number[0][lastIndex - i] == '-':
            output *= -1
            return output
        val = charToInt(number[0][lastIndex - i])
        if val is None:
            raise ValueError("Invalid digit in integer part")
        output += val * (base ** i)
        i += 1
    return output

def convertFromDecimal(number, base):
    """Convert a decimal number to the target base.
       Returns a list [integer_part, fractional_part]."""
    negative = False
    if number < 0:
        negative = True
        number = -number
    intPart = int(number)
    fracPart = number - intPart
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
    if negative:
        outInt.insert(0, '-')
    return [''.join(outInt), ''.join(outFrac)]

def convertBase(number, baseIn, baseOut):
    """Convert a number (list [integer_part, fractional_part]) from baseIn to baseOut."""
    dec = convertToDecimal(number, baseIn)
    return convertFromDecimal(dec, baseOut)

def formatOutput(number):
    """Format the output ensuring both integer and fractional parts are present."""
    if number[0] == "":
        number[0] = "0"
    if number[1] == "":
        number[1] = "0"
    return number[0] + "." + number[1]

def getAllowedDigits(base):
    """Return a string with all allowed digits for the given base."""
    digits = ""
    for i in range(base):
        digits += intToChar(i) + " "
    return digits.strip()

class BaseConversionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Base Conversion")
        self.geometry("800x600")
        self.configure(fg_color="#131313")

        # Input base label and entry
        self.label_input_base = ctk.CTkLabel(self, text="Input Base:", text_color="white", font=("Arial", 14))
        self.label_input_base.pack(pady=(20, 5))
        self.entry_input_base = ctk.CTkEntry(self, placeholder_text="e.g. 10", width=200)
        self.entry_input_base.pack(pady=5)

        # Allowed digits label
        self.label_allowed = ctk.CTkLabel(self, text="", text_color="white")
        self.label_allowed.pack(pady=5)

        # Number to convert label and entry
        self.label_number = ctk.CTkLabel(self, text="Number to Convert:", text_color="white", font=("Arial", 14))
        self.label_number.pack(pady=5)
        self.entry_number = ctk.CTkEntry(self, placeholder_text="e.g. 123.45", width=200)
        self.entry_number.pack(pady=5)

        # Output base label and entry
        self.label_output_base = ctk.CTkLabel(self, text="Output Base:", text_color="white", font=("Arial", 14))
        self.label_output_base.pack(pady=5)
        self.entry_output_base = ctk.CTkEntry(self, placeholder_text="e.g. 2", width=200)
        self.entry_output_base.pack(pady=5)

        # Convert button
        self.button_convert = ctk.CTkButton(self, text="Convert", command=self.convert)
        self.button_convert.pack(pady=20)

        # Result label
        self.label_result = ctk.CTkLabel(self, text="", text_color="white", font=("Arial", 16))
        self.label_result.pack(pady=20)

        self.entry_input_base.bind("<FocusOut>", self.updateAllowedDigits)

    def updateAllowedDigits(self, event=None):
        try:
            base_in = int(self.entry_input_base.get())
            if base_in < 2 or base_in > 62:
                self.label_allowed.configure(text="Base must be between 2 and 62.")
            else:
                digits = getAllowedDigits(base_in)
                self.label_allowed.configure(text=f"Allowed digits: {digits}")
        except:
            self.label_allowed.configure(text="")

    def convert(self):
        try:
            base_in = int(self.entry_input_base.get())
            base_out = int(self.entry_output_base.get())
            num_str = self.entry_number.get().strip()
            if not (2 <= base_in <= 62):
                self.label_result.configure(text="Invalid input base (must be between 2 and 62).")
                return
            if not (2 <= base_out <= 62):
                self.label_result.configure(text="Invalid output base (must be between 2 and 62).")
                return
            if "." in num_str:
                parts = num_str.split(".")
                if len(parts) != 2:
                    self.label_result.configure(text="Invalid number.")
                    return
                number = [parts[0], parts[1]]
            else:
                number = [num_str, ""]
            for ch in number[0]:
                if ch == '-' and number[0].index(ch) == 0:
                    continue
                val = charToInt(ch)
                if val is None or val >= base_in:
                    self.label_result.configure(text="Invalid digit in the input number.")
                    return
            for ch in number[1]:
                val = charToInt(ch)
                if val is None or val >= base_in:
                    self.label_result.configure(text="Invalid digit in the input number.")
                    return
            result = convertBase(number, base_in, base_out)
            formatted = formatOutput(result)
            self.label_result.configure(text=f"Converted number: {formatted}")
        except Exception as e:
            self.label_result.configure(text=f"Error: {str(e)}")

def run():
    app = BaseConversionApp()
    app.mainloop()

def main():
    run()

if __name__ == "__main__":
    main()
