"""
    File : Search modules for US Patents
 Authors : Minhoe Hur
  +Email : mhoe.hur@gmail.com

 History :
  2018/03/03 Minhoe Hur - Created

   Notes :
  This program is runs under Python 3.x Runtime Environments.
"""
# -*- coding: utf-8 -*-

import pickle
import os
import time
import sys

# ------------------------------------------------------------------------------
# Configurations
LOCAL_BASE   = '/Users/dninb/PycharmProjects/USPTO_Full_DB/Patents' # Local path for extracting zip files
DEFAULT_PATH = '/Users/dninb/PycharmProjects/USPTO_Full_DB'
now = time.localtime()
# ------------------------------------------------------------------------------


def Valid_Keywords(_KEYWORDS):
    Keyword_list = []
    if _KEYWORDS != '' and _KEYWORDS != []:
        try:
            Keyword_list = _KEYWORDS.split(',')

            idx = 0
            while idx < len(Keyword_list):
                if Keyword_list[idx] is '':
                    del Keyword_list[idx]
                elif '_' in Keyword_list[idx]:
                    Keyword_list[idx] = Keyword_list[idx].replace('_', ' ')
                else:
                    pass
                idx = idx + 1
            return Keyword_list, True
        except:
            print(' Parameter Error in text words :')
            print(' Please put semi-colon(;) between each words')
            return Keyword_list, False
    else:
        return Keyword_list, True


def Valid_Date(DATE, Mode):

    if Mode == 'From':
        DATE_return = '00000101'
    elif Mode == 'To':
        DATE_return = '99991231'
    else:
        print(' - Error in Valid date.')
        sys.exit(-1)

    if DATE == '' or len(DATE) == 0:
        return DATE_return, True

    DATE_return = DATE.replace('-', '').replace('/', '')

    date_len = len(DATE_return)
    if date_len > 8 or date_len < 4:
        print('Parameter Error in Date :')
        print(' Please check the format of date (e.g. YYYYMMDD, YYYYMM, YYYY)')
        return DATE, False

    if date_len == 4:
        DATE_return = DATE_return + '0000'
    elif date_len == 5:
        DATE_return = DATE_return[:4] + '0' + DATE_return[4] + '00'
    elif date_len == 6:
        DATE_return = DATE_return + '00'
    elif date_len == 7:
        DATE_return = DATE_return[:6] + '0' + DATE_return[6]
    else:
        pass

    try:
        #DATE_int = int(DATE)
        if int(DATE_return[4:6]) < 0 or int(DATE_return[4:6]) > 12:
            print('Parameter Error in Date :')
            print(' Please check the Month of date 00 <= MM <= 12')
            return DATE, False
        elif int(DATE_return[6:8]) < 0 or int(DATE_return[6:8]) > 31:
            print('Parameter Error in Date :')
            print(' Please check the Day of date 00 <= DD <= 31')
            return DATE, False
        else:
            #DATE_int = int(DATE)
            return DATE_return, True

    except:
        print(' Parameter Error in Date :')
        print(' Please check the format of date (e.g. YYYYMMDD, YYYYMM, YYYY)')
        return DATE, False


def Valid_FromTo(self, FirstDay, LastDay, _FROM, _TO):
    VALID = True
    if _FROM < FirstDay or _FROM > LastDay:
        print('Parameter Error in From :')
        print(' Please check the date. ')
        VALID = False
    if _TO < FirstDay or _TO > LastDay:
        print('Parameter Error in To :')
        print(' Please check the date.')
        VALID = False
    if _FROM > _TO:
        print('Parameter Error in From and To :')
        print(' Please check the date. To date should be later than From date')
        VALID = False
    return VALID


def DocNoToList(doc_src, mode):

    ElementList = []
    if mode == 'file':
        if doc_src != '':
            try:
                fid = open(os.path.join(doc_src), 'r')
                ElementList = [line.strip() for line in fid]
                fid.close()
            except:
                print(' - Cannot find the Patent List file : ', os.path.join(doc_src))
    elif mode == 'param':
        if doc_src == '':
            pass
        elif '[' not in doc_src and ']' not in doc_src:
            print(' - Document numbers in parameter should be in [ ... ]')
        else:
            try:
                ElementList = eval(doc_src)
            except:
                print(' Error. Failed to read doc numbers from parameter')
                sys.exit(-1)
    else:
        pass
    return ElementList


