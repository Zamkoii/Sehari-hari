from pathlib import Path


# Menentukan lokasi folder utama proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# Lokasi folder penyimpanan data
DATA_DIR = BASE_DIR / "data"


# Daftar file TXT yang digunakan aplikasi
DATA_FILES = {
    "transactions": "transactions.txt",
    "budgets": "budgets.txt",
    "savings_goals": "savings_goals.txt",
    "tasks": "tasks.txt"
}

# Definisi nama kolom (field) dan tipe datanya untuk setiap file .txt
DATA_SCHEMAS = {
    "transactions": [
        ("id", str),
        ("type", str),
        ("category", str),
        ("description", str),
        ("amount", int),
        ("date", str),
    ],
    "budgets": [
        ("id", str),
        ("category", str),
        ("amount", int),
    ],
    "savings_goals": [
        ("id", str),
        ("name", str),
        ("target_amount", int),
        ("current_amount", int),
        ("deadline", str),
    ],
    "tasks": [
        ("id", str),
        ("title", str),
        ("description", str),
        ("deadline", str),
        ("priority", str),
        ("status", str),
    ],
}

DELIMITER = "|"


def initialize_data_files():
    """
    Membuat folder dan file TXT kosong jika belum tersedia.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename in DATA_FILES.values():
        file_path = DATA_DIR / filename

        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")

    print("Sistem penyimpanan (.txt) berhasil disiapkan.")


def load_data(data_name):
    """
    Membaca data dari file TXT dan mengubahnya kembali menjadi list of dictionary.
    """
    if data_name not in DATA_FILES:
        raise ValueError("Nama data tidak dikenali.")

    file_path = DATA_DIR / DATA_FILES[data_name]

    if not file_path.exists():
        raise FileNotFoundError(
            f"File {file_path.name} tidak ditemukan."
        )

    schema = DATA_SCHEMAS[data_name]
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            # Lewati baris kosong
            if not line:
                continue

            parts = line.split(DELIMITER)

            if len(parts) != len(schema):
                raise ValueError(
                    f"Format baris ke-{line_number} pada {file_path.name} tidak valid."
                )

            item = {}
            try:
                for (field_name, field_type), value in zip(schema, parts):
                    item[field_name] = field_type(value)
            except ValueError as error:
                raise ValueError(
                    f"Tipe data tidak valid pada baris ke-{line_number} di {file_path.name}."
                ) from error

            records.append(item)

    return records


def save_data(data_name, data):
    """
    Menyimpan list of dictionary ke dalam file TXT dengan pemisah '|'.
    """
    if data_name not in DATA_FILES:
        raise ValueError("Nama data tidak dikenali.")

    if not isinstance(data, list):
        raise TypeError("Data yang disimpan harus berupa list.")

    file_path = DATA_DIR / DATA_FILES[data_name]
    schema = DATA_SCHEMAS[data_name]

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    lines = []
    for item in data:
        if not isinstance(item, dict):
            raise TypeError("Setiap elemen data harus berupa dictionary.")

        row_values = []
        for field_name, _ in schema:
            raw_value = str(item.get(field_name, ""))
            # Mencegah karakter delimiter '|' atau baris baru merusak format file .txt
            clean_value = raw_value.replace(DELIMITER, "/").replace("\n", " ").strip()
            row_values.append(clean_value)

        lines.append(DELIMITER.join(row_values))

    with open(file_path, "w", encoding="utf-8") as file:
        if lines:
            file.write("\n".join(lines) + "\n")
        else:
            file.write("")