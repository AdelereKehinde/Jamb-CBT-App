import tkinter as tk
from tkinter import messagebox, ttk
import requests
import random

BASE_URL = "http://127.0.0.1:8000"

class ExamWindow(tk.Toplevel):
    def __init__(self, parent, subject, username, base_url):
        super().__init__(parent)
        self.title(f"{subject} - Jamb CBT")
        self.geometry("900x600")
        self.configure(bg="white")
        self.subject = subject
        self.username = username
        self.base_url = base_url
        self.current_index = 0
        self.answers = {}
        self.questions = []
        self.remaining_time = 1200  # 20 minutes
        self.timer_running = False

        navbar = tk.Frame(self, bg="green", height=50)
        navbar.pack(fill="x")
        tk.Label(navbar, text="Jamb CBT Practice", fg="white", bg="green", font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=10)
        tk.Button(navbar, text="Usage Guide", command=self.open_usage_guide, bg="yellow").pack(side="left", padx=10)
        tk.Button(navbar, text="Calculator", command=self.open_calculator, bg="yellow").pack(side="left", padx=10)
        self.timer_label = tk.Label(navbar, text="20:00", font=("Arial", 12, "bold"), fg="white", bg="green")
        self.timer_label.pack(side="right", padx=20)

        tk.Label(self, text=f"{subject} - Jamb CBT", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        self.time_limit_label = tk.Label(self, text="", font=("Arial", 12), fg="black", bg="white")
        self.time_limit_label.pack()

        self.progress = tk.Canvas(self, height=10, bg="white", highlightthickness=0)
        self.progress.pack(fill="x", padx=40)

        self.question_label = tk.Label(self, text="", font=("Arial", 14), wraplength=700, bg="white")
        self.question_label.pack(pady=15)

        self.option_var = tk.StringVar()
        self.option_buttons = []
        self.option_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.option_frame.pack(pady=5, padx=50, fill="x")

        for option in ["A", "B", "C", "D"]:
            btn = tk.Radiobutton(self.option_frame, text="", variable=self.option_var, value=option,
                                 font=("Arial", 12), anchor="w", bg="white", wraplength=700)
            btn.pack(anchor="w", padx=20, pady=5)
            self.option_buttons.append(btn)

        nav_btns = tk.Frame(self, bg="white")
        nav_btns.pack(pady=10)
        tk.Button(nav_btns, text="Previous", command=self.prev_question, bg="red", fg="white", width=10).pack(side="left", padx=10)
        tk.Button(nav_btns, text="Next", command=self.next_question, bg="blue", fg="white", width=10).pack(side="left", padx=10)
        tk.Button(self, text="Submit Exam", command=self.submit_exam, bg="green", fg="white", width=20).pack(pady=10)

        self.load_questions()
        self.start_timer()

    def load_questions(self):
        try:
            response = requests.get(f"{self.base_url}/questions/{self.subject}")
            all_questions = response.json()
            if not all_questions:
                messagebox.showerror("No Questions", "No questions found for this subject.")
                self.destroy()
                return
            random.shuffle(all_questions)
            self.questions = all_questions[:20]
            self.display_question()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            self.destroy()

    def display_question(self):
        if 0 <= self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            self.question_label.config(
                text=f"Question {self.current_index + 1} of {len(self.questions)}\n\n{q['question']}"
            )
            selected_answer = self.answers.get(q["id"], "")
            self.option_var.set(selected_answer)

            options = q.get("options", {})


            for i, opt in enumerate(["A", "B", "C", "D"]):
                self.option_buttons[i].config(text=f"{opt}. {options.get(opt, '')}")

            self.progress.delete("bar")
            self.progress.update_idletasks()
            width = self.progress.winfo_width()
            percent = (self.current_index + 1) / len(self.questions)
            self.progress.create_rectangle(0, 0, percent * width, 10, fill="blue", tags="bar")
        else:
            messagebox.showinfo("End", "End of questions.")

    def save_answer(self):
        try:
            qid = self.questions[self.current_index]['id']
            selected = self.option_var.get()
            if selected:
                self.answers[qid] = selected
        except:
            pass

    def next_question(self):
        self.save_answer()
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.display_question()

    def prev_question(self):
        self.save_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.display_question()

    def submit_exam(self):
        self.save_answer()
        unanswered = [q['id'] for q in self.questions if q['id'] not in self.answers]
        if unanswered:
            if not messagebox.askyesno("Unanswered Questions", f"You have {len(unanswered)} unanswered questions. Submit anyway?"):
                return

        score = sum(1 for q in self.questions if self.answers.get(q["id"]) == q.get("correct_option"))

        try:
            res = requests.post(f"{self.base_url}/submit_score", json={
                "username": self.username,
                "subject": self.subject,
                "score": score,
                "time_taken": 1200 - self.remaining_time
            })
            if res.status_code == 200:
                result_text = f"You scored {score}/{len(self.questions)}.\n\nCorrect Answers:\n"
                for q in self.questions:
                    correct = q.get("correct_option")
                    result_text += f"\nQ: {q['question']}\nCorrect: {correct}\n"
                messagebox.showinfo("Submitted", result_text)
                self.destroy()
            else:
                messagebox.showerror("Error", res.text)
        except Exception as e:
            messagebox.showerror("Error", f"Submission failed: {e}")

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.winfo_exists():
            return
        if self.timer_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.time_limit_label.config(text=f"Time limit: {mins:02d}:{secs:02d}")
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.after(1000, self.update_timer)
            else:
                messagebox.showinfo("Time's Up", "Time is up! The exam will be submitted.")
                self.submit_exam()

    def pause_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def open_usage_guide(self):
        self.pause_timer()
        guide = tk.Toplevel(self)
        guide.title("Usage Guide")
        guide.geometry("400x250")
        guide_text = (
            "Welcome to the CBT Exam App!\n\n"
            "- Answer each question by selecting one option.\n"
            "- Use 'Next' and 'Previous' to navigate.\n"
            "- The timer counts down from 20 minutes.\n"
            "- Click 'Submit' to finish early.\n\n"
            "Good luck!"
        )
        tk.Label(guide, text=guide_text, font=("Arial", 12), justify="left", wraplength=380).pack(padx=10, pady=10)
        tk.Button(guide, text="Close", command=lambda: [guide.destroy(), self.resume_timer()]).pack(pady=10)

    def open_calculator(self):
        self.pause_timer()
        calc = tk.Toplevel(self)
        calc.title("Calculator")
        calc.geometry("390x497")
        calc.configure(bg="#e8f5e9")

        entry = tk.Entry(calc, width=16, font=("Arial", 24), bd=4, relief="ridge", justify="right")
        entry.pack(pady=10, padx=10, ipady=10)

        def click(val): entry.insert("end", val)
        def clear(): entry.delete(0, "end")
        def equals():
            try:
                result = eval(entry.get())
                entry.delete(0, "end")
                entry.insert("end", str(result))
            except:
                entry.delete(0, "end")
                entry.insert("end", "Error")

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+", "C"
        ]

        btn_frame = tk.Frame(calc, bg="#e8f5e9")
        btn_frame.pack()

        for i, text in enumerate(buttons):
            cmd = equals if text == "=" else clear if text == "C" else lambda val=text: click(val)
            tk.Button(btn_frame, text=text, width=5, height=2, font=("Arial", 16),
                      bg="#a5d6a7" if text.isdigit() or text == "." else "#81c784", command=cmd).grid(row=i//4, column=i%4, padx=3, pady=3)

        tk.Button(calc, text="Close Calculator", command=lambda: [calc.destroy(), self.resume_timer()],
                  bg="red", fg="white", font=("Arial", 12)).pack(pady=10)