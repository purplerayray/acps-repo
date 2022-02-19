import sqlite3
import datetime


class CreateDatabase:
    currentDateTime = datetime.datetime.now()

    conn = sqlite3.connect('vehicles.db',
                           detect_types=sqlite3.PARSE_DECLTYPES |
                           sqlite3.PARSE_COLNAMES)

    c = conn.cursor()

    c.execute("""CREATE TABLE admin (
                 admin_id INTEGER NOT NULL PRIMARY KEY,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL
                )""")

    c.execute("INSERT INTO admin(username, password) VALUES('admin', 'admin')")

    c.execute("""CREATE TABLE vehicle (
                 plate_no VARCHAR(12) PRIMARY KEY NOT NULL,
                 slot_no INTEGER,
                 time_of_entry TIMESTAMP,
                 FOREIGN KEY(slot_no) REFERENCES parking_slots(slot_no)
                )""")

    c.execute("""CREATE TABLE slot_status (
                status TEXT PRIMARY KEY
               )""")

    c.execute("INSERT INTO slot_status(status) VALUES('empty')")
    c.execute("INSERT INTO slot_status(status) VALUES('filled')")
    c.execute("INSERT INTO slot_status(status) VALUES('disabled')")

    c.execute("""CREATE TABLE parking_slots (
                 slot_no INTEGER PRIMARY KEY,
                 status TEXT DEFAULT "empty" NOT NULL,
                 plate_no VARCHAR(12) UNIQUE,
                 FOREIGN KEY(plate_no) REFERENCES vehicle(plate_no)
                 FOREIGN KEY(status) REFERENCES slot_status(status)
                )""")

    slots = [('100',), ('101',), ('102',), ('103',), ('104',), ('105',), ('106',), ('107',), ('108',), ('109',),
             ('200',), ('201',), ('202',), ('203',), ('204',), ('205',), ('206',), ('207',), ('208',), ('209',),
             ('300',), ('301',), ('302',), ('303',), ('304',), ('305',), ('306',), ('307',), ('308',), ('309',),
             ('400',), ('401',), ('402',), ('403',), ('404',), ('405',), ('406',), ('407',), ('408',), ('409',),
             ('500',), ('501',), ('502',), ('503',), ('504',), ('505',), ('506',), ('507',), ('508',), ('509',),
             ('600',), ('601',), ('602',), ('603',), ('604',), ('605',), ('606',), ('607',), ('608',), ('609',),
             ('700',), ('701',), ('702',), ('703',), ('704',), ('705',), ('706',), ('707',), ('708',), ('709',),
             ('800',), ('801',), ('802',), ('803',), ('804',), ('805',), ('806',), ('807',), ('808',), ('809',),
             ('900',)]

    c.executemany("INSERT INTO parking_slots(slot_no) VALUES(?);", slots)

    c.execute("""CREATE TABLE parking_log (
                 plate_no VARCHAR(12) NOT NULL,
                 slot_no INTEGER,
                 time_of_entry TIMESTAMP,
                 exit_time TIMESTAMP,
                 hrs_spent INT,
                 amount FLOAT,
                 FOREIGN KEY(time_of_entry) REFERENCES vehicle(time_of_entry),
                 FOREIGN KEY(slot_no) REFERENCES parking_slots(slot_no)
                 )""")

    c.execute("""CREATE TABLE parking_fee (
                 fee FLOAT NOT NULL,
                 date_of_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                  )""")

    conn.commit()
    c.close()
    conn.close()


