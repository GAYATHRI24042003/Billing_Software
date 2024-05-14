from tkinter import *
from tkinter import messagebox
from datetime import date, datetime
import mysql.connector as sql
from docxtpl import DocxTemplate
from docx2pdf import convert

tk = Tk()
tk.geometry("1250x720")
tk.config(bg="#F5F5F5")
tk.title("Expense Tracker - Gayathri Tex")
tk.configure(bg='white')

mycon = sql.connect(host="localhost", user="root", passwd="Gayathri@2404", database="gtex_db")
cursor = mycon.cursor()

def display_block():
    today = date.today()
    show = ("SELECT amount FROM accounts where date = '{date}'".format(date=today))
    cursor.execute(show)
    today_data = cursor.fetchall()

    today_balance_amount = 0.0
    today_from_account = 0.0
    today_to_account = 0.0
    for i in today_data:
        if(i[0] < 0):
            today_from_account += i[0]
        else:
            today_to_account += i[0]

    today_balance_amount = today_to_account + today_from_account
    if(today_from_account < 0):
        today_from_account *= (-1)

    month = date.today().month
    show = ("SELECT amount FROM accounts where month(date) = '{month}'".format(month=month))
    cursor.execute(show)
    month_data = cursor.fetchall()

    month_balance_amount = 0.0
    month_from_account = 0.0
    month_to_account = 0.0
    for i in month_data:
        if(i[0] < 0):
            month_from_account += i[0]
        else:
            month_to_account += i[0]

    month_balance_amount = month_to_account + month_from_account
    if(month_from_account < 0):
        month_from_account *= (-1)

    show = ("SELECT amount FROM accounts")
    cursor.execute(show)
    total_data = cursor.fetchall()

    total_balance_amount = 0.0
    total_from_account = 0.0
    total_to_account = 0.0
    for i in total_data:
        if(i[0] < 0):
            total_from_account += i[0]
        else:
            total_to_account += i[0]

    total_balance_amount = total_to_account + total_from_account
    if(total_from_account < 0):
        total_from_account *= (-1)

def generate_report():
    date1 = str(from_date_entry.get())
    date2 = str(to_date_entry.get())

    invoice_query = ("SELECT invoice.invoice_no, invoice.date, invoice_details.particulars, "
                     "invoice_details.quantity, invoice_details.unit_price, invoice_details.line_total "
                     "FROM invoice "
                     "INNER JOIN invoice_details ON invoice.invoice_no = invoice_details.invoice_no "
                     "WHERE invoice.date BETWEEN '{}' AND '{}'").format(date1, date2)

    cursor.execute(invoice_query)
    data = cursor.fetchall()

    open_balance_query = ("SELECT SUM(line_total) FROM invoice_details "
                          "WHERE invoice_no IN (SELECT invoice_no FROM invoice WHERE date < '{}')").format(date1)
    cursor.execute(open_balance_query)
    open_balance_row = cursor.fetchone()
    open_balance = float(open_balance_row[0]) if open_balance_row[0] is not None else 0.0

    close_balance_query = ("SELECT SUM(line_total) FROM invoice_details "
                           "WHERE invoice_no IN (SELECT invoice_no FROM invoice WHERE date <= '{}')").format(date2)
    cursor.execute(close_balance_query)
    close_balance_row = cursor.fetchone()
    close_balance = float(close_balance_row[0]) if close_balance_row[0] is not None else 0.0

    data_list = []
    total_from = 0.0
    total_to = 0.0
    for row in data:
        nest_list = list(row)
        try:
            quantity = float(nest_list[3])
        except ValueError:
            continue
        else:
            if quantity < 0:
                total_from += quantity * float(nest_list[4]) * (-1)
            else:
                total_to += quantity * float(nest_list[4])
            data_list.append(nest_list)

    doc = DocxTemplate("expence_template.docx")
    doc.render({"from_date": date1,
                "to_date": date2,
                "expence_list": data_list,
                "total_from": total_from,
                "total_to": total_to,
                "open_balance": open_balance,
                "close_balance": close_balance})

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    doc_name = "Expence_Report_{}_{}.docx".format(date1, timestamp)

    doc.save('E:/gtex_billing/Billing_Software/Expences Report/' + doc_name)

    convert('E:/gtex_billing/Billing_Software/Expences Report/' + doc_name)

    from_date_entry.delete(0, END)
    to_date_entry.delete(0, END)

    messagebox.showinfo("Success", "Report generated successfully!")

Label(tk, text="GAYATHRI TEX - ERODE", font=("Arial", 20, "bold"), bg="white", fg="#1A374D").place(x=440, y=20)

Label(tk, text="- - - - - Generate Report - - - - -", font=("Arial", 13, "bold"), bg="white", fg="#1A374D").place(x=500, y=200)
from_date_lable = Label(tk, text="From Date", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=440, y=240)
from_date_entry = Entry(tk, font=("Arial", 12), bd=3)
from_date_entry.place(x=390, y=280)

to_date_lable = Label(tk, text="To Date", font=("Arial", 12, "bold"), bg="white", fg="#1A374D").place(x=695, y=240)
to_date_entry = Entry(tk, font=("Arial", 12), bd=3)
to_date_entry.place(x=640, y=280)

generate_button = Button(tk, text="Generate Report", font=("Arial", 10, "bold"), bg="#1A374D", fg="#F5F5F5", width=50, command=generate_report)
generate_button.place(x=410, y=350)

display_block()
tk.mainloop()
