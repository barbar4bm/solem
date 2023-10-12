from decouple import config 
import pymysql

def get_connection():
    try:
        return pymysql.connect(
            host=config('localhost')
            password=condfig('postgres')
            db=config('postgres')
        )
    except Exception as ex:
        print(ex)