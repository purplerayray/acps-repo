import sqlite3
import socket
import datetime
import sys


class BackEnd:
    def __init__(self):
        self.database = self.retrieve_database()
        global database
        database = self.database

    def retrieve_database(self):
        db = self.initialize_server()
        if db is None:
            sys.exit('Database retrieval failed!')
        else:
            return db

    def initialize_server(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 5434
        host = 'localhost'
        try:
            client.connect((host, port))
            data = bytes.decode(client.recv(1824))
            print(data)
            try:
                client.send(str.encode('send_database'))
                db = bytes.decode(client.recv(1824))

                client.send(str.encode('end_connection'))
                end_message = bytes.decode(client.recv(1824))
                print(end_message)

                client.close()
            except ConnectionAbortedError:
                print('Connection Error!')
                db = None
            except ConnectionResetError:
                print('Connection Error!')
                db = None
            return db
        except ConnectionRefusedError:
            print('Server is offline')


    @classmethod
    def login_check(cls, name, password):
        try:
            conn = sqlite3.connect(database)
            c = conn.cursor()
            mypass = c.execute("SELECT password FROM admin where username=?", [name]).fetchone()[0]
            c.close()
            conn.close()
            if password == mypass:
                return True
            else:
                return False
        except TypeError:
            return False


    @classmethod
    def load_slots(cls):
        slots = dict()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        slots['all_slots'] = [i[0] for i in c.execute('SELECT slot_no FROM parking_slots ORDER BY slot_no')]
        slots['available_slots'] = [i[0] for i in c.execute('SELECT slot_no FROM parking_slots WHERE status = "empty"')]
        slots['filled_slots'] = [i[0] for i in c.execute('SELECT slot_no FROM parking_slots WHERE status = "filled"')]
        slots['disabled_slots'] = [i[0] for i in c.execute('SELECT slot_no FROM parking_slots WHERE status = "disabled"')]
        c.close()
        conn.close()
        return slots


    @classmethod
    def all_cars(cls):
        cars_data = dict()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        cars_data['parked_cars'] = [i[0] for i in c.execute('SELECT plate_no FROM vehicle')]
        cars_data['exited_cars'] = [i[0] for i in c.execute('SELECT plate_no FROM parking_log')]
        c.close()
        conn.close()
        return cars_data


    @classmethod
    def update_slot(cls, slot):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("""UPDATE parking_slots SET status = 'filled' WHERE slot_no = ?""", [slot])
        conn.commit()
        c.close()
        conn.close()

    @classmethod
    def get_slot(cls, plate_no):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        slot = c.execute('SELECT slot_no FROM vehicle WHERE plate_no= ?', [plate_no])
        slot_num = slot.fetchone()[0]
        c.close()
        conn.close()
        return slot_num

    @classmethod
    def log_exit(cls, data):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("INSERT INTO parking_log VALUES(?,?,?,?,?,?)", data)
        conn.commit()
        c.close()
        conn.close()

    @classmethod
    def get_fee(cls):
        default_fee = '100.0'
        conn = sqlite3.connect(database)
        c = conn.cursor()
        try:
            row = c.execute("""SELECT fee FROM parking_fee""").fetchall()[-1]
        except IndexError:
            return default_fee
        c.close()
        conn.close()
        fee = row[0]
        return fee

    @classmethod
    def car_entry_time(cls, plate_no):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        entry = c.execute('SELECT time_of_entry FROM vehicle WHERE plate_no= ?', [plate_no])
        entry_time = entry.fetchone()[0]
        c.close()
        conn.close()
        return entry_time

    @classmethod
    def exit_lot(cls, plate, slot):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("DELETE FROM vehicle WHERE plate_no = ?", [plate])
        c.execute("UPDATE parking_slots SET plate_no = NULL WHERE slot_no = ?", [slot])
        c.execute("UPDATE parking_slots SET status = 'empty' WHERE slot_no = ?", [slot])
        conn.commit()
        c.close()
        conn.close()
        return True

    @classmethod
    def park_lot(cls, plate, slot, date):
        data = (plate, slot, date)
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("""INSERT INTO 'vehicle'('plate_no','slot_no','time_of_entry') 
                        VALUES(?,?,?)""", data)
        v_id = c.execute("""SELECT plate_no FROM vehicle WHERE slot_no = ?""", [slot])
        car_id = v_id.fetchone()[0]
        data2 = (car_id, slot)
        c.execute("""UPDATE parking_slots SET plate_no = ? WHERE slot_no = ?""", data2)
        conn.commit()
        c.close()
        conn.close()
        return True


    @classmethod
    def gen_search(cls, plate_no):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        data1 = c.execute("""SELECT time_of_entry, 
                            slot_no FROM vehicle WHERE plate_no= ?""", [plate_no]).fetchall()
        data = c.execute("""SELECT time_of_entry, exit_time, 
                         hrs_spent, amount, slot_no FROM parking_log WHERE plate_no= ?""", [plate_no])
        search_data = (data.fetchall(), data1)
        c.close()
        conn.close()
        return search_data

    @classmethod
    def check_slot(cls, slot):
        slots = BackEnd.load_slots()
        if slot in slots["all_slots"]:
            return True
        else:
            return False

    @classmethod
    def config_slot(cls, action, slot_no):
        slots = BackEnd.load_slots()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        if action == "add":
            try:
                c.execute("""INSERT INTO parking_slots('slot_no') 
                             VALUES(?)""", [slot_no])
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

        elif action == "dis":
            if slot_no in slots['available_slots']:
                c.execute("""UPDATE parking_slots SET status = 'disabled' WHERE slot_no = ?""", [slot_no])
                conn.commit()
                return True
            else:
                return False

        elif action == "en":
            if slot_no in slots['disabled_slots']:
                c.execute("""UPDATE parking_slots SET status = 'empty' WHERE slot_no = ?""", [slot_no])
                conn.commit()
                return True
            else:
                return False

        elif action == "del":
            if slot_no in slots['available_slots']:
                c.execute("""DELETE FROM parking_slots WHERE slot_no = ?""", [slot_no])
                conn.commit()
                return True
            else:
                return False

        c.close()
        conn.close()

    @classmethod
    def parked_view(cls):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        data = c.execute("""SELECT plate_no, slot_no,
                            time_of_entry
                            FROM vehicle""")
        log_data = data.fetchall()
        c.close()
        conn.close()
        return log_data

    @classmethod
    def price_update(cls, new_price):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("""INSERT INTO parking_fee('fee') 
                            VALUES(?)""", [new_price])
        conn.commit()
        c.close()
        conn.close()

    @classmethod
    def history_view(cls):
        cur_date = datetime.date.today()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        data = c.execute("""SELECT plate_no,
                                    time_of_entry, exit_time, hrs_spent, amount
                                    FROM parking_log WHERE exit_time >= ?""", [cur_date])
        log_data = data.fetchall()
        c.close()
        conn.close()
        return log_data

    @classmethod
    def history_total_view(cls):
        cur_date = datetime.date.today()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        data = c.execute("""SELECT amount
                            FROM parking_log WHERE exit_time >= ?""", [cur_date])
        log_data = data.fetchall()
        c.close()
        conn.close()
        data = (log_data, cur_date)
        return data





