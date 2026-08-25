import sqlite3

DB_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            marks REAL
        )
    """)
    return conn


def add_student():
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    course = input("Course: ").strip()
    marks = input("Marks: ").strip()

    conn = get_connection()
    conn.execute(
        "INSERT INTO students (name, age, course, marks) VALUES (?, ?, ?, ?)",
        (name, age, course, marks),
    )
    conn.commit()
    conn.close()
    print("Student added.\n")


def view_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    if not rows:
        print("No records found.\n")
        return

    print(f"{'ID':<5}{'Name':<15}{'Age':<6}{'Course':<10}{'Marks':<6}")
    print("-" * 42)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<15}{r[2]:<6}{r[3]:<10}{r[4]:<6}")
    print()


def search_student():
    keyword = input("Enter name or ID to search: ").strip()
    conn = get_connection()
    if keyword.isdigit():
        rows = conn.execute("SELECT * FROM students WHERE id = ?", (keyword,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{keyword}%",)).fetchall()
    conn.close()

    if not rows:
        print("No matching student found.\n")
        return

    print(f"{'ID':<5}{'Name':<15}{'Age':<6}{'Course':<10}{'Marks':<6}")
    print("-" * 42)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<15}{r[2]:<6}{r[3]:<10}{r[4]:<6}")
    print()


def update_student():
    student_id = input("Enter ID of student to update: ").strip()
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not row:
        print("Student not found.\n")
        conn.close()
        return

    print(f"Current: Name={row[1]}, Age={row[2]}, Course={row[3]}, Marks={row[4]}")
    name = input(f"New name (leave blank to keep '{row[1]}'): ").strip() or row[1]
    age = input(f"New age (leave blank to keep '{row[2]}'): ").strip() or row[2]
    course = input(f"New course (leave blank to keep '{row[3]}'): ").strip() or row[3]
    marks = input(f"New marks (leave blank to keep '{row[4]}'): ").strip() or row[4]

    conn.execute(
        "UPDATE students SET name=?, age=?, course=?, marks=? WHERE id=?",
        (name, age, course, marks, student_id),
    )
    conn.commit()
    conn.close()
    print("Student updated.\n")


def delete_student():
    student_id = input("Enter ID of student to delete: ").strip()
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not row:
        print("Student not found.\n")
        conn.close()
        return

    confirm = input(f"Delete '{row[1]}' (ID {row[0]})? (y/n): ").strip().lower()
    if confirm == "y":
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        print("Student deleted.\n")
    else:
        print("Cancelled.\n")
    conn.close()


def main():
    menu = """
================================
       STUDENT MANAGEMENT
================================
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
"""
    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
    }

    while True:
        print(menu)
        choice = input("Enter choice: ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()