import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
import datetime
import random
import math
import functions



class my_colors:
    silver = '#C0C0C0'
    light_blue = "#9FAFCA"
    black = "#191516"
    dark_blue = '#0E387A'


class ACPS_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (login_interface, home_page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("login_interface")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# ==============================================LOGIN INTERFACE=========================================================


class login_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=c.light_blue)
        self.controller = controller
        self.controller.title("Parking Lot Portal")
        self.controller.state("zoomed")
        self.controller.iconphoto(True, tk.PhotoImage(file='parking-area.png'))
        self.bg = tk.PhotoImage(file="park-3.png")
        self.admin_name = StringVar()
        self.admin_pass = StringVar()
        self.login_widgets()

    def login(self):
        name = self.admin_name.get()
        password = self.admin_pass.get()
        if a_obj.login_check(name, password):
            global login_det
            login_det = {'username': name, 'password': password}
            self.reset()
            self.controller.show_frame('home_page')
        else:
            messagebox.showerror("Login System", "Authentication Failed!")


    def reset(self):
        self.admin_name.set("")
        self.admin_pass.set("")
        self.admin_name_ent.focus()

    def exit(self):
        exit_stuff = messagebox.askyesno("Login System", "Are you sure you want to exit?")
        if exit_stuff > 0:
            self.controller.destroy()
        else:
            self.reset()

    def login_widgets(self):
        self.lbl = Label(self, image=self.bg)
        self.lbl.place(x=0, y=0)
        # ========================================Frames=====================================================
        self.empty_frame = Frame(self)
        self.empty_frame.pack(pady=150)

        self.headerframe = Frame(self, bg=c.light_blue, relief='ridge', bd=10)
        self.headerframe.pack(pady=20)

        self.topframe = Frame(self, bg=c.silver, width=1350, height=600,
                              relief='ridge', bd=8)
        self.topframe.pack()

        self.bottomframe = Frame(self, bg=c.light_blue, width=1000, height=600,
                                 relief='ridge', bd=8)
        self.bottomframe.pack(pady=20)

        # =======================================Labels and Entry=======================================================

        self.login_header = Label(self.headerframe, text='CITY PARKING LOT LOGIN', font='Arial 50 bold',
                                  bg=c.light_blue, fg=c.black)
        self.login_header.pack(pady=5, padx=100)

        self.admin_name_lbl = Label(self.topframe, text='USERNAME: ', font='Arial 22 bold',
                                    bd=15, bg=c.silver, fg=c.black)
        self.admin_name_lbl.grid(row=0, column=0)

        self.admin_name_ent = Entry(self.topframe, font='Arial 22 bold', relief='sunken',
                                    width=34, bd=6, textvariable=self.admin_name)
        self.admin_name_ent.focus()
        self.admin_name_ent.grid(row=0, column=1, pady=16, padx=20)

        self.admin_pass_lbl = Label(self.topframe, text='PASSWORD: ', font='Arial 20 bold',
                                    bd=15, bg=c.silver, fg=c.black)
        self.admin_pass_lbl.grid(row=1, column=0)

        self.admin_pass_ent = Entry(self.topframe, font='Arial 22 bold',
                                    relief='sunken', bd=6, show='*', width=34,
                                    textvariable=self.admin_pass)
        self.admin_pass_ent.grid(row=1, column=1, columnspan=2, pady=16, padx=20)

        # ==========================================Buttons==================================================

        self.submit_bt = Button(self.bottomframe, text='Log In', width=17,
                                font='Arial 16 bold', command=self.login)
        self.submit_bt.grid(row=0, column=0, pady=6, padx=4)

        self.reset_bt = Button(self.bottomframe, text='Reset', width=17,
                               font='Arial 16 bold', command=self.reset)
        self.reset_bt.grid(row=0, column=1, pady=6, padx=4, )

        self.exit_bt = Button(self.bottomframe, text='Exit', width=17,
                              font='Arial 16 bold', command=self.exit)
        self.exit_bt.grid(row=0, column=2, pady=6, padx=4)

        # self.incorrect_pass = Label(self, text="",
        #                             font='Courier 24 bold', bg=c.light_blue,
        #                             )
        # self.incorrect_pass.pack(pady=5)


# ==========================================HOMEPAGE===============================================

