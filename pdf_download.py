# This python program downloads the PDF-file to the local folder 'pdf-files'

import os
from os import listdir
from os.path import isfile , join 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

import random

# disable HTTPS warning  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set the Url of the main Website 
url = "https://swgdrug.org/monographs.htm"

# Create an Array with urls of every PDF 
fileUrls = []

# Print every PDF-Url in CLI
def print_all_html_filelinks():
    for url in fileUrls: 
        print(url)


# Get all PDF links from Website url and save them in 'fileUrls'
def get_all_pdf_links():
    # Url Requests to get the Website as response object
    # verify=False because of an SSL Error with the specific website 
    response = requests.get(url, verify=False)

    # Parse obtained text
    soup = BeautifulSoup(response.text, 'html.parser')

    # look at every link and filter ohne references with .pdf ending 
    for link in soup.select("a[href$='.pdf']"):
        # append then to 'fileUrls' array
        fileUrls.append(urljoin(url,link['href']))


# download PDF into folder (with PDF link e.g. 'https://swgdrug.org/Monographs/A04%20HCl.pdf')
def download_pdf_files(fileUrl):
    
    # Create folder pdf-files if there is no such folder
    # TODO try under WINDOWS 
    folder_location = r'pdf-files'
    if not os.path.exists(folder_location):os.mkdir(folder_location)

    # Request URL and get response object
    response = requests.get(fileUrl, stream=True, verify=False)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(fileUrl)
    
    # check status 200 is a successful response code
    if response.status_code == 200:
        
        # Save in current working directory
        filepath = os.path.join(folder_location, pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            # save PDF file byte wise with '.content'
            pdf_object.write(response.content)
            # positive feedback 
            print(pdf_file_name, ' successfully downloaded in directory.')
            
    else:
        # negative feedback
        print('This file could not be downloaded: ', pdf_file_name)
        print('HTTP response status code: ',response.status_code)


# cut PDF-file that only first page exists 
def cut_pdf(file):
    pass


# -------- main-functions ---------
# get every Link and download all PDFs into local folder
def download_all():
    get_all_pdf_links()
    for url in fileUrls:
        download_pdf_files(url)

# download num random files 
def download_random(num):
    get_all_pdf_links()
    for i in range(0,int(num)):
        tmp = random.randint(0,len(fileUrls))
        download_pdf_files(fileUrls[tmp])

# get extra info
def get_info():
    print_all_html_filelinks()
    print(len(fileUrls))