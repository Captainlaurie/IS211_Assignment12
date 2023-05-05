import sqlite3 as lite


if __name__ == "__main__":
    
    con = lite.connect('studentquizzes.db')
    
    
    with con:
    
        cur = con.cursor()
        
        cur.execute("DROP TABLE IF EXISTS students")
        
        cur.execute("""CREATE TABLE students (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT)""")
        
        
        cur.execute("DROP TABLE IF EXISTS quizzes")
        
        cur.execute("""CREATE TABLE quizzes (quizid INTEGER PRIMARY KEY, subject TEXT, num_questions INT, quiz_date DATE)""")
        
        
        cur.execute("DROP TABLE IF EXISTS results")
        
        cur.execute("""CREATE TABLE results (studentid INT, quizid INT, score INT )""")
        
