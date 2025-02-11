"""
This program solves systems of linear equations
using the Jacobi and Gauss-Seidel iterative methods. 
It allows users to enter the matrix coefficients and parameters such as tolerance and number of iterations.
The program checks for diagonal dominance and warns the user if the matrix does
not satisfy this condition. The solution is displayed with the number of iterations taken.
"""

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
            s = 0
            for j in range(rows):
                if i != j:
                    s += abs(matrix[i][j])
            if s > pivot:
                return False
        return True

    def isImpossible(A, B):
        # Aumented Matrix [A | B]
        augmented_matrix = np.column_stack((A, B))
        if np.linalg.det(A) == 0:
            return False
        return False

    def askToContinue():
        return messagebox.askyesno(
            "Careful!",
            "The matrix is not Diagonal Dominant\nDo you still want to proceed?")

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
            result_text.set("The system of equations is impossible")
            clearEntries()
            return None
        if not isDiagonallyDominant(A):
            if not askToContinue():
                result_text.set("Canceled by the user")
                clearEntries()
                return None
        for k in range(iterations):
            x = np.vstack([x, [0] * len(B)])
            for i in range(len(B)):
                s = 0
                for j in range(len(B)):
                    if j != i:
                        s += A[i][j] * x[k][j]
                x[k + 1][i] = (B[i] - s) / A[i][i]
            if abs(np.linalg.norm(x[k + 1] - x[k]) / np.linalg.norm(x[k + 1])) < tolerance:
                return x[k + 1], k + 1
        return x[iterations], iterations

    def gauss(A, B, x, iterations, tolerance):
        if isImpossible(A, B):
            result_text.set("Canceled by the user")
            clearEntries()
            return None
        if not isDiagonallyDominant(A):
            if not askToContinue():
                result_text.set("Canceled by the user")
                clearEntries()
                return None
        for k in range(iterations):
            x = np.vstack([x, [0] * (len(B))])
            for i in range(len(B)):
                x[k + 1][i] = B[i]
                s = 0
                for j in range(len(B)):
                    if j < i:
                        s += A[i][j] * x[k + 1][j]
                    elif j > i:
                        s += A[i][j] * x[k][j]
                x[k + 1][i] = (B[i] - s) / A[i][i]
            if abs(np.linalg.norm(x[k + 1] - x[k]) / np.linalg.norm(x[k + 1])) < tolerance:
                return x[k + 1], k
        return x[iterations], iterations

    def solve():
        result_text.set("")
        try:
            dimension = int(entry_dimension.get())
            try:
                acceptable_error = float(entry_error.get())
            except ValueError:
                acceptable_error = 1E-4
            try:
                N = int(entry_iterations.get())
                if N < 1:
                    raise ValueError("Number of iterations invalid")
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

        # A, B and X text boxes
        ctk.CTkLabel(frame_matrix, text="A", text_color="#FFFFFF").grid(row=0, column=0, columnspan=dimension, pady=5)
        ctk.CTkLabel(frame_matrix, text="X", text_color="#FFFFFF").grid(row=0, column=dimension, pady=5)
        ctk.CTkLabel(frame_matrix, text="B", text_color="#FFFFFF").grid(row=0, column=dimension + 1, pady=5)

        for i in range(dimension):
            for j in range(dimension):
                entriesA[i][j] = ctk.CTkEntry(frame_matrix, width=50, fg_color="#2E2E2E", text_color="white", placeholder_text="")
                entriesA[i][j].grid(row=i + 1, column=j, padx=5, pady=5)
            entriesX[i] = ctk.CTkEntry(frame_matrix, width=50, fg_color="#2E2E2E", text_color="white", placeholder_text="")
            entriesX[i].grid(row=i + 1, column=dimension, padx=35, pady=5)
            entriesB[i] = ctk.CTkEntry(frame_matrix, width=50, fg_color="#2E2E2E", text_color="white", placeholder_text="")
            entriesB[i].grid(row=i + 1, column=dimension + 1, padx=5, pady=5)

        frame_matrix.grid(row=2, column=0, pady=20, columnspan=3)
        frame_bottom.grid(row=3, column=0, pady=20, padx=10)

    # base UI
    app = ctk.CTk()
    app.title("Sistema de Equações Lineares")
    app.geometry("1200x800")
    app.grid_columnconfigure(0, weight=1)
    app.configure(fg_color="#131313")

    frame_top = ctk.CTkFrame(app, fg_color="#131313")
    frame_top.grid(row=0, column=0, pady=20, padx=10)
    frame_matrix = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom = ctk.CTkFrame(app, fg_color="#131313")
    frame_bottom.grid(row=1, column=0, pady=20, padx=10)

    ctk.CTkLabel(frame_top, text="Dimensão da Matriz:", text_color="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
    entry_dimension = ctk.CTkEntry(frame_top, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
    entry_dimension.grid(row=0, column=1, pady=5, padx=10)

    ctk.CTkLabel(frame_top, text="Erro de tolerância:", text_color="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
    entry_error = ctk.CTkEntry(frame_top, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
    entry_error.grid(row=1, column=1, pady=5, padx=10)

    ctk.CTkLabel(frame_top, text="Número de iterações:", text_color="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
    entry_iterations = ctk.CTkEntry(frame_top, width=100, fg_color="#2E2E2E", text_color="white", placeholder_text="")
    entry_iterations.grid(row=2, column=1, pady=5, padx=10)

    ctk.CTkButton(frame_top, text="Criar Matriz", command=createEntries, text_color="#FFFFFF").grid(row=3, column=0, pady=20)

    method_var = tk.StringVar(value="Jacobi")
    ctk.CTkRadioButton(frame_bottom, text="Jacobi", variable=method_var, value="Jacobi", text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)
    ctk.CTkRadioButton(frame_bottom, text="Gauss-Seidel", variable=method_var, value="Gauss-Seidel", text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)

    ctk.CTkButton(frame_bottom, text="Resolver", command=solve, text_color="#FFFFFF").pack(side=tk.LEFT, padx=10)

    result_text = tk.StringVar()
    ctk.CTkLabel(app, textvariable=result_text, text_color="#FFFFFF").grid(row=4, column=0, pady=20, padx=10)

    app.mainloop()

if __name__ == "__main__":
    run()