class home_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=c.light_blue)
        self.controller = controller
        self.controller.state("zoomed")
        self.slots = a_obj.load_slots()
        self.all_cars = a_obj.all_cars()
        global fee
        fee = a_obj.get_fee()
        self.checkbox = list(self.slots['all_slots'])
        self.checkboxVar = list(self.slots['all_slots'])
        self.park_plate_num = StringVar()
        self.exit_plate_num = StringVar()
        self.home_widgets()
        self.check_button()

    def generate_slot(self):
        rand_idx = random.randint(0, len(self.slots['available_slots'])-1)
        random_slot = self.slots['available_slots'][rand_idx]
        return random_slot

    def slot_update(self, slot):
        a_obj.update_slot(slot)

    def park_slot(self, slot):
        idx = self.slots["all_slots"].index(slot)
        self.checkboxVar[idx].set(True)

    def exit_slot(self, slot):
        idx = self.slots["all_slots"].index(slot)
        self.checkboxVar[idx].set(False)

    def park_car(self):
        plate = self.park_plate_num.get()
        if self.slots['available_slots']:
            if self.check_car(plate):
                slot = self.generate_slot()
                self.slot_update(slot)
                if a_obj.park_lot(plate, slot, datetime.datetime.now()):
                    self.emptylbl1.config(text=f"Assigned to slot {slot}", fg=c.black)
                    self.park_slot(slot)
                    self.slot_frame.config(text=f'PARKING SLOTS: {self.refresh_av_slots()}')
                else:
                    messagebox.showerror("Info", "Park Unsuccessful Try Again or Restart application!")
            else:
                self.emptylbl1.config(text="Car is parked!", fg=c.black)
        else:
            self.emptylbl1.config(text="Parking Lot Full!", fg=c.black)

    def park_reset(self):
        self.park_plate_num.set("")
        self.emptylbl1.config(text="")

    def exit_reset(self):
        self.exit_plate_num.set("")
        self.emptylbl2.config(text="")

    def check_car(self, plate):
        self.all_cars = {}
        self.all_cars = a_obj.all_cars()
        if plate in self.all_cars['parked_cars']:
            return False
        else:
            return True

    def log_check(self, plate):
        self.all_cars = {}
        self.all_cars = a_obj.all_cars()
        if plate in self.all_cars['exited_cars']:
            return True
        else:
            return False

    @staticmethod
    def calc_time(entry_time):
        global exit_time
        exit_time = datetime.datetime.now()
        time_diff = exit_time - entry_time
        time_spent = int(math.ceil(time_diff.total_seconds()/3600))
        return time_spent

    def calc_fee(self, time_spent):
        bill = time_spent * float(fee)
        return bill

    def display_fee(self, bill):
        self.emptylbl2.config(text=f"Bill is N{bill}", fg=c.black)

    def exit_car(self):
        self.slots = {}
        self.slots = a_obj.load_slots()
        plate = self.exit_plate_num.get()
        if self.log_check(plate):
            slot = a_obj.get_slot(plate)
            if a_obj.exit_lot(plate, slot):
                self.exit_slot(slot)
                self.update_label()
                self.emptylbl2.config(text="Exit Successful! Collect Receipt")
                # print receipt
            else:
                messagebox.showerror("Info", "Exit Unsuccessful Try Again or Restart application!")
        else:
            messagebox.showinfo("Info", "Bill has not been paid!")

    def exit_bill(self):
        self.slots = {}
        self.slots = a_obj.load_slots()
        plate = self.exit_plate_num.get()
        if self.check_car(plate):
            self.emptylbl2.config(text="Car is not parked", fg=c.black)
        else:
            ent = datetime.datetime.strptime(a_obj.car_entry_time(plate), '%Y-%m-%d %H:%M:%S.%f')
            hrs = self.calc_time(ent)
            amt = self.calc_fee(hrs)
            slot = a_obj.get_slot(plate)
            data = (plate, slot, ent, exit_time, hrs, amt)
            self.display_fee(amt)
            a_obj.log_exit(data)

    def refresh_av_slots(self):
        self.slots = {}
        self.slots = a_obj.load_slots()
        return len(self.slots['available_slots'])

    def update_label(self):
        self.slot_frame.config(text=f'PARKING SLOTS: {self.refresh_av_slots()}')



