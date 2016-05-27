#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree

import browser_utils

user_agent = browser_utils.random_user_agent()
html_utf8_parser = etree.HTMLParser(encoding="utf-8")

headers = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.8,is;q=0.6',
	'Cache-Control': 'no-cache',
	'Connection': 'keep-alive',
	'Content-Type': 'text/xml',
	'Host': 'www.iata.org',
	'Origin': 'http://www.iata.org',
	'Pragma': 'no-cache',
	'Referer': 'http://www.iata.org/publications/Pages/code-search.aspx',
	'SOAPAction': 'http://schemas.microsoft.com/sharepoint/soap/GetUpdatedFormDigest',
	'User-Agent': user_agent,
}

iata_search_page = 'http://www.iata.org/publications/Pages/code-search.aspx'

from pprint import pprint
import pdb # noqa

def lookup_airline_by_iata(iata_code):
	session = requests.session()
	session.get(iata_search_page, headers=headers)
	soap_envelope = '''<?xml version="1.0" encoding="utf-8"?>
	<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
		<soap:Body>
			<GetUpdatedFormDigest
			 xmlns="http://schemas.microsoft.com/sharepoint/soap/" />
		</soap:Body>
	</soap:Envelope>'''.replace('\t', '').replace('\n', '')
	headers['Content-Length'] = len(soap_envelope)
	iata_search_endpoint = 'http://www.iata.org/publications/_vti_bin/sites.asmx'
	res = session.post(iata_search_endpoint, data=soap_envelope, headers={
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.8,is;q=0.6',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Content-Type': 'text/xml',
		'Host': 'www.iata.org',
		'Origin': 'http://www.iata.org',
		'Pragma': 'no-cache',
		'Referer': 'http://www.iata.org/publications/Pages/code-search.aspx',
		'SOAPAction': 'http://schemas.microsoft.com/sharepoint/soap/GetUpdatedFormDigest',
		'User-Agent': user_agent,
	})
	root = etree.fromstring(res.content)
	soap_ns = '{http://schemas.microsoft.com/sharepoint/soap/}'
	request_digest = root.find('.//%sGetUpdatedFormDigestResult' % (soap_ns, )).text
	mistery_key = 'ctl00$SPWebPartManager1$g_e3b09024_878e_4522_bd47_acfefd1000b0$ctl00$'
	form_data = {
		'ctl00$sm': 'ctl00$sm|%sbutSearch' % (mistery_key, ),
		'__SPSCEditMenu': 'true',
		'_wpcmWpid': '',
		'wpcmVal': '',
		'MSOWebPartPage_PostbackSource': '',
		'MSOTlPn_SelectedWpId': '',
		'MSOTlPn_View': 0,
		'MSOTlPn_ShowSettings': 'False',
		'MSOGallery_SelectedLibrary': '',
		'MSOGallery_FilterString': '',
		'MSOTlPn_Button': 'none',
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'__REQUESTDIGEST': request_digest,
		'ctl00_sm_HiddenField': '',
		'MSOSPWebPartManager_DisplayModeName': 'Browse',
		'MSOSPWebPartManager_StartWebPartEditingName': 'false',
		'MSOSPWebPartManager_EndWebPartEditing': 'false',
		'__VIEWSTATE': '',
		'__VIEWSTATEGENERATOR': '',
		'ctl00$Header$AdvanceSearchBox$DisplayContent$SearchTextBox': '',
		'%sddlImLookingFor' % (mistery_key, ): 'ByAirlineCode',
		'%stxtSearchCriteria' % (mistery_key, ): iata_code,
		'%stxtSearchCriteriaRequiredValidatorCalloutExtender_ClientState' % (mistery_key, ): '',
		'__ASYNCPOST': 'true',
		'%sbutSearch' % (mistery_key, ): 'Search'
	}
	res = session.post(iata_search_page, data=form_data, headers={
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.8,is;q=0.6',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Content-Length': 5816,
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Host': 'www.iata.org',
		'Origin': 'http://www.iata.org',
		'Pragma': 'no-cache',
		'Referer': 'http://www.iata.org/publications/Pages/code-search.aspx',
		'User-Agent': user_agent,
		'X-MicrosoftAjax': 'Delta=true',
		'X-Requested-With': 'XMLHttpRequest'
	})
	print res
	print 'WOW found' if 'WOW Air ehf' in res.content else 'WOW not found'
	print >> open('dump.html', 'w'), res.content
	pdb.set_trace()


if __name__ == '__main__':
	lookup_airline_by_iata('WW')
