import psycopg2
import csv
import os


connection = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()


def init_phonebook_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        )
    """)
    connection.commit()


def add_contact_from_input():
    fname = input("Enter name: ")
    ph_number = input("Enter phone: ")
    try:
        cursor.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (fname, ph_number))
        connection.commit()
        print("Contact saved.")
    except Exception as err:
        print("Error:", err)
        connection.rollback()


def load_contacts_from_csv(file_path):
    try:
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for line in csv_reader:
                if len(line) >= 2:
                    cursor.execute(
                        "INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                        (line[0], line[1])
                    )
        connection.commit()
        print("CSV contacts loaded.")
    except Exception as err:
        print("Error:", err)
        connection.rollback()


def modify_contact_by_id(contact_id, updated_name=None, updated_phone=None):
    try:
        if updated_name:
            cursor.execute("UPDATE PhoneBook SET first_name = %s WHERE id = %s", (updated_name, contact_id))
        if updated_phone:
            cursor.execute("UPDATE PhoneBook SET phone = %s WHERE id = %s", (updated_phone, contact_id))
        connection.commit()
        print("Contact updated.")
    except psycopg2.Error as err:
        print("Error:", err.pgerror)
        connection.rollback()


def display_contacts(search_field=None, keyword=None):
    try:
        if search_field == "name":
            cursor.execute("SELECT * FROM PhoneBook WHERE first_name ILIKE %s", (f"%{keyword}%",))
        elif search_field == "phone":
            cursor.execute("SELECT * FROM PhoneBook WHERE phone ILIKE %s", (f"%{keyword}%",))
        else:
            cursor.execute("SELECT * FROM PhoneBook")
        entries = cursor.fetchall()
        for entry in entries:
            print(entry)
    except Exception as err:
        print("Error:", err)


def remove_contact(lookup_value):
    try:
        cursor.execute("DELETE FROM PhoneBook WHERE first_name = %s OR phone = %s", (lookup_value, lookup_value))
        connection.commit()
        print("Contact removed.")
    except Exception as err:
        print("Error:", err)
        connection.rollback()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_main_menu():
    print("\n--- PhoneBook System ---")
    print("1. Add contact (manual input)")
    print("2. Import contacts from CSV")
    print("3. Update contact by ID")
    print("4. View/search contacts")
    print("5. Delete contact")
    print("6. Exit")


if __name__ == "__main__":
    init_phonebook_table()

    while True:
        show_main_menu()
        user_choice = input("Choose option (1-6): ").strip()

        if user_choice == "1":
            clear_screen()
            add_contact_from_input()
        elif user_choice == "2":
            clear_screen()
            path = input("Enter CSV filename (e.g., data.csv): ").strip()
            load_contacts_from_csv(path)
        elif user_choice == "3":
            clear_screen()
            print("Current contacts:")
            display_contacts()
            try:
                selected_id = int(input("\nEnter ID of contact to update: "))
                updated_name = input("New name (press Enter to keep current): ").strip()
                updated_phone = input("New phone (press Enter to keep current): ").strip()
                modify_contact_by_id(
                    selected_id,
                    updated_name if updated_name else None,
                    updated_phone if updated_phone else None
                )
            except ValueError:
                print("Invalid ID.")
        elif user_choice == "4":
            clear_screen()
            filter_field = input("Search by 'name', 'phone' or leave empty: ").strip().lower()
            filter_val = input("Enter search term (or leave blank): ").strip()
            display_contacts(filter_field if filter_field else None, filter_val if filter_val else None)
        elif user_choice == "5":
            clear_screen()
            identifier = input("Enter name or phone of the contact to delete: ").strip()
            remove_contact(identifier)
        elif user_choice == "6":
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")

    cursor.close()
    connection.close()