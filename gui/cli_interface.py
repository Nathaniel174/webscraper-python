import cmd
import os

# import own scripts
from scripts.pdf_download import *
from scripts.data_extraction import *

class Cli_Interface(cmd.Cmd):
    intro = 'Welcome to the CLI Interface of our webscraper project. Type help or ? to list commands.\n'
    prompt = '(webscraper) -> '
    file = None
    
    # ------- basic dev commands -------
    def do_downloadAll(self, arg):
        download_all()
    
    def do_downloadRandom(self, arg):
        download_random(arg)
    
    def do_addToJSON(self, arg):
        add_all_to_json()
    
    def do_deleteDATA(self, arg):
        delete()
        
    def do_quit(self, arg):
        return True
        
def delete(): 
    if "pdf-files" in os.listdir("./"):
        for file in os.listdir("./pdf-files/"): 
            os.remove("./pdf-files/" + file)
            print(file + " successfully removed")
        os.rmdir("./pdf-files")
        print("pdf-files directory successfully removed")
    else: 
        print("There is no pdf-files directory")
    if "data.json" in os.listdir("./"):
        os.remove("./data.json")
        print("data.json successfully removed")
        
    else: 
        print("There is no data.json")

if __name__ == '__main__':
    Cli_Interface().cmdloop()