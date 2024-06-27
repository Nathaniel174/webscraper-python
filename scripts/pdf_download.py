# This python program downloads the PDF-file to the local folder 'pdf-files'

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3
from PyPDF2 import PdfReader, PdfWriter
import json
import logging
from datetime import datetime

# disable HTTPS warning  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set the Url of the main Website 
url = "https://swgdrug.org/monographs.htm"

# Set header for http-get request
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Accept-Language': 'de-DE,de;q=0.7',
    'Referer': 'https://google.com',
    'DNT': '1'
}

# Setup logging:
logger = logging.getLogger("download_logger")
hdlr = logging.FileHandler(os.path.join("logging", "download.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Create an Array with urls of every PDF 
file_urls = []

# Create an Array with urls of already downloaded and initilized PDFs
already_downloaded_urls = []

# Print every PDF-Url in CLI
def print_all_html_filelinks():
    i = 0
    print("================== All PDF Files ==================")
    for url in file_urls: 
        i = i + 1
        print(i , ".: " , url)
    print("Anzahl PDF-Links: ",len(file_urls))

# Get all already downloaded PDF-links from 'data.json'
def init_all_downloaded_urls():
    try:
        file = open('data.json')
        data = json.load(file)
        for chemical in data:
            already_downloaded_urls.append(chemical['source'][1])
        file.close()
    except:
        logger.warning("There is no data.json file")

# Get all PDF-links from Website url and save them in 'file_urls'
def get_all_pdf_links():
    logger.info("Getting all html filelinks on Website...")

    try:
        # Url Requests to get the Website as response object
        # verify=False because of an SSL Error with the specific website
        response = requests.get(url, verify=False, headers=headers)

        # Parse obtained text
        soup = BeautifulSoup(response.text, 'html.parser')

        # look at every link and filter all references with .pdf ending
        for link in soup.select("a[href$='.pdf']"):
            tmp_link = urljoin(url,link['href'])

            # Check if PDF is in "Monographs"-folder
            if "/Monographs/" not in tmp_link:
                continue
            # Check if Large_Logo PDF
            if "Large_Logo" in tmp_link:
                continue

            # then append NOT downloaded link to 'file_urls' array
            if tmp_link not in already_downloaded_urls:
                file_urls.append(tmp_link)

        if (len(file_urls) == 0):
            logger.warning("All PDFs already downloaded and initialized into data.json")
        logger.info(f"Anzahl PDF-Links: {len(file_urls)}")
    except:
        logger.critical("Something went wrong during getting all pdflinks")

def download_pdf_files(fileUrl):
    # Create folder pdf-files if there is no such folder
    folder_location = r'pdf-files'
    
    if not os.path.exists(folder_location):
        logger.info("Creating pdf-folder")
        os.mkdir(folder_location)

    try:
        # Request URL and get response object
        response = requests.get(fileUrl, stream=True, verify=False, headers=headers)

        # isolate PDF filename from URL
        pdf_file_name = os.path.basename(fileUrl)

        logger.info(f"Checking HTTP Status Code for {pdf_file_name}")
        # check status 200 is a successful response code
        if response.status_code == 200:
            logger.info("Check successful, starting download...")
            # Save in current working directory
            filepath = os.path.join(folder_location, pdf_file_name)
            with open(filepath, 'wb') as pdf_object:
                # save PDF file byte wise with '.content'
                pdf_object.write(response.content)
            cut_pdf(filepath)
            logger.info(f"Successfully downloaded {pdf_file_name}")
            return True
            
        else:
            logger.warning(f"This file could not be downloaded: {pdf_file_name}")
            logger.warning(f"HTTP response status code: {response.status_code}")
            return False
    except:
        logger.error(f"Something went wrong during downloading this file: {fileUrl}")

# cut PDF-file that only first page exists 
def cut_pdf(filepath):
    reader = PdfReader(filepath)
    writer = PdfWriter()
    page = reader.pages[0]
    writer.add_page(page)
    
    with open(filepath, "wb") as filepage:
        writer.write(filepage)

# get extra info
def get_info():
    if len(file_urls) == 0:
        get_all_pdf_links()
    print_all_html_filelinks()

# -------- main-functions ---------
# get every Link and download all PDFs into local folder
def download_all():
    # number of downloaded files
    i = 0

    # get already download Urls and new Urls
    init_all_downloaded_urls()
    get_all_pdf_links()

    # If new Urls exists download pdfs
    if (len(file_urls) > 0):
        # Get some info for the User
        get_info()

        print("Starting Download...")
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        logger.info(f"STARTING DOWNLOAD at {date_time}")

        for url in file_urls:
            if download_pdf_files(url) == True:
                i += 1
            else:
                logger.warning(f"This file could not be downloaded: {url}")

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        logger.info(f"FINISHED DOWNLOAD at {date_time}")
        logger.info(f"Downloaded {i} files")
        print("Downloaded ",i," files")
        if((len(file_urls) - i) > 0):
            print(f"There are {len(file_urls)-i} PDFs that could not be downloaded. Check Download logs for more Information. ")
            logger.warning(f"{len(file_urls) - i} could NOT be downloaded")
    else:
        print("There are no PDF-files to download")
        logger.info("There are no PDF-files to download")