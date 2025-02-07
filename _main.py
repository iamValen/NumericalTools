import tkinter as tk
import customtkinter as ctk

from _methodrow import MethodRow

import bases

import gj
import integration
import nonLinearSystems

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Numerical Tools")
        self.geometry("1200x800")
        self.configure(fg_color="#131313")

        # Create a container for the method rows that fills the window.
        methods_frame = ctk.CTkFrame(self, fg_color="#131313")
        methods_frame.pack(expand=True, fill="both")  # This makes the container expand to fill available space

        # Top spacer: fills extra space above the buttons.
        top_spacer = ctk.CTkFrame(methods_frame, fg_color="#131313")
        top_spacer.pack(expand=True, fill="both")

        # Container for the button rows.
        buttons_container = ctk.CTkFrame(methods_frame, fg_color="#131313")
        buttons_container.pack()  # This container will hold your buttons (and it will be centered vertically due to the spacers)

        # Fixed button width for all method rows.
        button_width = 200

        BaseConvertion = MethodRow(
            buttons_container,
            button_text="Base Convertion",
            tooltip_text="Convert any number from any base to other base",
            command=self.bases,
            button_width=button_width
        )
        BaseConvertion.pack(pady=5, fill="x", anchor="center")

        NLSroots = MethodRow(
            buttons_container,
            button_text="Roots of Non Linear Systems",
            tooltip_text="Find the aproximated values\nof Non Linear Systems using\nthe Bissection, Newton or the Secant method",
            button_width=button_width
        )
        NLSroots.pack(pady=5, fill="x", anchor="center")

        # Create each method row within the buttons container.
        LinearSystems = MethodRow(
            buttons_container,
            button_text="Linear Systems",
            tooltip_text="Solve linear systems using \n Gauss & Jordan elimination",
            command=self.gj,
            button_width=button_width
        )
        LinearSystems.pack(pady=5, fill="x", anchor="center")

        method4 = MethodRow(
            buttons_container,
            button_text="Integration",
            command=self.integration,
            tooltip_text="Find the integrals of functions\nor tables with coordinates",
            button_width=button_width
        )
        method4.pack(pady=5, fill="x", anchor="center")

        method5 = MethodRow(
            buttons_container,
            button_text="Non Linear Systems",
            tooltip_text="Solve non linear systems using \n the Newton elimination.",
            command=self.nonLinearSystems,
            button_width=button_width
        )
        method5.pack(pady=5, fill="x", anchor="center")

        # Bottom spacer: fills extra space below the buttons.
        bottom_spacer = ctk.CTkFrame(methods_frame, fg_color="#131313")
        bottom_spacer.pack(expand=True, fill="both")

    def bases(self):
        bases.run()

    def gj(self):
        gj.run()
    
    def integration(self):
        integration.run()

    def nonLinearSystems(self):
        nonLinearSystems.run()


if __name__ == "__main__":
    app = Main()
    app.mainloop()
