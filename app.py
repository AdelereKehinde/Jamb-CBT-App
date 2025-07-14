import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from subjects import SubjectSelection
from tkinter import PhotoImage
from exam_window import ExamWindow
import threading


BASE_URL = "http://127.0.0.1:8000"  

root = tk.Tk()
root.geometry("600x500")
root.title("D' Royal School JAMB CBT App")
icon  = PhotoImage(file="school_logo.png")
root.iconphoto(True, icon)
root.configure(bg="yellow")
is_logged_in = False
current_user = None



frames = {}
frame_names = ("LoginPage", "RegisterPage", "HomePage", "UserGuidePage", "D' Royal Model school ")


for name in frame_names:
    frame = tk.Frame(root, bg="yellow")
    frame.place(x=0, y=50, relwidth=1, relheight=1)
    frames[name] = frame


navbar = tk.Frame(root, height=70, bg="green")
navbar.pack(fill="x")


logo_img = PhotoImage(file="school_logo.png")
logo_img = logo_img.subsample(9, 8)

logo_label = tk.Label(navbar, image=logo_img)
logo_label.image = logo_img

logo_label.pack(side="right",padx=50)

def raise_frame(frame_name):
    frames[frame_name].tkraise()

btn_login = tk.Button(navbar, text="Login", width=12, height=1, font=("Arial", 13, "bold"),bg="yellow" ,command=lambda: raise_frame("LoginPage"))
btn_register = tk.Button(navbar, text="Register", bg="yellow", width=12, height=1, font=("Arial", 13, "bold"),command=lambda: raise_frame("RegisterPage"))
btn_home = tk.Button(navbar, text="Home", bg="yellow",   width=12, height=1, font=("Arial", 13, "bold"),command=lambda: raise_frame("HomePage"))
btn_help = tk.Button(navbar, text="User Guide", bg="yellow",   width=12, height=1, font=("Arial", 13, "bold"),command=lambda: raise_frame("UserGuidePage"))
name = tk.Label(navbar, text="D' Royal Model secondary school", font=("Arial", 18, "bold"), bg="green", fg="white", borderwidth=0, highlightthickness=0)
def logout():
    global is_logged_in
    is_logged_in = False

    btn_logout.pack_forget()
    login_username.delete(0, tk.END)
    login_password.delete(0, tk.END)
    raise_frame("LoginPage")

btn_logout = tk.Button(navbar, text="Logout", bg="red", fg="white", width=12, height=1, font=("Arial", 13, "bold"), command=logout)
btn_logout.pack_forget() 


btn_login.pack(side="left", padx=10, pady=1)
btn_register.pack(side="left", padx=10, pady=1)
btn_home.pack(side="left", padx=10, pady=1)
btn_help.pack(side="left", padx=10, pady=1)
name.pack(side="right", padx=120)

guide_frame = frames["UserGuidePage"]
tk.Label(guide_frame, text="How to use the app", font=("Arial", 18, "bold"), bg="yellow").pack(pady=20)
tk.Label(guide_frame, text=(
    ''' 
    1. Click Register to create an account .

    2. After Registering, click 'Login'  and enter your credentials.

    3. ONCE logged in, select your subjectsand start the test.

    4. Use the built-in calculator if needed.

    5. Use the next and previouus button to change and Skip questions

    6. When done, smash on the Submit button  to view your score

    7. Visit the leaderboard to see top performances`

    8. Only registered Students can login

    9. Your history is saved under your Profile

    10. If misused you will be automatically deleted by the school Admin 
    '''
), bg="yellow" , font=("Arial", 15, "bold"), justify="left", anchor="w").pack(padx=20)

login_frame = frames["LoginPage"]

login_box = tk.Frame(login_frame, bg="green", bd=2, relief="groove")
login_box.place(relx=0.5, rely=0.3, anchor="center", width=400, height=230 )


