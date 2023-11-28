import psycopg2 
import psycopg2.extras
 
DB_HOST = "localhost"
DB_NAME = "perfumes"
DB_USER = "postgres"
DB_PASS = "123456"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)