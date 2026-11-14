
from modules.storage import (
    initialize_data_files,
    load_data,
    save_data
)


# 1. Persiapkan file
initialize_data_files()


# 2. Simpan data contoh
sample_data = [
    {
        "id": "TEST001",
        "name": "Data Percobaan",
        "amount": 100000
    }
]

save_data("transactions", sample_data)

print("\nData berhasil disimpan.")


# 3. Baca kembali data
loaded_data = load_data("transactions")

print("\nData yang berhasil dibaca:")
print(loaded_data)


# 4. Periksa hasil
if loaded_data == sample_data:
    print("\nTEST BERHASIL!")
else:
    print("\nTEST GAGAL!")
