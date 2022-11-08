import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv
from csv import reader
import os
import pandas as pd

"""def import_csv():
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open csv", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(fln) as myfile:
        csvread = csv.reader(myfile, delimiter=",")
        for i in csvread:
            mydata.append(i)
        update(mydata)"""


def openNewWindow():
    newWindow = Toplevel(window)
    newWindow.title("New")
    newFrame = tkinter.Frame(newWindow)
    newFrame.pack()
    treeview_frame = tkinter.LabelFrame(newFrame, text="Treeview")
    treeview_frame.grid(row=0, column=0, padx=20, pady=10)
    tv = ttk.Treeview(treeview_frame, show="headings", height=10)
    columns = []
    # Treeview for csv
    displaySelectedItems = displayListbox_select.curselection()
    for i in range(0, len(displaySelectedItems)):
        columns.append(displayListbox_select.get(displaySelectedItems[i]))
        # tv.heading(i + 1, text=displayListbox_select.get(displaySelectedItems[i]))
    print(columns)
    tv["columns"] = columns
    for i in columns:
        tv.column(i, width=500, anchor='c')
    for i in columns:
        tv.heading(i, text=i)
    tv.grid(row=0, column=0)

    # open file in read mode
    with open('1.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        r_set = [row for row in csv_reader]
        v = []
        for data in r_set:
            if len(displaySelectedItems) > 1:
                for i in range(0, len(displaySelectedItems)):
                    v.append(data[displaySelectedItems[i]])
            else:
                v.append(data[displaySelectedItems[0]])
            print("v:", v)
            print("\n")
            tv.insert('', 'end', values=v)
            v.clear()
            # print(row)
    for widget2 in treeview_frame.winfo_children():
        widget2.grid_configure(padx=10, pady=5)


def insertListbox():
    ListValues = ["Product", "Issue", "Company", "State", "Complaint ID", "Zip Code"]
    for item in ListValues:
        filterListbox_select.insert(END, item)
    for item in ListValues:
        displayListbox_select.insert(END, item)


def button_command():
    threshold_value = threshold_value_entry.get()
    thread_count = thread_count_entry.get()
    stringFilterValue = stringFilter_value_entry.get()
    print("Threshold Value:" + threshold_value + " Thread Count:" + thread_count)
    filterSelectedItems = filterListbox_select.curselection()
    displaySelectedItems = displayListbox_select.curselection()
    print("Filtrelenmesi istenen columnlar")
    for item in filterSelectedItems:
        print(filterListbox_select.get(item).lower())
    print("Gosterilmesi istenen columnlar")
    for item2 in displaySelectedItems:
        print(displayListbox_select.get(item2).lower())
    # String Filter Varsa
    stringFilterStatus = reg_status_var.get()
    if stringFilterStatus == "true":
        print("Filtrelenecek String", stringFilterValue)
    return None


window = tkinter.Tk()
window.title("Yazlab 1.2")

frame = tkinter.Frame(window)
frame.pack()

requirements_frame = tkinter.LabelFrame(frame, text="Requirements")
requirements_frame.grid(row=1, column=0, padx=20, pady=10)

threshold_value_label = tkinter.Label(requirements_frame, text="Threshold Value")
threshold_value_label.grid(row=0, column=0)
thread_count_label = tkinter.Label(requirements_frame, text="Thread Count")
thread_count_label.grid(row=0, column=1)

threshold_value_entry = tkinter.Entry(requirements_frame)
thread_count_entry = tkinter.Entry(requirements_frame)
threshold_value_entry.grid(row=1, column=0)
thread_count_entry.grid(row=1, column=1)

filterListbox_label = tkinter.Label(requirements_frame, text="Filtrelenecek Columnlar")
filterListbox_select = tkinter.Listbox(requirements_frame, selectmode=MULTIPLE, exportselection=0, width=11, height=5,
                                       font=('calibri', 15))
filterListbox_label.grid(row=2, column=0)
filterListbox_select.grid(row=3, column=0)

displayListbox_label = tkinter.Label(requirements_frame, text="Gosterilecek Columnlar")
displayListbox_select = tkinter.Listbox(requirements_frame, selectmode=MULTIPLE, exportselection=0, width=11, height=5,
                                        font=('calibri', 15))
displayListbox_label.grid(row=2, column=1)
displayListbox_select.grid(row=3, column=1)

for widget in requirements_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(courses_frame, text="String Filtreleme")

reg_status_var = tkinter.StringVar(value="false")
registered_check = tkinter.Checkbutton(courses_frame, text="İsme göre filtrele",
                                       variable=reg_status_var, onvalue="true", offvalue="false")

registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

stringFilter_value_label = tkinter.Label(courses_frame, text="Filtrelenecek String")
stringFilter_value_label.grid(row=0, column=1)

stringFilter_value_entry = tkinter.Entry(courses_frame)
stringFilter_value_entry.grid(row=1, column=1)

"""numcourses_label = tkinter.Label(courses_frame, text="# Completed Courses")
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(courses_frame, text="# Semesters")
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to="infinity")
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)"""

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button1 = tkinter.Button(frame, text="Start", command=button_command)
button1.grid(row=3, column=0, sticky="news", padx=20, pady=10)

button2 = tkinter.Button(frame, text="New Window", command=openNewWindow)
button2.grid(row=4, column=0, sticky="news", padx=20, pady=10)

insertListbox()
window.mainloop()
