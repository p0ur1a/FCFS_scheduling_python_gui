import operator
import tkinter as tk
from statistics import mean

# defines window
root = tk.Tk()

# set size for window
root.geometry("800x400")

# set title for window
root.title('FCFS')


# A node which holds process attributes including arrivalTime, serviceTime, turnaroundTime, finishTime, tr/ts
class Fcfs_process:
    turnaround_time = 0
    finish_time = 0
    trts = 0

    def __init__(self, arrival_time, service_time, process_name):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.process_name = process_name


# gets number of processes from user
def get_NOP():

    global NO_P, offset_gui, NOP_gui

    # entry for number of processes
    NO_P_label = tk.Label(root, text='number of processess: ', font=(
        'calibre', 10)).grid(column=0, row=offset_gui, padx=(10, 0), pady=25)
    NO_P_entry = tk.Entry(root, textvariable=NOP_gui,
                          font=('calibre', 10, 'normal'), width=5)
    NO_P_entry.grid(column=1, row=offset_gui, padx=20)

    # submiting the entry
    sub_btn = tk.Button(root, text='submit', command=lambda: sub_btn1(
        sub_btn, NO_P_entry), bg='#adc4bb', font=('calibre', 9, 'bold'))
    sub_btn.grid(row=offset_gui, column=3, padx=20)

    # contents have been grided in this line, so we move on
    offset_gui = offset_gui_up(offset_gui, 1)


# changes row
def offset_gui_up(fun_offset_gui, n):
    fun_offset_gui += n
    return fun_offset_gui


# at this point user have entered number of processes, so we should now get arrival and service time from them
def sub_btn1(fun_sub_btn: tk.Button, fun_NP_entry: tk.Entry):

    global offset_gui

    # prevents new changes from user
    fun_sub_btn.grid_forget()
    fun_NP_entry.config(state='disabled')

    try:

        # passes the entry from gui to program for further computations
        n = int(NOP_gui.get())
        error_label.grid_forget()

    except ValueError:

        # checks if the entry is a valid integer. if it's not then removes everything and asks for new valid entry
        for widget in root.winfo_children():
            if widget is not error_label:
                widget.destroy()
        error_label.grid(column=4, row=0, padx=10)
        offset_gui = 0
        get_NOP()
        return

    # these arrays store arrival time and service time of processes given by user to the program
    arrival_arr = []
    service_arr = []

    get_arv_srv(arrival_arr, service_arr, n)


# gets arrival and service time from user in GUI
def get_arv_srv(fun_arv_arr, fun_srv_arr, number_of_process):
    global offset_gui

    for i in range(number_of_process):

        # GUI variable for getting arrival and service time from user
        arrival_gui = tk.StringVar()
        service_gui = tk.StringVar()

        # shows which process is user intracting with
        process_label = tk.Label(root, text='process #%s :' % (
            i+1), font=('calibre', 9, 'bold')).grid(row=offset_gui + i, column=0)

        # entry for arrival time in GUI
        arrival_label = tk.Label(root, text='Arrival time: ', font=(
            'calibre', 9, 'bold')).grid(row=offset_gui + i, column=1)
        arrival_entry = tk.Entry(
            root, textvariable=arrival_gui, font=('calibre', 9, 'bold'), width=5)
        arrival_entry.grid(row=offset_gui + i, column=2, padx=8)

        # entry for service time in GUI
        service_label = tk.Label(root, text='service time: ', font=(
            'calibre', 9, 'bold')).grid(row=offset_gui + i, column=3)
        service_entry = tk.Entry(
            root, textvariable=service_gui, font=('calibre', 9, 'bold'), width=5)
        service_entry.grid(row=offset_gui + i, column=4, padx=8)

        # appends user inputs to an array for further computations
        fun_arv_arr.append(arrival_entry)
        fun_srv_arr.append(service_entry)

    # increase target row as much as number of processes
    offset_gui = offset_gui_up(offset_gui, number_of_process)

    # submit button for arrival and service time entries
    as_btn = tk.Button(root, command=lambda: sub_btn2(
        as_btn, fun_arv_arr, fun_srv_arr), text='submit', bg='#adc4bb', font=('calibre', 9, 'bold'))
    as_btn.grid(row=offset_gui, column=6, padx=10)

    # one more line for submit button
    offset_gui = offset_gui_up(offset_gui, 1)


# user has enterd arrival time and service time of processes. now we can calculate the other attributes
def sub_btn2(fun_sub_btn2: tk.Button, fun_arrival_arr, fun_service_arr):

    global offset_gui

    # first index is for average turnaround time and the 2nd one is for average tr/ts time
    mean = [0, 0]

    process_full_attr(fun_arrival_arr, fun_service_arr, queue, mean)

    # removes submit button to prevent new changes
    fun_sub_btn2.grid_forget()

    # these three functions show the final table on GUI
    table_titles()
    table_process_attr(queue)
    table_mean(mean, len(queue)+1)
    credits()


