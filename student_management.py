import sqlite3

DB_NAME = "students.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_student():
    name = input("Enter student name: ").strip()
    age = input("Enter age: ").strip()
    course = input("Enter course: ").strip()
    marks = input("Enter marks: ").strip()

    if not name or not age or not course or not marks:
        print("All fields are required.\n")
        return

    try:
        age = int(age)
        marks = float(marks)
    except ValueError:
        print("Age must be integer and marks must be numeric.\n")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, course, marks) VALUES (?, ?, ?, ?)",
        (name, age, course, marks)
    )
    conn.commit()
    conn.close()
    print("Student added successfully.\n")


def view_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    if not students:
        print("No student records found.\n")
        return

    print("\nStudent Records")
    print("-" * 60)
    print(f"{'ID':<5}{'Name':<20}{'Age':<8}{'Course':<15}{'Marks':<10}")
    print("-" * 60)
    for student in students:
        print(f"{student[0]:<5}{student[1]:<20}{student[2]:<8}{student[3]:<15}{student[4]:<10}")
    print()


def search_student():
    keyword = input("Enter student name to search: ").strip()

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + keyword + '%',))
    students = cursor.fetchall()
    conn.close()

    if not students:
        print("No matching student found.\n")
        return

    print("\nSearch Results")
    print("-" * 60)
    print(f"{'ID':<5}{'Name':<20}{'Age':<8}{'Course':<15}{'Marks':<10}")
    print("-" * 60)
    for student in students:
        print(f"{student[0]:<5}{student[1]:<20}{student[2]:<8}{student[3]:<15}{student[4]:<10}")
    print()


def update_student():
    student_id = input("Enter student ID to update: ").strip()

    if not student_id.isdigit():
        print("Invalid ID.\n")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        print("Student not found.\n")
        return

    print("Leave field empty to keep current value.")
    name = input(f"Enter new name [{student[1]}]: ").strip()
    age = input(f"Enter new age [{student[2]}]: ").strip()
    course = input(f"Enter new course [{student[3]}]: ").strip()
    marks = input(f"Enter new marks [{student[4]}]: ").strip()

    new_name = name if name else student[1]
    new_age = student[2]
    new_course = course if course else student[3]
    new_marks = student[4]

    if age:
        try:
            new_age = int(age)
        except ValueError:
            conn.close()
            print("Age must be an integer.\n")
            return

    if marks:
        try:
            new_marks = float(marks)
        except ValueError:
            conn.close()
            print("Marks must be numeric.\n")
            return

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?, marks = ?
        WHERE id = ?
    """, (new_name, new_age, new_course, new_marks, student_id))

    conn.commit()
    conn.close()
    print("Student updated successfully.\n")


def delete_student():
    student_id = input("Enter student ID to delete: ").strip()

    if not student_id.isdigit():
        print("Invalid ID.\n")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        print("Student not found.\n")
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    print("Student deleted successfully.\n")


def menu():
    while True:
        print("===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        print()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    create_table()
    menu()
