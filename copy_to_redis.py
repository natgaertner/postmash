from postgres_conn import get_connection
from psycopg2.extras import DictCursor
import redis

def get_posts():
    conn = get_connection('postmash')
    sql = "SELECT postid, text from posts"
    curs = conn.cursor(cursor_factory=DictCursor)
    curs.execute(sql)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for row in curs.fetchall():
	print row['postid']
	r.set(row['postid'],row['text'])

if __name__ == '__main__':
    get_posts()
