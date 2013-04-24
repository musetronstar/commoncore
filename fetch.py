# fetch.py
# scrape the Common Core State Standards XML
#
# MIT License:
# Copyright (C) 2013 Quentin Donnellan
# http://qdonnellan.appspot.com
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib2
import xml.etree.ElementTree as ET
import re
import json

data = {}

urls = ['http://www.corestandards.org/ELA-Literacy.xml', 'http://www.corestandards.org/Math.xml']

for url in urls:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    raw_xml = response.read() 

    #This very stupid character &#8217 (which seems to be a relic from MS-Word) gets unescaped then crashes everything
    #Let's just replace it before anything bad happens...
    raw_xml = re.sub('&#8217;', "'", raw_xml)

    #Create an ElementTree from the raw XML data provided at the urls above
    tree = ET.fromstring(raw_xml)

    #The first child levels of the common core xml are the individual learning standards
    for standard in tree:
      standard_statements = []      
      for codes in standard.findall('StatementCodes'):
        for code in codes:
          #The standard code is a decimal-delimited string such as CCSS.Math.Content.HS-RRA.A.1 or something 
          standard_code = code.text

      for statements in standard.findall('Statements'):        
        for statement in statements:
          #The statement is the actual sentence containing the core standard, i.e. "The student should know what a number is"
          standard_statements.append(statement.text)

      if standard_code not in data:
        #Let's attach the statement code to the statement text so that we'll have something to parse later
        data[standard_code] = standard_statements

#Dump out dictionary into a json file - this json is unstructured, non-hierarchical, unordered, and potentially contains redundant information
#use create.py to parse this json and make a human-readable json file
with open('data.json', 'wb') as f:
  json.dump(data, f)
f.closed