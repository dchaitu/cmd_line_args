import sqlite3
import json
import sys

def create_quotes_table(cursor):
	cursor.execute(
		"""CREATE TABLE IF NOT EXISTS Quote 
		(
		quote_id INTEGER PRIMARY KEY,
		content text,
		author_id INTEGER,
		FOREIGN KEY(author_id) REFERENCES Author(id)
		
		)"""
	)

def create_tag_table(cursor):
	cursor.execute(
		"""CREATE TABLE IF NOT EXISTS Tag 
		(
		tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
		content text NOT NULL UNIQUE
		)"""
	)

# Junction Table
def create_quote_tag_table(cursor):
	cursor.execute(
		"""CREATE TABLE IF NOT EXISTS Quote_Tag 
		(
		tag_id INTEGER ,
		quote_id INTEGER,
		PRIMARY KEY (tag_id, tag_id),
		FOREIGN KEY(tag_id) REFERENCES Tag(tag_id)
		FOREIGN KEY(quote_id) REFERENCES Quote(quote_id)

		)"""
	)


def create_author_table(cursor):
	cursor.execute(
		"""CREATE TABLE IF NOT EXISTS Author
		(
		author_id INTEGER PRIMARY KEY AUTOINCREMENT,
		name text NOT NULL , 
		born text NOT NULL , 
		reference text UNIQUE NOT NULL
		)"""
	)



def insert_author_details(cursor):
	f = open('./updated_quotes_json.json','r')
	data = f.read()
	json_data = json.loads(data)
	for author in json_data["authors"]:
		cursor.execute('''INSERT OR IGNORE INTO Author (name, born, reference) VALUES (?, ?, ?)''', 
			(author['name'], author['born'], author['reference']))

	f.close()


def insert_quotes(cursor):
	f = open('./updated_quotes_json.json','r')
	data = f.read()
	json_data = json.loads(data)
	for quote in json_data["quotes"]:
		author_id = get_author_id(cursor,quote['author'])
		cursor.execute('''INSERT OR IGNORE INTO Quote (quote_id, content, author_id) VALUES (?, ?, ?)''', 
			(quote['id'], quote['quote'], author_id))

	f.close()

def insert_tags(cursor):
	f = open('./updated_quotes_json.json','r')
	data = f.read()
	json_data = json.loads(data)
	for quote in json_data["quotes"]:
		tags = quote['tags']
		for tag in tags:
			try:
				cursor.execute('''INSERT OR IGNORE INTO Tag (content) VALUES (?)''', (tag,))
			except sqlite3.IntegrityError:
				print(f'{tag} skipped already present')

	f.close()

def insert_quote_tag(cursor):
	f = open('./updated_quotes_json.json','r')
	data = f.read()
	json_data = json.loads(data)
	for quote in json_data["quotes"]:
		quote_id = quote['id']
		tags = quote['tags']

		for tag in tags:
			cursor.execute('''SELECT * FROM Tag WHERE content = ?''', (tag,))

			tag_id = cursor.fetchone()[0] if cursor.fetchone()!=None else None
			cursor.execute(
				'''INSERT OR IGNORE INTO Quote_Tag (quote_id, tag_id) VALUES (?, ?)''',
				(quote_id, tag_id)
			)





def get_author_id(cursor, name):
	cursor.execute('''SELECT author_id FROM Author WHERE name = (?)''',(name,))
	return cursor.fetchone()[0]

def get_quote(cursor, quote_id):
	cursor.execute('''SELECT content FROM Quote WHERE quote_id = (?)''',(quote_id,))
	return cursor.fetchone()[0]


def get_quotes_by_author(cursor, author_name):
	cursor.execute('''SELECT content FROM Quote WHERE author_id = (SELECT author_id FROM Author WHERE name = (?) )''',(author_name,))
	return cursor.fetchall()

def get_quotes_by_tag(cursor, tag):
	cursor.execute('''SELECT content FROM Quote WHERE quote_id IN (SELECT quote_id From Quote_Tag WHERE tag_id IN (SELECT tag_id FROM Tag WHERE content = (?)))''',(tag,))
	return cursor.fetchall()


def get_quotes_by_search_text(cursor, search_text):
	cursor.execute('''SELECT content FROM Quote WHERE content LIKE (?)''',('%' + search_text.lower() + '%',))
	return cursor.fetchall()
	
def populate_table(cursor):
	create_quotes_table(cursor)
	create_tag_table(cursor)
	create_quote_tag_table(cursor)
	create_author_table(cursor)
	insert_author_details(cursor)
	insert_quotes(cursor)
	insert_tags(cursor)
	insert_quote_tag(cursor)



if __name__ == '__main__':
	conn = sqlite3.connect('updated_quotes.db')
	cursor = conn.cursor()
	populate_table(cursor)
	if sys.argv[1]=="--quote" or sys.argv[1]=='-q':
		quote_id = int(sys.argv[2])
		quote = get_quote(cursor, quote_id)
		print(quote)

	elif sys.argv[1]=="--author" or sys.argv[1]=='-a':
		author_name = sys.argv[2]
		author_quotes = get_quotes_by_author(cursor, author_name)
		print(author_quotes)

	elif sys.argv[1]=="--tag" or sys.argv[1]=='-t':
		tag = sys.argv[2]
		author_quotes = get_quotes_by_tag(cursor, tag)
		print(author_quotes)


	elif sys.argv[1]=="--search" or sys.argv[1]=='-s':
		search_text = sys.argv[2]
		author_quotes = get_quotes_by_search_text(cursor, search_text)
		print(author_quotes)

	else:
		print(f"Error {sys.argv[1]} argument is not available")


	conn.close()