# ===============================================OPEN WINDOWS===========================================================
    def search_window(self):
        self.search_frame = search_page(self.controller)
        self.search_frame.grab_set()

    def config_window(self):
        self.config_frame = config_slot(self.controller)
        self.config_frame.grab_set()

    def parked_window(self):
        self.parked_frame = park_log(self.controller)
        self.parked_frame.grab_set()

    def history_window(self):
        self.history_frame = history(self.controller)
        self.history_frame.grab_set()

    def fee_window(self):
        self.fee_frame = change_fee(self.controller)
        self.fee_frame.grab_set()

    def close(self):
        self.close = messagebox.askyesno("Login System", "Are you sure you want to log out?")
        if self.close > 0:
            self.controller.show_frame('login_interface')
        else:
            pass

    def home_widgets(self):

        # ========================================Frames=====================================================
        self.top = Frame(self, bg=c.silver, bd=15, relief='ridge')
        self.top.pack(side=TOP, pady=30)

        self.outer_frame = Frame(self, bg=c.light_blue, bd=0, relief='ridge')
        self.outer_frame.pack(padx=20, pady=10)

        self.menu_frame = Frame(self.outer_frame, bg=c.light_blue, bd=10, relief='ridge')
        self.menu_frame.grid(row=0, column=0, columnspan=2, sticky=N)

        self.slot_frame = LabelFrame(self.outer_frame, bg=c.light_blue,
                                     text=f'PARKING SLOTS: {self.refresh_av_slots()}',
                                     font='Arial 20 bold', fg=c.black, bd=6)
        self.slot_frame.grid(row=1, column=0, sticky=N)

        self.opt_frame = Frame(self.outer_frame, bg=c.light_blue, bd=0, relief='ridge')
        self.opt_frame.grid(row=1, column=1, sticky=NE)

        self.fee_frame = Frame(self.opt_frame, bg=c.silver, bd=8, relief='ridge')
        self.fee_frame.grid(row=0, column=0)

        self.park_frame = Frame(self.opt_frame, bg=c.silver, bd=8, relief='ridge')
        self.park_frame.grid(row=1, column=0)

        self.exit_frame = Frame(self.opt_frame, bg=c.silver, bd=8, relief='ridge')
        self.exit_frame.grid(row=2, column=0)

        # ======================================Labels=====================================================
        self.label_1 = Label(self.top, text='CITY PARKING LOT PORTAL', bd=10,
                             font='Arial 45 bold', bg=c.silver, fg=c.dark_blue, justify=CENTER)
        self.label_1.grid(row=0, column=0, padx=200)

        # ==========================================Buttons==================================================

        self.park_bt = Button(self.menu_frame, text='Search Cars', width=21, height=1, bg=c.light_blue,
                              highlightcolor=c.dark_blue, font='Arial 16 bold',
                              command=self.search_window)
        self.park_bt.grid(row=0, column=0)

        self.ex_bt = Button(self.menu_frame, text='Configure Slot', width=21, height=1,
                            highlightcolor=c.dark_blue, bg=c.light_blue, font='Arial 16 bold',
                            command=self.config_window)
        self.ex_bt.grid(row=0, column=1)

        self.reg_bt = Button(self.menu_frame, text='View All Parked Cars', width=21, height=1,
                             highlightcolor=c.dark_blue, bg=c.light_blue, font='Arial 16 bold',
                             command=self.parked_window)
        self.reg_bt.grid(row=0, column=2)

        self.hist_bt = Button(self.menu_frame, text='View Today\'s Exited Cars', width=21, height=1,
                              highlightcolor=c.dark_blue, bg=c.light_blue, font='Arial 16 bold',
                              command=self.history_window)
        self.hist_bt.grid(row=0, column=3)

        self.logout_bt = Button(self.menu_frame, text='Admin LOGOUT', width=21, height=1,
                                highlightcolor=c.dark_blue, bg=c.light_blue, font='Arial 16 bold',
                                command=self.close)
        self.logout_bt.grid(row=0, column=4)

        c_row = 0
        c_col = 0
        for i in range(len(self.slots['all_slots'])):
            c_col += 1
            self.checkboxVar[i] = BooleanVar()
            self.checkbox[i] = Checkbutton(self.slot_frame, text=self.slots['all_slots'][i],
                                           variable=self.checkboxVar[i],
                                           font='Arial 16 bold', disabledforeground=c.black,
                                           bg=c.light_blue, state="disabled")
            self.checkbox[i].grid(row=c_row, column=c_col, sticky=W, padx=21)
            if c_col == 9:
                c_row += 1
                c_col = 0

    def check_button(self):
        for i in range(len(self.slots['all_slots'])):
            if self.slots['all_slots'][i] in self.slots['available_slots']:
                self.checkboxVar[i].set(False)
            else:
                self.checkboxVar[i].set(True)

        # ===================================PARK========================================================
        # ====================================Labels=======================================================
        self.park_lbl = Label(self.park_frame, text="PARK CAR", fg=c.dark_blue, bg=c.silver,
                              font='Arial 18 bold')
        self.park_lbl.grid(row=0, column=0, columnspan=2, padx=6, pady=10)

        self.park_plate_lbl = Label(self.park_frame, text="Plate No: ", bg=c.silver, font='Arial 16 bold')
        self.park_plate_lbl.grid(row=1, column=0, padx=8, pady=8)

        # ===================================Entry and buttons=============================================
        self.park_plate = Entry(self.park_frame, font="Arial 18 italic", bd=4, textvariable=self.park_plate_num)
        self.park_plate.grid(row=1, column=1, padx=8, pady=8)

        self.emptylbl1 = Label(self.park_frame, text="", bg=c.silver, font='Arial 16 italic')
        self.emptylbl1.grid(row=2, column=0, columnspan=2)

        self.park_bt = Button(self.park_frame, text="Park", bg=c.light_blue, font="Arial 16 bold",
                              width=7, command=self.park_car)
        self.park_bt.grid(row=3, column=0, pady=10, padx=2, sticky=E)
        self.park_reset_bt = Button(self.park_frame, text="Reset", bg=c.light_blue, font="Arial 16 bold",
                                    width=7, command=self.park_reset)
        self.park_reset_bt.grid(row=3, column=1, pady=10, padx=2, sticky=W)
        # ====================================EXIT=====================================================
        # ====================================Labels=======================================================

        self.exit_lbl = Label(self.exit_frame, text="EXIT CAR", fg=c.dark_blue, bg=c.silver,
                              font='Arial 18 bold')
        self.exit_lbl.grid(row=0, column=0, columnspan=3, padx=6, pady=10)

        self.exit_plate_lbl = Label(self.exit_frame, text="Plate No: ", bg=c.silver,
                                    font='Arial 16 bold')
        self.exit_plate_lbl.grid(row=1, column=0, padx=8, pady=8)

        # ===================================EXIT Entry & buttons=============================================
        self.exit_plate = Entry(self.exit_frame, font="Arial 18 italic", bd=4, textvariable=self.exit_plate_num)
        self.exit_plate.grid(row=1, column=1, columnspan=2, padx=8, pady=8)

        self.emptylbl2 = Label(self.exit_frame, text="", bg=c.silver, font='Arial 16 italic')
        self.emptylbl2.grid(row=2, column=0, columnspan=3)

        self.exit_bt_frame = Frame(self.exit_frame, bg=c.silver)
        self.exit_bt_frame.grid(row=3, column=0, columnspan=3)

        self.exit_bt = Button(self.exit_bt_frame, text="Exit", bg=c.light_blue, font="Arial 16 bold", width=9,
                            command=self.exit_car)
        self.exit_bt.grid(row=0, column=0, pady=6, padx=2)

        self.exit_reset_bt = Button(self.exit_bt_frame, text="Reset", bg=c.light_blue, font="Arial 16 bold", width=9,
                                    command=self.exit_reset)
        self.exit_reset_bt.grid(row=0, column=1, pady=6, padx=2)

        self.bill_bt = Button(self.exit_bt_frame, text="Pay Bill", bg=c.light_blue, width=9,
                              font="Arial 16 bold", command=self.exit_bill)
        self.bill_bt.grid(row=0, column=2, pady=6, padx=2)

        #============================================FEE=====================================================


        self.fee_lbl2 = Label(self.fee_frame, text=f'Parking Fee is N{fee} per hour', font="Arial 16 normal", bg=c.silver)
        self.fee_lbl2.grid(row=0, column=0, padx=54, pady=2)

        self.fee_bt = Button(self.fee_frame, text='Change Fee', font="Arial 16 bold", bg=c.light_blue, width=10, command=self.fee_window)
        self.fee_bt.grid(row=1, column=0, columnspan=2, padx=62, pady=15)

