# Functions for the User Interfaces

# Import packages/modules
import os
import time
import logging

# Import Scripts:
from scripts import pdf_download, data_extraction, data_validation

# Logging:
logger = logging.getLogger("program_logger")
hdlr = logging.FileHandler(os.path.join("logging", "program.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Paths
json_file_path = os.path.join("data", "output", "data.json")
pdf_folder_path = os.path.join("data", "pdf-files")

# ---------- MAIN FUNCTIONS ----------
def collect_data():

    start = time.time()
    pdf_download.download_all()
    data_extraction.extract_to_json()
    data_validation.validate_data()
    end = time.time()

    logger.info(f"Collection time:  {time.strftime("%H:%M:%S", time.gmtime(end - start))}")
    print(f"Collection time: {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

def recollect_data():

    start = time.time()
    delete()
    pdf_download.download_all()
    data_extraction.extract_to_json()
    data_validation.validate_data()
    end = time.time()

    logger.info(f"ReCollection time: {time.strftime("%H:%M:%S", time.gmtime(end - start))}")
    print(f"ReCollection time: {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

# delete function for user
def delete_data():
    try:
        delete()
        logger.info(f"Delete: Successfull")
        print(f"Delete: Successfull")

    except:
        logger.info(f"Delete: Error occurred")
        print(f"Delete: Error occurred")


# ---------- SUB FUNCTIONS ----------

# download pdf files from website into pdf-files
def download_pdf():
    start = time.time()
    pdf_download.download_all()
    end = time.time()
    print(f"Download time: {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

# add pdf-data to json file
def add_to_json():
    start = time.time()
    data_extraction.extract_to_json()
    end = time.time()
    print(f"Add pdf-data to 'data.json' time: {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

# validate data in json file
def validate_json_data():
    start = time.time()
    data_validation.validate_data()
    end = time.time()
    print(f"Validate time: {time.strftime("%H:%M:%S", time.gmtime(end - start))}")

# delete pdf-files and data.json
def delete():
    if not os.path.exists(pdf_folder_path):
        logger.error(f"PDF folder does not exist: {pdf_folder_path}")
        raise FileNotFoundError(f"PDF folder does not exist: {pdf_folder_path}")
    else:
        for file in os.listdir(pdf_folder_path):
            os.remove(pdf_folder_path + file)
            print(file + " successfully removed")

    if not os.path.exists(json_file_path):
        logger.error(f"data.json does not exist: {pdf_folder_path}")
        raise FileNotFoundError(f"data.json does not exist: {pdf_folder_path}")
    else:
        os.remove(json_file_path)
        print("data.json successfully removed")