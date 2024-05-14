from tkinter import *
from tkinter import ttk
from docxtpl import DocxTemplate
import datetime
import time
from tkinter import messagebox
import mysql.connector as sql
from docx2pdf import convert  # Importing convert function from docx2pdf

tk = Tk()
tk.geometry("1250x720")
tk.config(bg="#F5F5F5")
tk.title("Invoice - Gayathri Tex")
tk.configure(bg='white')

mycon = sql.connect(host="localhost", user="root", passwd="Gayathri@2404", database="gtex_db")
cursor = mycon.cursor()

show = ("SELECT COUNT(*) FROM invoice")
cursor.execute(show)
invoice_no = cursor.fetchall()
invoice_no = int(invoice_no[0][0]) + 1

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
    tree.insert('', 'end', values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item) 
    
    update_totals()
    
def update_totals():
    sub_total = sum(item[3] for item in invoice_list)
    cgst = sub_total * 0.06
    sgst = sub_total * 0.06
    grand_total = sub_total + cgst + sgst
    
    stotal_entry.delete(0, END)
    stotal_entry.insert(0, sub_total)
    
    cgst_entry.delete(0, END)
    cgst_entry.insert(0, cgst)
    
    sgst_entry.delete(0, END)
    sgst_entry.insert(0, sgst)
    
    gtotal_entry.delete(0, END)
    gtotal_entry.insert(0, grand_total)

def generate_invoice():
    doc = DocxTemplate("invoice_template.docx")
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_number_entry.get()
    gst = gst_entry.get()
    inno = "IN-2425-{number:06}".format(number=invoice_no)
    current_date = datetime.date.today()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    subtotal = sum(item[3] for item in invoice_list)
    cgst = subtotal * 0.06
    sgst = subtotal * 0.06
    gtotal = subtotal + cgst + sgst
        
    doc.render({"name": name,
                "address": address,
                "phone": phone,
                "gst": gst,
                "invoiceno": inno,
                "invoicedate": current_date,
                "invoicetime": current_time,
                "invoice_list": invoice_list,
                "subtotal": subtotal,
                "cgst": cgst,
                "sgst": sgst,
                "gtotal": gtotal})
    
    particulars_data = []
    quantity_data = []
    price_data = []
    amount_data = []
    
    for item in invoice_list:
        particulars_data.append(item[0])
        quantity_data.append(item[1])
        price_data.append(item[2])
        amount_data.append(item[3])
    
    insert_invoice = ("INSERT INTO invoice (invoice_no, date, time, grand_total) "
                      "VALUES (%s, %s, %s, %s)")
    invoice_data = (inno, current_date, current_time, gtotal)
    cursor.execute(insert_invoice, invoice_data)
    
    insert_details = ("INSERT INTO invoice_details (invoice_no, particulars, quantity, unit_price, line_total) "
                      "VALUES (%s, %s, %s, %s, %s)")
    details_data = [(inno, particulars_data[i], quantity_data[i], price_data[i], amount_data[i]) 
                    for i in range(len(invoice_list))]
    cursor.executemany(insert_details, details_data)
    
    mycon.commit()         
           
    doc_name = "IN-2425-{number:06}".format(number=invoice_no) + ".docx"
    doc_path = 'E:/gtex_billing/Billing_Software/Invoices/' + doc_name
    doc.save(doc_path)
    
    convert(doc_path)
    
    messagebox.showinfo("Invoice Complete", "Invoice Complete")
    clear_cells()
    
def clear_cells():
    name_entry.delete(0, END)
    address_entry.delete(0, END)
    phone_number_entry.delete(0, END)
    gst_entry.delete(0, END)
    tree.delete(*tree.get_children())  # Clearing all rows in the treeview
    clear_item()
    update_totals()
    
def new_invoice():
    name_entry.delete(0, END)
    address_entry.delete(0, END)
    phone_number_entry.delete(0, END)
    gst_entry.delete(0, END)
    
    for item in tree.get_children():
        tree.delete(item)
        
    clear_item()
    update_totals()

