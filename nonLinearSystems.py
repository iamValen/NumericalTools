import numpy as np
import tkinter as tk
import customtkinter as ctk
from sympy import symbols, Matrix, lambdify, sympify, pi, E, sin, cos, tan

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def run():
    def newton_nonlinear_system():
        result_text.set("")
        try:
            # Obter nr de equações
            n = int(entry_num_vars.get())
            vars = [symbols(f'x{i+1}') for i in range(n)]
            
            extra = {
                'pi': pi,
                'e': E,
                'sin': sin,
                'sen' : sin,
                'cos': cos,
                'tan': tan,
                **{str(var): var for var in vars}
            }

            # Obter equações
            equations = []
            for i in range(n):
                eq = equations_entries[i].get()
                eq_split = eq.split("=")
                if len(eq_split) != 2:
                    raise ValueError(f"Equação {i+1} no formato inválido. Use 'lado esquerdo = valor'.")
                else:
                    left_side = eq_split[0].strip()
                    right_side = eq_split[1].strip()
                
                left_exp = sympify(left_side, locals=extra)
                right_exp = sympify(right_side, locals=extra)
                # Igualar expressão a 0
                equation = left_exp - right_exp
                equations.append(equation)

            # Obter aproximação inicial
            x0 = []
            for i in range(n):
                x0.append(float(initial_approximations_entries[i].get()))
            x0 = np.array(x0)

            # Critérios de paragem
            max_iter = int(entry_max_iter.get())
            tolerance = float(entry_tolerance.get())

            # Montar o vetor de funções e a Jacobiana
            F = Matrix(equations)
            J = F.jacobian(vars)

            # Converter funções simbólicas em funções numéricas
            F_func = lambdify(vars, F, modules='numpy')
            J_func = lambdify(vars, J, modules='numpy')

            # Método de Newton
            xk = x0
            for k in range(max_iter):
                # Avaliar F(x) e J(x)
                Fx = np.array(F_func(*xk), dtype=float).flatten()
                Jx = np.array(J_func(*xk), dtype=float)

                # Verificar critério de convergência na norma infinito
                if np.linalg.norm(Fx, ord=np.inf) < tolerance:
                    result_text.set(f"Solução encontrada em {k} iterações: {xk}")
                    print(f"Solução encontrada em {k} iterações: {xk}")
                    if n <= 3:
                        plot_graph(equations, vars, x0, solution=xk)
                    return

                # Resolver sistema linear J(x) * dx = -F(x)
                try:
                    delta_x = np.linalg.solve(Jx, -Fx)
                except np.linalg.LinAlgError:
                    print(f"Iteração {k}:")
                    print("F(x):")
                    print(Fx)
                    print("Matriz Jacobiana (Jx):")
                    print(Jx)
                    result_text.set(f"A matriz Jacobiana da iteração {k} é singular, logo não é possível determinar uma solução")
                    print((f"A matriz Jacobiana da iteração {k} é singular, logo não é possível determinar uma solução"))
                    return
                # Atualizar xk
                xk = xk + delta_x
                print(f"Iteração {k}:")
                print(f"xk: {xk}")
                print("Matriz Jacobiana (Jx):")
                print(Jx)
                print("F(x):")
                print(Fx)
                print("\n")

            result_text.set(f"Número máximo de iterações atingido. Solução aproximada:\n{xk}")
            print(f"Número máximo de iterações atingido. Solução aproximada:\n{xk}")
            if n <= 3:
                plot_graph(equations, vars, x0, solution=xk)
        
        except ValueError as e:
            result_text.set(str(e))
        except Exception as e:
            result_text.set(f"Erro: {str(e)}")

    # Cria o gráfico
    def plot_graph(equations, vars, x0, solution=None, path=None):
        if len(vars) == 2:
            x, y = vars
            eq_funcs = [lambdify((x, y), eq, modules='numpy') for eq in equations]

            x_vals = np.linspace(x0[0] - 100, x0[0] + 100, 1000)
            y_vals = np.linspace(x0[1] - 100, x0[1] + 100, 1000)
            X, Y = np.meshgrid(x_vals, y_vals)

            plt.figure(figsize=(8, 6))

            for i, func in enumerate(eq_funcs):
                try:
                    Z = func(X, Y)
                    plt.contour(X, Y, Z, levels=[0], colors=f'C{i}', label=f'Eq {i+1}', alpha=0.6)
                except Exception as e:
                    print(f"Erro ao processar a equação {i + 1} no gráfico: {e}")

            if solution is not None:
                plt.scatter(solution[0], solution[1], color='red', label='Solução do Método de Newton', zorder=10)

            plt.xlabel(f'{x}')
            plt.ylabel(f'{y}')
            plt.title("")
            plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
            plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.show()

        elif len(vars) == 3:
            x, y, z = vars
            eq_funcs = [lambdify((x, y, z), eq, modules='numpy') for eq in equations]

            x_vals = np.linspace(x0[0] - 25, x0[0] + 25, 30)
            y_vals = np.linspace(x0[1] - 25, x0[1] + 25, 30)
            z_vals = np.linspace(x0[2] - 25, x0[2] + 25, 30)

            X, Y = np.meshgrid(x_vals, y_vals)
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            # Paleta de cores distintas
            colors = plt.cm.tab10.colors  # Usar a paleta de 10 cores do Matplotlib
            num_colors = len(colors)

            # Plotar cada função com uma cor diferente
            for i, (func, eq) in enumerate(zip(eq_funcs, equations)):
                Z = func(X, Y, np.zeros_like(X))  # manter z fixo no plano
                ax.plot_surface(
                    X, Y, Z, 
                    alpha=0.7, 
                    rstride=1, cstride=1, 
                    cmap=None,  # Remove cmap padrão para usar cores fixas
                    color=colors[i % num_colors],  # Escolher uma cor distinta
                    edgecolor='none', 
                    label=f"Equação {i+1}"
                )

            # Ponto de solução em vermelho
            if solution is not None:
                ax.scatter(
                    solution[0], solution[1], solution[2],  
                    color='red', label='Solução do Método de Newton', s=100
                )
                ax.legend()

            # Configurações visuais
            ax.set_xlabel(f"{x}")
            ax.set_ylabel(f"{y}")
            ax.set_zlabel(f"{z}")
            plt.title("Gráfico 3D das Funções")
            plt.show()

    # Função para criar os campos de entrada
    def createEntries():
        try:
            num_vars = int(entry_num_vars.get())
            if num_vars <= 0:
                raise ValueError("O número de variáveis deve ser maior que 0.")
        except ValueError:
            result_text.set("Número de variáveis inválido.")
            return
        
        for widget in frame_matrix.winfo_children():
            widget.destroy()

        global equations_entries, initial_approximations_entries
        equations_entries = []
        initial_approximations_entries = []

        for i in range(num_vars):
            # Entradas para as equações
            ctk.CTkLabel(frame_matrix, text=f"Equação {i+1}:", text_color="#FFFFFF").grid(row=i, column=0, pady=5, padx=10)
            eq_entry = ctk.CTkEntry(frame_matrix, width=300)
            eq_entry.grid(row=i, column=1, pady=5)
            equations_entries.append(eq_entry)

            # Entradas para aproximações iniciais
            ctk.CTkLabel(frame_matrix, text=f"x{i+1} inicial:", text_color="#FFFFFF").grid(row=i, column=2, pady=5, padx=10)
            initial_approx_entry = ctk.CTkEntry(frame_matrix, width=100)
            initial_approx_entry.grid(row=i, column=3, pady=5)
            initial_approximations_entries.append(initial_approx_entry)

        frame_matrix.grid(row=2, column=0, pady=20, columnspan=4)
        frame_bottom.grid(row=3, column=0, pady=20)


    # UI base
    app = ctk.CTk()
    app.title("Solução de Equações Não Lineares - Método de Newton")
    app.geometry("1000x600")
    app.grid_columnconfigure(0, weight=1)
    app.configure(fg_color="#131313")

    # Divisão em partes
    frame_top = ctk.CTkFrame(app, fg_color="#131313")
    frame_top.grid(row=0, column=0, pady=20, padx=10)
    frame_matrix = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom.grid(row=1, column=0, pady=20, padx=10)

    # Entrada para o número de variáveis
    ctk.CTkLabel(frame_top, text="Número de variáveis:", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
    entry_num_vars = ctk.CTkEntry(frame_top, width=100)
    entry_num_vars.grid(row=0, column=1, pady=5, padx=10)

    # Entrada para o número máximo de iterações
    ctk.CTkLabel(frame_top, text="Número máximo de iterações:", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
    entry_max_iter = ctk.CTkEntry(frame_top, width=100)
    entry_max_iter.grid(row=1, column=1, pady=5, padx=10)

    # Entrada para tolerância
    ctk.CTkLabel(frame_top, text="Tolerância:", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
    entry_tolerance = ctk.CTkEntry(frame_top, width=100)
    entry_tolerance.grid(row=2, column=1, pady=5, padx=10)

    # Botão "Criar Entradas"
    ctk.CTkButton(frame_top, text="Criar Entradas", command=createEntries, text_color="#FFFFFF").grid(row=3, column=0, pady=20)

    # Botão "Resolver"
    ctk.CTkButton(frame_bottom, text="Resolver", command=newton_nonlinear_system, text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)

    # Variável para o resultado
    result_text = tk.StringVar()
    ctk.CTkLabel(app, textvariable=result_text, text_color="#FFFFFF").grid(row=4, column=0, pady=20, padx=10)

    # Executar o aplicativo
    app.mainloop()


    # Ex1
    # -x1*(x1+1) + 2*x2 = 18
    # (x1-1)**2 + (x2-6)**2 = 25


    # Ex2
    # x1**2-2*x1+x2**2-x3+1=0
    # x1*x2**2-x1-3*x2+x2*x3+2=0
    # x1*x3**2-3*x3+x2*x3**2+x1*x2=0

if __name__ == "__main__":
    run()