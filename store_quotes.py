import json
import sqlite3


def create_author_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Authors
        (
        id INTEGER PRIMARY KEY ,
        name text NOT NULL , 
        born text NOT NULL , 
        reference text UNIQUE NOT NULL
        )"""
    )


def create_quotes_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Quotes 
        (
        quotes_id INTEGER PRIMARY KEY AUTO,
        quote text,
        author_id INTEGER,
        FOREIGN KEY(author_id) REFERENCES Authors(id)
        )"""
    )


def create_tags_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Tags 
        (
        tags_id INTEGER PRIMARY KEY ,
        quote text,
        tags text,
        quotes_id INTEGER,
        FOREIGN KEY(quotes_id) REFERENCES Quotes(quotes_id)
        )"""
    )


def insert_authors():
    authors_set = set()
    for row in traffic["authors"]:
        authors = (row["name"], row["born"], row["reference"])
        authors_set.add(authors)

    for author in authors_set:
        cursor.execute(
            "INSERT OR IGNORE INTO Authors(name,born,reference) values(?,?,?)", author
        )


def insert_quotes():
    author_id_name = {}
    author_details = cursor.execute("""SELECT id,name FROM Authors""")
    for author in author_details:
        author_id_name.update({author[1]: author[0]})

    for i in range(len(traffic["quotes"])):
        quotes = (
            author_id_name[traffic["quotes"][i]["author"]],
            traffic["quotes"][i]["quote"],
        )

        cursor.execute(
            "INSERT OR IGNORE INTO Quotes(author_id,quote) values(?,?)", quotes
        )


def insert_tags():
    quote_id_dict = {}
    quote_details = cursor.execute("""SELECT quotes_id,quote FROM Quotes""")
    for quote in quote_details:
        quote_id_dict.update({quote[1]: quote[0]})

    for i in range(len(traffic["quotes"])):
        for tag in traffic["quotes"][i]["tags"]:
            quote_tags = (quote_id_dict[traffic["quotes"][i]["quote"]], tag)
            cursor.execute(
                "INSERT OR IGNORE INTO Tags(tags,quotes_id) values(?,?)", quote_tags
            )


if __name__ == "__main__":

    connection = sqlite3.connect("quotes.db")
    cursor = connection.cursor()
    traffic = json.load(open("quotes.json"))

    create_author_table()
    create_quotes_table()
    create_tags_table()

    insert_authors()
    insert_quotes()
    insert_tags()

    connection.commit()
    connection.close()
