import re
from sanic import Sanic
from sanic import response
import sqlite3

class db_adapter():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS records
                  (amount integer, email text, fio text)
               """)

    def sp_SaveData(self, amount, email, fio):
        self.cur.execute("""INSERT INTO records VALUES (?,?,?)""", amount, email, fio)
        return amount % 2


db = None
app = Sanic(__name__)

app.static('/', './static')
app.static('/', './static/index.html', 
    content_type="text/html; charset=utf-8")



@app.route("/submit", methods=['POST','GET'])
async def SaveData(r):
    #print(dir(r))
    #print(r.body)
    print(r.json)
    data = r.json
    
    try:
        amount = int(data["amount"])
        email = data["email"]
        fio = data["fio"]

        parity = db.sp_SaveData(amount, email, fio)

    except ValueError:
        return response.json({
            "error": "Validation Error", 
            "text": "Validation Error"
        })
        



    return response.json({"text":"record added", "parity":bool(parity)})


class db_adapter():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS records
                  (amount integer, email text, fio text)
               """)

    def sp_SaveData(self, amount, email, fio):

        re_mail = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(re_mail, email) == None:
            raise ValueError

        if re.match(r"(^[a-zA-Z\s]+$)",fio) == None:
            raise ValueError

        if(amount>10 or amount <0):
            raise ValueError

        self.cur.execute("""INSERT INTO records VALUES (?,?,?)""",
            (amount, email, fio))
        self.conn.commit()
        return amount % 2

    def count(self):
        results = self.cur.execute("""SELECT COUNT(*) from records""")
        return results.fetchone()[0]

    def peek(self):
        results = self.cur.execute("""SELECT * from records""")
        for r in results:
            print(r)
if __name__ == "__main__":
    #conn = sqlite3.connect("database.db") # или :memory: чтобы сохранить в RAM
    #cursor = conn.cursor()

    db = db_adapter(":memory")

    app.run(host="0.0.0.0", port=8000)