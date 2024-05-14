from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

def login():
    en1 = c1.get()
    en2 = d1.get()
    
    if en1 == "gtexerode" and en2 == "gtexadmin123":
        tk.destroy()
        import mainpage
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")
tk = Tk()
tk.geometry("1250x720")
tk.config(bg="#F5F5F5")
tk.title("GAYATHRI Tex - Erode")
tk.configure(bg='white')

# Load the background image and resize it using LANCZOS filter
background_image = Image.open("E:/gtex_billing/main.png")
background_image = background_image.resize((1280, 720), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas to display the background image
canvas = Canvas(tk, width=1280, height=720)
canvas.pack(fill="both", expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, image=background_photo, anchor="nw")

a = Label(tk, text="GAYATHRI TEX - ERODE", font=("Arial", 30, "bold"), bg="white", fg="#1A374D")
a.place(x=400, y=20)

b = Label(tk, text="LOGIN", font=("Arial", 20, "bold"), bg="white", fg="#1A374D")
b.place(x=600, y=130)

c = Label(tk, text="USERNAME", font=("Arial", 20), bg="white", fg="#1A374D")
c.place(x=575, y=250)

c1 = Entry(tk, font=("Calibri", 18), bd=5, justify="center")
c1.place(x=530, y=300)

d = Label(tk, text="PASSWORD", font=("Arial", 20), bg="white", fg="#1A374D")
d.place(x=575, y=400)

d1 = Entry(tk, font=("Calibri", 18), show="*", bd=5, justify="center")
d1.place(x=530, y=450)

bt1 = Button(tk, text="LOGIN", font=("Arial", 15), bg="#1A374D", fg="#F5F5F5", width=10, height=1, command=login)
bt1.place(x=600, y=550)

tk.mainloop()
