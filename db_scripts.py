from random import randint
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username, password):
    """Создание нового пользователя"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)  # Хеширование пароля

    try:
        cursor.execute('''
        INSERT INTO users (username, password) 
        VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Если имя пользователя уже существует
    finally:
        conn.close()


def get_user_by_username(username):
    """Получение пользователя по логину"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_password(stored_password, provided_password):
    """Проверка пароля"""
    return check_password_hash(stored_password, provided_password)


db_name = "quiz.db"
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    """удаляет все таблицы"""
    open()
    query = """DROP TABLE IF EXISTS quiz_content"""
    do(query)
    query = """DROP TABLE IF EXISTS question"""
    do(query)
    query = """DROP TABLE IF EXISTS quiz"""
    do(query)
    close()


def create():
    open()
    cursor.execute("PRAGMA foreign_keys=on")
    quiz_query = """
    CREATE TABLE IF NOT EXISTS quiz 
    (id INTEGER PRIMARY KEY,
    name VARCHAR,
    min_age INTEGER,
    max_age INTEGER)
    """
    do(quiz_query)
    question_query = """
    CREATE TABLE IF NOT EXISTS question
    (id INTEGER PRIMARY KEY,
    question VARCHAR,
    answer VARCHAR,
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR)
    """
    do(question_query)
    content_query = """
    CREATE TABLE IF NOT EXISTS quiz_content
    (id INTEGER PRIMARY KEY,
    quiz_id INTEGER,
    question_id INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
    FOREIGN KEY (question_id) REFERENCES question (id))
    """
    do(content_query)
    close()


def add_questions():
    questions = [
        ("Сколько месяцев в году имеют 28 дней?", "Все", "Один", "Ни одного", "Два"),
        (
            "Каким станет зелёный утёс, если упадёт в Красное море?",
            "Мокрым",
            "Красным",
            "Не изменится",
            "Фиолетовым",
        ),
        ("Какой рукой лучше размешивать чай?", "Ложкой", "Правой", "Левой", "Любой"),
        (
            "Что не имеет длины, глубины, ширины, высоты, а можно измерить?",
            "Время",
            "Глупость",
            "Море",
            "Воздух",
        ),
        (
            "Когда сетью можно вытянуть воду?",
            "Когда вода замёрзла",
            "Когда нет рыбы",
            "Когда уплыла золотая рыбка",
            "Когда сеть порвалась",
        ),
        (
            "Что больше слона и ничего не весит?",
            "Тень слона",
            "Воздушный шар",
            "Парашют",
            "Облако",
        ),
        (
            "Что может путешествовать по всему свету, оставаясь в углу?",
            "Марка",
            "Письмо",
            "Фотография",
            "Книга",
        ),
        (
            "Что может идти вперед, оставаясь на месте?",
            "Часы",
            "Календарь",
            "Поезд",
            "Человек",
        ),
        (
            "Какое животное самое высокое?",
            "Жираф",
            "Слон",
            "Кит",
            "Носорог",
        ),
        (
            "Какой континент самый маленький по площади?",
            "Австралия",
            "Антарктида",
            "Европа",
            "Южная Америка",
        ),
        (
            "Какая река самая длинная в мире?",
            "Амазонка",
            "Нил",
            "Янцзы",
            "Миссисипи",
        ),
        (
            "Какая планета ближе всего к Солнцу?",
            "Меркурий",
            "Венера",
            "Марс",
            "Юпитер",
        ),
        (
            "Какой инструмент используют для измерения артериального давления?",
            "Тонометр",
            "Термометр",
            "Стетоскоп",
            "Эндоскоп",
        ),
        (
            "Какой газ является основным компонентом атмосферы Земли?",
            "Азот",
            "Кислород",
            "Углекислый газ",
            "Водород",
        ),
    ]
    open()
    query = """
    INSERT INTO question
    (question, answer, wrong1, wrong2, wrong3)
    VALUES (?,?,?,?,?)
    """
    cursor.executemany(query, questions)
    conn.commit()
    close()


def add_quiz():
    quizes = [
        ("Своя игра", 12, 14),
        ("Кто хочет стать миллионером?", 14, 16),
        ("Самый умный", 10, 12),
    ]
    open()
    query = """
    INSERT INTO quiz
    (name, min_age, max_age)
    VALUES (?,?,?)
    """
    cursor.executemany(query, quizes)
    conn.commit()
    close()


def add_links():
    open()
    cursor.execute("PRAGMA foreign_keys=on")
    query = """
    INSERT INTO quiz_content
    (quiz_id, question_id) VALUES (?,?)
    """
    answer = input("Добавить связь (y/n)?")
    while answer != "n":
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y/n)?")
    close()


def get_quizes():
    """получить все викторины из БД"""
    query = "SELECT * FROM quiz ORDER BY id"
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result


def get_quiz_count():
    """получить количество викторин"""
    query = "SELECT MAX(quiz_id) FROM quiz_content"
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result


def get_random_quiz_id():
    """получить случайную викторину"""
    query = "SELECT quiz_id FROM quiz_content"
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    num = randint(0, len(result) - 1)
    rand_id = result[num][0]
    close()
    return rand_id


def show(table):
    query = "SELECT * FROM " + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()


def show_tables():
    show("question")
    show("quiz")
    show("quiz_content")


def get_next_question(question_id=0, quiz_id=1):
    open()
    query = """
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3 
    FROM quiz_content, question
    WHERE quiz_content.question_id == question.id 
    AND quiz_content.quiz_id == ?
    AND quiz_content.id > ?
    ORDER BY quiz_content.id
    """
    cursor.execute(query, [quiz_id, question_id])
    result = cursor.fetchone()
    close()
    return result


def check_answer(question_id, answer):
    query = """
    SELECT question.answer
    From quiz_content, question
    WHERE quiz_content.id == ?
    AND quiz_content.question_id = question.id
    """
    open()
    cursor.execute(query, [str(question_id), ])
    result = cursor.fetchone()
    close()
    if result is None:
        return False
    else:
        if result[0] == answer:
            return True
        else:
            return False


def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()
    print(get_next_question(1, 1))


if __name__ == "__main__":
    main()
