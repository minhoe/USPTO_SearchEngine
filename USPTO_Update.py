"""
    File : Main program of building or updating USPTO patent parsed file
 Authors : Minhoe Hur
  +Email : mhoe.hur@gmail.com

 History :
  2013/03/05 Minhoe Hur - Created
  2018/01/28 Minhoe Hur - Modified

   Notes :
  This program is runs under Python 3.x Runtime Environments.
"""
# -*- coding: utf-8 -*-

import io, os, glob, time, math
import xml.etree.ElementTree as ET
import itertools as IT
import re
import pickle
from USPTO_XML_Parser import xml_parsing
import USPTO

#------------------------------------------------------------------------------
# Configurations
LOCAL_BASE  = '/Users/dninb/PycharmProjects/USPTO_Full_DB/Patents' # Local path for extracting zip files
#------------------------------------------------------------------------------


start_time = time.time()

# Get the list of *.xml patent files
fileList = glob.glob(os.path.join(LOCAL_BASE, '*.xml'))
print(' - ', len(fileList), ' files are found.')

tot_ptn_no = 1
xml_ptn_no = 1

# Index files
PATENT_IDX = {}
PUB_COUNTRY_IDX = {}
PUB_DATE_IDX = {}
APP_DOCNUMBER_IDX = {}
#APP_COUNTRY_IDX = {} # Lack of memory..
#APP_DATE_IDX = {} # Lack of memory..
INV_TITLE_IDX = {}
APPLICANTS_IDX = {}
CITING_IDX = {}

## INDEX SETTING ------------------------------------------------------------------------------------

def IDX_SET_PATENT(USPTN):
    if USPTN.pub_docnumber in PATENT_IDX:
        print(' - Warning! Duplicate USPTN : ', USPTN)
    else:
        PATENT_IDX[USPTN.pub_docnumber] = USPTN

def IDX_SET_PUB_COUNTRY(USPTN):
    if USPTN.pub_country.upper() in PUB_COUNTRY_IDX:
        PUB_COUNTRY_IDX[USPTN.pub_country.upper()].append(USPTN.pub_docnumber)
    else:
        PUB_COUNTRY_IDX[USPTN.pub_country.upper()] = [USPTN.pub_docnumber]

def IDX_SET_PUB_DATE(USPTN):
    if USPTN.pub_date in PUB_DATE_IDX:
        PUB_DATE_IDX[USPTN.pub_date].append(USPTN.pub_docnumber)
    else:
        PUB_DATE_IDX[USPTN.pub_date] = [USPTN.pub_docnumber]

def IDX_SET_APP_DOCNUMBER_IDX(USPTN):
    if USPTN.app_docnumber in APP_DOCNUMBER_IDX:
        APP_DOCNUMBER_IDX[USPTN.app_docnumber].append(USPTN.pub_docnumber)
    else:
        APP_DOCNUMBER_IDX[USPTN.app_docnumber] = [USPTN.pub_docnumber]

# def IDX_SET_APP_COUNTRY(USPTN):
#     if USPTN.app_country.upper() in APP_COUNTRY_IDX:
#         APP_COUNTRY_IDX[USPTN.app_country.upper()].append(USPTN.pub_docnumber)
#     else:
#         APP_COUNTRY_IDX[USPTN.app_country.upper()] = [USPTN.pub_docnumber]
#
# def IDX_SET_APP_DATE_IDX(USPTN):
#     if USPTN.app_date in APP_DATE_IDX:
#         APP_DATE_IDX[USPTN.app_date].append(USPTN.pub_docnumber)
#     else:
#         APP_DATE_IDX[USPTN.app_date] = [USPTN.pub_docnumber]

def IDX_SET_INV_TITLE(USPTN):
    if USPTN.invention_title is not None and USPTN.invention_title != '':
        word_list = [t.lower() for t in USPTN.invention_title.split(' ')]
        for word in word_list:
            if word in INV_TITLE_IDX:
                INV_TITLE_IDX[word].append(USPTN.pub_docnumber)
            else:
                INV_TITLE_IDX[word] = [USPTN.pub_docnumber]

def IDX_SET_APPLICANTS(USPTN):
    #print(USPTN.Applicants_list)
    org_list = [item.orgname.lower() for item in USPTN.Applicants_list if item.orgname != '']
    for org in org_list:
        if org in APPLICANTS_IDX:
            APPLICANTS_IDX[org].append(USPTN.pub_docnumber)
        else:
            APPLICANTS_IDX[org] = [USPTN.pub_docnumber]

