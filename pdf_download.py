# This python program downloads the PDF-file to the local folder 'pdf-files'

import os
from os import listdir
from os.path import isfile , join 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

from PyPDF2 import PdfReader, PdfWriter

import random

# disable HTTPS warning  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set the Url of the main Website 
url = "https://swgdrug.org/monographs.htm"

# Create an Array with urls of every PDF 
fileUrls = []

# Print every PDF-Url in CLI
def print_all_html_filelinks():
    i = 0
    print("================== All PDF Files ==================")
    for url in fileUrls: 
        i = i + 1
        print(i , ".: " , url)
        
    print("Anzahl PDF-Links: ",len(fileUrls))    


# Get all PDF links from Website url and save them in 'fileUrls'
def get_all_pdf_links():
    # Url Requests to get the Website as response object
    # verify=False because of an SSL Error with the specific website 
    response = requests.get(url, verify=False)

    # Parse obtained text
    soup = BeautifulSoup(response.text, 'html.parser')

    # look at every link and filter ohne references with .pdf ending 
    for link in soup.select("a[href$='.pdf']"):
        
        tmp_link = urljoin(url,link['href'])
        
        # Check if PDF is in "Monographs"-folder
        if "Monographs" not in tmp_link:
            continue
        # Check if Large_Logo PDF 
        if "Large_Logo" in tmp_link:
            continue
        
        # append then to 'fileUrls' array
        fileUrls.append(tmp_link)
        
    if (len(fileUrls) == 0):
        print("CHECKING AGAIN")
        get_all_pdf_links()
    

# download PDF into folder (with PDF link e.g. 'https://swgdrug.org/Monographs/A04%20HCl.pdf')
def download_pdf_files(fileUrl):
    
    # Create folder pdf-files if there is no such folder
    # TODO try under WINDOWS 
    folder_location = r'pdf-files'
    
    
    if not os.path.exists(folder_location):
        print("================== Creating folder: pdf-files ==================")
        os.mkdir(folder_location)

    # Request URL and get response object
    response = requests.get(fileUrl, stream=True, verify=False)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(fileUrl)
    
    print("================== Checking http-status-code ==================")
    # check status 200 is a successful response code
    if response.status_code == 200:
        
        print("Check successful, starting download...")
        # Save in current working directory
        filepath = os.path.join(folder_location, pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            # save PDF file byte wise with '.content'
            pdf_object.write(response.content)
        
        cut_pdf(filepath)
        # positive feedback 
        print(pdf_file_name, ' successfully downloaded in directory.')
        return True
            
    else:
        # negative feedback
        print('This file could not be downloaded: ', pdf_file_name)
        print('HTTP response status code: ',response.status_code)
        return False


# cut PDF-file that only first page exists 
def cut_pdf(filepath):
    reader = PdfReader(filepath)
    writer = PdfWriter()
    page = reader.pages[0]
    writer.add_page(page)
    
    with open(filepath, "wb") as filepage:
        writer.write(filepage)


# -------- main-functions ---------
# get every Link and download all PDFs into local folder
def download_all():
    # number of downloaded files
    i = 0
    
    get_all_pdf_links()
    for url in fileUrls:
        if download_pdf_files(url) == True:
            i += 1
            
    print("Downloaded ",i," files.")

# download num random files 
def download_random(num):
    get_all_pdf_links()
    for i in range(0,int(num)):
        tmp = random.randint(0,len(fileUrls))
        download_pdf_files(fileUrls[tmp])

# get extra info
def get_info():
    if len(fileUrls) == 0:
        get_all_pdf_links()
        
    print_all_html_filelinks()
    