# ==============================================SEARCH BAR=========================================================

class search_page(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, bg=c.light_blue)
        self.plate_num = StringVar()
        self.bg = tk.PhotoImage(file="park-4.png")
        self.search_widgets()
        self.plate_ent.focus()

    def search_func(self):
        self.table_reset()
        self.emptylbl.config(text="")
        data = a_obj.gen_search(self.plate_num.get())

        def search_display():
            if data[1]:
                self.emptylbl.config(text="Car is currently parked")
            else:
                if not data[0]:
                    self.emptylbl.config(text="Car not found...")
        search_display()
        i = 1
        for a in data[1]:
            self.result_table.insert("", tk.END, values=(i, a[0], "--", "--", "--", a[1]))
            i += 1
        for b in data[0]:
            self.result_table.insert("", tk.END, values=(i, b[0], b[1], b[2], b[3], b[4]))
            i += 1

    def search_reset(self):
        self.plate_num.set("")
        self.emptylbl.config(text="")
        self.table_reset()

    def table_reset(self):
        for item in self.result_table.get_children():
            self.result_table.delete(item)


    def search_widgets(self):
        self.lbl = Label(self, image=self.bg)
        self.lbl.place(x=0, y=0)


        self.headframe = Frame(self, bg=c.light_blue, relief='ridge', bd=6)
        self.headframe.grid(row=0, column=0, columnspan=5, pady=40)

        self.empty_frame = Frame(self)
        self.empty_frame.grid(row=1, column=0, pady=10)

        self.frame2 = Frame(self, bg=c.silver, relief='ridge', bd=8)
        self.frame2.grid(row=2, column=0, padx=30, sticky=W)

        self.resultframe = Frame(self, bg=c.light_blue, relief='ridge', bd=8)
        self.resultframe.grid(row=3, column=0, padx=30, pady=25, columnspan=5)

        self.headlbl = Label(self.headframe, text='SEARCH', bg=c.light_blue,
                             fg=c.dark_blue, font='Arial 40 bold')
        self.headlbl.grid(row=0, column=0, padx=90, pady=5)

        self.platelbl = Label(self.frame2, text='Plate No: ', bg=c.silver,
                              font='Arial 16 bold')
        self.platelbl.grid(row=0, column=0, padx=3, pady=10)

        self.plate_ent = Entry(self.frame2,
                               font='Arial 16 bold', bd=4, textvariable=self.plate_num)
        self.plate_ent.grid(row=0, column=1, padx=6, pady=10)

        self.emptylbl = Label(self.frame2, font='Arial 16 italic', text="", bg=c.silver)
        self.emptylbl.grid(row=1, column=0, columnspan=2)

        self.plate_bt = Button(self.frame2, text='Search', bg=c.light_blue,
                               font='Arial 16 bold', width=10, command=self.search_func)
        self.plate_bt.grid(row=2, column=0, padx=4, pady=10, sticky=E)

        self.plate_reset_bt = Button(self.frame2, text='Reset', bg=c.light_blue,
                                     font='Arial 16 bold', width=10, command=self.search_reset)
        self.plate_reset_bt.grid(row=2, column=1, padx=4, pady=10, sticky=W)

        # scroll bar
        self.scroll_x = ttk.Scrollbar(self.resultframe, orient=HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.resultframe, orient=VERTICAL)

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                             font=('Calibri', 16))  # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 20, 'bold'))

        self.columns = ('sn', 't_in', 't_out', 'total_time', 'amt', 'p_slot')

        self.result_table = ttk.Treeview(self.resultframe,
                                         style="mystyle.Treeview",
                                         columns=self.columns,
                                         show='headings',
                                         xscrollcommand=self.scroll_x.set,
                                         yscrollcommand=self.scroll_y.set)
        self.result_table.column("sn", anchor=CENTER, stretch=NO, width=50)
        self.result_table.heading('sn', text='S/N')
        self.result_table.column("t_in", anchor=CENTER, stretch=NO, width=400)
        self.result_table.heading('t_in', text='Time In')
        self.result_table.column("t_out", anchor=CENTER, stretch=NO, width=400)
        self.result_table.heading('t_out', text='Time Out')
        self.result_table.column("total_time", anchor=CENTER, stretch=NO, width=150)
        self.result_table.heading('total_time', text='Time Spent')
        self.result_table.column("amt", anchor=CENTER, stretch=NO, width=200)
        self.result_table.heading('amt', text='Amount Paid')
        self.result_table.column("p_slot", anchor=CENTER, stretch=NO, width=200)
        self.result_table.heading('p_slot', text='Parking Slot')

        self.result_table.grid(row=0, column=0, sticky='nsew')
        self.scroll_x.grid(row=1, column=0, sticky='ew')
        self.scroll_y.grid(row=0, column=1, sticky='ns')
        self.scroll_y.config(command=self.result_table.yview)
        self.scroll_x.config(command=self.result_table.xview)

