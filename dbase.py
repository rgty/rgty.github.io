import pymysql
import configparser

def get_connection():
	config = configparser.ConfigParser()
	config.read('config.ini')
	try:
		mysql = config['MYSQL']
		return pymysql.connect(host=mysql['host'],
           port=int(mysql['port']),
           user=mysql['user'],
           passwd=mysql['pass'],
           db=mysql['db'],
           cursorclass=pymysql.cursors.DictCursor)
	except Exception as e:
		print(str(e))