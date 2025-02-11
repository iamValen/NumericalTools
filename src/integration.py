"""
This program is an application that allows users to compute numerical integrals 
using the Newton-Cotes formulas (both closed and open variants)
"""

import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt

def run():
    extra = {
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
        "log": np.log, "ln": np.log,
        "pi": np.pi, "e": np.e, "sqrt": np.sqrt
    }

    def closedNewtonCotes(x, y, n):
        h = (x[n] - x[0]) / n
        if n == 1:  # Trapezoidal rule
            return h / 2 * (y[0] + y[1])
        elif n == 2:  # Simpson's rule
            return h / 3 * (y[0] + 4 * y[1] + y[2])
        elif n == 3:  # Simpson 3/8 rule
            return (3 * h / 8) * (y[0] + 3 * y[1] + 3 * y[2] + y[3])
        elif n == 4:  # Boole's rule
            return (2 * h / 45) * (7 * y[0] + 32 * y[1] + 12 * y[2] + 32 * y[3] + 7 * y[4])
        else:
            raise ValueError("Invalid n for closed formulas.")

    def openNewtonCotes(x, y, n):
        h = (x[-1] - x[0]) / (n + 2)
        # Remove first and last points
        x = x[1:-1]
        y = y[1:-1]
        if n == 0:  # Midpoint rule (open)
            return 2 * h * y[0]
        elif n == 1:
            return (3 * h / 2) * (y[0] + y[1])
        elif n == 2:
            return (4 * h / 3) * (2 * y[0] - y[1] + 2 * y[2])
        elif n == 3:
            return (5 * h / 24) * (11 * y[0] + y[1] + y[2] + 11 * y[3])
        else:
            raise ValueError("Invalid n for open formulas.")

    # --- Plot the function and integration interval ---
    def plotGraph(x, y, func=None):
        plt.figure(figsize=(8, 6))
        if func:
            x_dense = np.linspace(x[0], x[-1], 500)
            y_dense = np.array([func(xi) for xi in x_dense])
            plt.plot(x_dense, y_dense, label="f(x)", color='blue', alpha=0.6)
        plt.scatter(x, y, color='red', label='Points (x, f(x))', zorder=5)
        plt.plot(x, y, color='green', label='Interpolation', linestyle='--')
        plt.fill_between(x, y, alpha=0.3, color="blue", label="Integration interval")
        plt.xlabel('x')
        plt.ylabel('f(x)')
        if m == "closed":
            plt.title(f"Closed Newton-Cotes (n={n})\nApproximate Integral: {res:.5f}")
        else:
            plt.title(f"Open Newton-Cotes (n={n})\nApproximate Integral: {res:.5f}")
        plt.legend()
        plt.grid(True, alpha=0.4)
        plt.show()

    # --- Solve the integral based on selected method ---
    def solve(method):
        result_text.set("")
        result_text_open.set("")
        try:
            global n, res, m
            m = method
            if method == "closed":
                n = int(input_n.get())
                if n < 1 or n > 4:
                    result_text.set("Invalid value of n.")
                    return
                input_type = input_var.get()
                if input_type == "func":
                    func = input_f.get()
                    def f(x):
                        return eval(func, {**extra, "x": x})
                    a = eval(input_a.get(), extra)
                    b = eval(input_b.get(), extra)
                    points = n + 1
                    x = np.linspace(a, b, points)
                    y = np.array([f(xi) for xi in x])
                    res = closedNewtonCotes(x, y, n)
                    result_text.set(f"Approximate integral: {res}")
                    plotGraph(x, y, func=f)
                else:
                    x = []
                    y = []
                    for entry in input_x:
                        x.append(eval(entry.get(), extra))
                    for entry in input_y:
                        y.append(eval(entry.get(), extra))
                    res = closedNewtonCotes(x, y, n)
                    result_text.set(f"Approximate integral: {res}\nIf points are not equally spaced, the result may be incorrect.")
                    plotGraph(x, y)
            else:
                n = int(input_n_open.get())
                if n < 0 or n > 3:
                    result_text_open.set("Invalid value of n.")
                    return
                input_type = input_var_open.get()
                if input_type == "func":
                    func = input_f_open.get()
                    def f(x):
                        return eval(func, {**extra, "x": x})
                    a = eval(input_a_open.get(), extra)
                    b = eval(input_b_open.get(), extra)
                    points = n + 3
                    x = np.linspace(a, b, points)
                    y = np.array([f(xi) for xi in x])
                    res = openNewtonCotes(x, y, n)
                    result_text_open.set(f"Approximate integral: {res}")
                    plotGraph(x, y, func=f)
                else:
                    x = []
                    y = []
                    for entry in input_x_open:
                        x.append(eval(entry.get(), extra))
                    for entry in input_y_open:
                        y.append(eval(entry.get(), extra))
                    res = openNewtonCotes(x, y, n)
                    result_text_open.set(f"Approximate integral: {res}\nIf points are not equally spaced, the result may be incorrect.")
                    plotGraph(x, y)
        except ValueError as e:
            result_text.set(str(e))
        except Exception as e:
            result_text.set(str(e))

    # --- Navigation functions ---
    def showFrame(frame):
        frame.tkraise()

    def backToMain():
        showFrame(frames['main'])

    # --- Main navigation page ---
    def mainFrame(app, frames):
        frame = ctk.CTkFrame(app, fg_color='#131313')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=1)
        button1 = ctk.CTkButton(frame, text="Closed Newton-Cotes Formulas", command=lambda: showFrame(frames['closed']), width=400, height=75)
        button1.grid(row=1, column=0, pady=30)
        button2 = ctk.CTkButton(frame, text="Open Newton-Cotes Formulas", command=lambda: showFrame(frames['open']), width=400, height=75)
        button2.grid(row=2, column=0, pady=30)
        return frame

    # --- Page for Closed Newton-Cotes Formulas ---
    def closedNewtonCotesFrame(app, frames):
        frame = ctk.CTkFrame(app, fg_color='#131313')
        frame.grid_columnconfigure(0, weight=1)
        top_frame = ctk.CTkFrame(frame, fg_color='#131313')
        top_frame.grid(row=0, column=0, pady=100)
        top_frame.grid_columnconfigure(1, weight=1)
        input_frame = ctk.CTkFrame(frame, fg_color="#131313")
        input_frame.grid(row=1, column=0)
        bottom_frame = ctk.CTkFrame(frame, fg_color='#131313')
        bottom_frame.grid(row=2, column=0)
        ctk.CTkLabel(top_frame, text="Choose the degree of the Closed Formula (n)", text_color="#FFFFFF").grid(row=1, column=0, pady=5)
        global input_n
        input_n = ctk.CTkEntry(top_frame, width=50, fg_color="#2E2E2E", text_color="white", placeholder_text="")
        input_n.grid(row=1, column=1, pady=5)
        global result_text
        result_text = tk.StringVar()
        def updateInput(*args):
            for widget in input_frame.winfo_children():
                widget.destroy()
            result_text.set("")
            if input_var.get() == "func":
                ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
                global input_f
                input_f = ctk.CTkEntry(input_frame, width=200, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                input_f.grid(row=0, column=1, pady=5, padx=0)
                ctk.CTkLabel(input_frame, text="Lower integration limit", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
                global input_a
                input_a = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                input_a.grid(row=1, column=1, pady=5, padx=0)
                ctk.CTkLabel(input_frame, text="Upper integration limit", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
                global input_b
                input_b = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                input_b.grid(row=2, column=1, pady=5, padx=0)
            elif input_var.get() == "table":
                n = int(input_n.get())
                if n > 0 and n < 5:
                    num_points = n + 1
                    ctk.CTkLabel(input_frame, text="x", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=5)
                    global input_x
                    global input_y
                    input_x = []
                    input_y = []
                    for i in range(num_points):
                        entry_x = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                        entry_x.grid(row=1, column=i+1, pady=5, padx=5)
                        input_x.append(entry_x)
                        entry_y = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                        entry_y.grid(row=2, column=i+1, pady=5, padx=5)
                        input_y.append(entry_y)
                        if i > 1 and i < num_points:
                            ctk.CTkLabel(input_frame, text=f"x{i-1}", text_color="#FFFFFF").grid(row=0, column=i, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="a/x0", text_color="#FFFFFF").grid(row=0, column=1, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text=f"b/x{num_points-1}", text_color="#FFFFFF").grid(row=0, column=num_points, pady=5, padx=5)
        ctk.CTkLabel(top_frame, text="Select input type:", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
        global input_var
        input_var = tk.StringVar(value="func")
        input_var.trace("w", updateInput)
        ctk.CTkRadioButton(top_frame, text="Function", variable=input_var, value="func", text_color="#FFFFFF").grid(row=3, column=0, padx=10, pady=20)
        ctk.CTkRadioButton(top_frame, text="Table", variable=input_var, value="table", text_color="#FFFFFF").grid(row=3, column=1, padx=10, pady=20)
        updateInput()
        ctk.CTkButton(bottom_frame, text="Solve", command=lambda: solve("closed"), text_color="#FFFFFF").grid(row=1, column=0, padx=20, pady=30)
        ctk.CTkLabel(bottom_frame, textvariable=result_text, text_color="#FFFFFF").grid(row=0, column=0, pady=50, padx=10)
        back = ctk.CTkButton(bottom_frame, text="Back", command=backToMain)
        back.grid(row=2, column=0, padx=10, pady=50)
        return frame

    # --- Page for Open Newton-Cotes Formulas ---
    def openNewtonCotesFrame(app, frames):
        frame = ctk.CTkFrame(app, fg_color='#131313')
        frame.grid_columnconfigure(0, weight=1)
        top_frame = ctk.CTkFrame(frame, fg_color='#131313')
        top_frame.grid(row=0, column=0, pady=100)
        top_frame.grid_columnconfigure(1, weight=1)
        input_frame = ctk.CTkFrame(frame, fg_color="#131313")
        input_frame.grid(row=1, column=0)
        bottom_frame = ctk.CTkFrame(frame, fg_color='#131313')
        bottom_frame.grid(row=2, column=0)
        ctk.CTkLabel(top_frame, text="Select degree of Open Formula (n)", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=0)
        global input_n_open
        input_n_open = ctk.CTkEntry(top_frame, width=50, fg_color="#2E2E2E", text_color="white", placeholder_text="")
        input_n_open.grid(row=1, column=1, pady=5, padx=0)
        global result_text_open
        result_text_open = tk.StringVar()
        def updateInput(*args):
            for widget in input_frame.winfo_children():
                widget.destroy()
            result_text_open.set("")
            if input_var_open.get() == "func":
                ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
                global input_f_open
                input_f_open = ctk.CTkEntry(input_frame, width=200, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                input_f_open.grid(row=0, column=1, pady=5, padx=0)
                ctk.CTkLabel(input_frame, text="Lower integration limit", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
                global input_a_open
                input_a_open = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                input_a_open.grid(row=1, column=1, pady=5, padx=0)
                ctk.CTkLabel(input_frame, text="Upper integration limit", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
                global input_b_open
                input_b_open = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                input_b_open.grid(row=2, column=1, pady=5, padx=0)
            elif input_var_open.get() == "table":
                n = int(input_n_open.get())
                if n > -1 and n < 4:
                    num_points = n + 3
                    ctk.CTkLabel(input_frame, text="x", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=5)
                    global input_x_open
                    global input_y_open
                    input_x_open = []
                    input_y_open = []
                    for i in range(num_points):
                        entry_x = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                        entry_x.grid(row=1, column=i+1, pady=5, padx=5)
                        input_x_open.append(entry_x)
                        entry_y = ctk.CTkEntry(input_frame, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                        entry_y.grid(row=2, column=i+1, pady=5, padx=5)
                        input_y_open.append(entry_y)
                        if i > 1 and i < num_points:
                            ctk.CTkLabel(input_frame, text=f"x{i-2}", text_color="#FFFFFF").grid(row=0, column=i, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="a", text_color="#FFFFFF").grid(row=0, column=1, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="b", text_color="#FFFFFF").grid(row=0, column=num_points, pady=5, padx=5)
        ctk.CTkLabel(top_frame, text="Select input type:", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
        global input_var_open
        input_var_open = tk.StringVar(value="func")
        input_var_open.trace("w", updateInput)
        ctk.CTkRadioButton(top_frame, text="Function", variable=input_var_open, value="func", text_color="#FFFFFF").grid(row=3, column=0, padx=10, pady=20)
        ctk.CTkRadioButton(top_frame, text="Table", variable=input_var_open, value="table", text_color="#FFFFFF").grid(row=3, column=1, padx=10, pady=20)
        updateInput()
        ctk.CTkButton(bottom_frame, text="Solve", command=lambda: solve("open"), text_color="#FFFFFF").grid(row=1, column=0, padx=20, pady=30)
        ctk.CTkLabel(bottom_frame, textvariable=result_text_open, text_color="#FFFFFF").grid(row=0, column=0, pady=50, padx=10)
        back = ctk.CTkButton(bottom_frame, text="Back", command=backToMain)
        back.grid(row=2, column=0, padx=10, pady=50)
        return frame

    # --- Initial App Configuration ---
    app = ctk.CTk()
    app.title("Numerical Integration")
    app.geometry("1200x800")
    app.grid_columnconfigure(0, weight=1)
    app.configure(fg_color="#131313")

    # Store frames for navigation
    frames = {}
    frames['main'] = mainFrame(app, frames)
    frames['open'] = openNewtonCotesFrame(app, frames)
    frames['closed'] = closedNewtonCotesFrame(app, frames)

    # Position all frames to fill the window
    for frame in frames.values():
        frame.place(relwidth=1, relheight=1)

    showFrame(frames['main'])
    app.mainloop()

if __name__ == "__main__":
    run()
