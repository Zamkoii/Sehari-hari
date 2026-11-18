# ==========================================
# ALGORITMA SEARCHING (LINEAR SEARCH)
# ==========================================

def search_tasks_by_keyword(tasks, keyword):
    """
    Mencari tugas berdasarkan kata kunci pada judul atau deskripsi
    menggunakan algoritma Linear Search (pencarian satu per satu).
    """
    results = []
    keyword_lower = keyword.lower().strip()

    for task in tasks:
        title_lower = task["title"].lower()
        desc_lower = task["description"].lower()

        # Cek apakah kata kunci ada di judul ATAU deskripsi
        if keyword_lower in title_lower or keyword_lower in desc_lower:
            results.append(task)

    return results


def search_transactions_by_keyword(transactions, keyword):
    """
    Mencari transaksi berdasarkan kata kunci pada kategori atau deskripsi
    menggunakan algoritma Linear Search.
    """
    results = []
    keyword_lower = keyword.lower().strip()

    for trx in transactions:
        cat_lower = trx["category"].lower()
        desc_lower = trx["description"].lower()

        if keyword_lower in cat_lower or keyword_lower in desc_lower:
            results.append(trx)

    return results


# ==========================================
# ALGORITMA SORTING (BUBBLE SORT)
# ==========================================

def sort_tasks_by_deadline(tasks):
    """
    Mengurutkan tugas berdasarkan deadline terdekat ke terjauh
    menggunakan algoritma Bubble Sort.
    """
    # Membuat salinan list agar data asli tidak berubah urutannya di memori
    sorted_list = list(tasks)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_list[j]["deadline"] > sorted_list[j + 1]["deadline"]:
                # Tukar posisi elemen
                temp = sorted_list[j]
                sorted_list[j] = sorted_list[j + 1]
                sorted_list[j + 1] = temp

    return sorted_list


def sort_tasks_by_priority(tasks):
    """
    Mengurutkan tugas berdasarkan prioritas (Tinggi -> Sedang -> Rendah)
    menggunakan algoritma Bubble Sort.
    """
    # Kamus bobot prioritas: angka lebih kecil berarti lebih penting
    priority_weight = {
        "Tinggi": 1,
        "Sedang": 2,
        "Rendah": 3
    }

    sorted_list = list(tasks)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            weight_1 = priority_weight.get(sorted_list[j]["priority"], 4)
            weight_2 = priority_weight.get(sorted_list[j + 1]["priority"], 4)

            if weight_1 > weight_2:
                temp = sorted_list[j]
                sorted_list[j] = sorted_list[j + 1]
                sorted_list[j + 1] = temp

    return sorted_list


def sort_transactions_by_amount(transactions, descending=True):
    """
    Mengurutkan transaksi berdasarkan nominal menggunakan Bubble Sort.
    descending=True  -> Terbesar ke terkecil
    descending=False -> Terkecil ke terbesar
    """
    sorted_list = list(transactions)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            amount_1 = sorted_list[j]["amount"]
            amount_2 = sorted_list[j + 1]["amount"]

            if descending:
                need_swap = amount_1 < amount_2
            else:
                need_swap = amount_1 > amount_2

            if need_swap:
                temp = sorted_list[j]
                sorted_list[j] = sorted_list[j + 1]
                sorted_list[j + 1] = temp

    return sorted_list