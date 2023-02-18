"""
Contains defined function for app.py usage
"""
import sqlite3
from collections import deque

# getting next number

def get_next_num(service,branch):
    with sqlite3.connect('bankQueue.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f'SELECT * FROM {branch};')
        rows = cur.fetchall()

    que = deque()
    for r in rows:
        if r[2] == service and r[3] == 'Individual':
            que.append(r[0])
        elif r[3] == 'Corporate':
            que.append(r[0])

    if que:
        next_num = que[0]
        waiting = []
        for i in range(1, len(que)):
            waiting.append(que[i])
        to_delete = que.popleft()
        cur.execute(f"DELETE FROM {branch} WHERE q_num = {to_delete}")
        con.commit()
    else:
        next_num = None
        waiting = None
        to_delete = None

    return next_num,waiting,to_delete
