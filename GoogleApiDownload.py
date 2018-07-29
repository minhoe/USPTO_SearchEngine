# -*- coding: utf-8 -*-
"""
    File : Downloading zip files of USPTO from Google API page
 Authors : Minhoe Hur
  +Email : mhoe.hur@gmail.com
          
 History :
  2013/04/15 Minhoe Hur - Created
  2016/11/11 Minhoe Hur - Modified
  2018/01/28 Minhoe Hur - Modified

   Notes :
  This program runs under Python 3.x Runtime Environments.
"""

from Decompression import Unzip
import glob, os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

# ------------------------------------------------------------------------------
# Configurations
URL_BASE    = 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/'    # Web page URL
FTP_BASE    = 'http://storage.googleapis.com/patents/grant_full_text/'              # File location URL
#LOCAL_BASE  = 'D:\\USPTO_Full_DB\\Patents'                                            # Local path for extracting zip files
#LOCAL_ZIP   = 'D:\\USPTO_Full_DB\\Patents\\Zipfiles'                                   # Local path for downloading bulk files
LOCAL_BASE  = '/Users/dninb/PycharmProjects/USPTO_Full_DB/Patents'                                      # For MAC OS
LOCAL_ZIP   = '/Users/dninb/PycharmProjects/USPTO_Full_DB/Patents/Zipfiles'                             # For MAC OS
YEAR_LIST = ['2018']
# ------------------------------------------------------------------------------


def filechk(fname, file_size):
    """
    :param fname:
    :param file_size:
    :return:
    Check whether downloaded file is same to the original file in the web
    """

    try:
        if os.path.getsize(LOCAL_ZIP+'/'+fname) == file_size:
            return True
        else:
            print(' Original file size : ', os.path.getsize(LOCAL_ZIP+'/'+fname), 'Downloaded file size :', file_size)
            os.remove(LOCAL_ZIP+'/'+fname)
            return False
    except os.error:
        print(' No file ', fname, ' found. ')
        return False


def get_file_names(Year):
    output = []
    # Loading all file URLs from Google USPTO page
    page_URL = URL_BASE + Year + '/'
    print(' - Accessing to USPTO URL : ', page_URL)
    req = Request(page_URL)
    try:
        #MainPage = urlopen(Download_config.URL_BASE)
        response = urlopen(req)
        MainPage_html = response.read()
        #html = MainPage.read().split('\n')
        #cnt = 1
        
        bs = BeautifulSoup(MainPage_html, 'html.parser')
       
        for html_line in bs.find_all("tr"):
            fname = ''
            fsize = 0
            for idx, html_line2 in enumerate(html_line.find_all("td", {"align":"left"})):
                #print(idx, '::', html_line2.text)
                if idx == 0 and '.zip' in str(html_line2.text):
                    #print(html_line2)
                    fname = str(html_line2.text)
                if idx == 1 and str(html_line2.text).isdigit():
                    fsize = int(str(html_line2.text))
            if fname is not '':
                output.append((fname, fsize))
                #print(fname, fsize)
    
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code, page_URL)
        return e.code, output
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason, page_URL)
        return e.code, output
    else:
        return 1, output    


def get_file_url(fname, Year):
    return URL_BASE+Year + '/' + fname


def download_uspto_files(FileList, Year):
    """
    :param FileList:
    :param Year:
    :return:
    Downloading all USPTO files
    """
    print(' - Downloading Year :',  year, 'Total :', len(FileList), ' Files are found.')
    
    try:
        idx = 0
        f_cnt = 0
        while idx < len(FileList):
            f_item = FileList[idx]
            
            FileURL = get_file_url(f_item[0], Year)
            f = urlopen(FileURL.replace('"', ''))
             
            meta = f.info()
            #print(meta)
            file_size = int(meta["Content-Length"])        
             
            if os.path.isfile(LOCAL_ZIP+'/'+f_item[0]) and filechk(f_item[0], file_size):
                print(' File [ %3d / %5d ]  %s already exists. Skip to download ' %(idx+1, len(FileList), f_item[0]))
                idx += 1
                f_cnt = 0
            else:
                print("Downloading [ %3d / %5d ]: %s Bytes: %s" % (idx+1, len(FileList), FileURL, file_size),)
                with open(LOCAL_ZIP+'/'+f_item[0], 'wb') as local_file:
                    local_file.write(f.read())
                if filechk(f_item[0], file_size):
                    print(' [ Succeed ]')
                    idx += 1
                    Unzip(LOCAL_ZIP, f_item[0], LOCAL_BASE)
                    #os.remove(Download_config.LOCAL_BASE+'\\'+fname)
                    #idx += 1
                    f_cnt = 0
                else:
                    f_cnt += 1
                    print(' [ Failed ]')
                    print(' Downloading again : ', FileURL)
            
            if f_cnt >= 3:
                print(' Fail to download. Skipping the url :', FileURL)
                idx += 1
                f_cnt = 0
             
    except HTTPError as e:
        print("HTTP Error:", e.code)
        print(FileURL)
    except URLError as e:
        print("URL Error:", e.reason, FileURL)


if __name__ == '__main__':
    for year in YEAR_LIST:
        chk, FileList = get_file_names(year)
        if chk is 1:
            download_uspto_files(FileList, year)
        else:
            print(' - Skip to download the year :', year)