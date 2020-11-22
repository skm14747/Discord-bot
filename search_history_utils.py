from db_utils import db_connect
from datetime import datetime


def add_search_history(search_keyword):
    con = db_connect()
    cur = con.cursor()

    # This query will update the timestamp with latest time for same query getting again and again
    product_sql = "insert or replace into search_history (ID, search_key) values ((select ID from search_history where search_key = ?), ?);"
    cur.execute(product_sql, (search_keyword, search_keyword))
    con.commit()


def get_search_history(search_key):
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT search_key FROM search_history WHERE search_key like '{0}' ORDER BY t DESC".format("%{0}%".format(search_key)))
    res = cur.fetchall()
    
    return [s_key[0] for s_key in res]
