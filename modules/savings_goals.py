from datetime import datetime
from modules.storage import load_data, save_data


def generate_savings_id(goals):
    """Membuat ID target tabungan secara otomatis."""
    if not goals:
        return "SAV001"

    numbers = []

    for goal in goals:
        try:
            number = int(goal["id"][3:])
            numbers.append(number)
        except (ValueError, KeyError, TypeError):
            continue

    if not numbers:
        return "SAV001"

    return f"SAV{max(numbers) + 1:03d}"


def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah."""
    return f"Rp{amount:,.0f}".replace(",", ".")

# CREATE SAVINGS GOAL

def add_savings_goal():
    """Menambahkan target tabungan baru."""
    goals = load_data("savings_goals")

    print("\n" + "=" * 45)
    print("          TAMBAH TARGET TABUNGAN")
    print("=" * 45)

    name = input("Nama target tabungan: ").strip()

    if not name:
        print("Nama target tidak boleh kosong.")
        return

    try:
        target_amount = int(input("Jumlah target (Rp): ").strip())

        if target_amount <= 0:
            print("Jumlah target harus lebih dari 0.")
            return

    except ValueError:
        print("Jumlah target harus berupa angka.")
        return

    deadline = input("Deadline (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("Format tanggal tidak valid.")
        return

    goal = {
        "id": generate_savings_id(goals),
        "name": name,
        "target_amount": target_amount,
        "current_amount": 0,
        "deadline": deadline
    }

    goals.append(goal)
    save_data("savings_goals", goals)

    print("\nTarget tabungan berhasil ditambahkan!")
    print(f"ID Target : {goal['id']}")
    print(f"Nama      : {goal['name']}")
    print(f"Target    : {format_rupiah(target_amount)}")
    print(f"Deadline  : {deadline}")

# READ SAVINGS GOALS

def view_savings_goals():
    """Menampilkan seluruh target tabungan."""
    goals = load_data("savings_goals")

    print("\n" + "=" * 55)
    print("                 DAFTAR TARGET TABUNGAN")
    print("=" * 55)

    if not goals:
        print("Belum ada target tabungan.")
        return

    for goal in goals:
        target = goal["target_amount"]
        current = goal["current_amount"]

        progress = (current / target) * 100
        remaining = max(target - current, 0)

        print(f"\nID Target        : {goal['id']}")
        print(f"Nama             : {goal['name']}")
        print(f"Target           : {format_rupiah(target)}")
        print(f"Tabungan Saat Ini: {format_rupiah(current)}")
        print(f"Sisa Target      : {format_rupiah(remaining)}")
        print(f"Deadline         : {goal['deadline']}")
        print(f"Progress         : {progress:.2f}%")

        if current >= target:
            print("Status           : Target Tercapai")
        else:
            print("Status           : Dalam Proses")

        print("-" * 55)

# UPDATE SAVINGS GOAL (TAMBAH TABUNGAN)

def add_savings_contribution():
    """Menambahkan uang ke target tabungan."""
    goals = load_data("savings_goals")

    print("\n" + "=" * 45)
    print("        TAMBAH UANG TABUNGAN")
    print("=" * 45)

    if not goals:
        print("Belum ada target tabungan.")
        return

    for goal in goals:
        print(f"{goal['id']} - {goal['name']} ({format_rupiah(goal['current_amount'])} / {format_rupiah(goal['target_amount'])})")

    goal_id = input("\nMasukkan ID target: ").strip().upper()

    selected_goal = None

    for goal in goals:
        if goal["id"] == goal_id:
            selected_goal = goal
            break

    if selected_goal is None:
        print("Target tabungan tidak ditemukan.")
        return

    try:
        amount = int(input("Jumlah uang yang ditabung (Rp): ").strip())

        if amount <= 0:
            print("Jumlah uang harus lebih dari 0.")
            return

    except ValueError:
        print("Jumlah uang harus berupa angka.")
        return

    selected_goal["current_amount"] += amount
    save_data("savings_goals", goals)

    print("\nUang tabungan berhasil ditambahkan!")
    print(f"Target        : {selected_goal['name']}")
    print(f"Penambahan    : {format_rupiah(amount)}")
    print(f"Total Tabungan: {format_rupiah(selected_goal['current_amount'])}")

    progress = (selected_goal["current_amount"] / selected_goal["target_amount"]) * 100
    print(f"Progress      : {progress:.2f}%")

    if selected_goal["current_amount"] >= selected_goal["target_amount"]:
        print("Selamat! Target tabungan berhasil tercapai!")

# DELETE SAVINGS GOAL

def delete_savings_goal():
    """Menghapus target tabungan berdasarkan ID."""
    goals = load_data("savings_goals")

    print("\n" + "=" * 45)
    print("          HAPUS TARGET TABUNGAN")
    print("=" * 45)

    if not goals:
        print("Belum ada target tabungan.")
        return

    for goal in goals:
        print(f"{goal['id']} - {goal['name']} (Terkumpul: {format_rupiah(goal['current_amount'])})")

    goal_id = input("\nMasukkan ID target yang ingin dihapus: ").strip().upper()

    for goal in goals:
        if goal["id"] == goal_id:
            print("\nTarget ditemukan:")
            print(f"Nama     : {goal['name']}")
            print(f"Target   : {format_rupiah(goal['target_amount'])}")
            print(f"Terkumpul: {format_rupiah(goal['current_amount'])}")

            confirmation = input("Yakin ingin menghapus target ini? (y/n): ").strip().lower()

            if confirmation == "y":
                goals.remove(goal)
                save_data("savings_goals", goals)
                print("Target tabungan berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")
            return

    print("Target tabungan tidak ditemukan.")

# MENU SAVINGS GOALS

def savings_goals_menu():
    """Menu utama pengelolaan target tabungan."""
    while True:
        print("\n" + "=" * 45)
        print("           SAVINGS GOALS")
        print("=" * 45)
        print("1. Tambah Target Tabungan")
        print("2. Lihat Target Tabungan")
        print("3. Tambah Uang Tabungan")
        print("4. Hapus Target Tabungan")
        print("0. Kembali ke FinTrack")
        print("=" * 45)

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            add_savings_goal()
        elif choice == "2":
            view_savings_goals()
        elif choice == "3":
            add_savings_contribution()
        elif choice == "4":
            delete_savings_goal()
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
