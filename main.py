from modules.storage import initialize_data_files, load_data
from modules.fintrack import transaction_menu
from modules.task_manager import task_manager_menu


def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah."""
    if amount < 0:
        return "-Rp" + f"{abs(amount):,.0f}".replace(",", ".")
    return "Rp" + f"{amount:,.0f}".replace(",", ".")


def show_overall_summary():
    """Menampilkan ringkasan gabungan dari FinTrack dan Daily Task Manager."""
    transactions = load_data("transactions")
    tasks = load_data("tasks")

    total_income = 0
    total_expense = 0

    for trx in transactions:
        if trx["type"] == "income":
            total_income += trx["amount"]
        elif trx["type"] == "expense":
            total_expense += trx["amount"]

    balance = total_income - total_expense

    pending_tasks = 0
    completed_tasks = 0

    for task in tasks:
        if task["status"] == "Completed":
            completed_tasks += 1
        else:
            pending_tasks += 1

    print("\n" + "=" * 45)
    print("         RINGKASAN UTAMA SEHARI-HARI")
    print("=" * 45)
    print("[Keuangan - FinTrack]")
    print("Saldo Saat Ini  :", format_rupiah(balance))
    print("Total Transaksi :", len(transactions))
    print("-" * 45)
    print("[Aktivitas - Daily Task Manager]")
    print("Tugas Pending   :", pending_tasks)
    print("Tugas Selesai   :", completed_tasks)
    print("=" * 45)

def show_main_menu():
    print("\n" + "=" * 45)
    print("             SEHARI-HARI")
    print("       Daily Life Management System")
    print("=" * 45)

    print("1. FinTrack ")
    print("2. Daily Task Manager ")
    print("3. Ringkasan Utama")
    print("0. Exit")

    print("=" * 45)

def main():
    initialize_data_files()

    while True:
        show_main_menu()

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            transaction_menu()

        elif choice == "2":
            task_manager_menu()

        elif choice == "3":
            show_overall_summary()

        elif choice == "0":
            print("\nTerima kasih telah menggunakan Sehari-Hari!")
            break

        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()