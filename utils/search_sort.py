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