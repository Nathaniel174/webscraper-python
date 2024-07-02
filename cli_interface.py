import cmd
from scripts import program


# ----------------------------------------------------------
#               CLI INTERFACE FOR WEBSCRAPER
# ----------------------------------------------------------

class Cli_Interface(cmd.Cmd):
    intro = 'Welcome to the CLI Interface of our webscraper project. Type help or ? to list commands.\n'
    prompt = '(webscraper) -> '
    file = None
    
    # ------- main dev commands -------

    # start collecting data from website if not already added to .json-file
    def do_collect(self, arg):
        program.collect_data()

    # delete all and start collecting data from website
    def do_recollect(self, arg):
        program.recollect_data()

    # delete PDFs and data.json
    def do_delete(self, arg):
        program.delete_data()

    # Quit CLI Interface
    def do_quit(self, arg):
        return True

    # ------- additional dev commands -------

    # start download from website
    def do_download(self, arg):
        program.download_pdf()

    # add PDF Data to data.json
    def do_extract(self, arg):
        program.add_to_json()

    # delete PDFs and data.json
    def do_validate(self, arg):
        program.validate_json_data()

if __name__ == '__main__':
    Cli_Interface().cmdloop()