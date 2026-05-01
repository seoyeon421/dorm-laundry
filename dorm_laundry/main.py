import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("백석대학교 기숙사 세탁기 예약 시스템")
app.geometry("560x780")
app.resizable(False, False)

BG = "#F3F7FC"
BLUE = "#005BAC"
DARK = "#003C7A"
CARD = "#FFFFFF"
LIGHT = "#EEF4FB"
RED = "#E53935"
GRAY = "#BFC4CC"

current_user = {
    "student_id": "",
    "password": "",
    "room": ""
}

reservations = {
    "세탁기 1": {},
    "세탁기 2": {}
}

machine_status = {
    "세탁기 3": "사용 가능",
    "세탁기 4": "사용중"
}

penalty_count = 1

history = [
    "2026-03-20 : 세탁기 3 사용 완료",
    "2026-03-22 : 세탁기 1 예약 후 노쇼",
    "2026-03-24 : 세탁기 4 사용 완료",
]

times = [
    "09:00 ~ 10:00", "10:00 ~ 11:00", "11:00 ~ 12:00",
    "12:00 ~ 13:00", "13:00 ~ 14:00", "14:00 ~ 15:00",
    "15:00 ~ 16:00", "16:00 ~ 17:00", "17:00 ~ 18:00",
    "18:00 ~ 19:00", "19:00 ~ 20:00", "20:00 ~ 21:00"
]

dates = []
today = datetime.now()
for i in range(7):
    day = today + timedelta(days=i)
    dates.append(day.strftime("%Y-%m-%d"))


def clear():
    for widget in app.winfo_children():
        widget.destroy()


def make_button(parent, text, command, color=BLUE, width=300, height=48):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=14,
        fg_color=color,
        hover_color="#004A91",
        text_color="white",
        font=("Arial", 15, "bold")
    )


def header(title):
    top = ctk.CTkFrame(app, fg_color=BLUE, height=75, corner_radius=0)
    top.pack(fill="x")
    ctk.CTkLabel(
        top,
        text=title,
        font=("Arial", 24, "bold"),
        text_color="white"
    ).pack(pady=20)


def show_login():
    global logo_img

    clear()
    app.configure(fg_color=BG)

    login_card = ctk.CTkFrame(app, fg_color=CARD, corner_radius=28)
    login_card.pack(padx=45, pady=55, fill="both", expand=True)

    logo_img = ctk.CTkImage(
        light_image=Image.open("bu_logo.png"),
        size=(125, 125)
    )

    ctk.CTkLabel(login_card, image=logo_img, text="").pack(pady=(45, 10))

    ctk.CTkLabel(
        login_card,
        text="백석대학교",
        font=("Arial", 25, "bold"),
        text_color=DARK
    ).pack(pady=(5, 3))

    ctk.CTkLabel(
        login_card,
        text="기숙사 세탁기 예약 시스템",
        font=("Arial", 20, "bold"),
        text_color=DARK
    ).pack(pady=(0, 30))

    student_entry = ctk.CTkEntry(login_card, placeholder_text="학번", width=320, height=46)
    student_entry.pack(pady=8)

    password_entry = ctk.CTkEntry(login_card, placeholder_text="비밀번호", width=320, height=46, show="*")
    password_entry.pack(pady=8)

    room_entry = ctk.CTkEntry(login_card, placeholder_text="방번호", width=320, height=46)
    room_entry.pack(pady=8)

    def login():
        if student_entry.get() == "" or password_entry.get() == "" or room_entry.get() == "":
            messagebox.showwarning("입력 오류", "학번, 비밀번호, 방번호를 모두 입력해주세요.")
            return

        current_user["student_id"] = student_entry.get()
        current_user["password"] = password_entry.get()
        current_user["room"] = room_entry.get()

        messagebox.showinfo("로그인 완료", "로그인되었습니다.")
        show_home()

    make_button(login_card, "로그인", login, width=320).pack(pady=30)


