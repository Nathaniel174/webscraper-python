import cmd
import os
import time
from scripts import pdf_download, data_extraction, data_validation

# ----------------------------------------------------------
#               CLI INTERFACE FOR WEBSCRAPER
# ----------------------------------------------------------

class Cli_Interface(cmd.Cmd):
    intro = 'Welcome to the CLI Interface of our webscraper project. Type help or ? to list commands.\n'
    prompt = '(webscraper) -> '
    file = None
    
    # ------- basic dev commands -------

    # start download from website
    def do_downloadAll(self, arg):
        start = time.time()
        pdf_download.download_all()
        end = time.time()
        print(f"Ausführung dauerte {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

    # add PDF Data to data.json
    def do_addToJSON(self, arg):
        start = time.time()
        data_extraction.extract_to_json()
        end = time.time()
        print(f"Ausführung dauerte {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

    # validate data in data.json
    def do_valJSON(self, arg):
        start = time.time()
        data_validation.validate_data()
        end = time.time()
        print(f"Ausführung dauerte {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

    # delete PDFs and data.json
    def do_deleteDATA(self, arg):
        delete()

    # Quit CLI Interface
    def do_quit(self, arg):
        return True

    # Start the programm
    def do_start(self, arg):
        start = time.time()
        pdf_download.download_all()
        data_extraction.extract_to_json()
        data_validation.validate_data()
        end = time.time()
        print(f"Ausführung dauerte {time.strftime("%H:%M:%S", time.gmtime(end-start))}")
        
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