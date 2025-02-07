import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter as ctk 

def run():
    def isDiagonallyDominant(matrix):
        rows = len(matrix)                 
        cols = len(matrix[0])  

        for i in range(cols):
            pivot = abs(matrix[i][i])
            if pivot == 0:
                return False

            sum = 0
            for j in range(rows):
                if i != j:
                    sum += abs(matrix[i][j])

            if sum > pivot:
                return False

        return True

    def isImpossible(A, B):
        # Faz a matriz aumentada [A | B]
        augmented_matrix = np.column_stack((A, B))
        # Verifica se o determinante da matriz A é zero, o que pode indicar um sistema impossível
        if np.linalg.det(A) == 0:
            # Verfica se a matriz aumentada também tem determinante zero
            return False

        return False

    def askToContinue():
        return messagebox.askyesno(
            "Atenção",
            "A matriz não é diagonalmente dominante.\nDeseja continuar mesmo assim?")

    def clearEntries():
        for row in entriesA:
            for entry in row:
                entry.delete(0, tk.END)
        for entry in entriesB:
            entry.delete(0, tk.END)
        for entry in entriesX:
            entry.delete(0, tk.END)

    def jacobi(A, B, x, iterations, tolerance):
        if isImpossible(A, B):
            result_text.set("O sistema de equações é impossível")
            clearEntries()
            return None

        if not isDiagonallyDominant(A):
            if not askToContinue():
                result_text.set("Cancelado pelo utilizador")
                clearEntries()
                return None

        for k in range(iterations):
            x = np.vstack([x, [0] * len(B)])

            for i in range(len(B)):
                sum = 0
                for j in range(len(B)):
                    if j != i:
                        sum += A[i][j] * x[k][j]
                x[k + 1][i] = (B[i] - sum) / A[i][i]

            if abs(np.linalg.norm(x[k + 1] - x[k]) / np.linalg.norm(x[k + 1])) < tolerance:
                return x[k + 1], k + 1

        return x[iterations], iterations

    def gauss(A, B, x, iterations, tolerance):
        if isImpossible(A, B):
            result_text.set("Cancelado pelo utilizador")
            clearEntries()
            return None

        if not isDiagonallyDominant(A):
            if not askToContinue():
                result_text.set("Cancelado pelo utilizador")
                clearEntries()
                return None

        for k in range(iterations):
            x = np.vstack([x, [0] * (len(B))])

            for i in range(len(B)):
                x[k + 1][i] = B[i]
                sum = 0

                for j in range(len(B)):
                    if j < i:
                        sum += A[i][j] * x[k + 1][j]
                    elif j > i:
                        sum += A[i][j] * x[k][j]

                x[k + 1][i] = (B[i] - sum) / A[i][i]

            if abs(np.linalg.norm(x[k + 1] - x[k]) / np.linalg.norm(x[k + 1])) < tolerance:
                return x[k + 1], k

        return x[iterations], iterations

    def solve():
        result_text.set("")  # Limpar mensagem de resultado
        try:
            dimension = int(entry_dimension.get())
            # Caso os valores sejam inválidos usa-se os valores default
            try:
                acceptable_error = float(entry_error.get())
            except ValueError:
                acceptable_error = 1E-4

            try:
                N = int(entry_iterations.get())
                if N < 1:
                    raise ValueError("Número de iterações inválido. Iterações Máximas: 10\n")
            except ValueError:
                N = 10

            method = method_var.get()

            A = [[float(entriesA[i][j].get()) for j in range(dimension)] for i in range(dimension)]
            B = [float(entriesB[i].get()) for i in range(dimension)]

            try:
                x = [float(entriesX[i].get()) for i in range(dimension)]
            except (ValueError, IndexError):
                x = [0.0] * dimension

            if method == "Jacobi":
                result = jacobi(A, B, x, N, acceptable_error)
            elif method == "Gauss-Seidel":
                result = gauss(A, B, x, N, acceptable_error)

            if result is not None:
                solution, iterations = result
                formatted_solution = f"{' ; '.join([f'{val:.6f}' for val in solution])}"
                if iterations < N:
                    result_text.set(f"Solução (em {iterations} iterações):\n{formatted_solution}")
                else:
                    result_text.set(f"Solução (em {iterations} iterações):\n{formatted_solution}\nMas este resultado pode não ser muito preciso...")

        except ValueError as e:
            result_text.set(str(e))
        except Exception as e:
            result_text.set(f"Erro: {str(e)}")


    def createEntries():
        try:
            dimension = int(entry_dimension.get())
            if dimension <= 0:
                raise ValueError("A dimensão da matriz deve ser maior que 0.")
        except ValueError:
            result_text.set("Insira uma dimensão válida para a matriz.")
            return

        for widget in frame_matrix.winfo_children():
            widget.destroy()

        global entriesA, entriesB, entriesX
        entriesA = [[None] * dimension for _ in range(dimension)]
        entriesB = [None] * dimension
        entriesX = [None] * dimension

        ctk.CTkLabel(frame_matrix, text="A", text_color="#FFFFFF").grid(row=0, column=0, columnspan=dimension, pady=5)
        ctk.CTkLabel(frame_matrix, text="X", text_color="#FFFFFF").grid(row=0, column=dimension, pady=5)
        ctk.CTkLabel(frame_matrix, text="B", text_color="#FFFFFF").grid(row=0, column=dimension + 1, pady=5)

        for i in range(dimension):
            for j in range(dimension):
                entriesA[i][j] = tk.Entry(frame_matrix, width=5, bg="#2E2E2E", fg="white", insertbackground="white",
                                          highlightbackground="#FFFFFF")
                entriesA[i][j].grid(row=i + 1, column=j, padx=5, pady=5)

            entriesX[i] = tk.Entry(frame_matrix, width=5, bg="#2E2E2E", fg="white", insertbackground="white",
                                   highlightbackground="#FFFFFF")
            entriesX[i].grid(row=i + 1, column=dimension, padx=35, pady=5)

            entriesB[i] = tk.Entry(frame_matrix, width=5, bg="#2E2E2E", fg="white", insertbackground="white",
                                   highlightbackground="#FFFFFF")
            entriesB[i].grid(row=i + 1, column=dimension + 1, padx=5, pady=5)

        frame_matrix.grid(row=2, column=0, pady=20, columnspan=3)
        frame_bottom.grid(row=3, column=0, pady=20, padx=10)


    # UI base
    app = ctk.CTk()
    app.title("Sistema de Equações Lineares")
    app.geometry("1200x800")
    app.grid_columnconfigure(0, weight=1)
    app.configure(fg_color="#131313")

    # Divisão em partes
    frame_top = ctk.CTkFrame(app, fg_color="#131313")
    frame_top.grid(row=0, column=0, pady=20, padx=10)
    frame_matrix = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom.grid(row=1, column=0, pady=20, padx=10)

    # Entry para a dimensão
    ctk.CTkLabel(frame_top, text="Dimensão da Matriz:", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
    entry_dimension = tk.Entry(frame_top, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
    entry_dimension.grid(row=0, column=1, pady=5, padx=10)

    # Entry para o erro
    ctk.CTkLabel(frame_top, text="Erro de tolerância:", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
    entry_error = tk.Entry(frame_top, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
    entry_error.grid(row=1, column=1, pady=5, padx=10)

    # Entry para as iterações
    ctk.CTkLabel(frame_top, text="Número de iterações:", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
    entry_iterations = tk.Entry(frame_top, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
    entry_iterations.grid(row=2, column=1, pady=5, padx=10)

    # Botão "Criar Matriz"
    ctk.CTkButton(frame_top, text="Criar Matriz", command=createEntries, text_color="#FFFFFF").grid(row=3, column=0, pady=20)

    # Botões radio para a escolha do método
    method_var = tk.StringVar(value="Jacobi")
    ctk.CTkRadioButton(frame_bottom, text="Jacobi", variable=method_var, value="Jacobi", text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)
    ctk.CTkRadioButton(frame_bottom, text="Gauss-Seidel", variable=method_var, value="Gauss-Seidel", text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)
    # Botão "Resolver"
    ctk.CTkButton(frame_bottom, text="Resolver", command=solve, text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)

    result_text = tk.StringVar()
    ctk.CTkLabel(app, textvariable=result_text, text_color="#FFFFFF").grid(row=4, column=0, pady=20, padx=10)

    app.mainloop()

if __name__ == "__main__":
    run()