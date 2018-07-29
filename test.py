import io, os, glob, time, math
import xml.etree.ElementTree as ET
import itertools as IT
import re
import pickle
from USPTO_XML_Parser import xml_parsing
import USPTO
from nltk.corpus import stopwords
import nltk

#nltk.download()


#------------------------------------------------------------------------------
# Configurations
LOCAL_BASE  = '/Users/dninb/PycharmProjects/USPTO_Full_DB/Patents' # Local path for extracting zip files
#------------------------------------------------------------------------------
#
# # Open database
# with open(os.path.join(LOCAL_BASE, 'Database.bin'), 'rb') as f:
#     PATENT_IDX = pickle.load(f)
#     PUB_COUNTRY_IDX = pickle.load(f)
#     PUB_DATE_IDX = pickle.load(f)
#     APP_DOCNUMBER_IDX = pickle.load(f)
#     APP_COUNTRY_IDX = pickle.load(f)
#     APP_DATE_IDX = pickle.load(f)
#     INV_TITLE_IDX = pickle.load(f)
#     APPLICANTS_IDX = pickle.load(f)
#     CITING_IDX = pickle.load(f)
#
# print(PATENT_IDX)
# print(PUB_COUNTRY_IDX)
# print(PUB_DATE_IDX)
# print(APPLICANTS_IDX)
# print(CITING_IDX)
# print(INV_TITLE_IDX)


print(','.join([]))
dd = "['a','b']"
cc = ''

gg = eval(cc)

gg.append('c')
print(gg)