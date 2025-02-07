import tkinter as tk
import customtkinter as ctk

from _section import Section

import bases
import nonLinearSystems
import LinearSystems
import integration
import NewtonRaphson

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Numerical Tools")
        self.geometry("1200x800")
        self.configure(fg_color="#131313")

        # Container frame that fills the window for sections
        methods_frame = ctk.CTkFrame(self, fg_color="#131313")
        methods_frame.pack(expand=True, fill="both")

        # Top spacer to center content vertically
        top_spacer = ctk.CTkFrame(methods_frame, fg_color="#131313")
        top_spacer.pack(expand=True, fill="both")

        # Container for section buttons
        buttons_container = ctk.CTkFrame(methods_frame, fg_color="#131313")
        buttons_container.pack()

        # Fixed button width for all sections
        button_width = 200

        # Section for Base Conversion
        BaseConversion = Section(
            buttons_container,
            button_text="              Base Conversion              ",
            tooltip_text="Convert any number from any base to another base",
            command=self.bases,
            button_width=button_width
        )
        BaseConversion.pack(pady=5)

        # Section for Integration
        Integration = Section(
            buttons_container,
            button_text="                   Integration                  ",
            command=self.integration,
            tooltip_text="Compute integrals of functions or coordinate tables",
            button_width=button_width
        )
        Integration.pack(pady=5, anchor="center")

        # Section for Linear Systems
        LinearSystemsSection = Section(
            buttons_container,
            button_text="               Linear Systems               ",
            tooltip_text="Solve linear systems using Jacobi or Gauss-Seidel methods",
            command=self.gj,
            button_width=button_width
        )
        LinearSystemsSection.pack(pady=5, anchor="center")

        # Section for Non-Linear Systems
        NonLinearSystemsSection = Section(
            buttons_container,
            button_text="            Non Linear Systems            ",
            tooltip_text="Approximate solutions of non-linear systems using Bisection, Newton or Secant methods",
            command=self.nonLinearSystems,
            button_width=button_width
        )
        NonLinearSystemsSection.pack(pady=5, anchor="center")

        # Section for Newton-Raphson applied to NLS
        NewtonRaphsonSection = Section(
            buttons_container,
            button_text="         NLS - Newton-Raphson         ",
            tooltip_text="Approximate solutions of non-linear systems using the Newton-Raphson method",
            command=self.NewtonRaphson,
            button_width=button_width
        )
        NewtonRaphsonSection.pack(pady=5, anchor="center")

        # Bottom spacer to center content vertically
        bottom_spacer = ctk.CTkFrame(methods_frame, fg_color="#131313")
        bottom_spacer.pack(expand=True, fill="both")

    # Section command callbacks
    def bases(self):
        bases.run()
    
    def integration(self):
        integration.run()

    def gj(self):
        LinearSystems.run()

    def nonLinearSystems(self):
        nonLinearSystems.run()

    def NewtonRaphson(self):
        NewtonRaphson.run()

if __name__ == "__main__":
    app = Main()
    app.mainloop()
