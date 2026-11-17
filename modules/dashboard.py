from datetime import datetime
from modules.storage import load_data


def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah."""
    if amount < 0:
        return "-Rp" + f"{abs(amount):,.0f}".replace(",", ".")
    return "Rp" + f"{amount:,.0f}".replace(",", ".")


def show_fintrack_dashboard():
    """
    Menampilkan ringkasan kondisi keuangan keseluruhan (Dashboard FinTrack):
    - Total pemasukan, total pengeluaran, dan saldo
    - Ringkasan pengeluaran per kategori
    - Ringkasan progres tabungan
    """
    transactions = load_data("transactions")
    savings_goals = load_data("savings_goals")

    print("\n" + "=" * 50)
    print("            DASHBOARD KEUANGAN FINTRACK")
    print("=" * 50)

    total_income = 0
    total_expense = 0
    expense_by_category = {}
    unique_categories = set()  # Menerapkan tipe data Set untuk kategori unik

    for trx in transactions:
        amount = trx["amount"]
        category = trx["category"].strip().title()
        unique_categories.add(category)

        if trx["type"] == "income":
            total_income += amount
        elif trx["type"] == "expense":
            total_expense += amount
            expense_by_category[category] = (
                expense_by_category.get(category, 0) + amount
            )

    balance = total_income - total_expense

    print(f"Total Pemasukan   : {format_rupiah(total_income)}")
    print(f"Total Pengeluaran : {format_rupiah(total_expense)}")
    print(f"Saldo Bersih      : {format_rupiah(balance)}")
    print(f"Jumlah Transaksi  : {len(transactions)} transaksi ({len(unique_categories)} kategori)")

    if balance > 0:
        print("Status Keuangan   : Surplus (Sehat)")
    elif balance == 0:
        print("Status Keuangan   : Seimbang")
    else:
        print("Status Keuangan   : Defisit (Pengeluaran melebihi pemasukan)")

    # Ringkasan pengeluaran per kategori
    print("\n--- PENGELUARAN PER KATEGORI ---")
    if not expense_by_category:
        print("Belum ada data pengeluaran.")
    else:
        for category, total in expense_by_category.items():
            percentage = (total / total_expense * 100) if total_expense > 0 else 0
            print(f"- {category:<18}: {format_rupiah(total)} ({percentage:.1f}%)")

    # Ringkasan singkat tabungan
    print("\n--- RINGKASAN TARGET TABUNGAN ---")
    if not savings_goals:
        print("Belum ada target tabungan.")
    else:
        total_saved = sum(goal["current_amount"] for goal in savings_goals)
        total_target = sum(goal["target_amount"] for goal in savings_goals)
        overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0
        print(f"Total Terkumpul   : {format_rupiah(total_saved)} dari {format_rupiah(total_target)} ({overall_progress:.1f}%)")

    print("=" * 50)


def show_monthly_report():
    """
    Menampilkan laporan keuangan sederhana berdasarkan periode bulan (YYYY-MM).
    """
    transactions = load_data("transactions")

    print("\n" + "=" * 50)
    print("         LAPORAN KEUANGAN BULANAN")
    print("=" * 50)

    if not transactions:
        print("Belum ada transaksi yang tercatat.")
        return

    period = input("Masukkan periode bulan (YYYY-MM, contoh 2026-11): ").strip()

    # Validasi format periode YYYY-MM
    try:
        datetime.strptime(period, "%Y-%m")
    except ValueError:
        print("Format periode tidak valid. Gunakan format YYYY-MM (contoh: 2026-11).")
        return

    filtered_transactions = [
        trx for trx in transactions if trx["date"].startswith(period)
    ]

    if not filtered_transactions:
        print(f"\nTidak ada transaksi pada periode {period}.")
        return

    monthly_income = 0
    monthly_expense = 0
    category_summary = {}

    print(f"\nRincian Transaksi Periode {period}:")
    print("-" * 50)

    for trx in filtered_transactions:
        jenis = "Masuk " if trx["type"] == "income" else "Keluar"
        print(
            f"{trx['date']} | {trx['id']} | {jenis} | "
            f"{trx['category']} - {trx['description']} : {format_rupiah(trx['amount'])}"
        )

        if trx["type"] == "income":
            monthly_income += trx["amount"]
        else:
            monthly_expense += trx["amount"]
            cat = trx["category"].strip().title()
            category_summary[cat] = category_summary.get(cat, 0) + trx["amount"]

    monthly_net = monthly_income - monthly_expense

    print("-" * 50)
    print(f"Pemasukan Bulan Ini   : {format_rupiah(monthly_income)}")
    print(f"Pengeluaran Bulan Ini : {format_rupiah(monthly_expense)}")
    print(f"Selisih Bersih        : {format_rupiah(monthly_net)}")

    if category_summary:
        print("\nRincian Pengeluaran per Kategori:")
        for cat, amount in category_summary.items():
            print(f"- {cat}: {format_rupiah(amount)}")

    print("=" * 50)