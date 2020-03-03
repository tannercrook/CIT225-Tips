import pymysql

def connection():
    conn = pymysql.connect(host="",
                           user = "",
                           passwd = "",
                           db = "")
    c = conn.cursor(pymysql.cursors.DictCursor)

    return c, conn
