"""
    File : Class of data type for USPatent, Applicants and Assignees in patents 
 Authors : Minhoe Hur
  +Email : mhoe.hur@gmail.com
          
 History :
  2012/11/04 Minhoe Hur - Created
  2018/01/28 Minhoe Hur - Modified

   Notes :
  This program is runs under Python 3.x Runtime Environments.
"""
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict


class USPatent():
    # pub_country_index = defaultdict(list)
    # pub_date_index    = defaultdict(list)
    # app_country_index = defaultdict(list)
    # app_date_index    = defaultdict(list)

    def __init__(self):
        self.pub_docnumber = '' # (1)
        self.pub_country = ''  # To be searched (2)
        self.pub_kind = ''     # (3)
        self.pub_date = ''      # To be searched (4)

        self.app_docnumber = '' # To be searched (5)
        self.app_country = ''   # To be searched (6)
        self.app_date = ''      # To be searched (7)
        
        self.invention_title = '' # To be searched (8)

        self.Applicants_list = [] # To be searched (9)

        self.Assignees_list = [] # (10)

        self.classification_national_list = [] # (11)

        self.classification_ipc_list = [] # (12)

        self.field_of_classification_search_list = [] # (13)

        self.number_claims = '' # (14)
        
        self.citation_list = [] # (15)
        
        self.other_reference_list = [] # (16)
            
        self.abstract = '' # (17)
        self.val_check = ['0'] * 17

    def valid_patent(self):
        if self.pub_docnumber != '':
            self.val_check[0] = '1'
        if self.pub_country != '':
            self.val_check[1] = '1'
        if self.pub_kind != '':
            self.val_check[2] = '1'
        if self.pub_date != '':
            self.val_check[3] = '1'
        if self.app_docnumber != '':
            self.val_check[4] = '1'
        if self.app_country != '':
            self.val_check[5] = '1'
        if self.app_date != '':
            self.val_check[6] = '1'
        if self.invention_title != '':
            self.val_check[7] = '1'
        if len(self.Applicants_list) != 0:
            self.val_check[8] = '1'
        if len(self.Assignees_list) != 0:
            self.val_check[9] = '1'
        if len(self.classification_national_list) != 0:
            self.val_check[10] = '1'
        if len(self.classification_ipc_list) != 0:
            self.val_check[11] = '1'
        if len(self.field_of_classification_search_list) != 0:
            self.val_check[12] = '1'
        if self.number_claims != '':
            self.val_check[13] = '1'
        if len(self.citation_list) != 0:
            self.val_check[14] = '1'
        if len(self.other_reference_list) != 0:
            self.val_check[15] = '1'
        if self.abstract != '':
            self.val_check[16] = '1'

        return ''.join(self.val_check)

    #
    # @property
    # def pub_country(self):
    #     return self._pub_country
    #
    # @pub_country.setter
    # def pub_country(self, input):
    #     self._pub_country = input
    #     USPatent.pub_country_index[input].append(self)
    #
    # @classmethod
    # def find_by_pub_country(cls, input):
    #     return USPatent.pub_country_index[input]
    #
    # @property
    # def pub_date(self):
    #     return self._pub_date
    #
    # @pub_date.setter
    # def pub_date(self, input):
    #     self._pub_date = input
    #     USPatent.pub_date_index[input].append(self)
    #
    # @classmethod
    # def find_by_pub_date(cls, input):
    #     return USPatent.pub_date_index[input]
    #
    # @property
    # def app_country(self):
    #     return self._app_country
    #
    # @app_country.setter
    # def app_country(self, input):
    #     self._app_country = input
    #     USPatent.app_country_index[input].append(self)
    #
    # @classmethod
    # def find_by_app_country(cls, input):
    #     return USPatent.app_country_index[input]
    #
    # @property
    # def app_date(self):
    #     return self._app_date
    #
    # @pub_date.setter
    # def app_date(self, input):
    #     self._app_date = input
    #     USPatent.app_date_index[input].append(self)
    #
    # @classmethod
    # def find_by_app_date(cls, input):
    #     return USPatent.app_date_index[input]

    def __repr__(self): # When the instance is executed
        return self.pub_docnumber
    def __str__(self): # When the instance is printed
        return self.pub_docnumber

            
class Applicant():
    def __init__(self):
        self.lastname = ''
        self.firstname = ''
        self.orgname = ''
        self.city = ''
        self.state = ''
        self.residence_country = ''

    def __repr__(self):
        if self.lastname == '':
            if self.firstname == '':
                return(self.orgname)
            else:
                return(self.firstname + '_' + self.orgname)
        else:
            return(self.lastname + '_' + self.firstname + '@' + self.orgname)

    def __str__(self):
        if self.lastname == '':
            if self.firstname == '':
                return(self.orgname)
            else:
                return self.firstname + '_' + self.orgname
        else:
            return self.lastname + '_' + self.firstname + '@' + self.orgname


class Assignee():
    def __init__(self):
        self.lastname = ''
        self.firstname = ''
        self.orgname = ''
        self.city = ''
        self.state = ''
        self.residence_country = ''

    def __repr__(self):
        if self.lastname == '':
            if self.firstname == '':
                return(self.orgname)
            else:
                return(self.firstname + '_' + self.orgname)
        else:
            return(self.lastname + '_' + self.firstname + '@' + self.orgname)

    def __str__(self):
        if self.lastname == '':
            if self.firstname == '':
                return(self.orgname)
            else:
                return(self.firstname + '_' + self.orgname)
        else:
            return(self.lastname + '_' + self.firstname + '@' + self.orgname)


class Citation():
    def __init__(self):
        self.country = ''
        self.docnumber = ''
        self.kind = ''
        self.name = ''
        self.date = ''

    def __repr__(self): # When the instance is executed
        return self.docnumber

    def __str__(self): # When the instance is printed
        return self.docnumber


class IPCR():
    def __init__(self):
        self.date = ''
        self.classification_level = ''
        self.section = ''
        self.I_class = ''
        self.I_subclass = ''
        self.main_group = ''
        self.subgroup = ''
        self.symbol_position = ''
        self.classification_value = ''
        self.action_date = ''
        self.generating_office = ''
        self.classification_status = ''
        self.classification_data_source = ''

    def __repr__(self): # When the instance is executed
        return self.I_class+'_'+self.main_group+'_'+self.classification_value

    def __str__(self): # When the instance is printed
        return self.I_class+'_'+self.main_group+'_'+self.classification_value


class Field_of_Class_Search():
    def __init__(self):
        self.country = ''
        self.main_classification = ''
        self.additional_info = ''

    def __repr__(self):
        return (self.country + '_' + self.main_classification + '_' + self.additional_info)

    def __str__(self):
        return(self.country + '_' + self.main_classification + '_' + self.additional_info)