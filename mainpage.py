from tkinter import *

tk=Tk()
tk.geometry("1250x720")
tk.title("Home Page - GAYATHRI Tex")
tk.configure(bg='white')

def invoice():
    import invoice
    
def delivery_slip():
    import delivery_slip

def expence_tracker():
    import expence_tracker
    
a = Label(tk,text="GAYATHRI TEX - ERODE",font=("Arial", 30, "bold"),bg="white",fg="#1A374D").place(x=400,y=20)
bt1 = Button(tk,text="INVOICE",font=("Arial",15),bg="#1A374D",fg="#F5F5F5",height=5,width=20,command=invoice).place(x=300,y=180)
bt2 = Button(tk,text="DELIVERY SLIP",font=("Arial",15),bg="#1A374D",fg="#F5F5F5",height=5,width=20,command=delivery_slip).place(x=750,y=180)
bt3 = Button(tk,text="EXPENSE TRACKER & REPORT",font=("Arial",15),bg="#1A374D",fg="#F5F5F5",height=5,width=30,command=expence_tracker).place(x=460,y=425)

tk.mainloop()