# =====================================Configure SLOTS=================================================

class config_slot(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent, bg=c.light_blue)
        self.slots = {}
        self.slots = a_obj.load_slots()
        self.slot_num = StringVar()
        self.config_widgets()
        self.slot_ent.focus()

    def disable_reset(self):
        self.slot_num.set("")
        self.emptylbl.config(text="")

    def add_slot(self):
        slot = self.slot_num.get()
        action = "add"
        if a_obj.config_slot(action, slot):
            self.emptylbl.config(text=f"Slot {slot} had been added!\nRestart Application before parking")
        else:
            self.emptylbl.config(text=f"Slot {slot} already exists")

    def dis_slot(self):
        slot_no = int(self.slot_num.get())
        action = "dis"
        if a_obj.check_slot(slot_no):
            if a_obj.config_slot(action, slot_no):
                self.emptylbl.config(text=f"Slot {slot_no} has been disabled\nRestart Application before parking")
            else:
                self.emptylbl.config(text=f"Slot {slot_no} is occupied. Try again Later")
        else:
            self.emptylbl.config(text=f"Slot {slot_no} does not exist")

    def en_slot(self):
        slot_no = int(self.slot_num.get())
        action = "en"
        if a_obj.check_slot(slot_no):
            if a_obj.config_slot(action, slot_no):
                self.emptylbl.config(text=f"Slot {slot_no} has been enabled\nRestart Application before parking")
            else:
                self.emptylbl.config(text=f"Something is wrong. Try again Later")
        else:
            self.emptylbl.config(text=f"Slot {slot_no} does not exist")

    def del_slot(self):
        slot_no = int(self.slot_num.get())
        action = "del"
        if a_obj.check_slot(slot_no):
            if a_obj.config_slot(action, slot_no):
                self.emptylbl.config(text=f"Slot {slot_no} has been deleted\nRestart Application before parking")
            else:
                self.emptylbl.config(text=f"Slot {slot_no} is occupied. Try again Later")
        else:
            self.emptylbl.config(text=f"Slot {slot_no} does not exist")





    def config_widgets(self):
        self.mainframe = Frame(self, bg=c.silver, bd=12, relief='ridge')
        self.mainframe.pack(side=TOP)

        self.frame1 = Frame(self.mainframe, bg=c.silver)
        self.frame1.pack(side=TOP, pady=15, padx=15)

        self.frame2 = Frame(self.mainframe, bg=c.silver)
        self.frame2.pack(side=TOP, pady=15, padx=15)

        self.slot_lbl = Label(self.frame1, text='Enter Slot Number: ', bg=c.silver, font='Arial 18 bold')
        self.slot_lbl.grid(row=0, column=0, padx=4, pady=4)

        self.slot_ent = Entry(self.frame1, font='Arial 18 italic', bd=4, textvariable=self.slot_num)
        self.slot_ent.grid(row=0, column=1, padx=4, pady=4)

        self.slot_bt4 = Button(self.frame1, text="Reset", bg=c.light_blue, width=10,
                               font="Arial 16 bold", command=self.disable_reset)
        self.slot_bt4.grid(row=1, column=1, sticky=E, pady=2)

        self.emptylbl =  Label(self.frame1, text='', bg=c.silver, font='Arial 18 italic')
        self.emptylbl.grid(row=2, column=0, columnspan=3, pady=15)

        self.slot_bt0 = Button(self.frame2, text="Add", bg=c.light_blue, width=9,
                               font="Arial 16 bold", command=self.add_slot)
        self.slot_bt0.grid(row=0, column=0, pady=2, padx=3)

        self.slot_bt1 = Button(self.frame2, text="Disable", bg=c.light_blue, width=9,
                               font="Arial 16 bold", command=self.dis_slot)
        self.slot_bt1.grid(row=0, column=1, pady=2, padx=3)

        self.slot_bt2 = Button(self.frame2, text="Enable", bg=c.light_blue, width=9,
                               font="Arial 16 bold", command=self.en_slot)
        self.slot_bt2.grid(row=0, column=2, pady=2, padx=3)

        self.slot_bt3 = Button(self.frame2, text="Delete", bg=c.light_blue, width=9,
                               font="Arial 16 bold", command=self.del_slot)
        self.slot_bt3.grid(row=0, column=3, pady=2, padx=3)


