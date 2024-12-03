import argparse
import sqlite3


class StorageImplementation:
	def __init__(self, db_name='updated_quotes.db'):
		self.conn = sqlite3.connect(db_name)
		self.cursor = self.conn.cursor()


	def __exit__(self, exc_type, exc_val, exc_tb):
		self.conn.commit()
		self.conn.close()

	def get_author_id(self, name):
		self.cursor.execute('''SELECT author_id FROM Author WHERE name = (?)''',(name,))
		return self.cursor.fetchone()[0]




	def get_quote(self, quote_id):
		self.cursor.execute('''SELECT content FROM Quote WHERE quote_id = (?)''',(quote_id,))
		return self.cursor.fetchone()[0]


	def get_quotes_by_author(self, author_name):
		self.cursor.execute('''SELECT content FROM Quote WHERE author_id = (SELECT author_id FROM Author WHERE name = (?) )''',(author_name,))
		return self.cursor.fetchall()

	def get_quotes_by_tag(self, tag):
		self.cursor.execute('''SELECT content FROM Quote WHERE quote_id IN (SELECT quote_id From Quote_Tag WHERE tag_id IN (SELECT tag_id FROM Tag WHERE content = (?)))''',(tag,))
		return self.cursor.fetchall()


	def get_quotes_by_search_text(self, search_text):
		self.cursor.execute('''SELECT content FROM Quote WHERE content LIKE (?)''',('%' + search_text.lower() + '%',))
		return self.cursor.fetchall()




if __name__ == '__main__':
	storage = StorageImplementation()
	parser = argparse.ArgumentParser(description="Accessing quotes")
	parser.add_argument('--quote', '-q', type=int, help='Get quotes by quote_id')
	parser.add_argument('--author', '-a', type=str, help='Get quotes by author_name')
	parser.add_argument('--tag', '-t', type=str, help='Get all quotes with the tag')
	parser.add_argument('--search', '-s', type=str, help='Get quotes by search_text')

	args = parser.parse_args()

	if args.quote:
		quote = storage.get_quote(args.quote)
		print(quote)

	elif args.author:
		author_quotes = storage.get_quotes_by_author(args.author)
		print(author_quotes)

	elif args.tag:
		author_quotes = storage.get_quotes_by_tag(args.tag)
		print(author_quotes)


	elif args.search:
		author_quotes = storage.get_quotes_by_search_text(args.search)
		print(author_quotes)

	else:
		print(f"Error  argument is not available")


