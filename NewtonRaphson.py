import numpy as np
import tkinter as tk
import customtkinter as ctk
from sympy import symbols, Matrix, lambdify, sympify, pi, E, sin, cos, tan
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def run():
    def NewtonRaphson():
        result_text.set("")
        try:
            # Get the number of equations
            n = int(entry_num_vars.get())
            vars = [symbols(f'x{i+1}') for i in range(n)]
            
            extra = {
                'pi': pi,
                'e': E,
                'sin': sin,
                'sen': sin,
                'cos': cos,
                'tan': tan,
                **{str(var): var for var in vars}
            }

            # Get the equations
            equations = []
            for i in range(n):
                eq = equations_entries[i].get()
                eq_split = eq.split("=")
                if len(eq_split) != 2:
                    raise ValueError(f"Equation {i+1} is in an invalid format. Use 'left side = right side'.")
                else:
                    left_side = eq_split[0].strip()
                    right_side = eq_split[1].strip()
                left_exp = sympify(left_side, locals=extra)
                right_exp = sympify(right_side, locals=extra)
                equation = left_exp - right_exp
                equations.append(equation)

            # Get the initial approximation
            x0 = []
            for i in range(n):
                x0.append(float(initial_approximations_entries[i].get()))
            x0 = np.array(x0)

            # Stopping criteria
            max_iter = int(entry_max_iter.get())
            tolerance = float(entry_tolerance.get())

            # Build the function vector and Jacobian
            F = Matrix(equations)
            J = F.jacobian(vars)

            F_func = lambdify(vars, F, modules='numpy')
            J_func = lambdify(vars, J, modules='numpy')

            # Newton's method
            xk = x0
            for k in range(max_iter):
                Fx = np.array(F_func(*xk), dtype=float).flatten()
                Jx = np.array(J_func(*xk), dtype=float)
                if np.linalg.norm(Fx, ord=np.inf) < tolerance:
                    result_text.set(f"Solution found in {k} iterations: {xk}")
                    if n <= 3:
                        plot_graph(equations, vars, x0, solution=xk)
                    return
                try:
                    delta_x = np.linalg.solve(Jx, -Fx)
                except np.linalg.LinAlgError:
                    result_text.set(f"Jacobian is singular at iteration {k}, cannot determine a solution.")
                    return
                xk = xk + delta_x
            result_text.set(f"Maximum iterations reached. Approximate solution:\n{xk}")
            if n <= 3:
                plot_graph(equations, vars, x0, solution=xk)
        
        except ValueError as e:
            result_text.set(str(e))
        except Exception as e:
            result_text.set(f"Error: {str(e)}")

    # --- 2D Graph Plotting ---
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
                    print(f"Error plotting equation {i+1}: {e}")
            if solution is not None:
                plt.scatter(solution[0], solution[1], color='red', label='Newton Solution', zorder=10)
            plt.xlabel(f'{x}')
            plt.ylabel(f'{y}')
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
            colors = plt.cm.tab10.colors
            num_colors = len(colors)
            for i, (func, eq) in enumerate(zip(eq_funcs, equations)):
                Z = func(X, Y, np.zeros_like(X))
                ax.plot_surface(
                    X, Y, Z, 
                    alpha=0.7, rstride=1, cstride=1, 
                    color=colors[i % num_colors],
                    edgecolor='none', 
                    label=f"Equation {i+1}"
                )
            if solution is not None:
                ax.scatter(solution[0], solution[1], solution[2], color='red', label='Newton Solution', s=100)
                ax.legend()
            ax.set_xlabel(f"{x}")
            ax.set_ylabel(f"{y}")
            ax.set_zlabel(f"{z}")
            plt.title("3D Graph of Equations")
            plt.show()

    # --- Create input fields for equations and initial approximations ---
    def createEntries():
        try:
            num_vars = int(entry_num_vars.get())
            if num_vars <= 0:
                raise ValueError("The number of variables must be greater than 0.")
        except ValueError:
            result_text.set("Invalid number of variables.")
            return
        
        for widget in frame_matrix.winfo_children():
            widget.destroy()

        global equations_entries, initial_approximations_entries
        equations_entries = []
        initial_approximations_entries = []

        for i in range(num_vars):
            ctk.CTkLabel(frame_matrix, text=f"Equation {i+1}:", text_color="#FFFFFF").grid(row=i, column=0, pady=5, padx=10)
            eq_entry = ctk.CTkEntry(frame_matrix, width=300)
            eq_entry.grid(row=i, column=1, pady=5)
            equations_entries.append(eq_entry)

            ctk.CTkLabel(frame_matrix, text=f"Initial x{i+1}:", text_color="#FFFFFF").grid(row=i, column=2, pady=5, padx=10)
            init_entry = ctk.CTkEntry(frame_matrix, width=100)
            init_entry.grid(row=i, column=3, pady=5)
            initial_approximations_entries.append(init_entry)

        frame_matrix.grid(row=2, column=0, pady=20, columnspan=4)
        frame_bottom.grid(row=3, column=0, pady=20)

    # --- UI Base Configuration ---
    app = ctk.CTk()
    app.title("Nonlinear Equation Solver - Newton's Method")
    app.geometry("1000x600")
    app.grid_columnconfigure(0, weight=1)
    app.configure(fg_color="#131313")

    frame_top = ctk.CTkFrame(app, fg_color="#131313")
    frame_top.grid(row=0, column=0, pady=20, padx=10)
    frame_matrix = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom.grid(row=1, column=0, pady=20, padx=10)

    ctk.CTkLabel(frame_top, text="Number of variables:", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
    entry_num_vars = ctk.CTkEntry(frame_top, width=100)
    entry_num_vars.grid(row=0, column=1, pady=5, padx=10)

    ctk.CTkLabel(frame_top, text="Maximum iterations:", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
    entry_max_iter = ctk.CTkEntry(frame_top, width=100)
    entry_max_iter.grid(row=1, column=1, pady=5, padx=10)

    ctk.CTkLabel(frame_top, text="Tolerance:", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
    entry_tolerance = ctk.CTkEntry(frame_top, width=100)
    entry_tolerance.grid(row=2, column=1, pady=5, padx=10)

    ctk.CTkButton(frame_top, text="Create Entries", command=createEntries, text_color="#FFFFFF").grid(row=3, column=0, pady=20)

    result_text = tk.StringVar()
    ctk.CTkLabel(app, textvariable=result_text, text_color="#FFFFFF").grid(row=4, column=0, pady=20, padx=10)

    app.mainloop()

if __name__ == "__main__":
    run()