# =================================PARKED LOG WINDOW=======================================================

class park_log(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, bg=c.light_blue)
        self.park_log_widgets()
        self.view_parked()

    def view_parked(self):
        i = 1
        for row in a_obj.parked_view():
            self.log_table.insert("", tk.END, values=(i, row[0], row[1], row[2]))
            i += 1

    def park_log_widgets(self):
        self.top = Frame(self, bg=c.silver, bd=9, relief='ridge')
        self.top.pack(side=TOP, pady=40)

        self.bottom = Frame(self, bg=c.light_blue)
        self.bottom.pack(side=TOP, pady=70)

        self.parked_frame = Frame(self.bottom, bg=c.silver, bd=9, relief='ridge')
        self.parked_frame.pack(side=TOP, pady=5, padx=40)

        self.lbl1 = Label(self.top, text='CARS PARKED', bd=6,
                          font='Arial 30 bold', bg=c.silver, fg=c.dark_blue, justify=CENTER)
        self.lbl1.grid(row=0, column=0, padx=200)

        #declare scrollbar
        self.scroll_x = ttk.Scrollbar(self.parked_frame, orient=HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.parked_frame, orient=VERTICAL)

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                             font=('Calibri', 16))  # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 20, 'bold'))

        self.columns = ('sn', 'plate_no', 'slot', 't_in')

        self.log_table = ttk.Treeview(self.parked_frame,
                                          columns=self.columns,
                                          show='headings', style="mystyle.Treeview",
                                          xscrollcommand=self.scroll_x.set,
                                          yscrollcommand=self.scroll_y.set)

        self.log_table.column("sn", anchor=CENTER, stretch=NO, width=50)
        self.log_table.heading('sn', text='S/N')
        self.log_table.column("plate_no", anchor=CENTER, stretch=NO, width=400)
        self.log_table.heading('plate_no', text='Plate No')
        self.log_table.column("slot", anchor=CENTER, stretch=NO, width=400)
        self.log_table.heading('slot', text='Slot Number')
        self.log_table.column("t_in", anchor=CENTER, stretch=NO, width=400)
        self.log_table.heading('t_in', text='Time In')

        self.log_table.grid(row=0, column=0, sticky='nsew')

        #scroll bar close
        self.scroll_x.grid(row=1, column=0, sticky='ew')
        self.scroll_y.grid(row=0, column=1, sticky='ns')

        self.scroll_x.config(command=self.log_table.xview)
        self.scroll_y.config(command=self.log_table.yview)