def show_home():
    clear()
    app.configure(fg_color=BG)

    header("홈")

    card = ctk.CTkFrame(app, fg_color=CARD, corner_radius=28)
    card.pack(padx=35, pady=35, fill="both", expand=True)

    ctk.CTkLabel(card, text="🧺", font=("Arial", 60)).pack(pady=(45, 10))

    ctk.CTkLabel(
        card,
        text="세탁실 예약 시스템",
        font=("Arial", 25, "bold"),
        text_color=DARK
    ).pack(pady=8)

    ctk.CTkLabel(
        card,
        text="원하는 메뉴를 선택해주세요.",
        font=("Arial", 14),
        text_color="#555555"
    ).pack(pady=(0, 35))

    make_button(card, "세탁기 예약", show_reservation_page).pack(pady=10)
    make_button(card, "내 페이지", show_mypage).pack(pady=10)
    make_button(card, "이용 안내", show_guide).pack(pady=10)

    make_button(card, "로그아웃", show_login, color="#555555", width=300).pack(pady=(35, 0))


def show_reservation_page():
    clear()
    app.configure(fg_color=BG)

    header("세탁기 예약")

    scroll = ctk.CTkScrollableFrame(app, fg_color=BG, width=520, height=680)
    scroll.pack(fill="both", expand=True)

    ctk.CTkLabel(
        scroll,
        text="세탁기를 선택하거나 상태를 확인하세요.",
        font=("Arial", 15),
        text_color="#333333"
    ).pack(pady=(20, 10))

    for machine in ["세탁기 1", "세탁기 2"]:
        machine_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
        machine_card.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(machine_card, text="👕", font=("Arial", 42)).pack(pady=(18, 5))
        ctk.CTkLabel(machine_card, text=machine, font=("Arial", 20, "bold"), text_color=DARK).pack()
        ctk.CTkLabel(machine_card, text="예약 전용 세탁기", font=("Arial", 13), text_color="#555555").pack(pady=4)

        make_button(machine_card, "예약하기", lambda m=machine: show_date_page(m), width=180).pack(pady=(10, 20))

    for machine, status in machine_status.items():
        machine_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
        machine_card.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(machine_card, text="👕", font=("Arial", 42)).pack(pady=(18, 5))
        ctk.CTkLabel(machine_card, text=machine, font=("Arial", 20, "bold"), text_color=DARK).pack()
        ctk.CTkLabel(machine_card, text="선착순 전용 세탁기", font=("Arial", 13), text_color="#555555").pack(pady=4)

        status_color = BLUE if status == "사용 가능" else RED

        ctk.CTkButton(
            machine_card,
            text=status,
            width=180,
            height=44,
            corner_radius=14,
            fg_color=status_color,
            hover_color=status_color,
            text_color="white",
            font=("Arial", 15, "bold"),
            state="disabled"
        ).pack(pady=(10, 20))

    make_button(scroll, "홈으로", show_home, width=180).pack(pady=25)


def show_date_page(machine):
    clear()
    app.configure(fg_color=BG)

    header(f"{machine} 날짜 선택")

    card = ctk.CTkFrame(app, fg_color=CARD, corner_radius=25)
    card.pack(padx=35, pady=30, fill="both", expand=True)

    ctk.CTkLabel(
        card,
        text="예약 날짜를 선택하세요.",
        font=("Arial", 18, "bold"),
        text_color=DARK
    ).pack(pady=(35, 20))

    for date in dates:
        make_button(
            card,
            date,
            lambda d=date, m=machine: show_time_page(m, d),
            width=260,
            height=45
        ).pack(pady=6)

    bottom = ctk.CTkFrame(card, fg_color="transparent")
    bottom.pack(pady=25)

    make_button(bottom, "뒤로가기", show_reservation_page, width=135).grid(row=0, column=0, padx=8)
    make_button(bottom, "홈으로", show_home, width=135).grid(row=0, column=1, padx=8)


