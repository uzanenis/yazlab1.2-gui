import concurrent.futures
import tkinter
from tkinter import *
from tkinter import ttk
import csv
from csv import reader
import os
import time
import pandas as pandas


def remove_blank_lines():
    with open('stop_last.csv', 'r', encoding="utf8") as file:
        lines = file.readlines()
        with open('newData_stop_blank.csv', 'w', encoding="utf8") as data:
            for line in lines:
                if line.strip():
                    data.write(line)

    print("Done")


def delete_cant_word():
    my_word = "CAN'T"
    with open('newData_stop_blank.csv', 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        with open('last.csv', 'w', encoding="utf8") as data:
            cols = ['product', 'issue', 'company', 'state', 'complaint_id', 'zip_code']
            writer = csv.DictWriter(data, fieldnames=cols)
            for line in reader:
                company = line['company']
                if my_word in company:
                    company = company.replace(my_word, "")
                    line['company'] = company
                writer.writerow(line)
    print("Done")


"""def remove_stopwords():
    with open('clean_data.csv', 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        with open('stop_last.csv', 'w', encoding="utf8") as data:
            cols = ['product', 'issue', 'company', 'state', 'complaint_id', 'zip_code']
            writer = csv.DictWriter(data, fieldnames=cols)
            my_words = ['cant', 'and', 'didnt', 'wasnt', 'for', 'into', 'of', 'other', 'the', 'we', 'your', 'our', 'to',
                        'at', 'in', 'on', 'not', 'cannot', 'now', 'by', 'it', 'was']
            for line in reader:
                # print("line: ", line)
                product = line['product']
                issue = line['issue']
                company = line['company']
                state = line['state']
                complaint_id = line['complaint_id']
                zip_code = line['zip_code']
                product = product.split()
                issue = issue.split()
                company = company.split()
                state = state.split()
                complaint_id = complaint_id.split()
                zip_code = zip_code.split()
                stop_words = set(stopwords.words('english'))
                product = [w for w in product if not w in stop_words]
                issue = [w for w in issue if not w in stop_words]
                company = [w for w in company if not w in stop_words]
                state = [w for w in state if not w in stop_words]
                complaint_id = [w for w in complaint_id if not w in stop_words]
                zip_code = [w for w in zip_code if not w in stop_words]
                for word in product:
                    if word.lower() in my_words:
                        product.remove(word)
                for word in issue:
                    if word.lower() in my_words:
                        issue.remove(word)
                for word in company:
                    if word.lower() in my_words:
                        company.remove(word)
                print(issue)
                product = ' '.join(product)
                issue = ' '.join(issue)
                company = ' '.join(company)
                state = ' '.join(state)
                complaint_id = ' '.join(complaint_id)
                zip_code = ' '.join(zip_code)
                line['product'] = product.capitalize()
                line['issue'] = issue.capitalize()
                line['company'] = company.capitalize()
                line['state'] = state.capitalize()
                line['complaint_id'] = complaint_id.capitalize()
                line['zip_code'] = zip_code.capitalize()
                writer.writerow(line)
    print("Done")"""


def get_main_columns():
    with open('rows.csv', 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)

        with open('data.csv', 'w', encoding="utf8") as data:
            cols = ['Product', 'Issue', 'Company', 'State', 'Complaint ID', 'ZIP code']
            writer = csv.DictWriter(data, fieldnames=cols)

            for line in reader:
                del line['Date received']
                del line['Sub-product']
                del line['Sub-issue']
                del line['Consumer complaint narrative']
                del line['Company public response']
                del line['Tags']
                del line['Consumer consent provided?']
                del line['Submitted via']
                del line['Date sent to company']
                del line['Company response to consumer']
                del line['Timely response?']
                del line['Consumer disputed?']
                writer.writerow(line)

            print("Done")


def get_bigger_count(first, second):
    first = first.split()
    second = second.split()
    first_count = len(first)
    second_count = len(second)
    if first_count > second_count:
        return first_count
    return second_count


def get_same_words_count(first, second):
    first = first.split()
    second = second.split()
    count = 0
    for word in first:
        if word in second:
            count += 1
    return count


def get_records_similarity_rate(str1, str2):
    bigger_count = get_bigger_count(str1, str2)
    same_word_count = get_same_words_count(str1, str2)
    similarity_rate_percent = (same_word_count / bigger_count) * 100
    return "% " + str(similarity_rate_percent)


selectedDisplay = []
searchCount = 0


def divide_rows_per_thread(thread_count, rate, selected_display, selected_filter, selectedString, stringFilterStatus):
    print("Dividing rows per thread")
    csv_file = csv.reader(open('test.csv', 'r', encoding="utf8"))
    row_count = sum(1 for _ in csv_file)
    print("Row count: ", row_count)
    rows_per_thread = int(row_count / thread_count)
    print("Rows per thread: ", rows_per_thread)

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        for i in range(thread_count):
            start = i * rows_per_thread
            end = start + rows_per_thread
            executor.submit(thread_similarity_rate, start, end, i, rate, selected_display, selected_filter,
                            selectedString, stringFilterStatus)


def thread_similarity_rate(start, end, thread_number, rate, selected_display, selected_filter, selected_string,
                           stringFilterStatus):
    print("Start: ", start)
    print("End: ", end)
    print("Thread number: ", thread_number + 1)
    print("\n\n")
    csvFile = pandas.read_csv('test.csv')
    ListValues = ["product", "issue", "company", "state", "complaint_id", "zip_code"]
    flag = False
    start_time = time.time()
    for i in range(start, end):
        for j in range(i + 1, len(csvFile)):
            similarity_rate = get_records_similarity_rate(csvFile[selected_filter][i], csvFile[selected_filter][j])
            similarity_rate = float(similarity_rate.replace("% ", "").replace(" ", ""))
            if similarity_rate >= rate:
                with open('records/similarity_rate/thread_' + str(thread_number + 1) + '.csv', 'a',
                          encoding="utf-8") as data:
                    for k in range(0, len(ListValues)):
                        if stringFilterStatus == 'true':
                            if csvFile[selected_string['name']][i] == selected_string['detail']:
                                flag = True
                                data.write(str(csvFile[ListValues[k]][i]) + ', ' + str(
                                    csvFile[ListValues[k]][j]) + ',' + str(similarity_rate) + '\n')
                            else:
                                flag = False
                        else:
                            if k == 0:
                                data.write("1. Kayit,")
                            data.write(str(csvFile[ListValues[k]][i]) + ',')

                            if k == len(ListValues) - 1:
                                data.write("2. Kayit,")
                                for m in range(0, len(ListValues)):
                                    data.write(str(csvFile[ListValues[m]][j]) + ',')
                                data.write(str(similarity_rate) + "\n")
                    if flag:
                        data.write("\n")
            else:
                pass
    end_time = time.time()
    print("Thread -> " + str(thread_number + 1) + " suresi ", end_time - start_time)


def appendCsvFiles():
    file_path = r"C:\Users\Enis\PycharmProjects\Yazlab1.2\records\similarity_rate"
    # list all the files from the directory
    file_list = os.listdir(file_path)
    print(file_list)
    # df_concat = pandas.concat([pandas.read_csv("C:\\Users\\Enis\\PycharmProjects\\pythonProject1\\records\similarity_rate\\" + f) for f in file_list], ignore_index=True)
    for f in file_list:
        df_concat = pandas.concat(
            [pandas.read_csv("C:\\Users\\Enis\\PycharmProjects\\Yazlab1.2\\records\similarity_rate\\" + f)],
            ignore_index=True)
        df_concat.to_csv('master.csv', mode='a', header=False, index=False)


def main():
    # appendCsvFiles()

    def openNewWindow():
        newWindow = Toplevel(window)
        newWindow.title("New")
        newFrame = tkinter.Frame(newWindow)
        newFrame.pack()
        treeview_frame = tkinter.LabelFrame(newFrame, text="Treeview")
        treeview_frame.grid(row=0, column=0, padx=20, pady=10)
        tv = ttk.Treeview(treeview_frame, show="headings", height=40)
        columns = ["1. Kayit"]
        # Treeview for csv
        displaySelectedItems = displayListbox_select.curselection()
        for i in range(0, len(displaySelectedItems)):
            columns.append(displayListbox_select.get(displaySelectedItems[i]) + "1")
            # tv.heading(i + 1, text=displayListbox_select.get(displaySelectedItems[i]))
        columns.append("2. Kayit")
        for i in range(0, len(displaySelectedItems)):
            columns.append(displayListbox_select.get(displaySelectedItems[i]))
        columns.append("Benzerlik Orani")
        print(columns)
        tv["columns"] = columns
        for i in columns:
            tv.column(i, width=100, anchor='c')
        for i in columns:
            tv.heading(i, text=i)
        tv.grid(row=0, column=0)

        # open file in read mode
        with open('master.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            r_set = [row for row in csv_reader]
            v = ["1. Kayit"]
            v2 = ["2. Kayit"]
            v3 = []
            v4 = []
            for index, data in enumerate(r_set):
                if len(displaySelectedItems) > 1:
                    for i in range(0, len(displaySelectedItems)):
                        v.append(data[displaySelectedItems[i] + 1])
                        v2.append(data[displaySelectedItems[i] + 1])
                        if i == len(displaySelectedItems) - 1:
                            v2.append(data[14])
                else:
                    v.append(data[displaySelectedItems[0] + 1])
                # print("v:", v)
                # print("\n")
                v3.extend(v)
                v3.extend(v2)
                tv.insert('', 'end', values=v3)
                v3.clear()
                v.clear()
                v2.clear()
                v.append("1. Kayit")
                v2.append("2. Kayit")
                # print(row)
        for widget2 in treeview_frame.winfo_children():
            widget2.grid_configure(padx=10, pady=5)

    def insertListbox():
        ListValues = ["Product", "Issue", "Company", "State", "Complaint ID", "Zip Code"]
        for item in ListValues:
            filterListbox_select.insert(END, item)
        for item in ListValues:
            displayListbox_select.insert(END, item)
        for item in ListValues:
            stringFilterListbox_select.insert(END, item)

    def button_command():
        threshold_value = threshold_value_entry.get()
        thread_count = thread_count_entry.get()
        stringFilterValue = stringFilter_value_entry.get()
        filterSelectedItems = filterListbox_select.curselection()
        print("Filtrelenmesi istenen columnlar")
        for item in filterSelectedItems:
            selectedFilter = filterListbox_select.get(item).lower().replace(" ", "_")
        displaySelectedItems = displayListbox_select.curselection()
        print("Gosterilmesi istenen columnlar")
        for item2 in displaySelectedItems:
            selectedDisplay.append(displayListbox_select.get(item2).lower().replace(" ", "_"))
        print("selected", selectedDisplay)
        print("Threshold Value:" + threshold_value + " Thread Count:" + thread_count)
        # String Filter Varsa
        selectedString = {}
        stringFilterStatus = reg_status_var.get()
        stringFilterSelectedItems = stringFilterListbox_select.curselection()
        if stringFilterStatus == "true":
            for item3 in stringFilterSelectedItems:
                selectedStringFilter = stringFilterListbox_select.get(item3).lower().replace(" ", "_")
            selectedString = {
                'name': selectedStringFilter,
                'detail': stringFilterValue,
            }
        print(selectedString)
        divide_rows_per_thread(int(thread_count), int(threshold_value), selectedDisplay, selectedFilter, selectedString,
                               stringFilterStatus)

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
    filterListbox_select = tkinter.Listbox(requirements_frame, selectmode=MULTIPLE, exportselection=0, width=11,
                                           height=5,
                                           font=('calibri', 15))
    filterListbox_label.grid(row=2, column=0)
    filterListbox_select.grid(row=3, column=0)

    displayListbox_label = tkinter.Label(requirements_frame, text="Gosterilecek Columnlar")
    displayListbox_select = tkinter.Listbox(requirements_frame, selectmode=MULTIPLE, exportselection=0, width=11,
                                            height=5,
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

    stringFilterListbox_label = tkinter.Label(courses_frame, text="İsme Göre Filtre Columnlar")
    stringFilterListbox_select = tkinter.Listbox(courses_frame, selectmode=MULTIPLE, exportselection=0, width=11,
                                                 height=5,
                                                 font=('calibri', 15))
    stringFilterListbox_label.grid(row=2, column=0)
    stringFilterListbox_select.grid(row=3, column=0)

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


if __name__ == "__main__":
    main()
