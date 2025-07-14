
from tkinter import *
from tkinter import messagebox
from leaderboard import LeaderboardWindow


BASE_URL = "http://127.0.0.1:8000"

class SubjectSelection(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="yellow")

        self.subjects = [
            "Accounting", "Agriculture", "Biology", "C . R . K", "I . R . S ", "Independence",
            "Chemistry", "Commerce", "Economics", "English", "Mathematics", "Lekki HeadMaster",
            "Physics", "Life changer", "Literature", "Government"
        ]

        self.selected_subject = StringVar(value="")
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Select CBT Subject Below to Begin!", 
              font=("Arial", 16, "bold"), bg="yellow", fg="black").pack(pady=20)

        # Scrollable container
        container = Frame(self, bg="yellow")
        container.pack(fill=BOTH, expand=True, padx=10, pady=(0, 20))

        canvas = Canvas(container, bg="yellow", highlightthickness=0)
        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="yellow")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create subject radio buttons
        for subject in self.subjects:
            Radiobutton(
                scrollable_frame, text=subject, variable=self.selected_subject, value=subject,
                font=("Arial", 14), bg="white", fg="blue", anchor="w", padx=20, bd=1, width=20,
                selectcolor="white"
            ).pack(anchor="w", pady=5)

        # Start Exam Button
        Button(
            self, text="Start Exam", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
            command=self.start_exam
        ).pack(pady=10)

        # View Leaderboard Button
        Button(
            self, text="View Leaderboard", font=("Arial", 12), bg="#2196F3", fg="white",
            command=self.view_leaderboard
        ).pack(pady=5)

    def start_exam(self):
        if hasattr(self, 'get_login_status') and not self.get_login_status():
            messagebox.showerror("Login Required", "Please log in before starting the exam.")
            return

        chosen = self.selected_subject.get()
        if not chosen:
            messagebox.showwarning("No Selection", "Please select a subject to begin.")
            return

        messagebox.showinfo("Subject Selected", f"You chose {chosen}. Exam will begin...")

        # Trigger exam start if callback is defined
        if hasattr(self, 'start_exam_callback'):
            self.start_exam_callback(chosen)

    def view_leaderboard(self):
        chosen = self.selected_subject.get()
        if not chosen:
            messagebox.showwarning("No Subject", "Select a subject to view its leaderboard.")
            return

        LeaderboardWindow(self, chosen)