tk.Label(login_box, text="Login", font=("Arial", 18, "bold"), bg="green", borderwidth=0, highlightthickness=0, fg="white").pack(pady=10)
tk.Label(login_box, text="Username", justify="left", bg="green", highlightthickness=0, borderwidth=0, fg="white", font=(8)).pack(pady=4)
login_username = ttk.Entry(login_box)
login_username.pack(padx=3, pady=8)


tk.Label(login_box, text="Password", justify="left" ,anchor="w", font=(8), fg="white", bg="green").pack()
login_password = ttk.Entry(login_box, show="*")
login_password.pack()
def login():
    global is_logged_in, current_user
    username = login_username.get()
    password = login_password.get()
    if not username or not password:
        messagebox.showwarning("Warning", "Please fill all fields")
        return
    try:
        response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        data = response.json()
        if response.status_code == 200:
            is_logged_in = True
            current_user = username
            messagebox.showinfo("Success", data["message"])
            btn_logout.pack(side="left", padx=10, pady=1)
            btn_login.pack_forget()
            btn_register.pack_forget()
            lbl_welcome.config(text=f"Welcome, {data['fullname']}")
            raise_frame("HomePage")
        else:
            messagebox.showerror("Error", data.get("detail", "Login failed"))
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("Error", f"Server error: {e}")
        threading.Thread(target=login).start()


tk.Button(login_box,  text="Login",  command=login, bg="yellow", bd=2, width=12).pack(pady=10)


register_frame = frames["RegisterPage"]
register_box = tk.Frame(register_frame, bg="green", bd=2, relief="groove", )
register_box.place(relx=0.5, rely=0.3, anchor="center", width=400, height=250)

tk.Label(register_box, text="Register", font=("Arial", 18, "bold"), bg="green", fg="white",highlightthickness=0, borderwidth=0).pack(pady=10)

tk.Label(register_box, text="Full Name: ", bg="green" ,fg="white", borderwidth=0, highlightthickness=0, font=(8)).pack(pady=4)

reg_fullname = ttk.Entry(register_box)
reg_fullname.pack()

tk.Label(register_box, text="Username: ", bg="green", fg="white", borderwidth=0, highlightthickness=0, font=(8)).pack(pady=4)
reg_username = ttk.Entry(register_box)
reg_username.pack()

tk.Label(register_box, text="Password: " ,bg="green", fg="white", borderwidth=0, highlightthickness=0, font=(8)).pack()
reg_password = ttk.Entry(register_box, show="*")
reg_password.pack()

def register():
    fullname = reg_fullname.get()
    username = reg_username.get()
    password = reg_password.get()
    if not fullname or not username or not password:
        messagebox.showwarning("Warning", "Please fill all fields")
        return
    try:
        response = requests.post(f"{BASE_URL}/register", json={"fullname": fullname, "username": username, "password": password})
        data = response.json()
        if response.status_code == 200:
            messagebox.showinfo("Success", data["message"])
            raise_frame("LoginPage")
        else:
            messagebox.showerror("Error", data.get("detail", "Registration failed"))
    except Exception as e:
        messagebox.showerror("Error", f"Server error: {e}")

tk.Button(register_box,  text="Register", command=register, bg="yellow" ,bd=2, width=12).pack(pady=10)

home_frame = frames["HomePage"]

lbl_welcome = tk.Label(home_frame, text="Welcome!", font=("Arial", 20) , highlightthickness=0, borderwidth=0)
lbl_welcome.pack(pady=10)


subject_frame = SubjectSelection(home_frame)
subject_frame.get_login_status = lambda: is_logged_in 
subject_frame.start_exam_callback = lambda subj: ExamWindow(root, subj, current_user, BASE_URL)
subject_frame.pack(pady=10, fill="both", expand=True)


tk.Button(home_frame, text="logout", command=logout).pack(pady=10)
raise_frame("LoginPage")

root.mainloop()