# =========================================HISTORY======================================================================

class history(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, bg=c.light_blue)
        self.history_widgets()
        self.log_view()
        self.total_view()

    def log_view(self):
        data = a_obj.history_view()
        if data:
            i = 1
            for row in data:
                self.history_table.insert("", tk.END, values=(i, row[0], row[1], row[2], row[3], row[4]))
                i += 1
        else:
            self.emptylbl.config(text="No cars have been exited today...")


    def total_view(self):
        data = a_obj.history_total_view()
        total_exit = len(data[0])
        total_amt = 0
        for row in data[0]:
            total_amt += row[0]
        self.total_table.insert("", tk.END, values=(data[1], total_exit, total_amt))

    def history_widgets(self):
        self.top = Frame(self, bg=c.silver, bd=9, relief='ridge')
        self.top.pack(side=TOP, pady=40)

        self.emptylbl = Label(self, bg=c.light_blue, text="", font='Arial 18 italic')
        self.emptylbl.pack(side=TOP, padx=6, pady=6)

        self.bottom = Frame(self, bg=c.light_blue)
        self.bottom.pack(side=TOP, pady=70)

        self.record_frame = Frame(self.bottom, bg=c.silver, bd=9, relief='ridge')
        self.record_frame.pack(side=TOP, pady=5, padx=40)

        self.total_frame = Frame(self.bottom, bg=c.silver, bd=9, relief='ridge')
        self.total_frame.pack(side=RIGHT, padx=40)

        self.label_1 = Label(self.top, text='DAILY PARKING LOG', bd=6,
                             font='Arial 30 bold', bg=c.silver, fg=c.dark_blue, justify=CENTER)
        self.label_1.grid(row=0, column=0, padx=200)

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                              font=('Calibri', 20))  # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 22, 'bold'))  # Modify the font of the headings

        #To show total made for that day
        self.columns = ('date', 'total_exit', 'total_amt')

        self.total_table = ttk.Treeview(self.total_frame,
                                          columns=self.columns,
                                          show='headings', height=3, style="mystyle.Treeview")
        self.total_table.column("date", anchor=CENTER)
        self.total_table.heading('date', text='Date')
        self.total_table.column("total_exit", anchor=CENTER)
        self.total_table.heading('total_exit', text='Total Car Exit')
        self.total_table.column("total_amt", anchor=CENTER)
        self.total_table.heading('total_amt', text='Total Paid')

        self.total_table.grid(row=0, column=0, sticky='nsew')

        # =====================================================================================

        # scroll bar
        self.scroll_x = ttk.Scrollbar(self.record_frame, orient=HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.record_frame, orient=VERTICAL)

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                              font=('Calibri', 16))  # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 20, 'bold'))

        self.columns = ('sn', 'plate_no', 't_in', 't_out', 'hours', 'amt')

        self.history_table = ttk.Treeview(self.record_frame,
                                          columns=self.columns,
                                          show='headings', style="mystyle.Treeview",
                                          height=11,
                                          xscrollcommand=self.scroll_x.set,
                                          yscrollcommand=self.scroll_y.set)

        self.history_table.column("sn", anchor=CENTER, stretch=NO, width=50)
        self.history_table.heading('sn', text='S/N')
        self.history_table.heading('plate_no', text='Plate No')
        self.history_table.column("t_in", anchor=CENTER, stretch=NO, width=400)
        self.history_table.heading('t_in', text='Time In')
        self.history_table.column("t_out", anchor=CENTER, stretch=NO, width=400)
        self.history_table.heading('t_out', text='Time Out')
        self.history_table.heading('hours', text='Time spent (HR)')
        self.history_table.heading('amt', text='Amount Paid')

        self.history_table.grid(row=0, column=0, sticky='nsew')

        self.scroll_x.grid(row=1, column=0, sticky='ew')
        self.scroll_y.grid(row=0, column=1, sticky='ns')

        self.scroll_x.config(command=self.history_table.xview)
        self.scroll_y.config(command=self.history_table.yview)


