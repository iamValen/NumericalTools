import customtkinter as ctk

class Section(ctk.CTkFrame):
    def __init__(self, master, button_text, tooltip_text, command=None, button_width=10000, **kwargs):
        super().__init__(master, fg_color="#131313", **kwargs)
        self.command = command
        self.tooltip_text = tooltip_text

        # Create a fixed-width button
        self.method_button = ctk.CTkButton(
            self,
            text=button_text,
            command=self.command,
            width=button_width,
            height=70,
            anchor="center",
            font=("Arial", 16)
        )
        self.method_button.grid(row=0, column=0, padx=10, pady=10)

        # Create a fixed-size frame for the "?" icon
        self.question_frame = ctk.CTkFrame(
            self,
            fg_color="#131313",
            corner_radius=15,
            width=60,
            height=60
        )
        self.question_frame.grid(row=0, column=1, padx=10)

        # Add the "?" label inside the frame
        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="?",
            font=("Arial", 24),
            text_color="white",
            fg_color="transparent"
        )
        self.question_label.pack(expand=True)

        # Setup the tooltip label (initially hidden)
        self.tooltip_label = ctk.CTkLabel(
            self.winfo_toplevel(),
            text=self.tooltip_text,
            fg_color="#333333",
            text_color="white",
            corner_radius=5
        )
        self.tooltip_label.place_forget()

        # Bind hover events to show/hide the tooltip
        self.question_label.bind("<Enter>", self.show_tooltip)
        self.question_label.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Calculate tooltip position relative to the window
        x = self.question_frame.winfo_rootx() - self.winfo_toplevel().winfo_rootx() + self.question_frame.winfo_width() + 5
        y = self.question_frame.winfo_rooty() - self.winfo_toplevel().winfo_rooty()
        self.tooltip_label.place(x=x, y=y)

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()
