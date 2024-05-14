from tkinter import *
from tkinter import ttk
from docxtpl import DocxTemplate
import datetime
import time
from tkinter import messagebox
import mysql.connector as sql

tk=Tk()
tk.geometry("1700x1000")
tk.config(bg="#F5F5F5")
tk.title("Delivery Slip Edit - Gayathri Tex")
tk.configure(bg='white')

mycon=sql.connect(host="localhost",user="root",passwd="Gayathri@2404",database="gtex_db")
cursor=mycon.cursor()

def clear_item():
    particulars_entry.delete(0,END)
    quantity_entry.delete(0,END)
    quantity_entry.insert(0, "0")
        
invoice_list = []
def add_item():
    particulars = particulars_entry.get()
    quantity = int(quantity_entry.get())
    invoice_item = [particulars, quantity]
    tree.insert('',0, values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item) 
    
def edit_invoice():
    inv_no = str(invoice_number_entry.get())
    show = ("SELECT * FROM delivery_slip WHERE delivery_slip_no = '{}'").format(inv_no)
    cursor.execute(show)
    data=cursor.fetchall()[0]
    
    print(data)  
    name_entry.insert(0,data[3])
    address_entry.insert(0,data[4])
    phone_number_entry.insert(0,data[5])
    gst_entry.insert(0,data[6])
        
    particulars = data[7].split(',')
    quantity = data[8].split(',')
    unit_price = data[9].split(',')
    line_total = data[10].split(',')
    
    for i in range(len(particulars)):
        invoice_item = [particulars[i], int(quantity[i])]
        tree.insert('',0, values=invoice_item)
        invoice_list.append(invoice_item)

def edit_selection():
   selected_item = tree.selection()[0]
   item = tree.item(selected_item)['values']
   
   particulars_entry.delete(0,END)
   particulars_entry.insert(0,item[0])
   quantity_entry.delete(0,END)
   quantity_entry.insert(0,int(item[1]))
      
    
Label(tk,text="GAYATHRI TEX - ERODE",font=("Arial", 20, "bold"),bg="white",fg="#1A374D").place(x=650,y=20)
Label(tk,text="Delivery Number : ",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=580,y=100)

invoice_number_entry = Entry(tk,font=("Arial", 12, "bold"),bd=3)
invoice_number_entry.place(x=730,y=100)

edit_button = Button(tk, text="Submit",font=("Arial", 10,"bold"),bg="#1A374D",fg="#F5F5F5",command=edit_invoice)
edit_button.place(x=930,y=97)

name_label = Label(tk, text="Name",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=260,y=150)
name_entry = Entry(tk,font=("Arial", 12),bd=3)
name_entry.place(x=190,y=180)

address_label = Label(tk, text="Address",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=560,y=150)
address_entry = Entry(tk,font=("Arial", 12),bd=3)
address_entry.place(x=500,y=180)

phone_number_label = Label(tk, text="Phone number",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=850,y=150)
phone_number_entry = Entry(tk,font=("Arial", 12),bd=3)
phone_number_entry.place(x=810,y=180)

gst_label = Label(tk, text="GST number",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1160,y=150)
gst_entry = Entry(tk,font=("Arial", 12),bd=3)
gst_entry.place(x=1110,y=180)

'''------- Product details -------'''

particulars_label = Label(tk, text="Particulars",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=550,y=230)
particulars_entry = Entry(tk,font=("Arial", 12),bd=3)
particulars_entry.place(x=500,y=260)

quantity_label = Label(tk, text="Quantity",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=870,y=230)
quantity_entry = Spinbox(tk, from_=1,to=100,font=("Arial", 12),bd=3)
quantity_entry.place(x=810,y=260)

add_item_button = Button(tk, text="Add item",font=("Arial", 10,"bold"),bg="#1A374D",fg="#F5F5F5",command=add_item)
add_item_button.place(x=1110,y=260)

columns = ('particulars', 'quantity')
tree = ttk.Treeview(tk, columns=columns, show="headings")
tree.heading('particulars', text='Particulars')
tree.heading('quantity', text='Quantity')
tree.place(x=580,y=330)

edit_btn = ttk.Button(tk,text="Edit", command=edit_selection)
edit_btn.place(x=900,y=570)

tk.mainloop()
