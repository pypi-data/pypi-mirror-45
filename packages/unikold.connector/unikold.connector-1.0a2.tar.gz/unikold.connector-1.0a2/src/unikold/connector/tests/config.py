# -*- coding: utf-8 -*-
soap_test_url = u'http://webservices.daehosting.com/services/isbnservice.wso?WSDL'
soap_test_method = u'IsValidISBN13'
soap_test_method_parameter = u'9783492700764'

# config data needed for LSF tests
lsf_wsdl_url = u'http://lsftomcat05:8080/qisserver/services/dbinterface?WSDL'
lsf_test_object_type = u'Lecture'  # LSF object type
lsf_test_conditions = [('id', '110903'), ('_Bezugssemester', '20182')]
lsf_auth_test_object_type = u'KOLAPerson'
lsf_auth_test_conditions = [('mail', 'mbarde@uni-koblenz.de')]
lsf_wsdl_search_url = u'http://lsftomcat05:8080/qisserver/services/soapsearch?WSDL'
lsf_search_test_method_parameter = u'<search><object>person</object><expression><column name="personal.nachname" value="Barde" /><column name="personal.vorname" value="Matthias" /></expression></search>'  # noqa: E501
lsf_auth_username = u'soapadmin'
lsf_auth_password = u'1q2w3e$r'
