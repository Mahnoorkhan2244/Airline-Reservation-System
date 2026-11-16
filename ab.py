import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import hashlib


def generate_booking_code():
    chars = string.ascii_uppercase + string.digits
    return "PKF-" + "".join(random.choices(chars, k=8))


def draw_qr_pattern(canvas, data, x, y, size):
    hash_val = hashlib.md5(data.encode()).hexdigest()
    bits = bin(int(hash_val, 16))[2:].zfill(128)
    cell = size // 10
    border = cell
    canvas.create_rectangle(x, y, x + size, y + size, fill="white", outline="")
    idx = 0
    for row in range(8):
        for col in range(8):
            if idx < len(bits) and bits[idx] == "1":
                cx = x + border + col * cell
                cy = y + border + row * cell
                canvas.create_rectangle(cx, cy, cx + cell, cy + cell, fill="#1a1a1a", outline="")
            idx += 1
    for pos in [(x + border, y + border),
                (x + size - border - cell * 3, y + border),
                (x + border, y + size - border - cell * 3)]:
        px, py = pos
        canvas.create_rectangle(px, py, px + cell * 3, py + cell * 3, fill="#1a1a1a", outline="")
        canvas.create_rectangle(px + cell, py + cell, px + cell * 2, py + cell * 2, fill="white", outline="")


class HotelNode:
    def __init__(self, name, phone, cnic, check_in, check_out, guests, room_type, meal_plan, cost):
        self.name = name
        self.phone = phone
        self.cnic = cnic
        self.check_in = check_in
        self.check_out = check_out
        self.guests = guests
        self.room_type = room_type
        self.meal_plan = meal_plan
        self.cost = cost
        self.next = None