def edit_invoice():
    import invoice_edit
    
Label(tk, text="GAYATHRI TEX - ERODE", font=("Arial", 20, "bold"), bg="white", fg="#1A374D").place(x=400, y=20)
Label(tk, text="Invoice Number : IN-2425-{number:06}".format(number=invoice_no), font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=940, y=20)

'''------- Buyer details -------'''
name_label = Label(tk, text="Name", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=120, y=100)
name_entry = Entry(tk, font=("Arial", 12), bd=3)
name_entry.place(x=50, y=130)

address_label = Label(tk, text="Address", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=440, y=100)
address_entry = Entry(tk, font=("Arial", 12), bd=3)
address_entry.place(x=375, y=130)

phone_number_label = Label(tk, text="Phone number", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=740, y=100)
phone_number_entry = Entry(tk, font=("Arial", 12), bd=3)
phone_number_entry.place(x=700, y=130)

gst_label = Label(tk, text="GST number", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=1068, y=100)
gst_entry = Entry(tk, font=("Arial", 12), bd=3)
gst_entry.place(x=1025, y=130)

'''------- Product details -------'''
particulars_label = Label(tk, text="Particulars", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=240, y=180)
particulars_entry = Entry(tk, font=("Arial", 12), bd=3)
particulars_entry.place(x=190, y=210)

quantity_label = Label(tk, text="Quantity", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=560, y=180)
quantity_entry = Spinbox(tk, from_=0, to=100, font=("Arial", 12), bd=3)
quantity_entry.place(x=500, y=210)

price_label = Label(tk, text="Unit Price", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=870, y=180)
price_entry = Spinbox(tk, from_=0.0, to=5000, increment=0.5, font=("Arial", 12), bd=3)
price_entry.place(x=810, y=210)

add_item_button = Button(tk, text="Add item", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", command=add_item)
add_item_button.place(x=1110, y=210)

columns = ('particulars', 'quantity', 'unit_price', 'amount')
tree = ttk.Treeview(tk, columns=columns, show="headings")
tree.heading('particulars', text='Particulars')
tree.heading('quantity', text='Quantity')
tree.heading('unit_price', text='Unit Price')
tree.heading('amount', text="Amount")
tree.place(x=190, y=280)

stotal_label = Label(tk, text="Sub Total : ", font=("Arial", 12), bg="white", fg="#1A374D").place(x=1020, y=300)
stotal_entry = Entry(tk, font=("Arial", 12), bd=3)
stotal_entry.place(x=1130, y=300)
stotal_entry.insert(0, "0.0")

cgst_label = Label(tk, text="CGST @6% : ", font=("Arial", 12), bg="white", fg="#1A374D").place(x=1020, y=350)
cgst_entry = Entry(tk, font=("Arial", 12), bd=3)
cgst_entry.place(x=1130, y=350)
cgst_entry.insert(0, "0.0")

sgst_label = Label(tk, text="SGST @6% : ", font=("Arial", 12), bg="white", fg="#1A374D").place(x=1020, y=400)
sgst_entry = Entry(tk, font=("Arial", 12), bd=3)
sgst_entry.place(x=1130, y=400)
sgst_entry.insert(0, "0.0")

gtotal_label = Label(tk, text="Grand Total : ", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=1020, y=500)
gtotal_entry = Entry(tk, font=("Arial", 12, "bold"), bd=3)
gtotal_entry.place(x=1130, y=500)
gtotal_entry.insert(0, "0.0")

save_invoice_button = Button(tk, text="Generate Invoice", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", width=30, height=2, command=generate_invoice)
save_invoice_button.place(x=250, y=560)

new_invoice_button = Button(tk, text="New Invoice", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", width=30, height=2, command=new_invoice)
new_invoice_button.place(x=500, y=560)

edit_invoice_button = Button(tk, text="Edit Invoice", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", width=30, height=2, command=edit_invoice)
edit_invoice_button.place(x=750, y=560)

tk.mainloop()