# calculates rest of process attributes such as finish time, turnaround time, tr/ts and the averages
def process_full_attr(fun_arrival_arr, fun_service_arr, fun_queue, fun_mean):
    global offset_gui

    # empties queue from values in the past
    fun_queue.clear()

    # length of arrival_arr is equal to length of sevice_arr so it makes no diffrence on which one to use
    for i in range(len(fun_arrival_arr)):

        try:

            # makes process node by getting the value stored in entries
            fun_queue.append(Fcfs_process(int(fun_arrival_arr[i].get(
            )), int(fun_service_arr[i].get()), 'process #%s' % (i+1)))
            error_label.grid_forget()

        except ValueError:

            # checks if the entry is a valid integer. if it's not then removes everything and asks for new valid entry
            for widget in root.winfo_children():
                if widget is not error_label:
                    widget.destroy()
            error_label.grid(column=4, row=0, padx=10)
            offset_gui = 0
            get_NOP()
            return

        # disables entries for new input
        fun_arrival_arr[i].config(state='disabled')
        fun_service_arr[i].config(state='disabled')

    # the program is not real-time so we must sort the processes by arrival time
    fun_queue.sort(key=operator.attrgetter('arrival_time'))

    time = 0
    for i in range(len(fun_queue)):

        # if there was spare time, the time variable will be equal to the first arrival time in queue
        if fun_queue[i].arrival_time > time:
            time = fun_queue[i].arrival_time

        # process attributes calculation
        fun_queue[i].finish_time = time + fun_queue[i].service_time
        fun_queue[i].turnaround_time = fun_queue[i].finish_time - \
            fun_queue[i].arrival_time
        fun_queue[i].trts = round(
            fun_queue[i].turnaround_time / fun_queue[i].service_time, 2)
        time = fun_queue[i].finish_time

    # calculates average of turnaround times and tr/tsS
    fun_mean[0] = round(
        mean([process.turnaround_time for process in queue]), 2)
    fun_mean[1] = round(mean([process.trts for process in queue]), 2)


# shows table titles on GUI
def table_titles():
    global offset_gui

    final_title_labels = ['Process', 'Arrival Time',
                          'Service Time (Ts)', 'Finish Time', 'Turnaround Time (Tr)', 'Tr/Ts']
    space_label = tk.Label(root).grid(row=offset_gui)
    offset_gui = offset_gui_up(offset_gui, 1)
    for i in range(len(final_title_labels)):
        final_label = tk.Label(
            root, text=final_title_labels[i], bg='#edc16f', width=23, borderwidth=1, relief='solid')
        final_label.grid(column=0, row=offset_gui + i, padx=(10, 0))


# shows process attribues on GUI
def table_process_attr(fun_queue):

    global offset_gui

    for i in range(len(fun_queue)):
        process_name_label = tk.Label(root, text=fun_queue[i].process_name, bg='#9ff28f', width=12, borderwidth=1, relief='solid').grid(
            column=(i+1), row=offset_gui)
        process_arvtime_label = tk.Label(root, text=fun_queue[i].arrival_time, bg='#9ff28f', width=12, borderwidth=1, relief='solid').grid(
            column=(i+1), row=offset_gui + 1)
        process_srvtime_label = tk.Label(root, text=fun_queue[i].service_time, bg='#9ff28f', width=12, borderwidth=1, relief='solid').grid(
            column=(i+1), row=offset_gui + 2)
        process_finishtime_label = tk.Label(root, text=fun_queue[i].finish_time, bg='#9ff28f', width=12, borderwidth=1, relief='solid').grid(
            column=(i+1), row=offset_gui + 3)
        process_trtime_label = tk.Label(root, text=fun_queue[i].turnaround_time, bg='#9ff28f', width=12, borderwidth=1, relief='solid').grid(
            column=(i+1), row=offset_gui + 4)
        process_TrTs_label = tk.Label(root, text=fun_queue[i].trts, bg='#9ff28f', width=12, borderwidth=1, relief='solid').grid(
            column=(i+1), row=offset_gui + 5)


# shows average values on GUI
def table_mean(fun_mean, coloumn_number):
    global offset_gui

    for i in range(6):
        label_text = ''

        if i == 0:
            label_text = 'mean'
        elif i == 4:
            label_text = str(fun_mean[0])
        elif i == 5:
            label_text = str(fun_mean[1])

        mean_values = tk.Label(root, text=label_text, bg='#F38B8B', width=10, borderwidth=1, relief='solid', font='Helvetica 9 bold').grid(
            column=coloumn_number, row=offset_gui+i)

    offset_gui = offset_gui_up(offset_gui, 6)


# credits
def credits():

    global offset_gui
    text = 'Pouria Bahri : 9729843\nMohammadParsa Hosni : 9733613'
    credit_label = tk.Label(root, text=text, borderwidth=0.5, relief='solid', font=('calibre', 7)).grid(
        row=offset_gui, column=0, padx=10, pady=20)


# main queue for FCFS scheduling
queue = []

# NOP -> number of processes   NOP_gui -> a value for storing entry from GUI
NO_P = 0
NOP_gui = tk.StringVar()

# this variable references to the row that the widget should grid on
offset_gui = 0

# error label which reminds user to inpupt only integers
error_label = tk.Label(root, text='ENTRY MUST BE A NUMBER',
                       font=('calibre', 12, 'bold'), fg='red')

get_NOP()

# program ends here
root.mainloop()
