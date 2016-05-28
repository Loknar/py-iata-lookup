#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree

import browser_utils

html_utf8_parser = etree.HTMLParser(encoding="utf-8")

iata_search_page = 'http://www.iata.org/publications/Pages/code-search.aspx'

def do_search(search_param, search_type):
	if search_type not in ('ByAirlineCode', 'ByAirlineName', 'ByLocationName', 'ByLocationCode'):
		raise Exception('Invalid search type.')
	user_agent = browser_utils.random_user_agent()
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
	iata_search_endpoint = 'http://www.iata.org/publications/_vti_bin/sites.asmx'
	res = session.post(iata_search_endpoint, data=soap_envelope, headers={
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.8,is;q=0.6',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Content-Length': len(soap_envelope),
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
		'%sddlImLookingFor' % (mistery_key, ): search_type,
		'%stxtSearchCriteria' % (mistery_key, ): search_param,
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
	root = etree.fromstring(res.content, html_utf8_parser)
	xpath = './/*[@id="ctl00_SPWebPartManager1_g_e3b09024_878e_4522_bd47_acfefd1000b0_ctl00_panResults"]/table'
	return root.find(xpath)

def lookup_airline_by_code(code):
	results = []
	table = do_search(code, 'ByAirlineCode')
	if table is not None:
		table_body = table.find('.//tbody')
		for table_row in table_body.findall('.//tr'):
			airline_name = table_row[0].text
			iata_code = table_row[1].text
			accounting_code = table_row[2].text
			airline_prefix_code = table_row[3].text
			results.append({
				'airline_name': airline_name,
				'iata_code': iata_code,
				'accounting_code': accounting_code,
				'airline_prefix_code': airline_prefix_code,
			})
	return results

def lookup_airline_by_name(name):
	results = []
	table = do_search(name, 'ByAirlineName')
	if table is not None:
		table_body = table.find('.//tbody')
		for table_row in table_body.findall('.//tr'):
			airline_name = table_row[0].text
			iata_code = table_row[1].text
			accounting_code = table_row[2].text
			airline_prefix_code = table_row[3].text
			results.append({
				'airline_name': airline_name,
				'iata_code': iata_code,
				'accounting_code': accounting_code,
				'airline_prefix_code': airline_prefix_code,
			})
	return results

def lookup_location_by_name(name):
	results = []
	table = do_search(name, 'ByLocationName')
	if table is not None:
		table_body = table.find('.//tbody')
		for table_row in table_body.findall('.//tr'):
			city_name = table_row[0].text
			city_code = table_row[1].text
			airport_name = table_row[2].text
			airport_code = table_row[3].text
			results.append({
				'city_name': city_name,
				'city_code': city_code,
				'airport_name': airport_name,
				'airport_code': airport_code,
			})
	return results

def lookup_location_by_code(code):
	results = []
	table = do_search(code, 'ByLocationCode')
	if table is not None:
		table_body = table.find('.//tbody')
		for table_row in table_body.findall('.//tr'):
			city_name = table_row[0].text
			city_code = table_row[1].text
			airport_name = table_row[2].text
			airport_code = table_row[3].text
			results.append({
				'city_name': city_name,
				'city_code': city_code,
				'airport_name': airport_name,
				'airport_code': airport_code,
			})
	return results

if __name__ == '__main__':
	print 'Manual tests.'
	print '\nLookup airline by code: "WW"'
	print lookup_airline_by_code('WW')
	print '\nLookup airline by name: "Norwegian"'
	print lookup_airline_by_name('Norwegian')
	print '\nLookup location by name: "London"'
	print lookup_location_by_name('London')
	print '\nLookup location by code: "YYZ"'
	print lookup_location_by_code('YYZ')
