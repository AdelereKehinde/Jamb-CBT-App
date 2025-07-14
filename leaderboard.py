import tkinter as tk
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class LeaderboardWindow(tk.Toplevel):
    def __init__(self, parent, subject):
        super().__init__(parent)
        self.title(f"{subject} Leaderboard")
        self.geometry("600x500")
        self.configure(bg="#e8f5e9")  # Light green background

        try:
            response = requests.get(f"{BASE_URL}/leaderboard/{subject}")
            data = response.json()
            leaderboard = data.get("leaderboard", [])

            # Score as percentage and points logic
            for entry in leaderboard:
                raw_score = entry.get("score", 100)
                time_taken = entry.get("time_taken", 1800)

                percent_score = min(10, raw_score)
                entry["percentage"] = f"{percent_score}%" 

                # Simple points logic (score + time bonus)
                entry["points"] = percent_score + int((1800 - time_taken) / 60)

            leaderboard.sort(key=lambda x: x["points"], reverse=True)

            # Title
            tk.Label(self, text=f"{subject} Leaderboard", font=("Arial", 18, "bold"),
                     bg="#388e3c", fg="white", pady=10).pack(fill="x")

            # Table Header
            leadframe = tk.Frame(self, bg="yellow", width=15)
            leadframe.pack(padx=10)

            header_frame = tk.Frame(leadframe, bg="yellow", width="15")
            header_frame.pack(fill="x", pady=(10, 0))

            headers = ["#Rank", "Username", "Result", "Points", "Entered"]
            for i, h in enumerate(headers):
                tk.Label(header_frame, text=h, font=("Arial", 12, "bold"),
                         bg="yellow", fg="black", width=10, borderwidth=0, highlightthickness=0).grid(row=0, column=i, padx=1, pady=5)

            # Table Rows
            table_frame = tk.Frame(leadframe, bg="yellow" ,borderwidth=0, highlightthickness=0)
            table_frame.pack(fill="both", expand=True, padx=5)

            if not leaderboard:
                tk.Label(table_frame, text="No scores submitted yet.",
                         bg="white", font=("Arial", 12)).pack(pady=20)
            else:
                for i, entry in enumerate(leaderboard):
                    entered_time = entry.get("entered_on", "")
                    try:
                        entered_time = datetime.strptime(entered_time, "%Y-%m-%dT%H:%M").strftime("%b %d, %Y %H:%M")
                    except:
                        pass

                    row_data = [
                        f"{i + 1}",
                        entry.get("username", ""),
                        entry.get("percentage", "10%"),
                        f"{entry.get('points', 0)}",
                        entered_time
                    ]

                    for j, value in enumerate(row_data):
                        tk.Label(table_frame, text=value, font=("Arial", 11, "bold"),
                                 bg="yellow", width=10, anchor="center", borderwidth=0,highlightthickness=0, relief="solid").grid(row=i, column=j, padx=1, pady=2)

        except Exception as e:
            tk.Label(self, text=f"Error loading leaderboard: {e}",
                     bg="white", fg="red", font=("Arial", 12)).pack(pady=20)

        # Go Back Button
        tk.Button(self, text="Go Back", command=self.destroy,
                  bg="green", fg="white", font=("Arial", 12, "bold"),
                  relief="raised").pack(pady=20)
