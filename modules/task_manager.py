from datetime import datetime
from modules.storage import load_data, save_data
from utils.search_sort import (
    search_tasks_by_keyword,
    sort_tasks_by_deadline,
    sort_tasks_by_priority
)


# ==========================================
# FUNGSI BANTUAN (HELPER)
# ==========================================

def generate_task_id(tasks):
    """Membuat ID tugas otomatis seperti TSK001, TSK002."""
    highest_id = 0

    for task in tasks:
        try:
            number = int(task["id"][3:])
            if number > highest_id:
                highest_id = number
        except (ValueError, KeyError, TypeError):
            continue

    return f"TSK{highest_id + 1:03d}"


def validate_date(date_text):
    """Memeriksa apakah format tanggal sesuai YYYY-MM-DD."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def choose_priority():
    """Meminta pengguna memilih prioritas tugas."""
    print("Pilih Prioritas:")
    print("1. Tinggi")
    print("2. Sedang")
    print("3. Rendah")

    choice = input("Masukkan pilihan (1/2/3): ").strip()

    if choice == "1":
        return "Tinggi"
    elif choice == "2":
        return "Sedang"
    elif choice == "3":
        return "Rendah"
    else:
        return None


def print_task_list(task_list):
    """Menampilkan daftar tugas dalam format yang seragam."""
    for task in task_list:
        print("-" * 45)
        print("ID Tugas  :", task["id"])
        print("Judul     :", task["title"])
        print("Deskripsi :", task["description"])
        print("Deadline  :", task["deadline"])
        print("Prioritas :", task["priority"])
        print("Status    :", task["status"])
    print("-" * 45)


# ==========================================
# 1. CREATE TASK (TAMBAH TUGAS)
# ==========================================

def add_task():
    tasks = load_data("tasks")

    print("\n========== TAMBAH TUGAS BARU ==========")

    title = input("Judul tugas: ").strip()
    if title == "":
        print("Judul tugas tidak boleh kosong.")
        return

    description = input("Deskripsi tugas: ").strip()
    if description == "":
        print("Deskripsi tidak boleh kosong.")
        return

    deadline = input("Tenggat waktu (YYYY-MM-DD): ").strip()
    if not validate_date(deadline):
        print("Format tanggal tidak valid. Gunakan YYYY-MM-DD.")
        return

    priority = choose_priority()
    if priority is None:
        print("Pilihan prioritas tidak valid.")
        return

    new_task = {
        "id": generate_task_id(tasks),
        "title": title,
        "description": description,
        "deadline": deadline,
        "priority": priority,
        "status": "Pending"
    }

    tasks.append(new_task)
    save_data("tasks", tasks)

    print("\nTugas berhasil ditambahkan!")
    print("ID Tugas :", new_task["id"])
    print("Judul    :", new_task["title"])


# ==========================================
# 2. READ TASKS (LIHAT DAFTAR TUGAS)
# ==========================================

def view_tasks():
    tasks = load_data("tasks")

    print("\n========== DAFTAR TUGAS HARIAN ==========")

    if len(tasks) == 0:
        print("Belum ada tugas yang tercatat.")
        return

    print_task_list(tasks)


# ==========================================
# 3. UPDATE TASK (UBAH DATA TUGAS)
# ==========================================

def update_task():
    tasks = load_data("tasks")

    print("\n========== UBAH TUGAS ==========")

    if len(tasks) == 0:
        print("Belum ada tugas.")
        return

    for task in tasks:
        print(f"{task['id']} - {task['title']} [{task['status']}]")

    task_id = input("\nMasukkan ID tugas yang ingin diubah: ").strip().upper()

    for task in tasks:
        if task["id"] == task_id:
            print("\nTugas ditemukan!")
            print("Kosongkan input (tekan Enter) jika tidak ingin mengubah bagian tersebut.")

            new_title = input("Judul baru: ").strip()
            if new_title != "":
                task["title"] = new_title

            new_description = input("Deskripsi baru: ").strip()
            if new_description != "":
                task["description"] = new_description

            new_deadline = input("Deadline baru (YYYY-MM-DD): ").strip()
            if new_deadline != "":
                if not validate_date(new_deadline):
                    print("Format tanggal tidak valid. Perubahan dibatalkan.")
                    return
                task["deadline"] = new_deadline

            change_priority = input("Ubah prioritas? (y/n): ").strip().lower()
            if change_priority == "y":
                new_priority = choose_priority()
                if new_priority is None:
                    print("Prioritas tidak valid. Perubahan dibatalkan.")
                    return
                task["priority"] = new_priority

            save_data("tasks", tasks)
            print("\nData tugas berhasil diperbarui!")
            return

    print("ID tugas tidak ditemukan.")


# ==========================================
# 4. UPDATE STATUS TUGAS (SELESAI / PENDING)
# ==========================================

def toggle_task_status():
    tasks = load_data("tasks")

    print("\n========== UBAH STATUS TUGAS ==========")

    if len(tasks) == 0:
        print("Belum ada tugas.")
        return

    for task in tasks:
        print(f"{task['id']} - {task['title']} (Status: {task['status']})")

    task_id = input("\nMasukkan ID tugas: ").strip().upper()

    for task in tasks:
        if task["id"] == task_id:
            print("\nPilih Status Baru:")
            print("1. Completed (Selesai)")
            print("2. Pending (Belum Selesai)")

            choice = input("Masukkan pilihan (1/2): ").strip()

            if choice == "1":
                task["status"] = "Completed"
            elif choice == "2":
                task["status"] = "Pending"
            else:
                print("Pilihan status tidak valid.")
                return

            save_data("tasks", tasks)
            print(f"\nStatus tugas {task['id']} berhasil diubah menjadi {task['status']}!")
            return

    print("ID tugas tidak ditemukan.")


# ==========================================
# 5. DELETE TASK (HAPUS TUGAS)
# ==========================================

def delete_task():
    tasks = load_data("tasks")

    print("\n========== HAPUS TUGAS ==========")

    if len(tasks) == 0:
        print("Belum ada tugas.")
        return

    for task in tasks:
        print(f"{task['id']} - {task['title']}")

    task_id = input("\nMasukkan ID tugas yang ingin dihapus: ").strip().upper()

    for task in tasks:
        if task["id"] == task_id:
            print("\nTugas ditemukan:")
            print("Judul   :", task["title"])
            print("Deadline:", task["deadline"])

            confirm = input("Yakin ingin menghapus tugas ini? (y/n): ").strip().lower()
            if confirm == "y":
                tasks.remove(task)
                save_data("tasks", tasks)
                print("Tugas berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")
            return

    print("ID tugas tidak ditemukan.")


# ==========================================
# 6. RINGKASAN AKTIVITAS HARIAN
# ==========================================

def show_task_summary():
    tasks = load_data("tasks")

    print("\n========== RINGKASAN AKTIVITAS HARIAN ==========")

    total_tasks = len(tasks)
    completed_count = 0
    pending_count = 0
    high_priority_pending = 0

    for task in tasks:
        if task["status"] == "Completed":
            completed_count += 1
        else:
            pending_count += 1
            if task["priority"] == "Tinggi":
                high_priority_pending += 1

    print("Total Tugas               :", total_tasks)
    print("Tugas Selesai (Completed) :", completed_count)
    print("Tugas Tertunda (Pending)  :", pending_count)
    print("Prioritas Tinggi Tertunda :", high_priority_pending)

    if total_tasks > 0:
        percent = (completed_count / total_tasks) * 100
        print(f"Persentase Penyelesaian   : {percent:.1f}%")
    else:
        print("Persentase Penyelesaian   : 0.0%")

    print("=" * 48)


# ==========================================
# 7. CARI TUGAS (SEARCHING)
# ==========================================

def search_tasks():
    tasks = load_data("tasks")

    print("\n========== CARI TUGAS ==========")

    if len(tasks) == 0:
        print("Belum ada tugas untuk dicari.")
        return

    keyword = input("Masukkan kata kunci (judul/deskripsi): ").strip()
    if keyword == "":
        print("Kata kunci tidak boleh kosong.")
        return

    results = search_tasks_by_keyword(tasks, keyword)

    if len(results) == 0:
        print(f"\nTidak ditemukan tugas dengan kata kunci '{keyword}'.")
    else:
        print(f"\nDitemukan {len(results)} tugas:")
        print_task_list(results)


# ==========================================
# 8. URUTKAN TUGAS (SORTING)
# ==========================================

def sort_tasks():
    tasks = load_data("tasks")

    print("\n========== URUTKAN TUGAS ==========")

    if len(tasks) == 0:
        print("Belum ada tugas untuk diurutkan.")
        return

    print("1. Urutkan berdasarkan Deadline (Terdekat)")
    print("2. Urutkan berdasarkan Prioritas (Tinggi ke Rendah)")

    choice = input("Pilih metode pengurutan (1/2): ").strip()

    if choice == "1":
        sorted_tasks = sort_tasks_by_deadline(tasks)
        print("\nDaftar Tugas (Urut Deadline Terdekat):")
        print_task_list(sorted_tasks)
    elif choice == "2":
        sorted_tasks = sort_tasks_by_priority(tasks)
        print("\nDaftar Tugas (Urut Prioritas Tertinggi):")
        print_task_list(sorted_tasks)
    else:
        print("Pilihan tidak valid.")


# ==========================================
# MENU UTAMA DAILY TASK MANAGER
# ==========================================

def task_manager_menu():
    while True:
        print("\n" + "=" * 45)
        print("            DAILY TASK MANAGER")
        print("=" * 45)
        print("1. Tambah Tugas")
        print("2. Lihat Daftar Tugas")
        print("3. Ubah Data Tugas")
        print("4. Ubah Status Tugas (Selesai/Pending)")
        print("5. Hapus Tugas")
        print("6. Ringkasan Aktivitas Harian")
        print("7. Cari Tugas")
        print("8. Urutkan Tugas")
        print("0. Kembali ke Menu Utama")
        print("=" * 45)

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            toggle_task_status()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            show_task_summary()
        elif choice == "7":
            search_tasks()
        elif choice == "8":
            sort_tasks()
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")