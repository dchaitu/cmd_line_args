import click
from argparse_quotes import StorageImplementation

# @click.group()
# def cli():
#     """Quotes CLI with multiple commands"""
#     pass

class ClickCLI:
    def __init__(self):
        self.cli = click.Group()
        self.cli.add_command(self.get_author_id)
        self.cli.add_command(self.get_quote)
        self.cli.add_command(self.get_quotes_by_author)
        self.cli.add_command(self.get_quotes_by_tag)
        self.cli.add_command(self.get_quotes_by_search_text)
        self.storage = StorageImplementation()


    @click.command()
    @click.option('--name', '-n',type=str, help='Get author_id from author name')
    def get_author_id(self, name):
        result = self.storage.get_author_id(name)
        click.echo(result)

    @click.command()
    @click.option('--quote', '-q',type=int, help='Get quotes by quote_id')
    def get_quote(self, quote):
        result = self.storage.get_quote(quote)
        click.echo(result)

    @click.command()
    @click.option('--author', '-a',type=str, help='Get quotes by author_name')
    def get_quotes_by_author(self, author_name):
        results = self.storage.get_quotes_by_author(author_name)
        for quote in results:
            click.echo(quote)

    @click.command()
    @click.option('--tag', '-t',type=str, help='Get all quotes with the tag')
    def get_quotes_by_tag(self, tag):
        results = self.storage.get_quotes_by_tag(tag)
        for quote in results:
            click.echo(quote)


    @click.command()
    @click.option('--search', '-s',type=str, help='Get quotes by search_text')
    def get_quotes_by_search_text(self, search_text):
        quotes = self.storage.get_quotes_by_search_text(search_text)
        for quote in quotes:
            click.echo(quote)


if __name__ == '__main__':
    click = ClickCLI()
    click.cli()




