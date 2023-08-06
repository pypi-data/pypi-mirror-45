import datetime
import os

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from axe_selenium_python import Axe

"""
/*
 * Takes the parsed data from the AXE JSON report and output to HTML
 * The HTML report will contain the following information - Impact, TargetHTML, Description, Failure Summary & Help Url
 * @param {string} filename - the filename for the HTML report
 * @param {string} URL - the URL for the page we are scanning
 * @param {number} criticalCount - the count for issues with critical severity
 * @param {number} seriousCount - the count for issues with serious severity
 * @param {number} moderateCount - the count for issues with moderate severity
 * @param {number} minorCount - the count for issues with minor severity
 * @param {string} violationsTableHTML - the HTML code for the violations table
 */
 """
def outputToHTML(filename, URL, criticalCount, seriousCount, moderateCount, minorCount, violationsTableHTML):
	# The HTML code with embedded css and javascript logic for severity filter
	violationsHTML = "<!DOCTYPE html>\
		<html lang=\"en\">\
			<head>\
				<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>\
				<style>\
					#summaryTable tr td {white-space: nowrap;}\
					table {font-family: arial, sans-serif; border-color: black; border-collapse: collapse; width: 100%;}\
					td, th {border: 1px solid black; text-align: left; padding: 8px;}\
					tr:nth-child(even) {background-color: #dddddd;}\
				</style>\
				<meta charset=\"utf-8\">\
				<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">\
				<meta name=\"theme-color\" content=\"#000000\">\
				<title>AXE Violations</title>\
				<script>\
					$(document).ready(function ($) {\
						$('#impactSelector').change(function () {\
							$('table').show();\
							var selection = $(this).val();\
							var dataset = $('#violationsTable tbody').find('tr');\
							dataset.show();\
							dataset.filter(function (index, item) {\
								return $(item).find('td:nth-child(2)').text().indexOf(selection) === -1;\
							}).hide();\
						});\
					});\
				</script>\
			</head>\
			<body>\
				<div>\
					<table id=\"summaryTable\" style=\"margin-bottom:10px;width:1%\">\
						<tr><th colspan=\"2\">Report Summary</th></tr>\
						<tr>\
							<td>Violation URL</td>\
							<td><a href=\"" + URL + "\">" + URL + "</a></td>\
						</tr>\
						<tr>\
							<td>Critical</td>\
							<td>" + str(criticalCount) + "</td>\
						</tr>\
						<tr>\
							<td>Serious</td>\
							<td>" + str(seriousCount) + "</td>\
						</tr>\
						<tr>\
							<td>Moderate</td>\
							<td>" + str(moderateCount) + "</td>\
						</tr>\
						<tr>\
							<td>Minor</td>\
							<td>" + str(minorCount) + "</td>\
						</tr>\
					</table>\
				</div>\
				<h3>Violations</h3>\
				<div>\
					<table id='violationsTable'>\
						<thead>\
							<tr>\
								<th>#</th>\
								<th>Impact\
									<select id='impactSelector'>\
										<option value=\"\">Show</option>\
										<option value=\"critical\">critical</option>\
										<option value=\"serious\">serious</option>\
										<option value=\"moderate\">moderate</option>\
										<option value=\"minor\">minor</option>\
									</select>\
								</th>\
								<th>Target HTML</th>\
								<th>Description</th>\
								<th>Failure Summary</th>\
								<th>Help Url</th>\
							</tr>\
						</thead>\
						<tbody>" + str(violationsTableHTML) + "</tbody>\
					</table>\
				</div>\
			</body>\
		</html>"


	# Output the report file to the "accessibility_reports" folder
	# The folder will be created if it didn't exist already
	f = open('./accessibility_reports/' + filename + '.html', 'w')
	f.write(violationsHTML)
	f.close()


"""
/*
 * Takes the parsed data from the AXE JSON report and output to HTML
 * @param {string} filename - the filename for the HTML report
 * @param {array} violations - the violations array from the AXE JSON report
 * @param {string} URL - the URL for the page we are scanning
 */
 """
def generateHTMLReport(filename, violations, URL):
	dir = './accessibility_reports'
	timestamp = ''
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	day = now.day
	hour = now.hour
	min = now.minute

	timestamp += str(year) + str(month) + str(day) + str(hour) + str(min)
	filename += '_' + timestamp

	# create the accessibility_reports folder if it didn't exsit already
	try:
		if(os.path.isdir(dir)):
			os.makedirs(dir)
	except OSError:
		print("Creation of the directory %s failed" % dir)
	else:
		print("Successfully created the directory %s " % dir)

	# Loop through the violations and parse them into HTML
	criticalCount = 0
	moderateCount = 0
	seriousCount = 0
	minorCount = 0
	violationsTableHTML = ''
	i = 0
	for violation in violations:
		description = violation['description'].replace('<', '"').replace('>', '"')
		helpUrl = violation['helpUrl']
		impact = violation['impact']
		if impact == "critical":
			criticalCount += 1
		if impact == "serious":
			seriousCount += 1
		if impact == "moderate":
			moderateCount += 1
		if impact == "minor":
			minorCount += 1

		nodesArray = violation['nodes']
		targetHTML = ''
		failureSummary = ''
		for node in nodesArray:
			targetHTML = str(node['target']).replace('<', '&lt ').replace('>', '&gt ')
			failureSummary = str(node['failureSummary']).replace('<', '"').replace('>', '"')

		impactColorHtml = '<td>'
		if impact == "critical":
			impactColorHtml = "<td style=\"color:red \">"
		if impact == "serious":
			impactColorHtml = "<td style=\"color:orange\">"
		if impact == "moderate": 
			impactColorHtml = "<td style=\"color:rgb(246,207,87)\">"
		if impact == "minor": 
			impactColorHtml = "<td style=\"color:blue\">"
		
		i += 1
		violationsTableHTML += "<tr>\
			<td>" + str(i) + "</td>" + str(impactColorHtml) + str(impact) + "</td>\
			<td>" + str(targetHTML) + "</td>\
			<td>" + str(description) + "</td>\
			<td>" + str(failureSummary) + "</td>\
			<td><a href=\"" + str(helpUrl) + "\">" + str(str(helpUrl).replace("?application=axeAPI", "")) + "</a></td>\
		</tr>"

	outputToHTML(filename, URL, criticalCount, seriousCount, moderateCount, minorCount, violationsTableHTML)


"""
/*
 * Run Axe scan with the given Webdriver object, then parse the report into HTML format
 * @param {webdriver} driver - the filename for the HTML report
 * @param {string} filename - the violations array from the AXE JSON report
 * @return {array} results.violations - the violations array in the JSON report
 */
 """
def AxeScan (driver, filename):
	# Inject axe-core javascript into page.
	axe = Axe(driver)
	axe.inject()

	# Run axe accessibility checks.
	results = ""
	try: 
		results = axe.run()
	except StaleElementReferenceException:
		print('stale element exception, trying again')
		results = axe.run()
	

	url = driver.current_url
	print(url)
	
	# Parse the JSON and convert into HTML format
	generateHTMLReport(filename, results['violations'], url)

	return results['violations']


"""
/**
 * Run Axe scan with the given Webdriver object, then return the violations JSON
 * @param {webdriver} driver - the filename for the HTML report
 * @return {array} results.violations - the violations array in the JSON report
 */
 """
def getViolations (driver):
	axe = Axe(driver)
	 # Inject axe-core javascript into page.
	axe.inject()
	
	# Run axe accessibility checks.
	results = ""

	try:
		results = axe.run()
	except StaleElementReferenceException:
		print('stale element exception, trying again')
		results = axe.run()

	return results['violations']