# ===========================================CHANGE FEE=========================================================

class change_fee(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, bg=c.light_blue)
        self.price = StringVar()
        self.fee_pass = StringVar()
        self.fee_widgets()
        self.price_ent.focus()

    def fee_reset(self):
        self.fee_pass.set("")
        self.price.set("")
        self.emptylbl.config(text="")

    @staticmethod
    def check_fee(new_price):
        try:
            float(new_price)
            return True
        except ValueError:
            return False

    def check_pass(self):
        new_price = self.price.get()
        if self.check_fee(new_price):
            p_word = self.fee_pass.get()
            if login_det['password'] == p_word:
                self.update_price(new_price)
            else:
                self.emptylbl.config(text="authorization failed")
        else:
            self.emptylbl.config(text="update failed...Enter valid price")

    def update_price(self, new_price):
        a_obj.price_update(new_price)
        self.emptylbl.config(text="Price Updated Successfully!\nRestart Application")

    def fee_widgets(self):
        self.mainframe = Frame(self, bg=c.silver, bd=12, relief='ridge')
        self.mainframe.pack(side=TOP)

        self.frame1 = Frame(self.mainframe, bg=c.silver)
        self.frame1.pack(side=TOP, pady=30, padx=15)

        self.price_lbl = Label(self.frame1, text='Enter New Price: ', bg=c.silver, font='Arial 18 bold')
        self.price_lbl.grid(row=0, column=0, padx=4, pady=4)

        self.price_ent = Entry(self.frame1, font='Arial 18 italic', bd=4, textvariable=self.price)
        self.price_ent.grid(row=0, column=1, padx=4, pady=4)

        self.pass_lbl = Label(self.frame1, text='Enter Password: ', bg=c.silver, font='Arial 18 bold')
        self.pass_lbl.grid(row=1, column=0, padx=4, pady=4)

        self.pass_ent = Entry(self.frame1, font='Arial 18 italic', show='*', bd=4, textvariable=self.fee_pass)
        self.pass_ent.grid(row=1, column=1, padx=4, pady=4)

        self.emptylbl = Label(self.frame1, text='', bg=c.silver, font='Arial 18 italic')
        self.emptylbl.grid(row=2, column=0, columnspan=2, pady=15)

        self.change_bt = Button(self.frame1, text="Change", bg=c.light_blue,
                              font="Arial 16 bold", width=8, command=self.check_pass)
        self.change_bt.grid(row=3, column=0, pady=5, sticky=E)

        self.exit_bt = Button(self.frame1, text="Reset", bg=c.light_blue,
                               font="Arial 16 bold", width=8, command=self.fee_reset)
        self.exit_bt.grid(row=3, column=1, pady=5, sticky=W)


if __name__ == "__main__":
    c = my_colors()
    a_obj = functions.BackEnd()
    app = ACPS_App()
    app.mainloop()

