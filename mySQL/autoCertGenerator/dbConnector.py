# Python connection with mySQL
# fetching data from mySQL personal db
# hard coding

def connectSQL(host,db,us,pw):
    import mysql.connector
    from mysql.connector import Error
    import pandas as pd
    
    try:
        con = mysql.connector.connect(host = host,
                                      database = db,
                                      user = us,
                                      password = pw)
                                      
        sql = "SELECT first_name,last_name FROM employees LIMIT 10" # cur version hard coded
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()

    #df = pd.DataFrame(cur.fetchall())
    #print(df)
        
    except Error as err:
        print(f"Failed to connect to MySQL: {err}")

    finally:
        if con.is_connected():
            cur.close()
            con.close()
            #print("MySQL connection is closed.")

if __name__ == "__main__":
    connectSQL()