class Hotel:
    ROOMS = {
        "Deluxe Room":      {"price": 8000,  "desc": "Queen Bed, City View"},
        "Executive Suite":  {"price": 15000, "desc": "King Bed, Lounge Area"},
        "Presidential Suite": {"price": 30000, "desc": "2 Bedrooms, Private Pool"},
        "Standard Room":    {"price": 5000,  "desc": "Twin Beds, Basic Amenities"},
    }
    MEAL_PLANS = {
        "Room Only":            0,
        "Breakfast Included":   800,
        "Half Board (B+D)":     1500,
        "Full Board (B+L+D)":   2500,
    }

    def __init__(self):
        self.head = None

    def insertion(self, name, phone, cnic, check_in, check_out, guests, room_type, meal_plan, cost):
        node = HotelNode(name, phone, cnic, check_in, check_out, guests, room_type, meal_plan, cost)
        if self.head is None:
            self.head = node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = node

    def open_booking(self):
        win = tk.Toplevel()
        win.title("Hotel Booking")
        win.geometry("950x720")
        win.configure(bg="#F0F3F4")
        win.resizable(False, False)

        tk.Label(win, text="🏨  HOTEL BOOKING", font=("Arial", 20, "bold"),
                 bg="#1B4F72", fg="white", pady=12).pack(fill="x")

        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[12, 5])

        tab1 = tk.Frame(notebook, bg="#EAF2FB")
        notebook.add(tab1, text="👤  Guest Info")

        def lbl_entry(parent, text, row, show=None):
            tk.Label(parent, text=text, font=("Arial", 11, "bold"), bg="#EAF2FB",
                     anchor="w").grid(row=row, column=0, padx=20, pady=8, sticky="w")
            e = tk.Entry(parent, font=("Arial", 11), width=30, bd=1, relief="solid", show=show or "")
            e.grid(row=row, column=1, padx=10, pady=8, sticky="w")
            return e

        guest_name  = lbl_entry(tab1, "Full Name *",         0)
        guest_cnic  = lbl_entry(tab1, "CNIC / Passport *",   1)
        guest_phone = lbl_entry(tab1, "Phone Number *",       2)
        guest_email = lbl_entry(tab1, "Email Address",        3)

        tk.Label(tab1, text="Number of Guests *", font=("Arial", 11, "bold"),
                 bg="#EAF2FB", anchor="w").grid(row=4, column=0, padx=20, pady=8, sticky="w")
        guest_count = ttk.Combobox(tab1, values=["1", "2", "3", "4", "5", "6"],
                                   font=("Arial", 11), width=10, state="readonly")
        guest_count.set("1")
        guest_count.grid(row=4, column=1, padx=10, pady=8, sticky="w")

        tk.Button(tab1, text="Next ▶", font=("Arial", 12, "bold"),
                  bg="#2980B9", fg="white", padx=20, pady=6,
                  command=lambda: notebook.select(1)).grid(row=6, column=1, pady=20, sticky="e", padx=10)

        tab2 = tk.Frame(notebook, bg="#EAFAF1")
        notebook.add(tab2, text="🛏  Room & Dates")

        def lbl2(text, row):
            tk.Label(tab2, text=text, font=("Arial", 11, "bold"), bg="#EAFAF1",
                     anchor="w").grid(row=row, column=0, padx=20, pady=8, sticky="w")

        def entry2(row):
            e = tk.Entry(tab2, font=("Arial", 11), width=25, bd=1, relief="solid")
            e.grid(row=row, column=1, padx=10, pady=8, sticky="w")
            return e

        lbl2("Check-In Date (DD/MM/YYYY) *", 0)
        check_in_entry = entry2(0)

        lbl2("Check-Out Date (DD/MM/YYYY) *", 1)
        check_out_entry = entry2(1)

        lbl2("Room Type *", 2)
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(tab2, values=list(Hotel.ROOMS.keys()),
                                  textvariable=room_var, font=("Arial", 11), width=23, state="readonly")
        room_combo.grid(row=2, column=1, padx=10, pady=8, sticky="w")

        room_desc_lbl = tk.Label(tab2, text="", font=("Arial", 10, "italic"),
                                 bg="#EAFAF1", fg="#117A65")
        room_desc_lbl.grid(row=3, column=1, padx=10, sticky="w")

        def on_room_change(*_):
            r = room_var.get()
            if r in Hotel.ROOMS:
                room_desc_lbl.config(text=f"  {Hotel.ROOMS[r]['desc']}  —  Rs. {Hotel.ROOMS[r]['price']:,} / night")

        room_var.trace("w", on_room_change)

        lbl2("Meal Plan *", 4)
        meal_var = tk.StringVar(value="Room Only")
        meal_combo = ttk.Combobox(tab2, values=list(Hotel.MEAL_PLANS.keys()),
                                  textvariable=meal_var, font=("Arial", 11), width=23, state="readonly")
        meal_combo.grid(row=4, column=1, padx=10, pady=8, sticky="w")

        tk.Button(tab2, text="◀ Back", font=("Arial", 11),
                  bg="#7F8C8D", fg="white", padx=15, pady=5,
                  command=lambda: notebook.select(0)).grid(row=6, column=0, pady=15, padx=20, sticky="w")
        tk.Button(tab2, text="Next ▶", font=("Arial", 12, "bold"),
                  bg="#2980B9", fg="white", padx=20, pady=6,
                  command=lambda: notebook.select(2)).grid(row=6, column=1, pady=15, sticky="e", padx=10)

        tab3 = tk.Frame(notebook, bg="#FDF2F8")
        notebook.add(tab3, text="💳  Payment")

        tk.Label(tab3, text="Select Payment Method", font=("Arial", 13, "bold"),
                 bg="#FDF2F8").pack(pady=15)

        hotel_pay_var = tk.StringVar(value="Credit / Debit Card")
        methods = ["Credit / Debit Card", "EasyPaisa", "JazzCash", "HBL Mobile", "Bank Transfer"]

        pay_btn_frame = tk.Frame(tab3, bg="#FDF2F8")
        pay_btn_frame.pack()
        for m in methods:
            tk.Radiobutton(pay_btn_frame, text=m, variable=hotel_pay_var, value=m,
                           font=("Arial", 11), bg="#FDF2F8").pack(anchor="w", pady=3)

        detail_frame = tk.Frame(tab3, bg="#FDF2F8")
        detail_frame.pack(pady=10, fill="x", padx=30)

        card_frame  = tk.Frame(detail_frame, bg="#EAF2FB", bd=1, relief="solid", padx=10, pady=10)
        mobi_frame  = tk.Frame(detail_frame, bg="#E8F8F5", bd=1, relief="solid", padx=10, pady=10)
        bank_frame  = tk.Frame(detail_frame, bg="#FEF9E7", bd=1, relief="solid", padx=10, pady=10)

        tk.Label(card_frame, text="Card Number", font=("Arial", 11), bg="#EAF2FB").grid(row=0, column=0, sticky="w", pady=3)
        h_card_num = tk.Entry(card_frame, font=("Arial", 11), width=22, bd=1, relief="solid")
        h_card_num.grid(row=0, column=1, padx=8)
        tk.Label(card_frame, text="Expiry (MM/YY)", font=("Arial", 11), bg="#EAF2FB").grid(row=1, column=0, sticky="w", pady=3)
        h_card_exp = tk.Entry(card_frame, font=("Arial", 11), width=10, bd=1, relief="solid")
        h_card_exp.grid(row=1, column=1, sticky="w", padx=8)
        tk.Label(card_frame, text="CVV", font=("Arial", 11), bg="#EAF2FB").grid(row=2, column=0, sticky="w", pady=3)
        h_card_cvv = tk.Entry(card_frame, font=("Arial", 11), width=6, show="*", bd=1, relief="solid")
        h_card_cvv.grid(row=2, column=1, sticky="w", padx=8)

        wallet_name_lbl = tk.Label(mobi_frame, text="EasyPaisa Number", font=("Arial", 11, "bold"), bg="#E8F8F5")
        wallet_name_lbl.grid(row=0, column=0, columnspan=2, sticky="w", pady=4)
        tk.Label(mobi_frame, text="Registered Number", font=("Arial", 11), bg="#E8F8F5").grid(row=1, column=0, sticky="w", pady=3)
        h_wallet_num = tk.Entry(mobi_frame, font=("Arial", 11), width=18, bd=1, relief="solid")
        h_wallet_num.grid(row=1, column=1, padx=8)
        tk.Label(mobi_frame, text="Transaction PIN", font=("Arial", 11), bg="#E8F8F5").grid(row=2, column=0, sticky="w", pady=3)
        h_wallet_pin = tk.Entry(mobi_frame, font=("Arial", 11), width=10, show="*", bd=1, relief="solid")
        h_wallet_pin.grid(row=2, column=1, sticky="w", padx=8)

        # Bank transfer fields
        tk.Label(bank_frame, text="Account Number", font=("Arial", 11), bg="#FEF9E7").grid(row=0, column=0, sticky="w", pady=3)
        h_bank_acc = tk.Entry(bank_frame, font=("Arial", 11), width=22, bd=1, relief="solid")
        h_bank_acc.grid(row=0, column=1, padx=8)
        tk.Label(bank_frame, text="Bank Name", font=("Arial", 11), bg="#FEF9E7").grid(row=1, column=0, sticky="w", pady=3)
        h_bank_name = ttk.Combobox(bank_frame, values=["HBL", "UBL", "MCB", "Meezan", "Allied Bank", "Bank Alfalah"],
                                   font=("Arial", 11), width=18, state="readonly")
        h_bank_name.grid(row=1, column=1, padx=8)

        def refresh_hotel_pay(*_):
            card_frame.pack_forget()
            mobi_frame.pack_forget()
            bank_frame.pack_forget()
            m = hotel_pay_var.get()
            if m == "Credit / Debit Card":
                card_frame.pack(fill="x")
            elif m in ("EasyPaisa", "JazzCash", "HBL Mobile"):
                wallet_name_lbl.config(text=f"{m} Number")
                mobi_frame.pack(fill="x")
            elif m == "Bank Transfer":
                bank_frame.pack(fill="x")

        hotel_pay_var.trace("w", refresh_hotel_pay)
        refresh_hotel_pay()

        nav3 = tk.Frame(tab3, bg="#FDF2F8")
        nav3.pack(fill="x", padx=20, pady=5)
        tk.Button(nav3, text="◀ Back", font=("Arial", 11),
                  bg="#7F8C8D", fg="white", padx=15, pady=5,
                  command=lambda: notebook.select(1)).pack(side="left")
        tk.Button(nav3, text="✅  CONFIRM BOOKING", font=("Arial", 12, "bold"),
                  bg="#117A65", fg="white", padx=15, pady=6,
                  command=lambda: confirm_hotel()).pack(side="right")

        tab4 = tk.Frame(notebook, bg="#F2F3F4")
        notebook.add(tab4, text="📋  Bookings")
        tk.Label(tab4, text="All Hotel Bookings", font=("Arial", 13, "bold"),
                 bg="#F2F3F4").pack(pady=8)
        bookings_text = tk.Text(tab4, font=("Consolas", 10), bg="white", height=18)
        bookings_text.pack(fill="both", expand=True, padx=10, pady=5)

        def refresh_bookings():
            bookings_text.delete("1.0", tk.END)
            temp = self.head
            i = 1
            while temp:
                bookings_text.insert(tk.END,
                    f"{'='*38}\n  Booking #{i}\n{'='*38}\n"
                    f"  Guest     : {temp.name}\n"
                    f"  CNIC      : {temp.cnic}\n"
                    f"  Phone     : {temp.phone}\n"
                    f"  Check-In  : {temp.check_in}\n"
                    f"  Check-Out : {temp.check_out}\n"
                    f"  Guests    : {temp.guests}\n"
                    f"  Room      : {temp.room_type}\n"
                    f"  Meal Plan : {temp.meal_plan}\n"
                    f"  Total     : Rs. {temp.cost:,}\n\n")
                temp = temp.next
                i += 1

        def confirm_hotel():
            name    = guest_name.get().strip()
            cnic    = guest_cnic.get().strip()
            phone   = guest_phone.get().strip()
            c_in    = check_in_entry.get().strip()
            c_out   = check_out_entry.get().strip()
            room    = room_var.get()
            meal    = meal_var.get()
            guests  = guest_count.get()
            pay     = hotel_pay_var.get()

            errors = []
            if not name:   errors.append("Guest name required")
            if not cnic:   errors.append("CNIC / Passport required")
            if not phone:  errors.append("Phone number required")
            if not c_in:   errors.append("Check-in date required")
            if not c_out:  errors.append("Check-out date required")
            if not room:   errors.append("Select a room type")
            if pay == "Credit / Debit Card":
                if len(h_card_num.get().replace(" ", "")) < 16: errors.append("Valid 16-digit card number required")
                if not h_card_exp.get().strip():                errors.append("Card expiry required")
                if len(h_card_cvv.get()) < 3:                   errors.append("Valid CVV required")
            elif pay in ("EasyPaisa", "JazzCash", "HBL Mobile"):
                if len(h_wallet_num.get().strip()) < 11:  errors.append(f"Valid {pay} number required")
                if len(h_wallet_pin.get().strip()) < 4:   errors.append("Transaction PIN required")
            elif pay == "Bank Transfer":
                if not h_bank_acc.get().strip():   errors.append("Account number required")
                if not h_bank_name.get():          errors.append("Select bank name")

            if errors:
                messagebox.showerror("Incomplete Form", "\n".join(f"• {e}" for e in errors))
                if not name:   guest_name.delete(0, tk.END)
                if not cnic:   guest_cnic.delete(0, tk.END)
                if not phone:  guest_phone.delete(0, tk.END)
                if not c_in:   check_in_entry.delete(0, tk.END)
                if not c_out:  check_out_entry.delete(0, tk.END)
                pay = hotel_pay_var.get()
                if pay == "Credit / Debit Card":
                    if len(h_card_num.get().replace(" ", "")) < 16: h_card_num.delete(0, tk.END)
                    if not h_card_exp.get().strip():                h_card_exp.delete(0, tk.END)
                    if len(h_card_cvv.get()) < 3:                   h_card_cvv.delete(0, tk.END)
                elif pay in ("EasyPaisa", "JazzCash", "HBL Mobile"):
                    if len(h_wallet_num.get().strip()) < 11: h_wallet_num.delete(0, tk.END)
                    if len(h_wallet_pin.get().strip()) < 4:  h_wallet_pin.delete(0, tk.END)
                elif pay == "Bank Transfer":
                    if not h_bank_acc.get().strip(): h_bank_acc.delete(0, tk.END)
                return

            cost = Hotel.ROOMS[room]["price"] + Hotel.MEAL_PLANS.get(meal, 0)
            self.insertion(name, phone, cnic, c_in, c_out, guests, room, meal, cost)
            refresh_bookings()
            notebook.select(3)

            print("\n" + "="*50)
            print("       ✅  HOTEL BOOKING CONFIRMED")
            print("="*50)
            print(f"  Guest Name  : {name}")
            print(f"  CNIC        : {cnic}")
            print(f"  Phone       : {phone}")
            print(f"  Email       : {guest_email.get().strip() or 'N/A'}")
            print(f"  Guests      : {guests}")
            print(f"  Check-In    : {c_in}")
            print(f"  Check-Out   : {c_out}")
            print(f"  Room Type   : {room}")
            print(f"  Meal Plan   : {meal}")
            print(f"  Payment     : {pay}")
            print(f"  Total Cost  : Rs. {cost:,}")
            print("="*50 + "\n")

            messagebox.showinfo("Booking Confirmed!",
                f"✅ Hotel booking confirmed!\n\n"
                f"Guest   : {name}\nRoom    : {room}\n"
                f"Check-In: {c_in}\nCheck-Out: {c_out}\n"
                f"Meal Plan: {meal}\nPayment : {pay}\n"
                f"Total   : Rs. {cost:,}")


class TicketCheckerApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Ticket Checker")
        self.root.geometry("680x460")
        self.root.configure(bg="#FADBD8")

        tk.Label(self.root, text="🎫  TICKET CHECKER", font=("Arial", 20, "bold"),
                 bg="#922B21", fg="white", pady=10).pack(fill="x")
        tk.Label(self.root, text="Enter PNR Number", font=("Arial", 12, "bold"), bg="#FADBD8").pack(pady=15)

        self.pnr_entry = tk.Entry(self.root, width=30, font=("Arial", 12), bd=1, relief="solid")
        self.pnr_entry.pack()

        tk.Button(self.root, text="CHECK TICKET", command=self.check_ticket,
                  bg="#2874A6", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(pady=15)

        self.result_text = tk.Text(self.root, height=12, width=52, font=("Consolas", 11),
                                   bg="white", bd=1, relief="solid")
        self.result_text.pack(padx=15)

    def check_ticket(self):
        pnr = self.pnr_entry.get().strip()
        if not pnr:
            messagebox.showerror("Error", "Please Enter PNR Number")
            return
        result = (f"\n  PNR Number      : {pnr}\n"
                  f"  Passenger Name  : John Doe\n"
                  f"  Flight          : PK-303\n"
                  f"  Departure       : Karachi\n"
                  f"  Arrival         : Lahore\n"
                  f"  Timing          : 09:00 AM — 11:00 AM\n"
                  f"  Seat            : 14B  (Economy)\n"
                  f"  Status          : ✅ Confirmed\n")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)


