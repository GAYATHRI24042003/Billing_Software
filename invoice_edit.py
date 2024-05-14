from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as sql

tk = Tk()
tk.geometry("1250x720")
tk.config(bg="#F5F5F5")
tk.title("Invoice Edit - Gayathri Tex")
tk.configure(bg='white')

mycon = sql.connect(host="localhost", user="root", passwd="Gayathri@2404", database="gtex_db")
cursor = mycon.cursor()
edit_selected_item = ""

def clear_item():
    particulars_entry.delete(0, END)
    quantity_entry.delete(0, END)
    quantity_entry.insert(0, "0")
    price_entry.delete(0, END)
    price_entry.insert(0, "0.0")

invoice_list = []

def add_item():
    particulars = particulars_entry.get()
    quantity = int(quantity_entry.get())
    unit_price = float(price_entry.get())
    line_total = quantity * unit_price
    invoice_item = [particulars, quantity, unit_price, line_total]
    tree.insert('', 0, values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item)

    sub_total = sum(item[3] for item in invoice_list)
    stotal_entry.delete(0, END)
    stotal_entry.insert(0, sub_total)

    cgst_entry.delete(0, END)
    cgst_entry.insert(0, sub_total * 0.06)

    sgst_entry.delete(0, END)
    sgst_entry.insert(0, sub_total * 0.06)

    gtotal_entry.delete(0, END)
    gtotal_entry.insert(0, sub_total + sub_total * 0.18)

def edit_invoice():
    inv_no = str(invoice_number_entry.get())
    show = ("SELECT * FROM invoice INNER JOIN invoice_details ON invoice.invoice_no = invoice_details.invoice_no WHERE invoice.invoice_no = '{}'").format(inv_no)
    cursor.execute(show)
    data = cursor.fetchall()

    if data:
        name_entry.insert(0, data[0][3])
        if len(data[0]) >= 5:
            address_entry.insert(0, data[0][4])
        if len(data[0]) >= 6:
            phone_number_entry.insert(0, data[0][5])
        if len(data[0]) >= 7:
            gst_entry.insert(0, data[0][6])
        if len(data[0]) >= 12:
            stotal_entry.insert(0, data[0][11])
        if len(data[0]) >= 13:
            cgst_entry.insert(0, data[0][12])
        if len(data[0]) >= 14:
            sgst_entry.insert(0, data[0][13])
        if len(data[0]) >= 15:
            gtotal_entry.insert(0, data[0][14])

        for row in data:
            particulars = row[6]
            quantity = row[7]
            unit_price = row[8]
            line_total = row[9]
            gtotal=row[10] if len(row) > 10 else 0  # Check if the tuple has more than 10 elements
            invoice_item = [particulars, quantity, unit_price, line_total]
            tree.insert('', 0, values=invoice_item)
            invoice_list.append(invoice_item)
    else:
        messagebox.showerror("Error", "Invoice number not found")

def edit_selection():
    selected_item = tree.selection()[0]
    item = tree.item(selected_item)['values']

    particulars_entry.delete(0, END)
    particulars_entry.insert(0, item[0])
    quantity_entry.delete(0, END)
    quantity_entry.insert(0, int(item[1]))
    price_entry.delete(0, END)
    price_entry.insert(0, float(item[2]))

Label(tk, text="GAYATHRI TEX - ERODE", font=("Arial", 20, "bold"), bg="white", fg="#1A374D").place(x=400, y=20)
Label(tk, text="Invoice Number : ", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=350, y=100)

invoice_number_entry = Entry(tk, font=("Arial", 12, "bold"), bd=3)
invoice_number_entry.place(x=500, y=100)

edit_button = Button(tk, text="Submit", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", command=edit_invoice)
edit_button.place(x=750, y=97)

name_label = Label(tk, text="Name", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=160, y=150)
name_entry = Entry(tk, font=("Arial", 12), bd=3)
name_entry.place(x=90, y=180)

address_label = Label(tk, text="Address", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=460, y=150)
address_entry = Entry(tk, font=("Arial", 12), bd=3)
address_entry.place(x=400, y=180)

phone_number_label = Label(tk, text="Phone number", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=750, y=150)
phone_number_entry = Entry(tk, font=("Arial", 12), bd=3)
phone_number_entry.place(x=710, y=180)

gst_label = Label(tk, text="GST number", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=1060, y=150)
gst_entry = Entry(tk, font=("Arial", 12), bd=3)
gst_entry.place(x=1010, y=180)

particulars_label = Label(tk, text="Particulars", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=240, y=230)
particulars_entry = Entry(tk, font=("Arial", 12), bd=3)
particulars_entry.place(x=190, y=260)

quantity_label = Label(tk, text="Quantity", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=560, y=230)
quantity_entry = Spinbox(tk, from_=0, to=100, font=("Arial", 12), bd=3)
quantity_entry.place(x=500, y=260)

price_label = Label(tk, text="Unit Price", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=870, y=230)
price_entry = Spinbox(tk, from_=0.0, to=5000, increment=0.5, font=("Arial", 12), bd=3)
price_entry.place(x=810, y=260)

add_item_button = Button(tk, text="Add item", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", command=add_item)
add_item_button.place(x=1110, y=260)

columns = ('particulars', 'quantity', 'unit_price', 'amount')
tree = ttk.Treeview(tk, columns=columns, show="headings")
tree.heading('particulars', text='Particulars')
tree.heading('quantity', text='Quantity')
tree.heading('unit_price', text='Unit Price')
tree.heading('amount', text="Amount")
tree.place(x=120, y=350)

edit_btn = ttk.Button(tk, text="Edit", command=edit_selection)
edit_btn.place(x=850, y=580)

stotal_label = Label(tk, text="Sub Total : ", font=("Arial", 12), bg="white", fg="#1A374D").place(x=950, y=350)
stotal_entry = Entry(tk, font=("Arial", 12), bd=3)
stotal_entry.place(x=1060, y=350)
stotal_entry.insert(0, "0.0")

cgst_label = Label(tk, text="CGST @6% : ", font=("Arial", 12), bg="white", fg="#1A374D").place(x=950, y=400)
cgst_entry = Entry(tk, font=("Arial", 12), bd=3)
cgst_entry.place(x=1060, y=400)
cgst_entry.insert(0, "0.0")

sgst_label = Label(tk, text="SGST @6% : ", font=("Arial", 12), bg="white", fg="#1A374D").place(x=950, y=450)
sgst_entry = Entry(tk, font=("Arial", 12), bd=3)
sgst_entry.place(x=1060, y=450)
sgst_entry.insert(0, "0.0")

gtotal_label = Label(tk, text="Grand Total : ", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=950, y=500)
gtotal_entry = Entry(tk, font=("Arial", 12, "bold"), bd=3)
gtotal_entry.place(x=1060, y=500)
gtotal_entry.insert(0, "0.0")

tk.mainloop()