# self.pub_docnumber = ''  # (1)
# self.pub_country = ''  # To be searched (2)
# self.pub_kind = ''  # (3)
# self.pub_date = ''  # To be searched (4)
#
# self.app_docnumber = ''  # To be searched (5)
# self.app_country = ''  # To be searched (6)
# self.app_date = ''  # To be searched (7)
#
# self.invention_title = ''  # To be searched (8)
#
# self.Applicants_list = []  # To be searched (9)
#
# self.Assignees_list = []  # (10)
#
# self.classification_national_list = []  # (11)
#
# self.classification_ipc_list = []  # (12)
#
# self.field_of_classification_search_list = []  # (13)
#
# self.number_claims = ''  # (14)
#
# self.citation_list = []  # (15)
#
# self.other_reference_list = []  # (16)


def PatentToFile(Doc, CITING_IDX, fw):

    result = '\t'.join([Doc.pub_docnumber,
                        Doc.pub_country,
                        Doc.pub_kind,
                        Doc.pub_date,
                        Doc.invention_title,
                        '%'.join([repr(x) for x in Doc.Applicants_list]),
                        '%'.join([repr(x) for x in Doc.Assignees_list]),
                        '%'.join(Doc.classification_national_list),
                        '%'.join([repr(x) for x in Doc.classification_ipc_list]),
                        '%'.join([repr(x) for x in Doc.field_of_classification_search_list]),
                        '%'.join([repr(x) for x in Doc.citation_list]),
                        '%'.join([repr(x) for x in Doc.other_reference_list])
                        ])
    if Doc.pub_docnumber in CITING_IDX:
        citing_list = '%'.join([repr(x) for x in CITING_IDX[Doc.pub_docnumber]])
        result = result + '\t' + citing_list
    #print(result)
    #print(CITING_IDX[Doc.pub_docnumber])
    fw.write(result)
    fw.write('\n')

start_time = time.time()


