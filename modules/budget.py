
from modules.storage import load_data, save_data


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def generate_budget_id(budgets):
    """Membuat ID anggaran secara otomatis."""

    highest_id = 0

    for budget in budgets:
        try:
            number = int(budget["id"][3:])

            if number > highest_id:
                highest_id = number

        except (ValueError, KeyError, TypeError):
            continue

    return f"BUD{highest_id + 1:03d}"


def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah."""

    return "Rp" + f"{amount:,.0f}".replace(",", ".")


def get_category_spending(category, transactions):
    """
    Menghitung total pengeluaran berdasarkan kategori.
    Hanya transaksi dengan type expense yang dihitung.
    """

    total_spending = 0

    for transaction in transactions:
        if (
            transaction.get("type") == "expense"
            and transaction.get("category", "").strip().casefold()
            == category.strip().casefold()
        ):
            total_spending += transaction.get("amount", 0)

    return total_spending


def calculate_budget_usage(budget, transactions):
    """Menghitung penggunaan dan status anggaran."""

    spending = get_category_spending(
        budget["category"],
        transactions
    )

    budget_amount = budget["amount"]

    percentage = (spending / budget_amount) * 100
    remaining = budget_amount - spending

    if percentage > 100:
        status = "Melewati batas"
    elif percentage >= 80:
        status = "Hampir habis"
    else:
        status = "Aman"

    return spending, percentage, remaining, status


def input_positive_amount(message):
    """Meminta input nominal positif."""

    try:
        amount = int(input(message).strip())

        if amount <= 0:
            print("Nominal harus lebih dari nol.")
            return None

        return amount

    except ValueError:
        print("Nominal harus berupa angka bulat.")
        return None


# ==========================================
# CREATE BUDGET
# ==========================================

def add_budget():

    budgets = load_data("budgets")

    print("\n========== TAMBAH ANGGARAN ==========")

    category = input("Nama kategori: ").strip()

    if not category:
        print("Kategori tidak boleh kosong.")
        return

    # Memastikan kategori tidak duplikat
    for budget in budgets:
        if budget["category"].casefold() == category.casefold():
            print("Anggaran untuk kategori tersebut sudah ada.")
            return

    amount = input_positive_amount(
        "Nominal anggaran (Rupiah): "
    )

    if amount is None:
        return

    budget = {
        "id": generate_budget_id(budgets),
        "category": category,
        "amount": amount
    }

    budgets.append(budget)
    save_data("budgets", budgets)

    print("\nAnggaran berhasil ditambahkan!")
    print("ID       :", budget["id"])
    print("Kategori :", budget["category"])
    print("Anggaran :", format_rupiah(budget["amount"]))


# ==========================================
# READ BUDGET
# ==========================================

def view_budgets():

    budgets = load_data("budgets")
    transactions = load_data("transactions")

    print("\n========== DAFTAR ANGGARAN ==========")

    if not budgets:
        print("Belum ada anggaran.")
        return

    for budget in budgets:

        spending, percentage, remaining, status = (
            calculate_budget_usage(budget, transactions)
        )

        print("-" * 50)
        print("ID          :", budget["id"])
        print("Kategori    :", budget["category"])
        print("Anggaran    :", format_rupiah(budget["amount"]))
        print("Terpakai    :", format_rupiah(spending))
        print("Persentase  :", f"{percentage:.1f}%")

        if remaining >= 0:
            print("Sisa        :", format_rupiah(remaining))
        else:
            print("Kelebihan   :", format_rupiah(abs(remaining)))

        print("Status      :", status)

    print("-" * 50)


# ==========================================
# UPDATE BUDGET
# ==========================================

def update_budget():

    budgets = load_data("budgets")

    print("\n========== UBAH ANGGARAN ==========")

    if not budgets:
        print("Belum ada anggaran.")
        return

    budget_id = input("Masukkan ID anggaran: ").strip().upper()

    for budget in budgets:

        if budget["id"] == budget_id:

            print("\nAnggaran ditemukan!")
            print("Kategori saat ini :", budget["category"])
            print("Nominal saat ini  :", format_rupiah(budget["amount"]))

            print("\nKosongkan input jika tidak ingin mengubah data.")

            new_category = input("Kategori baru: ").strip()

            if new_category:

                for other_budget in budgets:
                    if (
                        other_budget["id"] != budget_id
                        and other_budget["category"].casefold()
                        == new_category.casefold()
                    ):
                        print("Kategori tersebut sudah memiliki anggaran.")
                        return

            new_amount = input("Nominal anggaran baru: ").strip()

            # Validasi dilakukan sebelum mengubah data
            if new_amount:
                try:
                    amount = int(new_amount)

                    if amount <= 0:
                        print("Nominal harus lebih dari nol.")
                        return

                except ValueError:
                    print("Nominal harus berupa angka bulat.")
                    return
            else:
                amount = budget["amount"]

            if new_category:
                budget["category"] = new_category

            budget["amount"] = amount

            save_data("budgets", budgets)

            print("\nAnggaran berhasil diperbarui!")
            return

    print("Anggaran tidak ditemukan.")


# ==========================================
# DELETE BUDGET
# ==========================================

def delete_budget():

    budgets = load_data("budgets")

    print("\n========== HAPUS ANGGARAN ==========")

    if not budgets:
        print("Belum ada anggaran.")
        return

    budget_id = input("Masukkan ID anggaran: ").strip().upper()

    for budget in budgets:

        if budget["id"] == budget_id:

            print("\nAnggaran ditemukan!")
            print("Kategori :", budget["category"])
            print("Nominal  :", format_rupiah(budget["amount"]))

            confirmation = input(
                "Yakin ingin menghapus? (y/n): "
            ).strip().lower()

            if confirmation == "y":

                budgets.remove(budget)
                save_data("budgets", budgets)

                print("Anggaran berhasil dihapus!")

            else:
                print("Penghapusan dibatalkan.")

            return

    print("Anggaran tidak ditemukan.")


# ==========================================
# BUDGET REPORT
# ==========================================

def view_budget_report():

    budgets = load_data("budgets")
    transactions = load_data("transactions")

    print("\n========== LAPORAN PENGGUNAAN ANGGARAN ==========")

    if not budgets:
        print("Belum ada anggaran yang tersedia.")
        return

    for budget in budgets:

        spending, percentage, remaining, status = (
            calculate_budget_usage(budget, transactions)
        )

        print("-" * 50)
        print("Kategori :", budget["category"])
        print("Anggaran :", format_rupiah(budget["amount"]))
        print("Terpakai :", format_rupiah(spending))
        print("Penggunaan:", f"{percentage:.1f}%")
        if status == "Melewati batas":
            print("PERINGATAN: Pengeluaran telah melewati anggaran!")
        elif status == "Hampir habis":
            print("PERINGATAN: Anggaran sudah mencapai 80% atau lebih!")
        else:
            print("Status: Penggunaan anggaran masih aman.")
    print("-" * 50)

def budget_menu():

    while True:

        print("\n" + "=" * 45)
        print("          FINANCIAL BUDGET")
        print("           MANAGEMENT")
        print("=" * 45)

        print("1. Tambah Anggaran")
        print("2. Lihat Anggaran")
        print("3. Ubah Anggaran")
        print("4. Hapus Anggaran")
        print("5. Laporan Penggunaan Anggaran")
        print("0. Kembali")

        print("=" * 45)

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            add_budget()

        elif choice == "2":
            view_budgets()

        elif choice == "3":
            update_budget()

        elif choice == "4":
            delete_budget()

        elif choice == "5":
            view_budget_report()

        elif choice == "0":
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    budget_menu()
