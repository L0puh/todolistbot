import sqlite3 as sq 

def create_db():
    global cur, db
    db = sq.connect('todo.db')
    cur = db.cursor()
    if db: 
        print('[+] Data base is connected ')
    with open('database/sq_db.sql', 'r') as f: 
        cur.execute(f.read())
    db.commit()

async def create_task_db(state):
    async with state.proxy() as data:
        try:
            cur.execute('INSERT INTO todolist VALUES(?, ?,?)', tuple(data.values()))
            db.commit() 
            print(f'[+] CREATE TASK: {data["text"]}')
        except sq.Error as er: 
            print(f'[-] CREATE TASK - Error: {er}')

async def show_all_tasks():
    try: 
        cur.execute('SELECT * FROM todolist')
        res = cur.fetchall()
        if res:
            print('[+] SHOW ALL TASKS')
            return res 
    except sq.Error as er: 
        print(f'[-] SHOW ALL TASKS - Error: {er} ')
        return [] 

async def delete_task(text): 
    
    try: 
        cur.execute('SELECT * FROM todolist')
        res = cur.fetchall()
        for i in res: 
            if text == i[0]:
                cur.execute(f'DELETE FROM todolist WHERE text = "{text}"')
                db.commit() 
                print(f'[+] DELETE TASK - {text}')
                return True 
                
        print(f'[-] DELETE TASK {text} - task not found ')
    except sq.Error as er: 
        print(f'[-] DELETE TASK {text} - Error: {er}')
    return False

async def change_task(text, state): 
    async with state.proxy() as data: 
        try:
   
            cur.execute(f'UPDATE todolist SET primary_task = ?, date = ? WHERE text = "{text}"', (tuple(data.values())))
            db.commit()
            print(f'[+] CHANGE TASK: {text} ')
        except sq.Error as er: 
            print(f'[-] CHANGE TASK: {text} - Error:{er}')
            return 