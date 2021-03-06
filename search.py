#!/usr/bin/python
# -*- coding: utf-8 -*-

#TODO:
# 1. How to go next page [DONE]
# 2. month query [DONE]
# 3. detail [DONE]
# 4. write csv [DONE]
# 5. web site [DONE]
# 6. download doc

import requests, sys, string, re
import mydate
import csv
from subprocess import call

# global variable
table_starter = "<table width=\"0%\" border=\"0\" cellspacing=\"1\" cellpadding=\"0\">"
table_end = "</table>"
delimiter = "</tr>"
prefix = "http://www.sgs.gov.cn/shaic/"
punish_table_starter = "<table id=\"punishTable\" cellspacing=\"0\" cellpadding=\"0\" class=\"table_punish\">"

def query_first(start, end, keywords, pagenumber):
    data = {
            'caseName' : keywords,
            'startDate' : start,
            'endDate' : end,
            'pageNo' : pagenumber,
            #    'hotcrp': 'a0515c2055fa351715806b19ab87d919',
            }
    url="http://www.sgs.gov.cn/shaic/punish!getList.action"

    print "--Issue a request with " + keywords + "," + start + "-" +end + " page: " + str(pagenumber) + "--"
    content = requests.post(url, data=data).text
        
    #print content
    return content

def total_page(content):
    # get total pages
    matchObj = re.search( r'共(.*)页', content.encode("utf-8"), re.U)
    if matchObj:
        # this can crash
        totalpage = int(matchObj.group(1))
        print "Total pages are " + str(totalpage)
    else:
        print "\n\nERROR: cannot find total page!\n\n"
        totalpage = 1
    return totalpage

countentry = 0
def query_second(url):
    global countentry
    content = requests.get(url).text
    countentry += 1
    return content

def scoope(content, starter, end):
    start_pos = string.find(content, starter)
    content = content[start_pos+len(starter):]
    end_pos = string.find(content, end)
    info = content[:end_pos]
    return string.strip(info)

def download_doc(name, doc_link):
    filename = 'download/'+name
    print "-- download file: " + filename + " from " + doc_link
    call(['wget', '-O', filename, doc_link]) 

# an example
#<tr>
#<td>
#1
#</td>     
#<td align="left">
#时胡明在汇成中心街25号无照经营案
#</td>     
#<td>
#2015-10-30
#</td>     
#<td>
#<a target="_blank" href="punish!detail.action?uuid=02e48176510fefbf0151321dec345a09" >详情</a>
#</td>     

def pickInfoFromToken(token) :
    # find name
    name_starter = "<td align=\"left\">";
    name_start = string.find(token, name_starter)
    token = token[name_start+len(name_starter):]
    name_end = string.find(token, "</td>")
    name = string.strip(token[:name_end])
    print name

    # find date
    date_start = string.find(token, "<td>")
    token = token[date_start+len("<td>"):]
    date_end = string.find(token, "</td>")
    date = string.strip(token[:date_end])
    print date
 
    # find detail
    details = string.split(token)
    for piece in details:
        if string.find(piece, "href=") != -1 :
            link = piece[6:-1]
            break
    link = prefix + link
    print link

    # query second and continue parsing
    more_info = query_second(link)
    
    # find punish table
    punish_table_start = string.find(more_info, punish_table_starter)
    more_info = more_info[punish_table_start+len(punish_table_starter):]
    punish_table_end = string.find(more_info, "</table>")
    more_info = more_info[:punish_table_end]
    #print more_info

    # find all the element
    break_type = ""
    punish_content = ""
    doc_link = ""
    register_id = ""
    elements = string.split(more_info, "</tr>")
    for element in elements:
        key = scoope(element, "<th colspan=\"3\">", "</th>")
        value = scoope(element, "<td>", "</td>")
        # we only pick the following two
        if key.encode('utf8') == "违法行为类型":
            break_type = value
            #print break_type
        elif key.encode('utf-8') == "注册号":
            register_id = value
            #print punish_content
        elif key.encode('utf-8') == "行政处罚内容":
            punish_content = value
            #print punish_content
        elif key.encode('utf-8') == "行政处罚决定书":
            #print value
            doc_link = scoope(value, "<a href=\"http://", "\"")
            #print doc_link 

    # download
    download_doc(register_id+'.doc', doc_link)

    return [name, date, register_id, break_type, punish_content, doc_link, link]


def parseHtml(html):
    # first find the table
    table_start_pos = string.find(html, table_starter)
    html = html[table_start_pos:]
    table_end_pos = string.find(html, table_end)
    html = html[:table_end_pos]
    # split table by "</tr>"
    tokens = string.split(html, delimiter)
    # token first and last is not usable
    tokens.remove(tokens[0])
    # no result
    if (len(tokens) == 0) :
        return list()

    print tokens[len(tokens)-1]
    tokens.remove(tokens[len(tokens)-1])

    # fetch all the info
    cases = list()
    for token in tokens:
        cases.append(pickInfoFromToken(token))

    return cases

def replaceNewline(content):
    content = " ".join(string.split(content,'\n'))
    return content 

def searchMain(argv):
    if len(argv) != 3 :
        print "Usage: search.py <start-time> <end-time> <keywords>"
        print "    e.g. search.py 2015-10-01 2015-11-26 good"
        print len(argv)
        for arg in argv:
                print arg
        exit(0)
    args = argv

    #if len(argv) != 1:
    #    print "Usage: search.py <arg-file>"
    #    exit(0)

    #with open(argv[0], "r") as input_file:
    #    line = input_file.readline()

    #args = string.split(line, "|-|");

    startDate = args[0]
    endDate = args[1]
    keyword = args[2]
    print startDate
    print endDate
    print keyword

    countpage = 0    
    case_list = []

    datelist = mydate.query_dates(startDate, endDate)
    pagenumber = 1

    for datepair in datelist: 
        totalpage = 1
        begindate = datepair[0]
        finishdate = datepair[1]
        print "-- query from " + begindate + " to " +finishdate

        while True:
            content = query_first(begindate, finishdate, keyword, pagenumber)
            if pagenumber == 1:
                totalpage = total_page(content)
            case_list = case_list + parseHtml(content) # merge two list

            countpage += 1
            pagenumber = pagenumber + 1
            if (pagenumber > totalpage):
                break

        # orgnize the cases
        #lines = list()
        #for case in case_list:
        #    #map(replaceNewline, case)
        #    line = '","'.join(case)
        #    line = '"%s"' % line
        #    lines.append(line)

    # write as csv
    with open('doc.csv', 'wb') as output_file:
        csv_out = csv.writer(output_file)
        for case in case_list:
            csv_out.writerow(case)

    global countentry
    return "DONE. Fetching " + str(countentry) + " entries from " + str(countpage) + " pages"

if __name__ == "__main__":
         searchMain(sys.argv[1:])
