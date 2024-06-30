import cmd
from scripts import program


# ----------------------------------------------------------
#               CLI INTERFACE FOR WEBSCRAPER
# ----------------------------------------------------------

class Cli_Interface(cmd.Cmd):
    intro = 'Welcome to the CLI Interface of our webscraper project. Type help or ? to list commands.\n'
    prompt = '(webscraper) -> '
    file = None
    
    # ------- basic dev commands -------

    # start download from website
    def do_collect(self, arg):
        program.collect_data()

    # add PDF Data to data.json
    def do_recollect(self, arg):
        program.recollect_data()

    # delete PDFs and data.json
    def do_delete(self, arg):
        program.delete_data()

    # Quit CLI Interface
    def do_quit(self, arg):
        return True


if __name__ == '__main__':
    Cli_Interface().cmdloop()