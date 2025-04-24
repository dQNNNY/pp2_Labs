import psycopg2
import os
import csv


try:
    conn = psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)


menu_items = [
    "Add a user (console input)",
    "Add users from CSV",
    "Update or add a user",
    "Add multiple users",
    "Search by pattern",
    "Pagination of results",
    "Delete a user",
    "Exit"
]

def clear(): os.system("cls" if os.name == "nt" else "clear")

def print_menu(selected):
    clear()
    print("--- Phonebook Menu ---\n")
    for i, item in enumerate(menu_items):
        print(f"{i+1}. {item}" if i == selected else f"  {i+1}. {item}")

def menu_loop():
    while True:
        clear()
        print("--- Phonebook Menu ---\n")
        for i, item in enumerate(menu_items):
            print(f"{i+1}. {item}")
        
        try:
            choice = int(input("Enter your choice (1-8): ").strip())
            if 1 <= choice <= len(menu_items):
                return choice - 1  
            else:
                print("Invalid choice, please select a valid option (1-8).")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 8.")

def insert_user_console():
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    
    
    if not phone.isdigit() or len(phone) != 10:
        print("Invalid phone number format.")
        return

    try:
        cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("User added.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

def insert_from_csv(filename):
    if not os.path.isfile(filename):
        print("File not found.")
        return
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    name, phone = row[0].strip(), row[1].strip()
                    
                    if not phone.isdigit() or len(phone) != 10:
                        print(f"Invalid phone number for {name}: {phone}")
                        continue
                    cur.execute(
                        "INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                        (name, phone)
                    )
        conn.commit()
        print("Data from CSV added.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

def upsert_user():
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()

    
    if not phone.isdigit() or len(phone) != 10:
        print("Invalid phone number format.")
        return

    try:
        cur.execute(""" 
            INSERT INTO PhoneBook (first_name, phone)
            VALUES (%s, %s)
            ON CONFLICT (phone)
            DO UPDATE SET first_name = EXCLUDED.first_name
        """, (name, phone))
        conn.commit()
        print("User updated or added.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

def insert_many_users():
    names = input("Enter names (comma separated): ").split(",")
    phones = input("Enter phone numbers (comma separated): ").split(",")
    names = [n.strip() for n in names]
    phones = [p.strip() for p in phones]

    if len(names) != len(phones):
        print("The number of names and phone numbers must match!")
        return

    invalid = []
    try:
        for name, phone in zip(names, phones):
            
            if not phone.isdigit() or len(phone) != 10:
                invalid.append((name, phone))
                continue
            cur.execute(""" 
                INSERT INTO PhoneBook (first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (name, phone))
        conn.commit()
        if invalid:
            print("Invalid entries (possible duplicates or errors):")
            for i in invalid:
                print(" -", i)
        else:
            print("All users added.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

def search_pattern():
    pattern = input("Enter search pattern: ").strip()
    try:
        like_pattern = f"%{pattern}%"
        cur.execute("""
            SELECT * FROM PhoneBook
            WHERE first_name ILIKE %s OR phone ILIKE %s
        """, (like_pattern, like_pattern))
        results = cur.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No matches found.")
    except Exception as e:
        print(f"Error: {e}")

def paginate_results():
    try:
        limit = int(input("Enter limit: "))
        offset = int(input("Enter offset: "))
        cur.execute("""
            SELECT * FROM PhoneBook
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        results = cur.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No results on this page.")
    except Exception as e:
        print(f"Error: {e}")
    except ValueError:
        print("Invalid input for limit or offset.")

def delete_user():
    val = input("Enter name or phone number to delete: ").strip()
    confirm = input(f"Are you sure you want to delete the user with {val}? (y/n): ").strip().lower()
    if confirm != 'y':
        return
    try:
        cur.execute("""
            DELETE FROM PhoneBook
            WHERE first_name = %s OR phone = %s
        """, (val, val))
        conn.commit()
        print("User(s) deleted.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

def close():
    cur.close()
    conn.close()


if __name__ == "__main__":
    try:
        while True:
            choice = menu_loop()
            clear()
            if choice == 0:
                insert_user_console()
            elif choice == 1:
                filename = input("Enter the CSV filename: ").strip()
                insert_from_csv(filename)
            elif choice == 2:
                upsert_user()
            elif choice == 3:
                insert_many_users()
            elif choice == 4:
                search_pattern()
            elif choice == 5:
                paginate_results()
            elif choice == 6:
                delete_user()
            elif choice == 7:
                break
            input("\nPress any key to continue...")
    finally:
        close()