def IDX_SET_CITING(USPTN):
    # Citation
    for ptn in USPTN.citation_list:
        if ptn is None or ptn is '':
            pass
        else:
            #print(ptn)
            if ptn in CITING_IDX:
                CITING_IDX[ptn].append(USPTN.pub_docnumber)
            else:
                CITING_IDX[ptn] = [USPTN.pub_docnumber]
    # Other citation --> Skip to put other citations because of lack of memory.
    # for ptn in USPTN.other_reference_list:
    #     if ptn is None or ptn is '':
    #         pass
    #     else:
    #         #print('--->', ptn)
    #         if ptn in CITING_IDX:
    #             CITING_IDX[ptn].append(USPTN.pub_docnumber)
    #         else:
    #             CITING_IDX[ptn] = [USPTN.pub_docnumber]

## --------------------------------------------------------------------------------------------------


# Parsing *.xml files
for idx, file in enumerate(fileList):
    print(' - (% d / %d ) Loading %s file' %(idx+1, len(fileList), file))
    # Open file
    xml_file = open(file, 'r', encoding='utf-8')
    # Load contents from the file
    xml_contents = xml_file.read()

    # Remove namespaces (e.g. <!xml version ...> or <!DOCTYPE... >)
    #xml_contents = re.sub("(<\?|<!DOCTYPE).*>", "", xml_contents)
    xml_contents = re.sub("<\?[\s\S]*?>", "", xml_contents)
    xml_contents = re.sub("<!DOCTYPE[\s\S]*?>", "", xml_contents)

    #print(xml_contents)

    # Place the root node for parsing process
    try:
        tree = ET.fromstring("<root>\n" + xml_contents + "</root>")
    except ET.ParseError as err:
        lineno, column = err.position
        line = next(IT.islice(io.StringIO(xml_contents), lineno))
        caret = '{:=>{}}'.format('^', column)
        err.msg = '{}\n{}\n{}'.format(err, line, caret)
        print(' - Cannot parse the file :', file, '. Please check the *.xml format is properly defined.')
        #raise
    else:
        # Extract the information
        xml_ptn_no = 1
        for item in tree.findall('us-patent-grant'):
            USPTN = USPTO.USPatent()
            parse_chk = xml_parsing(item.attrib.get('dtd-version'), item, file, USPTN)

            if parse_chk == 1:
                # Index Setting
                IDX_SET_PATENT(USPTN)
                IDX_SET_PUB_COUNTRY(USPTN)
                IDX_SET_PUB_DATE(USPTN)
                IDX_SET_APP_DOCNUMBER_IDX(USPTN)
                #IDX_SET_APP_COUNTRY(USPTN)
                #IDX_SET_APP_DATE_IDX(USPTN)
                IDX_SET_INV_TITLE(USPTN)
                IDX_SET_APPLICANTS(USPTN)
                IDX_SET_CITING(USPTN)

                print('   > Saved Patent :  %10s  | Val : %18s | Total : %10d | In Xml : %10d '
                      %(USPTN.pub_docnumber, USPTN.valid_patent(), tot_ptn_no, xml_ptn_no))

                tot_ptn_no += 1
                xml_ptn_no += 1
            else:
                print('   > Cannot save the patent because of the failures in parsing process')

# Save database
print('\n - Saving Patent datafiles to ', LOCAL_BASE)
with open(os.path.join(LOCAL_BASE, 'Index_DB.bin'), 'wb') as fw:
    pickle.dump(PUB_COUNTRY_IDX, fw)
    pickle.dump(PUB_DATE_IDX, fw)
    pickle.dump(APP_DOCNUMBER_IDX, fw)
    pickle.dump(APP_COUNTRY_IDX, fw)
    pickle.dump(APP_DATE_IDX, fw)
    pickle.dump(INV_TITLE_IDX, fw)
    pickle.dump(APPLICANTS_IDX, fw)
    pickle.dump(CITING_IDX, fw)

with open(os.path.join(LOCAL_BASE, 'Patent_DB.bin'), 'wb') as fw:
    pickle.dump(PATENT_IDX, fw)

m, s = divmod(time.time() - start_time, 60)
h, m = divmod(m, 60)

print("\nTime elapsed : %d:%02d:%02d" % (h, m, s))

print('Program successfully terminated.')