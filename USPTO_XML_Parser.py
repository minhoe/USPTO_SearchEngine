"""
    File : Parsing modules for US patents
 Authors : Minhoe Hur
  +Email : mhoe.hur@gmail.com

 History :
  2013/03/05 Minhoe Hur - Created
  2018/01/28 Minhoe Hur - Modified

   Notes :
  This program is runs under Python 3.x Runtime Environments.
"""
# -*- coding: utf-8 -*-


import USPTO

def xml_value_to_string(elem, elem_name, file_name, pub_doc_no = '' ):
    output = ''
    try:
        output = elem.text.strip()
    except AttributeError as err:
        print(' [Warn] Cannot find "', elem_name, '"','  > pub_doc_no:', pub_doc_no, '> file:', file_name)
        output = ''
    return output

def xml_parsing(dtd_version, item, file, USPTN):
    #us-patent-grant-v40-2004-12-02.dtd
    if dtd_version == 'v4.0 2004-12-02' or dtd_version == 'v40 2004-12-02': #--------------------------------------------------------------------
        # pub_docnumber -- Done!
        pub_docnumber       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find(
            'doc-number')
        USPTN.pub_docnumber = xml_value_to_string(pub_docnumber, 'doc-number', file)

        # pub_country -- Done!
        pub_country       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('country')
        USPTN.pub_country = xml_value_to_string(pub_country, 'country', file, pub_docnumber.text)

        # pub_kind -- Done!
        pub_kind       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('kind')
        USPTN.pub_kind = xml_value_to_string(pub_kind, 'kind', file, pub_docnumber.text)

        # pub_date -- Done!
        pub_date       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('date')
        USPTN.pub_date = xml_value_to_string(pub_date, 'date', file, pub_docnumber.text)

        # app_docnumber -- Done!
        app_docnumber       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find(
            'doc-number')
        USPTN.app_docnumber = xml_value_to_string(app_docnumber, 'country', file, pub_docnumber.text)

        # app_country -- Done!
        app_country       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('country')
        USPTN.app_country = xml_value_to_string(app_country, 'country', file, pub_docnumber.text)

        # app_date -- Done!
        app_date       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('date')
        USPTN.app_date = xml_value_to_string(app_date, 'country', file, pub_docnumber.text)

        # invention_title -- Done!
        invention_title       = item.find('us-bibliographic-data-grant').find('invention-title')
        USPTN.invention_title = xml_value_to_string(invention_title, 'invention-title', file, pub_docnumber.text)

        # Applicants_list = [] -- Done!
        applicants = item.find('us-bibliographic-data-grant').find('parties').find('applicants')
        if applicants is not None:
            for applicant in applicants:
                Appnt = USPTO.Applicant()
                # Addressbook
                add_book = applicant.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Appnt.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Appnt.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Appnt.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                if zz.tag == 'city':
                                    Appnt.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Appnt.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                # Residence Country
                if applicant.find('residence') is not None:
                    for resid in applicant.find('residence').getchildren():
                        if resid.tag == 'country':
                            Appnt.residence_country = resid.text

                USPTN.Applicants_list.append(Appnt)

        # Assignees_list = [] -- Done
        assignees = item.find('us-bibliographic-data-grant').find('assignees')
        if assignees is not None:
            for assignee in assignees:
                Assgn = USPTO.Assignee()
                # Addressbook
                add_book = assignee.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Assgn.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Assgn.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Assgn.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                #print(zz.tag)
                                if zz.tag == 'city':
                                    Assgn.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Assgn.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                elif zz.tag == 'country':
                                    Assgn.residence_country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                USPTN.Assignees_list.append(Assgn)

        # classification_national_list = [] -- Done
        classification_national = item.find('us-bibliographic-data-grant').find('classification-national')
        if classification_national is not None:
            #print('here>?>>>')
            for cn in classification_national:
                if cn.tag == 'main-classification':
                    USPTN.classification_national_list.append(xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                elif cn.tag == 'further-classification':
                    USPTN.classification_national_list.append(
                        xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                else:
                    #print(' Cannot find!')
                    pass

        # classification_ipc_list = [] -- Done -- Cannot find ipcr element @ 051213.xml
        classification_ipcr = item.find('us-bibliographic-data-grant').find('classifications-ipcr')
        if classification_ipcr is not None:
            for ci in classification_ipcr:
                ipcr = USPTO.IPCR()
                for ci2 in ci.getchildren():
                    if ci2.tag == 'ipc-version-indicator':
                        ipcr.date = ci2.find('date')
                    elif ci2.tag == 'classification-level':
                        ipcr.classification_level = xml_value_to_string(ci2, 'classification-level', file, pub_docnumber.text)
                    elif ci2.tag == 'section':
                        ipcr.section = xml_value_to_string(ci2, 'section', file, pub_docnumber.text)
                    elif ci2.tag == 'class':
                        ipcr.I_class = xml_value_to_string(ci2, 'class', file, pub_docnumber.text)
                    elif ci2.tag == 'subclass':
                        ipcr.I_subclass = xml_value_to_string(ci2, 'subclass', file, pub_docnumber.text)
                    elif ci2.tag == 'main-group':
                        ipcr.main_group = xml_value_to_string(ci2, 'main-group', file, pub_docnumber.text)
                    elif ci2.tag == 'subgroup':
                        ipcr.subgroup = xml_value_to_string(ci2, 'subgroup', file, pub_docnumber.text)
                    elif ci2.tag == 'symbol-position':
                        ipcr.symbol_position = xml_value_to_string(ci2, 'symbol-position', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-value':
                        ipcr.classification_value = xml_value_to_string(ci2, 'classification-value', file, pub_docnumber.text)
                    elif ci2.tag == 'action-date':
                        ipcr.action_date = xml_value_to_string(ci2.find('date'), 'action-date', file, pub_docnumber.text)
                    elif ci2.tag == 'generating-office':
                        ipcr.generating_office = xml_value_to_string(ci2.find('country'), 'generating-office', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-status':
                        ipcr.classification_status = xml_value_to_string(ci2, 'classification-status', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-data-source':
                        ipcr.classification_data_source = xml_value_to_string(ci2, 'classification-data-source', file, pub_docnumber.text)
                    else:
                        pass

                USPTN.classification_ipc_list.append(ipcr)

        # fieldsearch_list = []  us-field-of-classification-search -- Done
        us_foc_search = item.find('us-bibliographic-data-grant').find('field-of-search')
        if us_foc_search is not None and us_foc_search.find('classification-national') is not None:
            for zz in us_foc_search.find('classification-national'):
                foc = USPTO.Field_of_Class_Search()

                if zz.tag == 'country':
                    foc.country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                elif zz.tag == 'main-classification':
                    foc.main_classification = xml_value_to_string(zz, 'main-classification', file, pub_docnumber.text)
                elif zz.tag == 'additional-info':
                    foc.additional_info = xml_value_to_string(zz, 'additional-info', file, pub_docnumber.text)
                else:
                    pass

                USPTN.field_of_classification_search_list.append(foc)

        # number_claims -- Done!
        noc = item.find('us-bibliographic-data-grant').find('number-of-claims')
        USPTN.number_claims = xml_value_to_string(noc, 'number-of-claims', file, pub_docnumber.text)

        # citation_list = [] -- Done!
        citations = item.find('us-bibliographic-data-grant').find('references-cited')
        if citations is not None:
            for cc in citations:
                #print(cc.getchildren())
                if cc.find('patcit') is not None:
                    num = cc.find('patcit').get('num')
                    cc_doc_num = cc.find('patcit').find('document-id').find('doc-number')
                    USPTN.citation_list.append(xml_value_to_string(cc_doc_num, 'doc-number', file, pub_docnumber.text))

                #print(cc, cc.getchildren())
                elif cc.find('nplcit') is not None:
                    #print(cc.find('nplcit').getchildren())
                    cc_ref = cc.find('nplcit').find('othercit')
                    USPTN.other_reference_list.append(xml_value_to_string(cc_ref, 'othercit', file, pub_docnumber.text))
                else:
                    pass

        # citing_list = []

        # abstract -- Done! -- 중간 태그가 삽입되는 경우(<i>.. </i>) 짤리는 문제가 있음!
        abs = item.find('abstract')
        if abs is not None:
            USPTN.abstract = abs.find('p').text


    # us-patent-grant-v41-2005-08-25.dtd -- OK
    elif dtd_version == 'v4.1 2005-08-25': #--------------------------------------------------------------------
        # pub_docnumber -- Done!
        pub_docnumber       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find(
            'doc-number')
        USPTN.pub_docnumber = xml_value_to_string(pub_docnumber, 'doc-number', file)

        # pub_country -- Done!
        pub_country       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('country')
        USPTN.pub_country = xml_value_to_string(pub_country, 'country', file, pub_docnumber.text)

        # pub_kind -- Done!
        pub_kind       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('kind')
        USPTN.pub_kind = xml_value_to_string(pub_kind, 'kind', file, pub_docnumber.text)

        # pub_date -- Done!
        pub_date       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('date')
        USPTN.pub_date = xml_value_to_string(pub_date, 'date', file, pub_docnumber.text)

        # app_docnumber -- Done!
        app_docnumber       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find(
            'doc-number')
        USPTN.app_docnumber = xml_value_to_string(app_docnumber, 'country', file, pub_docnumber.text)

        # app_country -- Done!
        app_country       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('country')
        USPTN.app_country = xml_value_to_string(app_country, 'country', file, pub_docnumber.text)

        # app_date -- Done!
        app_date       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('date')
        USPTN.app_date = xml_value_to_string(app_date, 'country', file, pub_docnumber.text)

        # invention_title -- Done!
        invention_title       = item.find('us-bibliographic-data-grant').find('invention-title')
        USPTN.invention_title = xml_value_to_string(invention_title, 'invention-title', file, pub_docnumber.text)

        # Applicants_list = [] -- Done!
        applicants = item.find('us-bibliographic-data-grant').find('parties').find('applicants')
        if applicants is not None:
            for applicant in applicants:
                Appnt = USPTO.Applicant()
                # Addressbook
                add_book = applicant.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Appnt.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Appnt.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Appnt.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                if zz.tag == 'city':
                                    Appnt.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Appnt.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                # Residence Country
                if applicant.find('residence') is not None:
                    for resid in applicant.find('residence').getchildren():
                        if resid.tag == 'country':
                            Appnt.residence_country = resid.text

                USPTN.Applicants_list.append(Appnt)

        # Assignees_list = [] -- Done
        assignees = item.find('us-bibliographic-data-grant').find('assignees')
        if assignees is not None:
            for assignee in assignees:
                Assgn = USPTO.Assignee()
                # Addressbook
                add_book = assignee.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Assgn.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Assgn.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Assgn.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                #print(zz.tag)
                                if zz.tag == 'city':
                                    Assgn.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Assgn.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                elif zz.tag == 'country':
                                    Assgn.residence_country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                USPTN.Assignees_list.append(Assgn)

        # classification_national_list = [] -- Done
        classification_national = item.find('us-bibliographic-data-grant').find('classification-national')
        if classification_national is not None:
            #print('here>?>>>')
            for cn in classification_national:
                if cn.tag == 'main-classification':
                    USPTN.classification_national_list.append(xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                elif cn.tag == 'further-classification':
                    USPTN.classification_national_list.append(
                        xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                else:
                    #print(' Cannot find!')
                    pass

        # classification_ipc_list = [] -- Done -- Cannot find ipcr element @ 051213.xml
        classification_ipcr = item.find('us-bibliographic-data-grant').find('classifications-ipcr')
        if classification_ipcr is not None:
            for ci in classification_ipcr:
                ipcr = USPTO.IPCR()
                for ci2 in ci.getchildren():
                    if ci2.tag == 'ipc-version-indicator':
                        ipcr.date = ci2.find('date')
                    elif ci2.tag == 'classification-level':
                        ipcr.classification_level = xml_value_to_string(ci2, 'classification-level', file, pub_docnumber.text)
                    elif ci2.tag == 'section':
                        ipcr.section = xml_value_to_string(ci2, 'section', file, pub_docnumber.text)
                    elif ci2.tag == 'class':
                        ipcr.I_class = xml_value_to_string(ci2, 'class', file, pub_docnumber.text)
                    elif ci2.tag == 'subclass':
                        ipcr.I_subclass = xml_value_to_string(ci2, 'subclass', file, pub_docnumber.text)
                    elif ci2.tag == 'main-group':
                        ipcr.main_group = xml_value_to_string(ci2, 'main-group', file, pub_docnumber.text)
                    elif ci2.tag == 'subgroup':
                        ipcr.subgroup = xml_value_to_string(ci2, 'subgroup', file, pub_docnumber.text)
                    elif ci2.tag == 'symbol-position':
                        ipcr.symbol_position = xml_value_to_string(ci2, 'symbol-position', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-value':
                        ipcr.classification_value = xml_value_to_string(ci2, 'classification-value', file, pub_docnumber.text)
                    elif ci2.tag == 'action-date':
                        ipcr.action_date = xml_value_to_string(ci2.find('date'), 'action-date', file, pub_docnumber.text)
                    elif ci2.tag == 'generating-office':
                        ipcr.generating_office = xml_value_to_string(ci2.find('country'), 'generating-office', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-status':
                        ipcr.classification_status = xml_value_to_string(ci2, 'classification-status', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-data-source':
                        ipcr.classification_data_source = xml_value_to_string(ci2, 'classification-data-source', file, pub_docnumber.text)
                    else:
                        pass

                USPTN.classification_ipc_list.append(ipcr)

        # fieldsearch_list = []  us-field-of-classification-search -- Done
        us_foc_search = item.find('us-bibliographic-data-grant').find('us-field-of-classification-search')
        if us_foc_search is not None and us_foc_search.find('classification-national') is not None:
            for zz in us_foc_search.find('classification-national'):
                foc = USPTO.Field_of_Class_Search()

                if zz.tag == 'country':
                    foc.country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                elif zz.tag == 'main-classification':
                    foc.main_classification = xml_value_to_string(zz, 'main-classification', file, pub_docnumber.text)
                elif zz.tag == 'additional-info':
                    foc.additional_info = xml_value_to_string(zz, 'additional-info', file, pub_docnumber.text)
                else:
                    pass

                USPTN.field_of_classification_search_list.append(foc)

        # number_claims -- Done!
        noc = item.find('us-bibliographic-data-grant').find('number-of-claims')
        USPTN.number_claims = xml_value_to_string(noc, 'number-of-claims', file, pub_docnumber.text)

        # citation_list = [] -- Done!
        citations = item.find('us-bibliographic-data-grant').find('references-cited')
        if citations is not None:
            for cc in citations:
                #print(cc.getchildren())
                if cc.find('patcit') is not None:
                    num = cc.find('patcit').get('num')
                    cc_doc_num = cc.find('patcit').find('document-id').find('doc-number')
                    USPTN.citation_list.append(xml_value_to_string(cc_doc_num, 'doc-number', file, pub_docnumber.text))

                #print(cc, cc.getchildren())
                elif cc.find('nplcit') is not None:
                    #print(cc.find('nplcit').getchildren())
                    cc_ref = cc.find('nplcit').find('othercit')
                    USPTN.other_reference_list.append(xml_value_to_string(cc_ref, 'othercit', file, pub_docnumber.text))
                else:
                    pass

        # citing_list = []

        # abstract -- Done! -- 중간 태그가 삽입되는 경우(<i>.. </i>) 짤리는 문제가 있음!
        abs = item.find('abstract')
        if abs is not None:
            USPTN.abstract = abs.find('p').text


    # us-patent-grant-v42-2006-08-23.dtd -- OK
    elif dtd_version == 'v4.2 2006-08-23': #--------------------------------------------------------------------
        # pub_docnumber -- Done!
        pub_docnumber       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find(
            'doc-number')
        USPTN.pub_docnumber = xml_value_to_string(pub_docnumber, 'doc-number', file)

        # pub_country -- Done!
        pub_country       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('country')
        USPTN.pub_country = xml_value_to_string(pub_country, 'country', file, pub_docnumber.text)

        # pub_kind -- Done!
        pub_kind       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('kind')
        USPTN.pub_kind = xml_value_to_string(pub_kind, 'kind', file, pub_docnumber.text)

        # pub_date -- Done!
        pub_date       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('date')
        USPTN.pub_date = xml_value_to_string(pub_date, 'date', file, pub_docnumber.text)

        # app_docnumber -- Done!
        app_docnumber       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find(
            'doc-number')
        USPTN.app_docnumber = xml_value_to_string(app_docnumber, 'country', file, pub_docnumber.text)

        # app_country -- Done!
        app_country       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('country')
        USPTN.app_country = xml_value_to_string(app_country, 'country', file, pub_docnumber.text)

        # app_date -- Done!
        app_date       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('date')
        USPTN.app_date = xml_value_to_string(app_date, 'country', file, pub_docnumber.text)

        # invention_title -- Done!
        invention_title       = item.find('us-bibliographic-data-grant').find('invention-title')
        USPTN.invention_title = xml_value_to_string(invention_title, 'invention-title', file, pub_docnumber.text)

        # Applicants_list = [] -- Done!
        applicants = item.find('us-bibliographic-data-grant').find('parties').find('applicants')
        if applicants is not None:
            for applicant in applicants:
                Appnt = USPTO.Applicant()
                # Addressbook
                add_book = applicant.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Appnt.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Appnt.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Appnt.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                if zz.tag == 'city':
                                    Appnt.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Appnt.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                # Residence Country
                if applicant.find('residence') is not None:
                    for resid in applicant.find('residence').getchildren():
                        if resid.tag == 'country':
                            Appnt.residence_country = resid.text

                USPTN.Applicants_list.append(Appnt)

        # Assignees_list = [] -- Done
        assignees = item.find('us-bibliographic-data-grant').find('assignees')
        if assignees is not None:
            for assignee in assignees:
                Assgn = USPTO.Assignee()
                # Addressbook
                add_book = assignee.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Assgn.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Assgn.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Assgn.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                #print(zz.tag)
                                if zz.tag == 'city':
                                    Assgn.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Assgn.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                elif zz.tag == 'country':
                                    Assgn.residence_country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                USPTN.Assignees_list.append(Assgn)

        # classification_national_list = [] -- Done
        classification_national = item.find('us-bibliographic-data-grant').find('classification-national')
        if classification_national is not None:
            #print('here>?>>>')
            for cn in classification_national:
                if cn.tag == 'main-classification':
                    USPTN.classification_national_list.append(xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                elif cn.tag == 'further-classification':
                    USPTN.classification_national_list.append(
                        xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                else:
                    #print(' Cannot find!')
                    pass

        # classification_ipc_list = [] -- Done -- Cannot find ipcr element @ 081104.xml
        classification_ipcr = item.find('us-bibliographic-data-grant').find('classifications-ipcr')
        if classification_ipcr is not None:
            for ci in classification_ipcr:
                ipcr = USPTO.IPCR()
                for ci2 in ci.getchildren():
                    if ci2.tag == 'ipc-version-indicator':
                        ipcr.date = ci2.find('date')
                    elif ci2.tag == 'classification-level':
                        ipcr.classification_level = xml_value_to_string(ci2, 'classification-level', file, pub_docnumber.text)
                    elif ci2.tag == 'section':
                        ipcr.section = xml_value_to_string(ci2, 'section', file, pub_docnumber.text)
                    elif ci2.tag == 'class':
                        ipcr.I_class = xml_value_to_string(ci2, 'class', file, pub_docnumber.text)
                    elif ci2.tag == 'subclass':
                        ipcr.I_subclass = xml_value_to_string(ci2, 'subclass', file, pub_docnumber.text)
                    elif ci2.tag == 'main-group':
                        ipcr.main_group = xml_value_to_string(ci2, 'main-group', file, pub_docnumber.text)
                    elif ci2.tag == 'subgroup':
                        ipcr.subgroup = xml_value_to_string(ci2, 'subgroup', file, pub_docnumber.text)
                    elif ci2.tag == 'symbol-position':
                        ipcr.symbol_position = xml_value_to_string(ci2, 'symbol-position', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-value':
                        ipcr.classification_value = xml_value_to_string(ci2, 'classification-value', file, pub_docnumber.text)
                    elif ci2.tag == 'action-date':
                        ipcr.action_date = xml_value_to_string(ci2.find('date'), 'action-date', file, pub_docnumber.text)
                    elif ci2.tag == 'generating-office':
                        ipcr.generating_office = xml_value_to_string(ci2.find('country'), 'generating-office', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-status':
                        ipcr.classification_status = xml_value_to_string(ci2, 'classification-status', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-data-source':
                        ipcr.classification_data_source = xml_value_to_string(ci2, 'classification-data-source', file, pub_docnumber.text)
                    else:
                        pass

                USPTN.classification_ipc_list.append(ipcr)

        # fieldsearch_list = []  us-field-of-classification-search -- Done
        us_foc_search = item.find('us-bibliographic-data-grant').find('us-field-of-classification-search')
        if us_foc_search is not None and us_foc_search.find('classification-national') is not None:
            for zz in us_foc_search.find('classification-national'):
                foc = USPTO.Field_of_Class_Search()

                if zz.tag == 'country':
                    foc.country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                elif zz.tag == 'main-classification':
                    foc.main_classification = xml_value_to_string(zz, 'main-classification', file, pub_docnumber.text)
                elif zz.tag == 'additional-info':
                    foc.additional_info = xml_value_to_string(zz, 'additional-info', file, pub_docnumber.text)
                else:
                    pass

                USPTN.field_of_classification_search_list.append(foc)

        # number_claims -- Done!
        noc = item.find('us-bibliographic-data-grant').find('number-of-claims')
        USPTN.number_claims = xml_value_to_string(noc, 'number-of-claims', file, pub_docnumber.text)

        # citation_list = [] -- Done!
        citations = item.find('us-bibliographic-data-grant').find('references-cited')
        if citations is not None:
            for cc in citations:
                #print(cc.getchildren())
                if cc.find('patcit') is not None:
                    num = cc.find('patcit').get('num')
                    cc_doc_num = cc.find('patcit').find('document-id').find('doc-number')
                    USPTN.citation_list.append(xml_value_to_string(cc_doc_num, 'doc-number', file, pub_docnumber.text))

                #print(cc, cc.getchildren())
                elif cc.find('nplcit') is not None:
                    #print(cc.find('nplcit').getchildren())
                    cc_ref = cc.find('nplcit').find('othercit')
                    USPTN.other_reference_list.append(xml_value_to_string(cc_ref, 'othercit', file, pub_docnumber.text))
                else:
                    pass


        # citing_list = []

        # abstract -- Done! -- 중간 태그가 삽입되는 경우(<i>.. </i>) 짤리는 문제가 있음!
        abs = item.find('abstract')
        if abs is not None:
            USPTN.abstract = abs.find('p').text


    # us-patent-grant-v43-2012-12-04.dtd -- OK
    elif dtd_version == 'v4.3 2012-12-04': #--------------------------------------------------------------------
        # pub_docnumber -- Done!
        pub_docnumber       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find(
            'doc-number')
        USPTN.pub_docnumber = xml_value_to_string(pub_docnumber, 'doc-number', file)

        # pub_country -- Done!
        pub_country       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('country')
        USPTN.pub_country = xml_value_to_string(pub_country, 'country', file, pub_docnumber.text)

        # pub_kind -- Done!
        pub_kind       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('kind')
        USPTN.pub_kind = xml_value_to_string(pub_kind, 'kind', file, pub_docnumber.text)

        # pub_date -- Done!
        pub_date       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('date')
        USPTN.pub_date = xml_value_to_string(pub_date, 'date', file, pub_docnumber.text)

        # app_docnumber -- Done!
        app_docnumber       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find(
            'doc-number')
        USPTN.app_docnumber = xml_value_to_string(app_docnumber, 'country', file, pub_docnumber.text)

        # app_country -- Done!
        app_country       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('country')
        USPTN.app_country = xml_value_to_string(app_country, 'country', file, pub_docnumber.text)

        # app_date -- Done!
        app_date       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('date')
        USPTN.app_date = xml_value_to_string(app_date, 'country', file, pub_docnumber.text)

        # invention_title -- Done!
        invention_title       = item.find('us-bibliographic-data-grant').find('invention-title')
        USPTN.invention_title = xml_value_to_string(invention_title, 'invention-title', file, pub_docnumber.text)

        # Applicants_list = [] -- Done!
        applicants = item.find('us-bibliographic-data-grant').find('us-parties').find('us-applicants')
        if applicants is not None:
            for applicant in applicants:
                Appnt = USPTO.Applicant()
                # Addressbook
                add_book = applicant.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Appnt.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Appnt.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Appnt.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                if zz.tag == 'city':
                                    Appnt.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Appnt.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                # Residence Country
                if applicant.find('residence') is not None:
                    for resid in applicant.find('residence').getchildren():
                        if resid.tag == 'country':
                            Appnt.residence_country = resid.text

                USPTN.Applicants_list.append(Appnt)

        # Assignees_list = [] -- Done
        assignees = item.find('us-bibliographic-data-grant').find('assignees')
        if assignees is not None:
            for assignee in assignees:
                Assgn = USPTO.Assignee()
                # Addressbook
                add_book = assignee.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Assgn.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Assgn.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Assgn.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                #print(zz.tag)
                                if zz.tag == 'city':
                                    Assgn.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Assgn.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                elif zz.tag == 'country':
                                    Assgn.residence_country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                USPTN.Assignees_list.append(Assgn)

        # classification_national_list = [] -- Done
        classification_national = item.find('us-bibliographic-data-grant').find('classification-national')
        if classification_national is not None:
            #print('here>?>>>')
            for cn in classification_national:
                if cn.tag == 'main-classification':
                    USPTN.classification_national_list.append(xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                elif cn.tag == 'further-classification':
                    USPTN.classification_national_list.append(
                        xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                else:
                    #print(' Cannot find!')
                    pass

        # classification_ipc_list = [] -- Done
        classification_ipcr = item.find('us-bibliographic-data-grant').find('classifications-ipcr')
        if classification_ipcr is not None:
            for ci in classification_ipcr:
                ipcr = USPTO.IPCR()
                for ci2 in ci.getchildren():
                    if ci2.tag == 'ipc-version-indicator':
                        ipcr.date = ci2.find('date')
                    elif ci2.tag == 'classification-level':
                        ipcr.classification_level = xml_value_to_string(ci2, 'classification-level', file, pub_docnumber.text)
                    elif ci2.tag == 'section':
                        ipcr.section = xml_value_to_string(ci2, 'section', file, pub_docnumber.text)
                    elif ci2.tag == 'class':
                        ipcr.I_class = xml_value_to_string(ci2, 'class', file, pub_docnumber.text)
                    elif ci2.tag == 'subclass':
                        ipcr.I_subclass = xml_value_to_string(ci2, 'subclass', file, pub_docnumber.text)
                    elif ci2.tag == 'main-group':
                        ipcr.main_group = xml_value_to_string(ci2, 'main-group', file, pub_docnumber.text)
                    elif ci2.tag == 'subgroup':
                        ipcr.subgroup = xml_value_to_string(ci2, 'subgroup', file, pub_docnumber.text)
                    elif ci2.tag == 'symbol-position':
                        ipcr.symbol_position = xml_value_to_string(ci2, 'symbol-position', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-value':
                        ipcr.classification_value = xml_value_to_string(ci2, 'classification-value', file, pub_docnumber.text)
                    elif ci2.tag == 'action-date':
                        ipcr.action_date = xml_value_to_string(ci2.find('date'), 'action-date', file, pub_docnumber.text)
                    elif ci2.tag == 'generating-office':
                        ipcr.generating_office = xml_value_to_string(ci2.find('country'), 'generating-office', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-status':
                        ipcr.classification_status = xml_value_to_string(ci2, 'classification-status', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-data-source':
                        ipcr.classification_data_source = xml_value_to_string(ci2, 'classification-data-source', file, pub_docnumber.text)
                    else:
                        pass

                USPTN.classification_ipc_list.append(ipcr)

        # fieldsearch_list = []  us-field-of-classification-search -- Done
        us_foc_search = item.find('us-bibliographic-data-grant').find('us-field-of-classification-search')
        if us_foc_search is not None and us_foc_search.find('classification-national') is not None:
            for zz in us_foc_search.find('classification-national'):
                foc = USPTO.Field_of_Class_Search()

                if zz.tag == 'country':
                    foc.country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                elif zz.tag == 'main-classification':
                    foc.main_classification = xml_value_to_string(zz, 'main-classification', file, pub_docnumber.text)
                elif zz.tag == 'additional-info':
                    foc.additional_info = xml_value_to_string(zz, 'additional-info', file, pub_docnumber.text)
                else:
                    pass

                USPTN.field_of_classification_search_list.append(foc)

        # number_claims -- Done!
        noc = item.find('us-bibliographic-data-grant').find('number-of-claims')
        USPTN.number_claims = xml_value_to_string(noc, 'number-of-claims', file, pub_docnumber.text)

        # citation_list = [] -- Done!
        citations = item.find('us-bibliographic-data-grant').find('us-references-cited')
        if citations is not None:
            for cc in citations:
                #print(cc.getchildren())
                if cc.find('patcit') is not None:
                    num = cc.find('patcit').get('num')
                    cc_doc_num = cc.find('patcit').find('document-id').find('doc-number')
                    USPTN.citation_list.append(xml_value_to_string(cc_doc_num, 'doc-number', file, pub_docnumber.text))

                #print(cc, cc.getchildren())
                elif cc.find('nplcit') is not None:
                    #print(cc.find('nplcit').getchildren())
                    cc_ref = cc.find('nplcit').find('othercit')
                    USPTN.other_reference_list.append(xml_value_to_string(cc_ref, 'othercit', file, pub_docnumber.text))
                else:
                    pass

        # citing_list = []

        # abstract -- Done! -- 중간 태그가 삽입되는 경우(<i>.. </i>) 짤리는 문제가 있음!
        abs = item.find('abstract')
        if abs is not None:
            USPTN.abstract = abs.find('p').text


    # us-patent-grant-v44-2013-05-16.dtd -- OK
    elif dtd_version == 'v4.4 2013-05-16': #--------------------------------------------------------------------
        # pub_docnumber -- Done!
        pub_docnumber       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find(
            'doc-number')
        USPTN.pub_docnumber = xml_value_to_string(pub_docnumber, 'doc-number', file)

        # pub_country -- Done!
        pub_country       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('country')
        USPTN.pub_country = xml_value_to_string(pub_country, 'country', file, pub_docnumber.text)

        # pub_kind -- Done!
        pub_kind       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('kind')
        USPTN.pub_kind = xml_value_to_string(pub_kind, 'kind', file, pub_docnumber.text)

        # pub_date -- Done!
        pub_date       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('date')
        USPTN.pub_date = xml_value_to_string(pub_date, 'date', file, pub_docnumber.text)

        # app_docnumber -- Done!
        app_docnumber       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find(
            'doc-number')
        USPTN.app_docnumber = xml_value_to_string(app_docnumber, 'country', file, pub_docnumber.text)

        # app_country -- Done!
        app_country       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('country')
        USPTN.app_country = xml_value_to_string(app_country, 'country', file, pub_docnumber.text)

        # app_date -- Done!
        app_date       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('date')
        USPTN.app_date = xml_value_to_string(app_date, 'country', file, pub_docnumber.text)

        # invention_title -- Done!
        invention_title       = item.find('us-bibliographic-data-grant').find('invention-title')
        USPTN.invention_title = xml_value_to_string(invention_title, 'invention-title', file, pub_docnumber.text)

        # Applicants_list = [] -- Done!
        applicants = item.find('us-bibliographic-data-grant').find('us-parties').find('us-applicants')
        if applicants is not None:
            for applicant in applicants:
                Appnt = USPTO.Applicant()
                # Addressbook
                add_book = applicant.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Appnt.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Appnt.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Appnt.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                if zz.tag == 'city':
                                    Appnt.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Appnt.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                # Residence Country
                if applicant.find('residence') is not None:
                    for resid in applicant.find('residence').getchildren():
                        if resid.tag == 'country':
                            Appnt.residence_country = resid.text

                USPTN.Applicants_list.append(Appnt)

        # Assignees_list = [] -- Done
        assignees = item.find('us-bibliographic-data-grant').find('assignees')
        if assignees is not None:
            for assignee in assignees:
                Assgn = USPTO.Assignee()
                # Addressbook
                add_book = assignee.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Assgn.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Assgn.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Assgn.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                #print(zz.tag)
                                if zz.tag == 'city':
                                    Assgn.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Assgn.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                elif zz.tag == 'country':
                                    Assgn.residence_country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                USPTN.Assignees_list.append(Assgn)

        # classification_national_list = [] -- Done
        classification_national = item.find('us-bibliographic-data-grant').find('classification-national')
        if classification_national is not None:
            #print('here>?>>>')
            for cn in classification_national:
                if cn.tag == 'main-classification':
                    USPTN.classification_national_list.append(xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                elif cn.tag == 'further-classification':
                    USPTN.classification_national_list.append(
                        xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                else:
                    #print(' Cannot find!')
                    pass

        # classification_ipc_list = [] -- Done
        classification_ipcr = item.find('us-bibliographic-data-grant').find('classifications-ipcr')
        if classification_ipcr is not None:
            for ci in classification_ipcr:
                ipcr = USPTO.IPCR()
                for ci2 in ci.getchildren():
                    if ci2.tag == 'ipc-version-indicator':
                        ipcr.date = ci2.find('date')
                    elif ci2.tag == 'classification-level':
                        ipcr.classification_level = xml_value_to_string(ci2, 'classification-level', file, pub_docnumber.text)
                    elif ci2.tag == 'section':
                        ipcr.section = xml_value_to_string(ci2, 'section', file, pub_docnumber.text)
                    elif ci2.tag == 'class':
                        ipcr.I_class = xml_value_to_string(ci2, 'class', file, pub_docnumber.text)
                    elif ci2.tag == 'subclass':
                        ipcr.I_subclass = xml_value_to_string(ci2, 'subclass', file, pub_docnumber.text)
                    elif ci2.tag == 'main-group':
                        ipcr.main_group = xml_value_to_string(ci2, 'main-group', file, pub_docnumber.text)
                    elif ci2.tag == 'subgroup':
                        ipcr.subgroup = xml_value_to_string(ci2, 'subgroup', file, pub_docnumber.text)
                    elif ci2.tag == 'symbol-position':
                        ipcr.symbol_position = xml_value_to_string(ci2, 'symbol-position', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-value':
                        ipcr.classification_value = xml_value_to_string(ci2, 'classification-value', file, pub_docnumber.text)
                    elif ci2.tag == 'action-date':
                        ipcr.action_date = xml_value_to_string(ci2.find('date'), 'action-date', file, pub_docnumber.text)
                    elif ci2.tag == 'generating-office':
                        ipcr.generating_office = xml_value_to_string(ci2.find('country'), 'generating-office', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-status':
                        ipcr.classification_status = xml_value_to_string(ci2, 'classification-status', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-data-source':
                        ipcr.classification_data_source = xml_value_to_string(ci2, 'classification-data-source', file, pub_docnumber.text)
                    else:
                        pass

                USPTN.classification_ipc_list.append(ipcr)

        # fieldsearch_list = []  us-field-of-classification-search -- Done
        us_foc_search = item.find('us-bibliographic-data-grant').find('us-field-of-classification-search')
        if us_foc_search is not None and us_foc_search.find('classification-national') is not None:
            for zz in us_foc_search.find('classification-national'):
                foc = USPTO.Field_of_Class_Search()

                if zz.tag == 'country':
                    foc.country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                elif zz.tag == 'main-classification':
                    foc.main_classification = xml_value_to_string(zz, 'main-classification', file, pub_docnumber.text)
                elif zz.tag == 'additional-info':
                    foc.additional_info = xml_value_to_string(zz, 'additional-info', file, pub_docnumber.text)
                else:
                    pass

                USPTN.field_of_classification_search_list.append(foc)

        # number_claims -- Done!
        noc = item.find('us-bibliographic-data-grant').find('number-of-claims')
        USPTN.number_claims = xml_value_to_string(noc, 'number-of-claims', file, pub_docnumber.text)

        # citation_list = [] -- Done!
        citations = item.find('us-bibliographic-data-grant').find('us-references-cited')
        if citations is not None:
            for cc in citations:
                #print(cc.getchildren())
                if cc.find('patcit') is not None:
                    num = cc.find('patcit').get('num')
                    cc_doc_num = cc.find('patcit').find('document-id').find('doc-number')
                    USPTN.citation_list.append(xml_value_to_string(cc_doc_num, 'doc-number', file, pub_docnumber.text))

                #print(cc, cc.getchildren())
                elif cc.find('nplcit') is not None:
                    #print(cc.find('nplcit').getchildren())
                    cc_ref = cc.find('nplcit').find('othercit')
                    USPTN.other_reference_list.append(xml_value_to_string(cc_ref, 'othercit', file, pub_docnumber.text))
                else:
                    pass

        # citing_list = []

        # abstract -- Done! -- 중간 태그가 삽입되는 경우(<i>.. </i>) 짤리는 문제가 있음!
        abs = item.find('abstract')
        if abs is not None:
            USPTN.abstract = abs.find('p').text

    # us-patent-grant-v45-2014-04-03.dtd -- OK
    elif dtd_version == 'v4.5 2014-04-03': #--------------------------------------------------------------------
        # pub_docnumber -- Done!
        pub_docnumber       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find(
            'doc-number')
        USPTN.pub_docnumber = xml_value_to_string(pub_docnumber, 'doc-number', file)

        # pub_country -- Done!
        pub_country       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('country')
        USPTN.pub_country = xml_value_to_string(pub_country, 'country', file, pub_docnumber.text)

        # pub_kind -- Done!
        pub_kind       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('kind')
        USPTN.pub_kind = xml_value_to_string(pub_kind, 'kind', file, pub_docnumber.text)

        # pub_date -- Done!
        pub_date       = item.find('us-bibliographic-data-grant').find('publication-reference').find('document-id').find('date')
        USPTN.pub_date = xml_value_to_string(pub_date, 'date', file, pub_docnumber.text)

        # app_docnumber -- Done!
        app_docnumber       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find(
            'doc-number')
        USPTN.app_docnumber = xml_value_to_string(app_docnumber, 'country', file, pub_docnumber.text)

        # app_country -- Done!
        app_country       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('country')
        USPTN.app_country = xml_value_to_string(app_country, 'country', file, pub_docnumber.text)

        # app_date -- Done!
        app_date       = item.find('us-bibliographic-data-grant').find('application-reference').find('document-id').find('date')
        USPTN.app_date = xml_value_to_string(app_date, 'country', file, pub_docnumber.text)

        # invention_title -- Done!
        invention_title       = item.find('us-bibliographic-data-grant').find('invention-title')
        USPTN.invention_title = xml_value_to_string(invention_title, 'invention-title', file, pub_docnumber.text)

        # Applicants_list = [] -- Done!
        applicants = item.find('us-bibliographic-data-grant').find('us-parties').find('us-applicants')
        if applicants is not None:
            for applicant in applicants:
                Appnt = USPTO.Applicant()
                # Addressbook
                add_book = applicant.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Appnt.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Appnt.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Appnt.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                if zz.tag == 'city':
                                    Appnt.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Appnt.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                # Residence Country
                if applicant.find('residence') is not None:
                    for resid in applicant.find('residence').getchildren():
                        if resid.tag == 'country':
                            Appnt.residence_country = resid.text

                USPTN.Applicants_list.append(Appnt)

        # Assignees_list = [] -- Done
        assignees = item.find('us-bibliographic-data-grant').find('assignees')
        if assignees is not None:
            for assignee in assignees:
                Assgn = USPTO.Assignee()
                # Addressbook
                add_book = assignee.find('addressbook')
                if add_book is not None:
                    for addr in add_book.getchildren():
                        if addr.tag == 'orgname':
                            Assgn.orgname = xml_value_to_string(addr, 'orgname', file, pub_docnumber.text)
                        elif addr.tag == 'last-name':
                            Assgn.lastname = xml_value_to_string(addr, 'last-name', file, pub_docnumber.text)
                        elif addr.tag == 'first-name':
                            Assgn.firstname = xml_value_to_string(addr, 'first-name', file, pub_docnumber.text)
                        elif addr.tag == 'address':
                            for zz in addr:
                                #print(zz.tag)
                                if zz.tag == 'city':
                                    Assgn.city = xml_value_to_string(zz, 'city', file, pub_docnumber.text)
                                elif zz.tag == 'state':
                                    Assgn.state = xml_value_to_string(zz, 'state', file, pub_docnumber.text)
                                elif zz.tag == 'country':
                                    Assgn.residence_country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                                else:
                                    pass
                        else:
                            pass

                USPTN.Assignees_list.append(Assgn)

        # classification_national_list = [] -- Done
        classification_national = item.find('us-bibliographic-data-grant').find('classification-national')
        if classification_national is not None:
            for cn in classification_national:
                if cn.tag == 'main-classification':
                    USPTN.classification_national_list.append(xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'main-classification', file, pub_docnumber.text))
                elif cn.tag == 'further-classification':
                    USPTN.classification_national_list.append(
                        xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                    #print(pub_docnumber.text, xml_value_to_string(cn, 'further-classification', file, pub_docnumber.text))
                else:
                    #print(' Cannot find!')
                    pass


        # classification_ipc_list = [] -- Done
        classification_ipcr = item.find('us-bibliographic-data-grant').find('classifications-ipcr')
        if classification_ipcr is not None:
            for ci in classification_ipcr:
                ipcr = USPTO.IPCR()
                for ci2 in ci.getchildren():
                    if ci2.tag == 'ipc-version-indicator':
                        ipcr.date = ci2.find('date')
                    elif ci2.tag == 'classification-level':
                        ipcr.classification_level = xml_value_to_string(ci2, 'classification-level', file, pub_docnumber.text)
                    elif ci2.tag == 'section':
                        ipcr.section = xml_value_to_string(ci2, 'section', file, pub_docnumber.text)
                    elif ci2.tag == 'class':
                        ipcr.I_class = xml_value_to_string(ci2, 'class', file, pub_docnumber.text)
                    elif ci2.tag == 'subclass':
                        ipcr.I_subclass = xml_value_to_string(ci2, 'subclass', file, pub_docnumber.text)
                    elif ci2.tag == 'main-group':
                        ipcr.main_group = xml_value_to_string(ci2, 'main-group', file, pub_docnumber.text)
                    elif ci2.tag == 'subgroup':
                        ipcr.subgroup = xml_value_to_string(ci2, 'subgroup', file, pub_docnumber.text)
                    elif ci2.tag == 'symbol-position':
                        ipcr.symbol_position = xml_value_to_string(ci2, 'symbol-position', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-value':
                        ipcr.classification_value = xml_value_to_string(ci2, 'classification-value', file, pub_docnumber.text)
                    elif ci2.tag == 'action-date':
                        ipcr.action_date = xml_value_to_string(ci2.find('date'), 'action-date', file, pub_docnumber.text)
                    elif ci2.tag == 'generating-office':
                        ipcr.generating_office = xml_value_to_string(ci2.find('country'), 'generating-office', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-status':
                        ipcr.classification_status = xml_value_to_string(ci2, 'classification-status', file, pub_docnumber.text)
                    elif ci2.tag == 'classification-data-source':
                        ipcr.classification_data_source = xml_value_to_string(ci2, 'classification-data-source', file, pub_docnumber.text)
                    else:
                        pass

                USPTN.classification_ipc_list.append(ipcr)

        # fieldsearch_list = []  us-field-of-classification-search -- Done
        us_foc_search = item.find('us-bibliographic-data-grant').find('us-field-of-classification-search')
        if us_foc_search is not None and us_foc_search.find('classification-national') is not None:
            for zz in us_foc_search.find('classification-national'):
                foc = USPTO.Field_of_Class_Search()

                if zz.tag == 'country':
                    foc.country = xml_value_to_string(zz, 'country', file, pub_docnumber.text)
                elif zz.tag == 'main-classification':
                    foc.main_classification = xml_value_to_string(zz, 'main-classification', file, pub_docnumber.text)
                elif zz.tag == 'additional-info':
                    foc.additional_info = xml_value_to_string(zz, 'additional-info', file, pub_docnumber.text)
                else:
                    pass

                USPTN.field_of_classification_search_list.append(foc)


        # number_claims -- Done!
        noc = item.find('us-bibliographic-data-grant').find('number-of-claims')
        USPTN.number_claims = xml_value_to_string(noc, 'number-of-claims', file, pub_docnumber.text)

        # citation_list = [] -- Done!
        citations = item.find('us-bibliographic-data-grant').find('us-references-cited')
        if citations is not None:
            for cc in citations:
                #print(cc.getchildren())
                if cc.find('patcit') is not None:
                    num = cc.find('patcit').get('num')
                    cc_doc_num = cc.find('patcit').find('document-id').find('doc-number')
                    USPTN.citation_list.append(xml_value_to_string(cc_doc_num, 'doc-number', file, pub_docnumber.text))

                #print(cc, cc.getchildren())
                elif cc.find('nplcit') is not None:
                    #print(cc.find('nplcit').getchildren())
                    cc_ref = cc.find('nplcit').find('othercit')
                    USPTN.other_reference_list.append(xml_value_to_string(cc_ref, 'othercit', file, pub_docnumber.text))
                else:
                    pass

        # citing_list = []

        # abstract -- Done! -- 중간 태그가 삽입되는 경우(<i>.. </i>) 짤리는 문제가 있음!
        abs = item.find('abstract')
        if abs is not None:
            USPTN.abstract = abs.find('p').text

    else:
        print('[Warn] Cannot find the proper xml parsing rules for DTD version : ', dtd_version)
        return 0
    return 1

