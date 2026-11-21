=================================================================
         SEHARI-HARI — Daily Life Management System
=================================================================

DESKRIPSI APLIKASI
Sehari-Hari adalah aplikasi berbasis Command Line Interface (CLI)
yang dibuat menggunakan bahasa pemrograman Python untuk membantu
pengguna mengelola keuangan pribadi (FinTrack) dan kegiatan
harian (Daily Task Manager) secara terintegrasi dan offline.

STRUKTUR FOLDER PROYEK
Sehari-Hari/
├── main.py                  : Titik masuk utama & menu navigasi
├── README.txt               : Dokumentasi dan panduan instalasi
├── requirements.txt         : Daftar kebutuhan library (Python standar)
├── data/                    : Folder penyimpanan data dalam format .txt
│   ├── transactions.txt     : Data transaksi pemasukan & pengeluaran
│   ├── budgets.txt          : Data anggaran per kategori
│   ├── savings_goals.txt    : Data target tabungan
│   └── tasks.txt            : Data tugas harian
├── modules/                 : Modul utama fitur aplikasi
│   ├── storage.py           : Pengelolaan baca/tulis file .txt
│   ├── fintrack.py          : CRUD transaksi & menu FinTrack
│   ├── budget.py            : CRUD anggaran & peringatan batas budget
│   ├── savings_goals.py     : CRUD target tabungan & progres
│   ├── dashboard.py         : Dashboard keuangan & laporan bulanan
│   └── task_manager.py      : CRUD tugas harian & ringkasan aktivitas
└── utils/                   : Modul bantuan
    └── search_sort.py       : Implementasi Linear Search & Bubble Sort

CARA INSTALASI DAN MENJALANKAN PROGRAM
1. Pastikan Python versi 3.8 atau lebih baru sudah terinstal.
2. Buka terminal / Command Prompt / terminal VS Code.
3. Arahkan direktori ke dalam folder proyek:
   cd Sehari-Hari
4. Jalankan program utama dengan perintah:
   python main.py

PENERAPAN MATERI PRAKTIKUM DASAR PEMROGRAMAN
1. Tipe Data Koleksi : List (daftar record), Dictionary (atribut data),
                       Tuple (skema kolom di storage.py), Set (kategori
                       unik di dashboard.py).
2. Fungsi            : Pemecahan kode secara modular pada setiap file.
3. Searching         : Linear Search untuk mencari tugas berdasarkan
                       kata kunci judul/deskripsi (utils/search_sort.py).
4. Sorting           : Bubble Sort untuk mengurutkan tugas berdasarkan
                       deadline & prioritas (utils/search_sort.py).
5. String            : Manipulasi teks (.strip(), .lower(), .upper(),
                       .title(), .split(), .join(), .startswith()).
6. File Handling     : Pembacaan dan penulisan data permanen pada file
                       berformat .txt menggunakan fungsi open().
7. CRUD              : Create, Read, Update, Delete lengkap pada
                       Transaksi, Anggaran, Target Tabungan, dan Tugas.
=================================================================