class SeatReservation:
    FLIGHTS = {
        "PK-301 | Karachi → Lahore":      {"dep": "Karachi",   "arr": "Lahore",    "time": "08:00 AM - 10:00 AM", "price": 8500},
        "PK-303 | Karachi → Islamabad":   {"dep": "Karachi",   "arr": "Islamabad", "time": "11:00 AM - 01:00 PM", "price": 9500},
        "PK-405 | Lahore → Karachi":      {"dep": "Lahore",    "arr": "Karachi",   "time": "02:00 PM - 04:00 PM", "price": 8500},
        "PK-507 | Islamabad → Quetta":    {"dep": "Islamabad", "arr": "Quetta",    "time": "05:00 PM - 07:00 PM", "price": 7500},
        "PK-609 | Peshawar → Karachi":    {"dep": "Peshawar",  "arr": "Karachi",   "time": "06:00 AM - 09:00 AM", "price": 10000},
    }
    SEAT_COSTS  = {"Window": 500, "Middle": 0, "Aisle": 300}
    CLASS_COSTS = {"Economy": 0, "Business": 5000, "First Class": 12000}

    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Seat Reservation")
        self.win.geometry("820x720")
        self.win.configure(bg="#EAF2FB")
        self.win.resizable(False, False)

        tk.Label(self.win, text="✈  SEAT RESERVATION", font=("Arial", 18, "bold"),
                 bg="#154360", fg="white", pady=12).pack(fill="x")

        notebook = ttk.Notebook(self.win)
        notebook.pack(fill="both", expand=True, padx=12, pady=8)

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[10, 5])

        t1 = tk.Frame(notebook, bg="#EAF2FB", padx=20)
        notebook.add(t1, text="👤  Passenger")

        def lrow(parent, label, row, bg, show=""):
            tk.Label(parent, text=label, font=("Arial", 11, "bold"), bg=bg,
                     anchor="w").grid(row=row, column=0, pady=8, sticky="w")
            e = tk.Entry(parent, font=("Arial", 11), width=28, bd=1, relief="solid", show=show)
            e.grid(row=row, column=1, padx=12, pady=8, sticky="w")
            return e

        self.name  = lrow(t1, "Full Name *",       0, "#EAF2FB")
        self.age   = lrow(t1, "Age *",              1, "#EAF2FB")
        self.cnic  = lrow(t1, "CNIC / Passport *", 2, "#EAF2FB")
        self.phone = lrow(t1, "Phone Number *",    3, "#EAF2FB")
        self.email = lrow(t1, "Email Address",     4, "#EAF2FB")

        tk.Button(t1, text="Next ▶", font=("Arial", 12, "bold"), bg="#2980B9", fg="white",
                  padx=20, pady=5, command=lambda: notebook.select(1)).grid(row=6, column=1, pady=15, sticky="e")

        t2 = tk.Frame(notebook, bg="#E9F7EF", padx=20)
        notebook.add(t2, text="✈  Flight Details")

        def frow(parent, label, row, widget):
            tk.Label(parent, text=label, font=("Arial", 11, "bold"), bg="#E9F7EF",
                     anchor="w").grid(row=row, column=0, pady=8, sticky="w")
            widget.grid(row=row, column=1, padx=12, pady=8, sticky="w")

        self.flight_var = tk.StringVar()
        flight_combo = ttk.Combobox(t2, values=list(self.FLIGHTS.keys()),
                                    textvariable=self.flight_var, font=("Arial", 11), width=30, state="readonly")
        frow(t2, "Select Flight *", 0, flight_combo)
        self.flight_var.trace("w", self._update_price)

        self.travel_date = tk.Entry(t2, font=("Arial", 11), width=20, bd=1, relief="solid")
        frow(t2, "Travel Date (DD/MM/YYYY) *", 1, self.travel_date)

        self.seat_class_var = tk.StringVar(value="Economy")
        seat_class_combo = ttk.Combobox(t2, values=["Economy", "Business", "First Class"],
                                        textvariable=self.seat_class_var, font=("Arial", 11), width=18, state="readonly")
        frow(t2, "Travel Class *", 2, seat_class_combo)
        self.seat_class_var.trace("w", self._update_price)

        self.seat_type_var = tk.StringVar(value="Window")
        seat_type_combo = ttk.Combobox(t2, values=["Window", "Middle", "Aisle"],
                                       textvariable=self.seat_type_var, font=("Arial", 11), width=14, state="readonly")
        frow(t2, "Seat Position *", 3, seat_type_combo)
        self.seat_type_var.trace("w", self._update_price)

        self.seat_num_var = tk.StringVar(value="12A")
        seats = [f"{r}{c}" for r in range(1, 31) for c in "ABCDEF"]
        seat_num_combo = ttk.Combobox(t2, values=seats, textvariable=self.seat_num_var,
                                      font=("Arial", 11), width=10, state="readonly")
        frow(t2, "Seat Number", 4, seat_num_combo)

        self.meal_var = tk.StringVar(value="Halal")
        meal_combo = ttk.Combobox(t2, values=["Standard Meal", "Vegetarian", "Halal", "No Meal"],
                                  textvariable=self.meal_var, font=("Arial", 11), width=18, state="readonly")
        frow(t2, "Meal Preference", 5, meal_combo)

        self.luggage_var = tk.StringVar(value="20 kg (Included)")
        luggage_combo = ttk.Combobox(t2, values=["20 kg (Included)", "30 kg (+Rs.1500)", "40 kg (+Rs.3000)"],
                                     textvariable=self.luggage_var, font=("Arial", 11), width=22, state="readonly")
        frow(t2, "Luggage Allowance", 6, luggage_combo)

        self.price_label = tk.Label(t2, text="Base Fare:  Rs. —", font=("Arial", 11),
                                    bg="#E9F7EF", anchor="w")
        self.price_label.grid(row=7, column=0, columnspan=2, pady=(12, 2), sticky="w")
        self.total_label = tk.Label(t2, text="Total:  Rs. —", font=("Arial", 13, "bold"),
                                    bg="#D5F5E3", anchor="w", padx=10, pady=6)
        self.total_label.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(2, 8))

        nav2 = tk.Frame(t2, bg="#E9F7EF")
        nav2.grid(row=9, column=0, columnspan=2, sticky="ew", pady=5)
        tk.Button(nav2, text="◀ Back", font=("Arial", 11), bg="#7F8C8D", fg="white", padx=15, pady=4,
                  command=lambda: notebook.select(0)).pack(side="left")
        tk.Button(nav2, text="Next ▶", font=("Arial", 12, "bold"), bg="#2980B9", fg="white", padx=20, pady=5,
                  command=lambda: notebook.select(2)).pack(side="right")

        t3 = tk.Frame(notebook, bg="#FDF2F8", padx=20)
        notebook.add(t3, text="💳  Payment")

        tk.Label(t3, text="Payment Method", font=("Arial", 13, "bold"), bg="#FDF2F8").pack(pady=12, anchor="w")

        self.pay_var = tk.StringVar(value="Credit / Debit Card")
        pay_methods_frame = tk.Frame(t3, bg="#FDF2F8")
        pay_methods_frame.pack(anchor="w")
        for m in ["Credit / Debit Card", "EasyPaisa", "JazzCash", "SadaPay", "NayaPay", "Bank Transfer"]:
            tk.Radiobutton(pay_methods_frame, text=m, variable=self.pay_var, value=m,
                           font=("Arial", 11), bg="#FDF2F8").pack(anchor="w", pady=2)

        self.pay_detail_frame = tk.Frame(t3, bg="#FDF2F8")
        self.pay_detail_frame.pack(fill="x", pady=8)

        self.card_frame = tk.Frame(self.pay_detail_frame, bg="#EAF2FB", bd=1, relief="solid", padx=10, pady=10)
        tk.Label(self.card_frame, text="Card Number", font=("Arial", 11), bg="#EAF2FB").grid(row=0, column=0, sticky="w", pady=3)
        self.card_num = tk.Entry(self.card_frame, font=("Arial", 11), width=22, bd=1, relief="solid")
        self.card_num.grid(row=0, column=1, padx=8)
        tk.Label(self.card_frame, text="Expiry (MM/YY)", font=("Arial", 11), bg="#EAF2FB").grid(row=1, column=0, sticky="w", pady=3)
        self.card_exp = tk.Entry(self.card_frame, font=("Arial", 11), width=10, bd=1, relief="solid")
        self.card_exp.grid(row=1, column=1, sticky="w", padx=8)
        tk.Label(self.card_frame, text="CVV", font=("Arial", 11), bg="#EAF2FB").grid(row=2, column=0, sticky="w", pady=3)
        self.card_cvv = tk.Entry(self.card_frame, font=("Arial", 11), width=6, show="*", bd=1, relief="solid")
        self.card_cvv.grid(row=2, column=1, sticky="w", padx=8)

        self.mobi_frame = tk.Frame(self.pay_detail_frame, bg="#E8F8F5", bd=1, relief="solid", padx=10, pady=10)
        self.wallet_title = tk.Label(self.mobi_frame, text="EasyPaisa", font=("Arial", 12, "bold"), bg="#E8F8F5")
        self.wallet_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=4)
        tk.Label(self.mobi_frame, text="Registered Number", font=("Arial", 11), bg="#E8F8F5").grid(row=1, column=0, sticky="w", pady=3)
        self.wallet_num = tk.Entry(self.mobi_frame, font=("Arial", 11), width=18, bd=1, relief="solid")
        self.wallet_num.grid(row=1, column=1, padx=8)
        tk.Label(self.mobi_frame, text="Transaction PIN", font=("Arial", 11), bg="#E8F8F5").grid(row=2, column=0, sticky="w", pady=3)
        self.wallet_pin = tk.Entry(self.mobi_frame, font=("Arial", 11), width=10, show="*", bd=1, relief="solid")
        self.wallet_pin.grid(row=2, column=1, sticky="w", padx=8)

        self.bank_frame = tk.Frame(self.pay_detail_frame, bg="#FEF9E7", bd=1, relief="solid", padx=10, pady=10)
        tk.Label(self.bank_frame, text="Account Number", font=("Arial", 11), bg="#FEF9E7").grid(row=0, column=0, sticky="w", pady=3)
        self.bank_acc = tk.Entry(self.bank_frame, font=("Arial", 11), width=22, bd=1, relief="solid")
        self.bank_acc.grid(row=0, column=1, padx=8)
        tk.Label(self.bank_frame, text="Bank Name", font=("Arial", 11), bg="#FEF9E7").grid(row=1, column=0, sticky="w", pady=3)
        self.bank_name = ttk.Combobox(self.bank_frame, values=["HBL", "UBL", "MCB", "Meezan", "Allied Bank", "Bank Alfalah"],
                                      font=("Arial", 11), width=18, state="readonly")
        self.bank_name.grid(row=1, column=1, padx=8)

        self.pay_var.trace("w", self._toggle_pay_fields)
        self._toggle_pay_fields()

        nav3 = tk.Frame(t3, bg="#FDF2F8")
        nav3.pack(fill="x", pady=10)
        tk.Button(nav3, text="◀ Back", font=("Arial", 11), bg="#7F8C8D", fg="white", padx=15, pady=4,
                  command=lambda: notebook.select(1)).pack(side="left")
        tk.Button(nav3, text="✅  CONFIRM & PAY", font=("Arial", 12, "bold"),
                  bg="#1ABC9C", fg="white", padx=15, pady=6,
                  command=self.submit).pack(side="right")

    def _update_price(self, *_):
        fk = self.flight_var.get()
        if not fk:
            return
        base  = self.FLIGHTS[fk]["price"]
        seat  = self.SEAT_COSTS.get(self.seat_type_var.get(), 0)
        cls   = self.CLASS_COSTS.get(self.seat_class_var.get(), 0)
        total = base + seat + cls
        self.price_label.config(text=f"Base: Rs.{base:,}  |  Seat: Rs.{seat:,}  |  Class: Rs.{cls:,}")
        self.total_label.config(text=f"  Total Payable:  Rs. {total:,}")

    def _toggle_pay_fields(self, *_):
        self.card_frame.pack_forget()
        self.mobi_frame.pack_forget()
        self.bank_frame.pack_forget()
        m = self.pay_var.get()
        if m == "Credit / Debit Card":
            self.card_frame.pack(fill="x")
        elif m in ("EasyPaisa", "JazzCash", "SadaPay", "NayaPay"):
            self.wallet_title.config(text=m)
            self.mobi_frame.pack(fill="x")
        elif m == "Bank Transfer":
            self.bank_frame.pack(fill="x")

    def _validate(self):
        errors = []
        if not self.name.get().strip():   errors.append("Full Name is required")
        if not self.age.get().strip().isdigit(): errors.append("Valid Age is required")
        if not self.cnic.get().strip():   errors.append("CNIC / Passport is required")
        if not self.phone.get().strip():  errors.append("Phone Number is required")
        if not self.flight_var.get():     errors.append("Please select a Flight")
        if not self.travel_date.get().strip(): errors.append("Travel Date is required")

        pay = self.pay_var.get()
        if pay == "Credit / Debit Card":
            if len(self.card_num.get().replace(" ", "")) < 16: errors.append("Valid 16-digit Card Number required")
            if not self.card_exp.get().strip():                errors.append("Card Expiry required")
            if len(self.card_cvv.get()) < 3:                   errors.append("Valid CVV required")
        elif pay in ("EasyPaisa", "JazzCash", "SadaPay", "NayaPay"):
            if len(self.wallet_num.get().strip()) < 11: errors.append(f"Valid {pay} number required (11 digits)")
            if len(self.wallet_pin.get().strip()) < 4:  errors.append("Transaction PIN required (min 4 digits)")
        elif pay == "Bank Transfer":
            if not self.bank_acc.get().strip():  errors.append("Account number required")
            if not self.bank_name.get():         errors.append("Select bank name")
        return errors

    def submit(self):
        errors = self._validate()
        if errors:
            messagebox.showerror("Incomplete Form", "\n".join(f"• {e}" for e in errors))
            # Sirf invalid fields clear karo, window band mat karo
            if not self.name.get().strip():   self.name.delete(0, tk.END)
            if not self.age.get().strip().isdigit(): self.age.delete(0, tk.END)
            if not self.cnic.get().strip():   self.cnic.delete(0, tk.END)
            if not self.phone.get().strip():  self.phone.delete(0, tk.END)
            if not self.travel_date.get().strip(): self.travel_date.delete(0, tk.END)
            pay = self.pay_var.get()
            if pay == "Credit / Debit Card":
                if len(self.card_num.get().replace(" ", "")) < 16: self.card_num.delete(0, tk.END)
                if not self.card_exp.get().strip():                self.card_exp.delete(0, tk.END)
                if len(self.card_cvv.get()) < 3:                   self.card_cvv.delete(0, tk.END)
            elif pay in ("EasyPaisa", "JazzCash", "SadaPay", "NayaPay"):
                if len(self.wallet_num.get().strip()) < 11: self.wallet_num.delete(0, tk.END)
                if len(self.wallet_pin.get().strip()) < 4:  self.wallet_pin.delete(0, tk.END)
            elif pay == "Bank Transfer":
                if not self.bank_acc.get().strip(): self.bank_acc.delete(0, tk.END)
            return

        fk   = self.flight_var.get()
        fi   = self.FLIGHTS[fk]
        seat = self.SEAT_COSTS.get(self.seat_type_var.get(), 0)
        cls  = self.CLASS_COSTS.get(self.seat_class_var.get(), 0)
        lug  = {"20 kg (Included)": 0, "30 kg (+Rs.1500)": 1500, "40 kg (+Rs.3000)": 3000}
        total = fi["price"] + seat + cls + lug.get(self.luggage_var.get(), 0)

        booking_code = generate_booking_code()

        print("\n" + "="*50)
        print("       ✈  SEAT RESERVATION CONFIRMED")
        print("="*50)
        print(f"  Booking Code : {booking_code}")
        print(f"  Passenger    : {self.name.get()}")
        print(f"  Age          : {self.age.get()}")
        print(f"  CNIC         : {self.cnic.get()}")
        print(f"  Phone        : {self.phone.get()}")
        print(f"  Email        : {self.email.get().strip() or 'N/A'}")
        print(f"  Flight       : {fk.split('|')[0].strip()}")
        print(f"  Route        : {fi['dep']}  →  {fi['arr']}")
        print(f"  Timing       : {fi['time']}")
        print(f"  Travel Date  : {self.travel_date.get()}")
        print(f"  Class        : {self.seat_class_var.get()}")
        print(f"  Seat         : {self.seat_num_var.get()} ({self.seat_type_var.get()})")
        print(f"  Meal         : {self.meal_var.get()}")
        print(f"  Luggage      : {self.luggage_var.get()}")
        print(f"  Payment      : {self.pay_var.get()}")
        print(f"  Total Paid   : Rs. {total:,}")
        print("="*50 + "\n")

        self._show_confirmation(booking_code, fi, total)

    def _show_confirmation(self, booking_code, fi, total):
        conf = tk.Toplevel()
        conf.title("Booking Confirmed")
        conf.geometry("680x720")
        conf.configure(bg="white")
        conf.resizable(False, False)

        tk.Label(conf, text="🎉  BOOKING CONFIRMED!", font=("Arial", 18, "bold"),
                 bg="#1ABC9C", fg="white", pady=15).pack(fill="x")

        card = tk.Frame(conf, bg="#F4F6F7", bd=1, relief="solid")
        card.pack(padx=20, pady=12, fill="x")

        tk.Label(card, text="✈  BOARDING PASS", font=("Arial", 13, "bold"),
                 bg="#154360", fg="white", pady=8).pack(fill="x")

        def irow(label, value, bold=False):
            f = tk.Frame(card, bg="#F4F6F7")
            f.pack(fill="x", padx=15, pady=2)
            tk.Label(f, text=label, font=("Arial", 10), bg="#F4F6F7",
                     fg="#566573", width=20, anchor="w").pack(side="left")
            tk.Label(f, text=value, font=("Arial", 11, "bold" if bold else "normal"),
                     bg="#F4F6F7", fg="#1B2631", anchor="w").pack(side="left")

        irow("Passenger",      self.name.get(),                       bold=True)
        irow("CNIC/Passport",  self.cnic.get())
        irow("Phone",          self.phone.get())
        irow("Flight",         self.flight_var.get().split("|")[0],   bold=True)
        irow("Route",          f"{fi['dep']}  →  {fi['arr']}",        bold=True)
        irow("Timing",         fi["time"])
        irow("Travel Date",    self.travel_date.get())
        irow("Class",          self.seat_class_var.get())
        irow("Seat",           f"{self.seat_num_var.get()} ({self.seat_type_var.get()})")
        irow("Meal",           self.meal_var.get())
        irow("Luggage",        self.luggage_var.get())
        irow("Payment",        self.pay_var.get())
        tk.Frame(card, bg="#BDC3C7", height=1).pack(fill="x", padx=15, pady=6)
        irow("Total Paid",     f"Rs. {total:,}",                      bold=True)

        cf = tk.Frame(conf, bg="#EAF2FB", bd=1, relief="solid")
        cf.pack(padx=20, pady=6, fill="x")
        tk.Label(cf, text="BOOKING CODE", font=("Arial", 10), bg="#EAF2FB", fg="#566573").pack(pady=(8, 2))
        tk.Label(cf, text=booking_code, font=("Courier", 22, "bold"),
                 bg="#EAF2FB", fg="#154360").pack(pady=4)

        qf = tk.Frame(conf, bg="white")
        qf.pack(pady=4)
        tk.Label(qf, text="Scan QR Code at Airport", font=("Arial", 10),
                 bg="white", fg="#808B96").pack()
        qr_canvas = tk.Canvas(qf, width=120, height=120, bg="white", highlightthickness=0)
        qr_canvas.pack(pady=4)
        draw_qr_pattern(qr_canvas, booking_code, 10, 10, 100)

        tk.Button(conf, text="CLOSE", font=("Arial", 12, "bold"),
                  bg="#E74C3C", fg="white", pady=8,
                  command=lambda: [conf.destroy(), self.win.destroy()]).pack(fill="x", padx=20, pady=10)


