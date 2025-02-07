import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt

def run():
    extra = {"sin": np.sin, "sen": np.sin, "cos": np.cos, "tan": np.tan,
            "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
            "log": np.log, "ln": np.log,
            "pi": np.pi, "e": np.e, "sqrt": np.sqrt}

    # Define Newton-Cotes methods
    def closedNewtonCotes(x, y, n):
        h = (x[n] - x[0]) / n
        if n == 1:  # Regra do Trapézio
            return h / 2 * (y[0] + y[1])
        elif n == 2:  # Regra de Simpson
            return h / 3 * (y[0] + 4 * y[1] + y[2])
        elif n == 3:  # Regra de Simpson 3/8
            return (3 * h / 8) * (y[0] + 3 * y[1] + 3 * y[2] + y[3])
        elif n == 4:  # Regra de Boole
            return (2 * h / 45) * (7 * y[0] + 32 * y[1] + 12 * y[2] + 32 * y[3] + 7 * y[4])
        else:
            raise ValueError("n inválido para fórmulas fechadas.")

    def openNewtonCotes(x, y, n):
        h = (x[-1] - x[0]) / (n+2)
        x = x[1:-1]  # elimina o primeiro e último elemento
        y = y[1:-1]  # porque x0 = a+h e xn = b-h

        if n == 0:  # Regra do ponto médio
            return 2 * h * y[0]
        elif n == 1:  # Fórmula aberta para n=1
            return (3 * h / 2) * (y[0] + y[1])
        elif n == 2:  # Regra do Milne
            return (4 * h / 3) * (2 * y[0] - y[1] + 2 * y[2])
        elif n == 3:  # Fórmula aberta para n=3
            return (5 * h / 24) * (11 * y[0] + y[1] + y[2] + 11 * y[3])

    def plot_graph(x, y, func=None):
        plt.figure(figsize=(8, 6))
        if func:
            x_dense = np.linspace(x[0], x[-1], 500)
            y_dense = np.array([func(xi) for xi in x_dense])
            plt.plot(x_dense, y_dense, label="f(x)", color='blue', alpha=0.6)

        plt.scatter(x, y, color='red', label='Pontos (x, f(x))', zorder=5)
        plt.plot(x, y, color='green', label='Interpolação entre pontos', linestyle='--')
        plt.fill_between(x, y, alpha=0.3, color="blue", label="Intervalo do Integral")

        plt.xlabel('x')
        plt.ylabel('f(x)')
        if(m == "closed"):
            plt.title(f"Método de Newton-Cotes Fechado (n={n})\nValor do Integral Aproximado: {res:.5f}")
        else:
            plt.title(f"Método de Newton-Cotes Aberto (n={n})\nValor do Integral Aproximado: {res:.5f}")
        plt.legend()
        plt.grid(True, alpha=0.4)
        plt.show()


    def solve(method):
        result_text.set("")
        result_text_open.set("")
        try:
            global n, res, m
            m = method
            if method == "closed":
                n = int(input_n.get())
                if n < 1 or n > 4:
                    result_text.set("Valor 'n' inválido.")
                    return

                input_type = input_var.get()
                if input_type == "func":
                    func = input_f.get()

                    def f(x):
                        return eval(func, extra | {"x": x})

                    a = eval(input_a.get(), extra)
                    b = eval(input_b.get(), extra)

                    pontos = n + 1
                    x = np.linspace(a, b, pontos)
                    y = np.array([f(xi) for xi in x])

                    res = closedNewtonCotes(x, y, n)
                    
                    result_text.set(f"O valor aproximado da integral é: {res}")
                    plot_graph(x, y, func=f)

                else:  # input = tabela
                    x = []
                    y = []

                    for entry in input_x:
                        x.append(eval(entry.get(), extra))
                    for entry in input_y:
                        y.append(eval(entry.get(), extra))

                    res = closedNewtonCotes(x, y, n)
                    result_text.set(f"O valor aproximado da integral é: {res}\nMas se os pontos não estiverem igualmente espaçados, o valor pode estar incorreto")
                    plot_graph(x, y)

            else:  # open methods
                n = int(input_n_open.get())
                if n < 0 or n > 3:
                    result_text_open.set("Valor 'n' inválido.")
                    return

                input_type = input_var_open.get()
                if input_type == "func":
                    func = input_f_open.get()

                    def f(x):
                        return eval(func, extra | {"x": x})

                    a = eval(input_a_open.get(), extra)
                    b = eval(input_b_open.get(), extra)

                    pontos = n + 3
                    x = np.linspace(a, b, pontos)
                    y = np.array([f(xi) for xi in x])

                    res = openNewtonCotes(x, y, n)
                    result_text_open.set(f"O valor aproximado da integral é: {res}")
                    plot_graph(x, y, func=f)

                else:  # input = tabela
                    x = []
                    y = []

                    for entry in input_x_open:
                        x.append(eval(entry.get(), extra))
                    for entry in input_y_open:
                        y.append(eval(entry.get(), extra))

                    res = openNewtonCotes(x, y, n)
                    result_text_open.set(f"O valor aproximado da integral é: {res}\nMas se os pontos não estiverem igualmente espaçados, o valor pode estar incorreto")
                    plot_graph(x, y)

        except ValueError as e:
            result_text.set(str(e))
        except Exception as e:
            result_text.set(str(e))


    # Função para mostrar as diferentes páginas
    def show_frame(frame):
        frame.tkraise()

    def back_to_main():
        show_frame(frames['main'])

    def mainFrame(app, frames):
        frame = ctk.CTkFrame(app, fg_color='#131313')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=1)

        button1 = ctk.CTkButton(frame, text="Formulas Newton-Cotes Fechadas", command=lambda: show_frame(frames['closed']), width=400, height=75)
        button1.grid(row=1, column=0, pady=30)

        button2 = ctk.CTkButton(frame, text="Formulas Newton-Cotes Abertas", command=lambda: show_frame(frames['open']), width=400, height=75)
        button2.grid(row=2, column=0, pady=30)

        return frame

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

        # n
        ctk.CTkLabel(top_frame, text="Escolha o grau da fórmula Fechada (n)", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=0)
        global input_n
        input_n = tk.Entry(top_frame, width=5, bg="#2E2E2E", fg="white", insertbackground="white")
        input_n.grid(row=1, column=1, pady=5, padx=0)

        global result_text
        result_text = tk.StringVar()
        # input of the function/points
        def updateInput(*args):
            for widget in input_frame.winfo_children():
                widget.destroy()

            result_text.set("")
            
            if input_var.get() == "func":
                ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
                global input_f
                input_f = tk.Entry(input_frame, width=20, bg="#2E2E2E", fg="white", insertbackground="white")
                input_f.grid(row=0, column=1, pady=5, padx=0)

                ctk.CTkLabel(input_frame, text="Limite inferior de integração", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
                global input_a
                input_a = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                input_a.grid(row=1, column=1, pady=5, padx=0)

                ctk.CTkLabel(input_frame, text="Limite superior de integração", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
                global input_b
                input_b = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                input_b.grid(row=2, column=1, pady=5, padx=0)

            elif input_var.get() == "table":
                n = int(input_n.get())
                if (n > 0 and n < 5):
                    num_points = n + 1

                    ctk.CTkLabel(input_frame, text="x", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=5)

                    global input_x
                    global input_y
                    input_x = []
                    input_y = []

                    for i in range(num_points):
                        input_x_entry = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                        input_x_entry.grid(row=1, column=i+1, pady=5, padx=5)
                        input_x.append(input_x_entry)

                        input_y_entry = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                        input_y_entry.grid(row=2, column=i+1, pady=5, padx=5)
                        input_y.append(input_y_entry)

                        if(i > 1 and i < num_points):
                            ctk.CTkLabel(input_frame, text=f"x{i-1}", text_color="#FFFFFF").grid(row=0, column=i, pady=5, padx=5)

                    # a label
                    ctk.CTkLabel(input_frame, text="a/x0", text_color="#FFFFFF").grid(row=0, column=1, pady=5, padx=5)
                    # b label
                    ctk.CTkLabel(input_frame, text=f"b/x{num_points-1}", text_color="#FFFFFF").grid(row=0, column=num_points, pady=5, padx=5)

        # Radio buttons
        ctk.CTkLabel(top_frame, text="Como deseja realizar o input: ", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
        global input_var
        input_var = tk.StringVar(value="func")
        input_var.trace("w", updateInput)

        ctk.CTkRadioButton(top_frame, text="Função", variable=input_var, value="func", text_color="#FFFFFF").grid(row=3, column=0, padx=10, pady=20)
        ctk.CTkRadioButton(top_frame, text="Tabela", variable=input_var, value="table", text_color="#FFFFFF").grid(row=3, column=1, padx=10, pady=20)

        updateInput()

        # Resolver
        ctk.CTkButton(bottom_frame, text="Resolver", command=lambda: solve("closed"), text_color="#FFFFFF").grid(row=1, column=0, padx=20, pady=30)

        # Result
        ctk.CTkLabel(bottom_frame, textvariable=result_text, text_color="#FFFFFF").grid(row=0, column=0, pady=50, padx=10)

        # Back
        back = ctk.CTkButton(bottom_frame, text="Voltar", command=back_to_main)
        back.grid(row=2, column=0, padx=10, pady=50)

        return frame

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

        # n
        ctk.CTkLabel(top_frame, text="Escolha o grau da fórmula Aberta (n)", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=0)
        global input_n_open
        input_n_open = tk.Entry(top_frame, width=5, bg="#2E2E2E", fg="white", insertbackground="white")
        input_n_open.grid(row=1, column=1, pady=5, padx=0)

        global result_text_open
        result_text_open = tk.StringVar()
        # input of the function/points
        def updateInput(*args):
            for widget in input_frame.winfo_children():
                widget.destroy()

            result_text_open.set("")

            if input_var_open.get() == "func":
                ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
                global input_f_open
                input_f_open = tk.Entry(input_frame, width=20, bg="#2E2E2E", fg="white", insertbackground="white")
                input_f_open.grid(row=0, column=1, pady=5, padx=0)

                ctk.CTkLabel(input_frame, text="Limite inferior de integração", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
                global input_a_open
                input_a_open = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                input_a_open.grid(row=1, column=1, pady=5, padx=0)

                ctk.CTkLabel(input_frame, text="Limite superior de integração", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
                global input_b_open
                input_b_open = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                input_b_open.grid(row=2, column=1, pady=5, padx=0)

            elif input_var_open.get() == "table":
                n = int(input_n_open.get())
                if (n > -1 and n < 4):
                    num_points = n + 3

                    ctk.CTkLabel(input_frame, text="x", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=5)
                    ctk.CTkLabel(input_frame, text="f(x)", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=5)

                    global input_x_open
                    global input_y_open
                    input_x_open = []
                    input_y_open = []

                    for i in range(num_points):
                        input_x_entry = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                        input_x_entry.grid(row=1, column=i+1, pady=5, padx=5)
                        input_x_open.append(input_x_entry)

                        input_y_entry = tk.Entry(input_frame, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
                        input_y_entry.grid(row=2, column=i+1, pady=5, padx=5)
                        input_y_open.append(input_y_entry)

                        if(i > 1 and i < num_points):
                            ctk.CTkLabel(input_frame, text=f"x{i-2}", text_color="#FFFFFF").grid(row=0, column=i, pady=5, padx=5)

                    # a label
                    ctk.CTkLabel(input_frame, text="a", text_color="#FFFFFF").grid(row=0, column=1, pady=5, padx=5)
                    # b label
                    ctk.CTkLabel(input_frame, text="b", text_color="#FFFFFF").grid(row=0, column=num_points, pady=5, padx=5)

        # Radio buttons
        ctk.CTkLabel(top_frame, text="Como deseja realizar o input: ", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
        global input_var_open
        input_var_open = tk.StringVar(value="func")
        input_var_open.trace("w", updateInput)

        ctk.CTkRadioButton(top_frame, text="Função", variable=input_var_open, value="func", text_color="#FFFFFF").grid(row=3, column=0, padx=10, pady=20)
        ctk.CTkRadioButton(top_frame, text="Tabela", variable=input_var_open, value="table", text_color="#FFFFFF").grid(row=3, column=1, padx=10, pady=20)

        updateInput()

        # Resolver
        ctk.CTkButton(bottom_frame, text="Resolver", command=lambda: solve("open"), text_color="#FFFFFF").grid(row=1, column=0, padx=20, pady=30)

        # Result
        ctk.CTkLabel(bottom_frame, textvariable=result_text_open, text_color="#FFFFFF").grid(row=0, column=0, pady=50, padx=10)

        # Back
        back = ctk.CTkButton(bottom_frame, text="Voltar", command=back_to_main)
        back.grid(row=2, column=0, padx=10, pady=50)

        return frame


    # Configuração inicial do programa
    app = ctk.CTk()
    app.title("Integração Numérica")
    app.geometry("1200x800")
    app.grid_columnconfigure(0, weight=1)
    app.configure(fg_color="#131313")

    # Armazena os frames
    frames = {}
    # Cria as diferentes páginas
    frames['main'] = mainFrame(app, frames)
    frames['open'] = openNewtonCotesFrame(app, frames)
    frames['closed'] = closedNewtonCotesFrame(app, frames)


    # Posicionar todos os frames
    for frame in frames.values():
        frame.place(relwidth=1, relheight=1)

    show_frame(frames['main'])
    app.mainloop()

if __name__ == "__main__":
    run()