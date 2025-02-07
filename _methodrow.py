import customtkinter as ctk
class MethodRow(ctk.CTkFrame):
    def __init__(self, master, button_text, tooltip_text, command=None, button_width=700, **kwargs):
        super().__init__(master, fg_color="#131313", **kwargs)
        self.command = command
        self.tooltip_text = tooltip_text

        # Create the method button with a fixed width
        self.method_button = ctk.CTkButton(
            self,
            text=button_text,
            command=self.command,
            width=button_width,  # Fixed width
            height=60,
            anchor="center",  # Center-align text
            font=("Arial", 16)  # Consistent font size
        )
        self.method_button.grid(row=0, column=0, padx=10, pady=10)

        # Create a fixed-sized frame for the "?" icon
        self.question_frame = ctk.CTkFrame(
            self,
            fg_color="#131313",
            corner_radius=15,
            width=60,
            height=60
        )
        self.question_frame.grid(row=0, column=1, padx=10)

        # Add the "?" label
        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="?",
            font=("Arial", 24),
            text_color="white",
            fg_color="transparent"
        )
        self.question_label.pack(expand=True)

        # Tooltip setup
        self.tooltip_label = ctk.CTkLabel(
            self.winfo_toplevel(),
            text=self.tooltip_text,
            fg_color="#333333",
            text_color="white",
            corner_radius=5
        )
        self.tooltip_label.place_forget()

        # Bind hover events
        self.question_label.bind("<Enter>", self.show_tooltip)
        self.question_label.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.question_frame.winfo_rootx() - self.winfo_toplevel().winfo_rootx() + self.question_frame.winfo_width() + 5
        y = self.question_frame.winfo_rooty() - self.winfo_toplevel().winfo_rooty()
        self.tooltip_label.place(x=x, y=y)

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()
