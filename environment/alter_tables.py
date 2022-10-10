import psycopg

def alter_tables():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg.connect("dbname=postgres user=postgres password=postgres host=localhost port=5432")
        return conn
    except:
        print("Unable to connect to the database")

def main():
    """Connect to the PostgreSQL database server."""
    conn = alter_tables()
    cur = conn.cursor()
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS head_type TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS head TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS relation TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS tail_type TEXT;")
    cur.execute("ALTER TABLE examples_example ADD COLUMN IF NOT EXISTS tail TEXT;")
    conn.commit()

if __name__ == '__main__':
    main()