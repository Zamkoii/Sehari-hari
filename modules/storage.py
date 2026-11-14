
import json
from pathlib import Path


# Menentukan lokasi folder utama proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# Lokasi folder penyimpanan data
DATA_DIR = BASE_DIR / "data"


# Daftar file JSON yang digunakan aplikasi
DATA_FILES = {
    "transactions": "transactions.json",
    "budgets": "budgets.json",
    "savings_goals": "savings_goals.json",
    "tasks": "tasks.json"
}


def initialize_data_files():
    """
    Membuat folder dan file JSON jika belum tersedia.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename in DATA_FILES.values():
        file_path = DATA_DIR / filename

        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    print("Sistem penyimpanan berhasil disiapkan.")


def load_data(data_name):
    """
    Membaca data dari file JSON.
    Mengembalikan list berisi data.
    """

    if data_name not in DATA_FILES:
        raise ValueError("Nama data tidak dikenali.")

    file_path = DATA_DIR / DATA_FILES[data_name]

    if not file_path.exists():
        raise FileNotFoundError(
            f"File {file_path.name} tidak ditemukan."
        )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                f"Format data {file_path.name} harus berupa list."
            )

        return data

    except json.JSONDecodeError as error:
        raise ValueError(
            f"File {file_path.name} memiliki format JSON yang rusak."
        ) from error


def save_data(data_name, data):
    """
    Menyimpan list data ke file JSON.
    """

    if data_name not in DATA_FILES:
        raise ValueError("Nama data tidak dikenali.")

    if not isinstance(data, list):
        raise TypeError("Data yang disimpan harus berupa list.")

    file_path = DATA_DIR / DATA_FILES[data_name]

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

