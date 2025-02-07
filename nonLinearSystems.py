import tkinter as tk
import customtkinter as ctk

# --- Root-finding functions ---
def secantMethod(func, x0, x1):
    def f(x):
        return eval(func)
    toleranceReached = False
    for i in range(1, 10):
        if f(x0) - f(x1) == 0:
            x0 = x0 - 0.001
        xi = x0 - f(x0) / (f(x0) - f(x1)) * (x0 - x1)
        x0 = x1
        x1 = xi
        if abs((x1 - x0) / x1) <= 1e-9:
            toleranceReached = True
            break
    result = f"Approximate root: {x1:.10f}"
    if not toleranceReached:
        result += " but this value may not be very accurate"
    return result

def newtonsMethod(func, x0):
    def f(x):
        return eval(func)
    def df(x):
        return (f(x + 1e-6) - f(x)) / 1e-6
    toleranceReached = False
    for i in range(1, 10):
        if df(x0) == 0:
            x0 = x0 - 0.001
        oldx0 = x0
        x0 = x0 - (f(x0) / df(x0))
        if abs((x0 - oldx0) / x0) <= 1e-9:
            toleranceReached = True
            break
    result = f"Approximate root: {x0:.10f}"
    if not toleranceReached:
        result += " but this value may not be very accurate"
    return result

def bisectionMethod(func, x0, x1):
    def f(x):
        return eval(func)
    toleranceReached = False
    for i in range(1, 20):
        xi = (x0 + x1) / 2.0
        if f(x0) * f(xi) > 0:
            x0 = xi
            lastUsed = 0
            if x0 == 0:
                x0 = 0.001
        else:
            x1 = xi
            lastUsed = 1
            if x1 == 0:
                x1 = 0.001
        if abs((x0 - x1) / (x0 if lastUsed == 0 else x1)) <= 1e-6:
            toleranceReached = True
            break
    result = f"Approximate root: {x0:.10f}"
    if not toleranceReached:
        result += " but this value may not be very accurate"
    return result

# --- Root Finder Application ---
class RootFinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Root-Finding Methods")
        self.geometry("800x600")
        self.configure(fg_color="#131313")
        
        # Instruction and method selection
        instruction_label = ctk.CTkLabel(
            self, text="Select a method and enter the data", font=("Arial", 16), text_color="white"
        )
        instruction_label.pack(pady=20)
        
        # Container for radio buttons
        methods_frame = ctk.CTkFrame(self, fg_color="#131313")
        methods_frame.pack(pady=10)
        # Variable for the selected method: 0 - Bisection, 1 - Newton, 2 - Secant
        self.method_var = tk.IntVar(value=0)
        rb_bisection = ctk.CTkRadioButton(methods_frame, text="Bisection", variable=self.method_var, value=0, text_color="white")
        rb_newton = ctk.CTkRadioButton(methods_frame, text="Newton", variable=self.method_var, value=1, text_color="white")
        rb_secant = ctk.CTkRadioButton(methods_frame, text="Secant", variable=self.method_var, value=2, text_color="white")
        rb_bisection.grid(row=0, column=0, padx=10)
        rb_newton.grid(row=0, column=1, padx=10)
        rb_secant.grid(row=0, column=2, padx=10)
        
        # Entry for function expression
        func_label = ctk.CTkLabel(self, text="Enter the function expression (use 'x' as variable):", text_color="white", font=("Arial", 14))
        func_label.pack(pady=5)
        self.func_entry = ctk.CTkEntry(self, width=400)
        self.func_entry.pack(pady=5)
        
        # Entry for initial value x0
        self.x0_label = ctk.CTkLabel(self, text="Value x0:", text_color="white", font=("Arial", 14))
        self.x0_label.pack(pady=5)
        self.x0_entry = ctk.CTkEntry(self, width=200)
        self.x0_entry.pack(pady=5)
        
        # Entry for second value x1 (for Bisection and Secant)
        self.x1_label = ctk.CTkLabel(self, text="Value x1 (for Bisection and Secant):", text_color="white", font=("Arial", 14))
        self.x1_label.pack(pady=5)
        self.x1_entry = ctk.CTkEntry(self, width=200)
        self.x1_entry.pack(pady=5)
        
        # Calculate button
        calc_button = ctk.CTkButton(self, text="Calculate", command=self.calculate)
        calc_button.pack(pady=20)
        
        # Label for result
        self.result_label = ctk.CTkLabel(self, text="", text_color="white", font=("Arial", 14))
        self.result_label.pack(pady=10)
        
        # Update interface based on selected method
        self.method_var.trace("w", self.updateEntries)
        self.updateEntries()

    def updateEntries(self, *args):
        method = self.method_var.get()
        if method == 1:
            # Newton uses only x0
            self.x1_entry.configure(state="disabled")
            self.x1_label.configure(state="disabled")
        else:
            self.x1_entry.configure(state="normal")
            self.x1_label.configure(state="normal")
            
    def calculate(self):
        try:
            func = self.func_entry.get().strip()
            method = self.method_var.get()
            if method == 1:
                x0 = float(self.x0_entry.get())
                result = newtonsMethod(func, x0)
            else:
                x0 = float(self.x0_entry.get())
                x1 = float(self.x1_entry.get())
                if method == 0:
                    result = bisectionMethod(func, x0, x1)
                elif method == 2:
                    result = secantMethod(func, x0, x1)
            self.result_label.configure(text=result)
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")

def run():
    app = RootFinderApp()
    app.mainloop()

def main():
    run()

if __name__ == "__main__":
    main()