class MainMenu:
    def __init__(self):
        self.hotel = Hotel()

        self.main_window = tk.Tk()
        self.main_window.title("Flight Reservation System")
        self.main_window.geometry("600x520")
        self.main_window.configure(bg="#AED6F1")
        self.main_window.resizable(False, False)

        tk.Label(self.main_window, text="✈  FLIGHT RESERVATION SYSTEM",
                 font=("Arial", 20, "bold"), bg="#154360", fg="white", pady=15).pack(fill="x")
        tk.Label(self.main_window, text="Pakistan Airlines — Booking Portal",
                 font=("Arial", 12, "italic"), bg="#AED6F1", fg="#1B4F72").pack(pady=20)

        btn = {"font": ("Arial", 13, "bold"), "width": 24, "height": 2, "fg": "white", "cursor": "hand2", "bd": 0}

        tk.Button(self.main_window, text="✈   Seat Reservation",
                  command=lambda: SeatReservation(), bg="#1ABC9C", **btn).pack(pady=8)
        tk.Button(self.main_window, text="🎫   Check Ticket",
                  command=lambda: TicketCheckerApp(), bg="#3498DB", **btn).pack(pady=8)
        tk.Button(self.main_window, text="🏨   Hotel Booking",
                  command=lambda: self.hotel.open_booking(), bg="#9B59B6", **btn).pack(pady=8)
        tk.Button(self.main_window, text="🚪   Exit",
                  command=self.main_window.quit, bg="#E74C3C", **btn).pack(pady=8)

        tk.Label(self.main_window, text="Developed in Python  •  Tkinter GUI",
                 font=("Arial", 9, "italic"), bg="#AED6F1", fg="#5D6D7E").pack(side="bottom", pady=15)

        self.main_window.mainloop()


if __name__ == "__main__":
    MainMenu()