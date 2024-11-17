import psycopg2

class DataBase:
    def __init__(self):
        self.db = psycopg2.connect(
            database='6-uy ishi',
            user='postgres',
            password='1',
            host='localhost',
        )

    def manager(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        with self.db as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
            return result

    # 1 va 2
    def create_table_students(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS students (
           students_id SERIAL PRIMARY KEY,
           students_age INTEGER CHECK(students_age > 0),
           email VARCHAR(50) UNIQUE NOT NULL
        );
        '''
        self.manager(sql, commit=True)

    def create_table_courses(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS courses (
           id SERIAL PRIMARY KEY,
           course_code VARCHAR(50) UNIQUE NOT NULL,
           credits INTEGER CHECK (credits BETWEEN 1 AND 5)
        );
        '''
        self.manager(sql, commit=True)

    def create_table_enrollments(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS enrollments (
           enrollment_id SERIAL PRIMARY KEY,
           student_id INTEGER,
           course_id INTEGER,
           FOREIGN KEY (student_id) REFERENCES students(students_id) ON DELETE CASCADE,
           FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
        );
        '''
        self.manager(sql, commit=True)

    def create_table_teachers(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS teachers (
           teacher_id SERIAL PRIMARY KEY,
           experience_years INTEGER CHECK (experience_years >= 0)
        );
        '''
        self.manager(sql, commit=True)

    def create_table_course_assignments(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS course_assignments (
           assignment_id SERIAL PRIMARY KEY,
           teacher_id INTEGER,
           course_id INTEGER,
           FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE SET DEFAULT,
           FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
        '''
        self.manager(sql, commit=True)

    # 3
    def insert_students(self):
        sql = '''
        INSERT INTO students (students_age, email) VALUES
        (22, 'ali@example.com'),
        (24, 'zarina@example.com'),
        (23, 'kamal@example.com'),
        (21, 'shahzod@example.com'),
        (25, 'dilnoza@example.com'),
        (20, 'beka@example.com'),
        (23, 'saida@example.com');
        '''
        self.manager(sql, commit=True)

    def insert_courses(self):
        sql = '''
        INSERT INTO courses (course_code, credits) VALUES
        ('CS101', 4),
        ('MATH101', 3),
        ('BIO101', 5);
        '''
        self.manager(sql, commit=True)

    def insert_teachers(self):
        sql = '''
        INSERT INTO teachers (experience_years) VALUES
        (5),
        (10);
        '''
        self.manager(sql, commit=True)

    def insert_course_assignments(self):
        sql = '''
        INSERT INTO course_assignments (teacher_id, course_id) VALUES
        (1, 1),
        (2, 2);
        '''
        self.manager(sql, commit=True)

    # 4
    def rename_students_table(self):
        sql = '''
        ALTER TABLE students
        RENAME TO student_info;
        '''
        self.manager(sql, commit=True)

    # Jadval nomi o'zgarganidan keyin ustun nomini o'zgartirish
    def rename_students_column(self):
        sql = '''
        ALTER TABLE student_info
        RENAME COLUMN students_age TO yosh;
        '''
        self.manager(sql, commit=True)

    # 5
    def update_student_ages(self):
        sql = '''
           UPDATE student_info
           SET yosh = 26
           WHERE students_id IN (1, 3);
           '''
        self.manager(sql, commit=True)

    # 6
    def delete_students(self):
        sql = '''
        DELETE FROM student_info
        WHERE students_id IN (4, 5);
        '''
        self.manager(sql, commit=True)


db = DataBase()

db.create_table_students()
db.create_table_courses()
db.create_table_enrollments()
db.create_table_teachers()
db.create_table_course_assignments()

db.insert_students()
db.insert_courses()
db.insert_teachers()
db.insert_course_assignments()

db.rename_students_table()
db.rename_students_column()

db.update_student_ages()

db.delete_students()