if __name__ == '__main__':
    # Index files
    PATENT_IDX = {}
    PUB_COUNTRY_IDX = {}
    PUB_DATE_IDX = {}
    APP_DOCNUMBER_IDX = {}
    APP_COUNTRY_IDX = {}
    APP_DATE_IDX = {}
    INV_TITLE_IDX = {}
    APPLICANTS_IDX = {}
    CITING_IDX = {}

    # Input variables
    CodePathFile = ''
    Tgt_Doc_No = ''
    DocList_file  = []
    DocList_param = []
    AND_KEYWORDS = []
    OR_KEYWORDS  = []
    NOT_KEYWORDS = []
    Pub_FROM = ''
    Pub_TO = ''
    App_FROM = ''
    App_TO = ''
    Applicant = ''

    # Open database
    try:
        print(' - Loading Index database : ', os.path.join(LOCAL_BASE, 'Index_DB.bin'))
        with open(os.path.join(LOCAL_BASE, 'Index_DB.bin'), 'rb') as f:
            #PATENT_IDX = pickle.load(f)
            PUB_COUNTRY_IDX = pickle.load(f)
            PUB_DATE_IDX = pickle.load(f)
            APP_DOCNUMBER_IDX = pickle.load(f)
            APP_COUNTRY_IDX = pickle.load(f)
            APP_DATE_IDX = pickle.load(f)
            INV_TITLE_IDX = pickle.load(f)
            APPLICANTS_IDX = pickle.load(f)
            CITING_IDX = pickle.load(f)

            #print(CITING_IDX.keys())

    except:
        print(' - ERROR on loading USPTO database. ')
        print(' - Please check the database file : ', os.path.join(LOCAL_BASE, 'Index_DB.bin'))
        sys.exit(-1)

    # Get the descriptive statistics for Index files
    #cnt_PATENT_IDX,        min_PATENT_IDX,        max_PATENT_IDX        = len(PATENT_IDX), min(PATENT_IDX), max(PATENT_IDX)
    cnt_PUB_COUNTRY_IDX,   min_PUB_COUNTRY_IDX,   max_PUB_COUNTRY_IDX   = len(PUB_COUNTRY_IDX), min(PUB_COUNTRY_IDX), max(PUB_COUNTRY_IDX)
    cnt_PUB_DATE_IDX ,     min_PUB_DATE_IDX,      max_PUB_DATE_IDX      = len(PUB_DATE_IDX), min(PUB_DATE_IDX), max(PUB_DATE_IDX)
    #cnt_APP_DOCNUMBER_IDX, min_APP_DOCNUMBER_IDX, max_APP_DOCNUMBER_IDX = len(APP_DOCNUMBER_IDX), min(APP_DOCNUMBER_IDX), max(APP_DOCNUMBER_IDX)
    cnt_APP_COUNTRY_IDX,   min_APP_COUNTRY_IDX,   max_APP_COUNTRY_IDX   = len(APP_COUNTRY_IDX), min(APP_COUNTRY_IDX), max(APP_COUNTRY_IDX)
    cnt_APP_DATE_IDX,      min_APP_DATE_IDX,      max_APP_DATE_IDX      = len(APP_DATE_IDX), min(APP_DATE_IDX), max(APP_DATE_IDX)
    cnt_INV_TITLE_IDX,     min_INV_TITLE_IDX,     max_INV_TITLE_IDX     = len(INV_TITLE_IDX), min(INV_TITLE_IDX), max(INV_TITLE_IDX)
    cnt_APPLICANTS_IDX,    min_APPLICANTS_IDX,    max_APPLICANTS_IDX    = len(APPLICANTS_IDX), min(APPLICANTS_IDX), max(APPLICANTS_IDX)
    cnt_CITING_IDX,        min_CITING_IDX,        max_CITING_IDX        = len(CITING_IDX), min(CITING_IDX), max(CITING_IDX)

    # Print the descriptive statistics for Index files
    print()
    print('------------------------------------------------------------------------')
    print('%15s | %10s | %12s | %12s' % ('Item', 'Count', 'Min_val', 'Max_val'))
    #print('%15s | %10d | %12s | %12s' % ('PATENT', cnt_PATENT_IDX, min_PATENT_IDX, max_PATENT_IDX))
    print('%15s | %10d | %12s | %12s' % ('PUB_COUNTRY', cnt_PUB_COUNTRY_IDX, min_PUB_COUNTRY_IDX, max_PUB_COUNTRY_IDX))
    print('%15s | %10d | %12s | %12s' % ('PUB_DATE', cnt_PUB_DATE_IDX , min_PUB_DATE_IDX, max_PUB_DATE_IDX))
    #print('%15s | %10d | %12s | %12s' % ('APP_DOCNO', cnt_APP_DOCNUMBER_IDX, min_APP_DOCNUMBER_IDX, max_APP_DOCNUMBER_IDX))
    print('%15s | %10d | %12s | %12s' % ('APP_DATE',  cnt_APP_DATE_IDX,      min_APP_DATE_IDX,      max_APP_DATE_IDX))
    print('%15s | %10d | %12s | %12s' % ('INV_TITLE', cnt_INV_TITLE_IDX,     min_INV_TITLE_IDX,     max_INV_TITLE_IDX))
    print('%15s | %10d | %12s | %12s' % ('APPLICANTS', cnt_APPLICANTS_IDX,    min_APPLICANTS_IDX,    max_APPLICANTS_IDX))
    print('%15s | %10d | %12s | %12s' % ('CITING', cnt_CITING_IDX,        min_CITING_IDX,        max_CITING_IDX))
    print('------------------------------------------------------------------------')
    print()


    # Parse the program arguments
    for arg in sys.argv:
        if arg.startswith('--Doc_File='):
            CodePathFile = arg[11:]

        elif arg.startswith('--DocNo='):
            Tgt_Doc_No = arg[8:]

        elif arg.startswith("--AND="):
            AND_KEYWORDS = arg[6:]

        elif arg.startswith("--NOT="):
            NOT_KEYWORDS = arg[6:]

        elif arg.startswith("--Pub_From="):
            Pub_FROM = arg[11:]

        elif arg.startswith("--Pub_To="):
            Pub_TO = arg[9:]

        elif arg.startswith("--App_From="):
            App_FROM = arg[11:]

        elif arg.startswith("--App_To="):
            App_TO = arg[9:]

        elif arg.startswith("--Applicant="):
            Applicant = arg[12:]

        elif arg.startswith("USPTO_Search"):
            if len(sys.argv) == 1:
                print(' - [Error] Please input arguments for patent search!')
                print(' - Program Terminated.')
                sys.exit(-1)
            else:
                pass

        else:
            print('[WARN] Unknown arguments : ', arg)


    # Validate the arguments
    FLAG = False
    DocList_file   = DocNoToList(CodePathFile, 'file')
    DocList_param  = DocNoToList(Tgt_Doc_No, 'param')
    AND_KEYWORDS, FLAG = Valid_Keywords(AND_KEYWORDS)
    NOT_KEYWORDS, FLAG = Valid_Keywords(NOT_KEYWORDS)
    Pub_FROM, FLAG = Valid_Date(Pub_FROM, 'From')
    Pub_TO, FLAG   = Valid_Date(Pub_TO, 'To')
    App_FROM, FLAG = Valid_Date(App_FROM, 'From')
    App_TO, FLAG   = Valid_Date(App_TO, 'To')

    # Print the arguments
    print()
    print('--- Input Parameters ---')
    print('Doc-code file :', CodePathFile, len(DocList_file), 'patent codes')
    print('Doc-code No   :', len(DocList_param), 'patent codes.')
    print('AND keywords  :', AND_KEYWORDS, len(AND_KEYWORDS), 'keywords.')
    print('NOT keywords  :', NOT_KEYWORDS, len(NOT_KEYWORDS), 'keywords.')
    print('Pub. From     :', Pub_FROM)
    print('Pub. TO       :', Pub_TO)
    print('App. From     :', App_FROM)
    print('App. TO       :', App_TO)
    print('Applicant     :', Applicant)
    print('------------------------')
    print()

    if FLAG is False:
        sys.exit('Program unsuccessfully terminated.')

    # Searching process start!
    if CodePathFile != '' and DocList_file != []:
        print(' - Searching for patents in the file.')
    elif DocList_param != []:
        print(' - Searching for the patent')
    else:
        # AND Keywords
        ANDPatentSet = set()
        SetList = []
        for item in AND_KEYWORDS:
            tempSet = set()
            for key in INV_TITLE_IDX:
                if item.lower() in key.lower():
                    tempSet.update(INV_TITLE_IDX[key])
            SetList.append(tempSet)
            #print(item, len(tempSet))
        ANDPatentSet = set.intersection(*SetList)
        #print(len(ANDPatentSet))

        # OR Keywords
        ORPatentSet = set()
        for item in OR_KEYWORDS:
            for key in INV_TITLE_IDX:
                if item.lower() in key.lower():
                    ANDPatentSet.update(INV_TITLE_IDX[key])

        # NOT Keywords
        NOTPatentSet = set()
        for item in NOT_KEYWORDS:
            for key in INV_TITLE_IDX:
                if item.lower() in key.lower():
                    NOTPatentSet.update(INV_TITLE_IDX[key])

        # Pub_From_To
        PubDateSet = set()
        for key in PUB_DATE_IDX:
            if int(key) >= int(Pub_FROM) and int(key) <= int(Pub_TO):
                PubDateSet.update(PUB_DATE_IDX[key])

        # App_From_To
        AppDateSet = set()
        for key in APP_DATE_IDX:
            if int(key) >= int(App_FROM) and int(key) <= int(App_TO):
                AppDateSet.update(APP_DATE_IDX[key])

        # Applicant
        ApplicantPatentSet = set()
        for key in APPLICANTS_IDX:
            if Applicant.lower() in key.lower():
                ApplicantPatentSet.update(APPLICANTS_IDX[key])
    

    del PUB_COUNTRY_IDX, PUB_DATE_IDX, APP_DOCNUMBER_IDX, APP_COUNTRY_IDX, APP_DATE_IDX, INV_TITLE_IDX, APPLICANTS_IDX

    # Open database
    try:
        print(' - Loading Index database : ', os.path.join(LOCAL_BASE, 'Patent_DB.bin'))
        with open(os.path.join(LOCAL_BASE, 'Patent_DB.bin'), 'rb') as f:
            PATENT_IDX = pickle.load(f)

    except:
        print(' - ERROR on loading USPTO database. ')
        print(' - Please check the database file : ', os.path.join(LOCAL_BASE, 'Patent_DB.bin'))
        sys.exit(-1)

    # Get the descriptive statistics for Index files
    cnt_PATENT_IDX,        min_PATENT_IDX,        max_PATENT_IDX        = len(PATENT_IDX), min(PATENT_IDX), max(PATENT_IDX)
    print()
    print('------------------------------------------------------------------------')
    print('%15s | %10s | %12s | %12s' % ('Item', 'Count', 'Min_val', 'Max_val'))
    print('%15s | %10d | %12s | %12s' % ('PATENT', cnt_PATENT_IDX, min_PATENT_IDX, max_PATENT_IDX))
    print('------------------------------------------------------------------------')

    # Open result file
    TimeString = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + "_" + str(now.tm_hour) + str(now.tm_min) + str(
        now.tm_sec)
    print(' - Write output file to : ', os.path.join(DEFAULT_PATH, TimeString+'_Output.txt'))
    fw = open(os.path.join(DEFAULT_PATH, TimeString+'_Output.txt'), 'w')
    fw.write('\t'.join(['PubDocNo',
                        'PubCountry',
                        'PubKind',
                        'PubDate',
                        'InvTitle',
                        'Applicants',
                        'Assignees',
                        'Classi_NatList',
                        'Classi_IPCList',
                        'FieldOfClassiSearch',
                        'CitationList',
                        'OtherRefList'
                        ]))
    fw.write('\n')

    # Case 1 : Doc list in the file
    if CodePathFile != '' and DocList_file != []:
        found_cnt = 0
        print(' - Case 1 : Search patents from doc-numbers in the file')
        for item in DocList_file:
            if item in PATENT_IDX:
                PatentToFile(PATENT_IDX[item], CITING_IDX, fw)
                found_cnt += 1
            else:
                print('  >  Cannot find the patent : ', item)
        print(' \n- Patent searched :', len(DocList_file), '/ Found patents :', found_cnt)
    # Case 2 : Doc number from parameter
    elif DocList_param != []:
        found_cnt = 0
        print(' - Case 2 : Search patents from doc-numbers in the parameter')
        for item in DocList_param:
            if item in PATENT_IDX:
                PatentToFile(PATENT_IDX[item], CITING_IDX, fw)
                found_cnt += 1
            else:
                print('  >  Cannot find the patent : ', item)
        print(' \n- Patent searched :', len(DocList_param), '/ Found patents :', found_cnt)
    # Case 3 : Filtering by parameters
    else:
        print(' - Case 3 : Search patents from parameters')
        FilteredSet = set()
        # AND Keywords
        if len(AND_KEYWORDS) > 0:
            print(' [AND] Found ', len(ANDPatentSet), 'patents.')
            if len(ANDPatentSet) > 0:
                FilteredSet = ANDPatentSet

        # Pub_From_To
        if len(PubDateSet) > 0:
            if len(FilteredSet) > 0:
                FilteredSet = FilteredSet.intersection(PubDateSet)
            else:
                FilteredSet = PubDateSet

        # App_From_To
        if len(AppDateSet) > 0:
            if len(FilteredSet) > 0:
                FilteredSet = FilteredSet.intersection(AppDateSet)
            else:
                FilteredSet = AppDateSet

        # Applicant
        if len(ApplicantPatentSet) > 0:
            if len(FilteredSet) > 0:
                FilteredSet = FilteredSet.intersection(ApplicantPatentSet)
            else:
                FilteredSet = ApplicantPatentSet

        # NOT Keywords
        if len(NOT_KEYWORDS) > 0:
            FilteredSet = FilteredSet.difference(NOT_KEYWORDS)

        # Print the patents
        for item in FilteredSet:
            if item in PATENT_IDX:
                PatentToFile(PATENT_IDX[item], CITING_IDX, fw)
            else:
                print(' - Cannot find the patent : ', item)

    fw.close()

# --------------------------------------------
m, s = divmod(time.time() - start_time, 60)
h, m = divmod(m, 60)

print("\nTime elapsed : %d:%02d:%02d" % (h, m, s))

print('\nProgram successfully terminated.')
