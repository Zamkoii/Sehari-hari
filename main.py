
def show_main_menu():
    print("\n" + "=" * 45)
    print("             SEHARI-HARI")
    print("       Daily Life Management System")
    print("=" * 45)
    print("1. FinTrack")
    print("2. Daily Task Manager")
    print("0. Exit")
    print("=" * 45)


def main():
    while True:
        show_main_menu()

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            print("\nFinTrack akan segera tersedia.")

        elif choice == "2":
            print("\nDaily Task Manager akan segera tersedia.")

        elif choice == "0":
            print("\nTerima kasih telah menggunakan Sehari-Hari!")
            break

        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    main()
