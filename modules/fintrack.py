from datetime import datetime
from modules.storage import load_data, save_data
from modules.budget import budget_menu
from modules.savings_goals import savings_goals_menu
from modules.dashboard import show_fintrack_dashboard, show_monthly_report

# HELPER FUNCTIONS

def generate_transaction_id(transactions):
    """Membuat ID transaksi secara otomatis."""
    highest_id = 0

    for transaction in transactions:
        try:
            number = int(transaction["id"][3:])
            if number > highest_id:
                highest_id = number
        except (ValueError, KeyError, TypeError):
            continue

    return f"TRX{highest_id + 1:03d}"

def validate_date(date_text):
    """Memeriksa format tanggal YYYY-MM-DD."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah."""
    return "Rp" + f"{amount:,.0f}".replace(",", ".")

# CREATE TRANSACTION

def add_transaction():
    transactions = load_data("transactions")

    print("\n========== TAMBAH TRANSAKSI ==========")
    print("1. Pemasukan")
    print("2. Pengeluaran")

    choice = input("Pilih jenis transaksi: ").strip()

    if choice == "1":
        transaction_type = "income"
    elif choice == "2":
        transaction_type = "expense"
    else:
        print("Pilihan tidak valid.")
        return

    category = input("Kategori: ").strip()
    if not category:
        print("Kategori tidak boleh kosong.")
        return

    description = input("Deskripsi: ").strip()
    if not description:
        print("Deskripsi tidak boleh kosong.")
        return

    try:
        amount = int(input("Nominal (Rupiah): ").strip())

        if amount <= 0:
            print("Nominal harus lebih dari nol.")
            return

    except ValueError:
        print("Nominal harus berupa angka bulat.")
        return

    date = input("Tanggal (YYYY-MM-DD): ").strip()

    if not validate_date(date):
        print("Format tanggal tidak valid.")
        return

    transaction = {
        "id": generate_transaction_id(transactions),
        "type": transaction_type,
        "category": category,
        "description": description,
        "amount": amount,
        "date": date
    }

    transactions.append(transaction)
    save_data("transactions", transactions)

    print("\nTransaksi berhasil ditambahkan!")
    print("ID:", transaction["id"])

# READ TRANSACTIONS

def view_transactions():
    transactions = load_data("transactions")

    print("\n========== DAFTAR TRANSAKSI ==========")

    if not transactions:
        print("Belum ada transaksi.")
        return

    for transaction in transactions:
        transaction_name = (
            "Pemasukan"
            if transaction["type"] == "income"
            else "Pengeluaran"
        )

        print("-" * 45)
        print("ID         :", transaction["id"])
        print("Jenis      :", transaction_name)
        print("Kategori   :", transaction["category"])
        print("Deskripsi  :", transaction["description"])
        print("Nominal    :", format_rupiah(transaction["amount"]))
        print("Tanggal    :", transaction["date"])

    print("-" * 45)

# UPDATE TRANSACTION

def update_transaction():
    transactions = load_data("transactions")

    print("\n========== UBAH TRANSAKSI ==========")

    if not transactions:
        print("Belum ada transaksi.")
        return

    transaction_id = input("Masukkan ID transaksi: ").strip().upper()

    for transaction in transactions:
        if transaction["id"] == transaction_id:

            print("\nTransaksi ditemukan!")
            print("Kosongkan input jika tidak ingin mengubah data.")

            new_category = input("Kategori baru: ").strip()
            if new_category:
                transaction["category"] = new_category

            new_description = input("Deskripsi baru: ").strip()
            if new_description:
                transaction["description"] = new_description

            new_amount = input("Nominal baru: ").strip()
            if new_amount:
                try:
                    amount = int(new_amount)

                    if amount <= 0:
                        print("Nominal harus lebih dari nol.")
                        return

                    transaction["amount"] = amount

                except ValueError:
                    print("Nominal harus berupa angka bulat.")
                    return

            new_date = input("Tanggal baru (YYYY-MM-DD): ").strip()
            if new_date:
                if not validate_date(new_date):
                    print("Format tanggal tidak valid.")
                    return

                transaction["date"] = new_date

            save_data("transactions", transactions)

            print("\nTransaksi berhasil diperbarui!")
            return

    print("Transaksi tidak ditemukan.")

# DELETE TRANSACTION

def delete_transaction():
    transactions = load_data("transactions")

    print("\n========== HAPUS TRANSAKSI ==========")

    if not transactions:
        print("Belum ada transaksi.")
        return

    transaction_id = input("Masukkan ID transaksi: ").strip().upper()

    for transaction in transactions:
        if transaction["id"] == transaction_id:

            print("\nTransaksi ditemukan:")
            print("Deskripsi:", transaction["description"])
            print("Nominal:", format_rupiah(transaction["amount"]))

            confirmation = input("Yakin ingin menghapus? (y/n): ").strip().lower()

            if confirmation == "y":
                transactions.remove(transaction)
                save_data("transactions", transactions)
                print("Transaksi berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")

            return

    print("Transaksi tidak ditemukan.")

# FINTRACK MENU

def transaction_management_menu():
    while True:
        print("\n" + "=" * 45)
        print("       TRANSACTION MANAGEMENT")
        print("=" * 45)

        print("1. Tambah Transaksi")
        print("2. Lihat Transaksi")
        print("3. Ubah Transaksi")
        print("4. Hapus Transaksi")
        print("0. Kembali")

        print("=" * 45)

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def transaction_menu():
    while True:
        print("\n" + "=" * 45)
        print("                FINTRACK")
        print("         PERSONAL FINANCE MANAGER")
        print("=" * 45)

        print("1. Transaction Management")
        print("2. Budget Management")
        print("3. Savings Goals")
        print("4. Dashboard Keuangan")
        print("5. Laporan Keuangan Bulanan")
        print("0. Kembali ke Menu Utama")

        print("=" * 45)

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            transaction_management_menu()
        elif choice == "2":
            budget_menu()
        elif choice == "3":
            savings_goals_menu()
        elif choice == "4":
            show_fintrack_dashboard()
        elif choice == "5":
            show_monthly_report()
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")