def show_time_page(machine, date):
    clear()
    app.configure(fg_color=BG)

    header(f"{machine} 예약")

    card = ctk.CTkFrame(app, fg_color=CARD, corner_radius=25)
    card.pack(padx=35, pady=30, fill="both", expand=True)

    ctk.CTkLabel(
        card,
        text=f"예약 날짜: {date}",
        font=("Arial", 17, "bold"),
        text_color=DARK
    ).pack(pady=(25, 10))

    ctk.CTkLabel(
        card,
        text="원하는 시간을 선택하세요.",
        font=("Arial", 14),
        text_color="#333333"
    ).pack(pady=(0, 20))

    if date not in reservations[machine]:
        reservations[machine][date] = []

    grid = ctk.CTkFrame(card, fg_color="transparent")
    grid.pack()

    for i, time in enumerate(times):
        reserved = time in reservations[machine][date]

        if reserved:
            text = f"{time.split(' ~ ')[0]}\n예약됨"
            color = GRAY
            state = "disabled"
        else:
            text = time.split(" ~ ")[0]
            color = BLUE
            state = "normal"

        ctk.CTkButton(
            grid,
            text=text,
            width=100,
            height=52,
            corner_radius=12,
            fg_color=color,
            hover_color="#004A91",
            text_color="white",
            state=state,
            font=("Arial", 13, "bold"),
            command=lambda m=machine, d=date, t=time: reserve_time(m, d, t)
        ).grid(row=i // 3, column=i % 3, padx=7, pady=7)

    ctk.CTkLabel(
        card,
        text="회색 버튼은 이미 예약된 시간입니다.",
        font=("Arial", 12),
        text_color="#777777"
    ).pack(pady=18)

    bottom = ctk.CTkFrame(card, fg_color="transparent")
    bottom.pack(pady=20)

    make_button(bottom, "날짜 선택", lambda: show_date_page(machine), width=135).grid(row=0, column=0, padx=8)
    make_button(bottom, "홈으로", show_home, width=135).grid(row=0, column=1, padx=8)


def reserve_time(machine, date, time):
    if date not in reservations[machine]:
        reservations[machine][date] = []

    if time in reservations[machine][date]:
        messagebox.showwarning("예약 불가", "이미 예약된 시간입니다.")
        return

    reservations[machine][date].append(time)

    today_text = datetime.now().strftime("%Y-%m-%d")
    history.append(f"{today_text} : {machine} / {date} / {time} 예약 완료")

    messagebox.showinfo(
        "예약 완료",
        f"{machine}\n예약 날짜: {date}\n예약 시간: {time}\n예약되었습니다."
    )

    show_time_page(machine, date)


def get_first_reservation():
    for machine, date_data in reservations.items():
        for date, reserved_times in date_data.items():
            if reserved_times:
                return machine, date, reserved_times[0]
    return None, None, None


def show_mypage():
    clear()
    app.configure(fg_color=BG)

    header("내 페이지")

    scroll = ctk.CTkScrollableFrame(app, fg_color=BG, width=520, height=680)
    scroll.pack(fill="both", expand=True)

    user_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
    user_card.pack(padx=20, pady=15, fill="x")

    ctk.CTkLabel(user_card, text="사용자 정보", font=("Arial", 20, "bold"), text_color=DARK).pack(anchor="w", padx=24, pady=(22, 10))
    ctk.CTkLabel(user_card, text=f"학번: {current_user['student_id']}", font=("Arial", 15)).pack(anchor="w", padx=24, pady=5)
    ctk.CTkLabel(user_card, text=f"방번호: {current_user['room']}", font=("Arial", 15)).pack(anchor="w", padx=24, pady=(5, 22))

    notice_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
    notice_card.pack(padx=20, pady=10, fill="x")

    ctk.CTkLabel(notice_card, text="공지사항", font=("Arial", 20, "bold"), text_color=DARK).pack(anchor="w", padx=24, pady=(22, 10))

    notice_box = ctk.CTkFrame(notice_card, fg_color=LIGHT, corner_radius=14)
    notice_box.pack(padx=24, pady=(5, 22), fill="x")

    notices = [
        "- 예약 세탁기 1, 2는 날짜와 시간대를 선택해 이용할 수 있습니다.",
        "- 예약은 오늘부터 최대 7일까지 가능합니다.",
        "- 선착순 세탁기 3, 4는 비어 있을 때 바로 사용할 수 있습니다.",
        "- 예약 후 5분 이내에 사용하지 않으면 노쇼로 처리됩니다.",
        "- 패널티를 받으면 세탁기 1, 2는 2주간 예약이 제한됩니다."
    ]

    for n in notices:
        color = RED if "노쇼" in n or "패널티" in n or "제한" in n else "#111111"
        ctk.CTkLabel(
            notice_box,
            text=n,
            font=("Arial", 14, "bold" if color == RED else "normal"),
            text_color=color,
            wraplength=430,
            justify="left"
        ).pack(anchor="w", padx=18, pady=6)

    reservation_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
    reservation_card.pack(padx=20, pady=10, fill="x")

    ctk.CTkLabel(reservation_card, text="예약 상태", font=("Arial", 20, "bold"), text_color=DARK).pack(anchor="w", padx=24, pady=(22, 10))

    machine, date, time = get_first_reservation()

    if machine:
        ctk.CTkLabel(reservation_card, text=f"현재 예약 세탁기: {machine}", font=("Arial", 15)).pack(anchor="w", padx=24, pady=4)
        ctk.CTkLabel(reservation_card, text=f"예약 날짜: {date}", font=("Arial", 15, "bold"), text_color=BLUE).pack(anchor="w", padx=24, pady=4)
        ctk.CTkLabel(reservation_card, text=f"예약 시간: {time}", font=("Arial", 15, "bold"), text_color=BLUE).pack(anchor="w", padx=24, pady=4)
        ctk.CTkLabel(reservation_card, text="예약 상태: 예약 완료", font=("Arial", 15, "bold"), text_color=BLUE).pack(anchor="w", padx=24, pady=(4, 22))
    else:
        ctk.CTkLabel(reservation_card, text="현재 예약 내역이 없습니다.", font=("Arial", 15)).pack(anchor="w", padx=24, pady=(5, 22))

    penalty_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
    penalty_card.pack(padx=20, pady=10, fill="x")

    ctk.CTkLabel(penalty_card, text="패널티 현황", font=("Arial", 20, "bold"), text_color=DARK).pack(anchor="w", padx=24, pady=(22, 10))
    ctk.CTkLabel(penalty_card, text=f"현재 패널티: {penalty_count}회", font=("Arial", 15, "bold"), text_color=RED).pack(anchor="w", padx=24, pady=4)
    ctk.CTkLabel(penalty_card, text="예약 제한 기간: 2026-04-08까지", font=("Arial", 15, "bold"), text_color=RED).pack(anchor="w", padx=24, pady=4)
    ctk.CTkLabel(penalty_card, text="이용 가능 세탁기: 세탁기 3, 4", font=("Arial", 15)).pack(anchor="w", padx=24, pady=(4, 22))

    history_card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=22)
    history_card.pack(padx=20, pady=10, fill="x")

    ctk.CTkLabel(history_card, text="사용 내역", font=("Arial", 20, "bold"), text_color=DARK).pack(anchor="w", padx=24, pady=(22, 10))

    for h in history[-6:]:
        ctk.CTkLabel(history_card, text=h, font=("Arial", 14), wraplength=430).pack(anchor="w", padx=24, pady=7)

    make_button(scroll, "홈으로", show_home, width=180).pack(pady=25)


def show_guide():
    clear()
    app.configure(fg_color=BG)

    header("이용 안내")

    card = ctk.CTkFrame(app, fg_color=CARD, corner_radius=25)
    card.pack(padx=35, pady=30, fill="both", expand=True)

    guide_text = """
1. 세탁기 1, 2는 예약 전용입니다.

2. 예약은 오늘부터 최대 7일까지 가능합니다.

3. 예약 가능 시간은 오전 9시부터 오후 9시까지입니다.

4. 예약은 1시간 단위로 가능합니다.

5. 이미 예약된 시간은 회색으로 표시됩니다.

6. 세탁기 3, 4는 선착순 전용이며 상태만 확인할 수 있습니다.

7. 예약 후 5분 이내에 사용하지 않으면 노쇼 처리됩니다.

8. 패널티가 있으면 예약 전용 세탁기 이용이 제한될 수 있습니다.
"""

    ctk.CTkLabel(
        card,
        text=guide_text,
        font=("Arial", 15),
        text_color="#222222",
        justify="left",
        wraplength=430
    ).pack(padx=28, pady=35)

    make_button(card, "홈으로", show_home, width=180).pack(pady=20)


show_login()
app.mainloop()