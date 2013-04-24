# create.py
# create a usable json file containing the Common Core State Standards
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

import json
import re

def format(content):
  content = re.sub(u'\u2013', '-', content)
  content = re.sub(u'\u2192', '->', content)
  content = re.sub(u'\u201c', '&ldquo;', content)
  content = re.sub(u'\u201d', '&rdquo;', content)
  content = re.sub(u'\u2605', '', content)
  content = re.sub(u'\u00e9', '', content)
  content = re.sub(u'\u2605', '', content)               
  content = re.sub('\n', '', content)
  return content

with open('data.json', 'rb') as f:
  data = json.load(f)
f.closed

core_json = {}

for item in data:
  if item not in [None, 'null']:
    
    
    bundle = item.split('.')
    
    if len(bundle) == 5:
      top, tree, strand, grade, standard = item.split('.')
    elif len(bundle) == 4:
      top, tree, strand, grade = item.split('.')
      if 'Math' in tree and 'Practice' in strand:
        standard = re.sub('MP', '', grade)
        grade = 'Practice'
        prefix = 'MP'
      else:
        standard = 0
    elif len(bundle) == 7:
      top, tree, uselss_stuff, grade, strand, prefix, standard = item.split('.')
    elif len(bundle) == 6:
      top, tree, uselss_stuff, strand, prefix, standard = item.split('.')
      if uselss_stuff == 'Content' and '-' in strand:
        grade,strand = strand.split('-')


    #If the tree doesn't already exist, add it
    if tree not in core_json:
      core_json[tree] = {}
    json_tree = core_json[tree]

    if 'Math' in tree:
      if grade not in json_tree:
        json_tree[grade] = {}
        core_json[tree] = json_tree
      json_grade = json_tree[grade]

      if strand not in json_grade:
        json_grade[strand] = {}
        json_tree[grade] = json_grade
        core_json[tree] = json_tree
      json_strand = json_grade[strand] 

      if prefix not in json_strand:
        json_strand[prefix] = {}
        json_grade[strand] = json_strand
        json_tree[grade] = json_grade
        core_json[tree] = json_tree
      json_prefix = json_strand[prefix]

      if standard not in json_prefix:
        contents = data[item]
        formatted_content = ''      
        for content in contents:
          formatted_content += format(content)
        json_prefix[standard] = formatted_content
        json_strand[prefix] = json_prefix
        json_grade[strand] = json_strand
        json_tree[grade] = json_grade
        core_json[tree] = json_tree

    elif 'ELA' in tree:
      if strand not in json_tree:
        json_tree[strand] = {}
        core_json[tree] = json_tree
      json_strand = json_tree[strand]

      if grade not in json_strand:
        json_strand[grade] = {}
        json_tree[strand] = json_strand
        core_json[tree] = json_tree
      json_grade = json_strand[grade]

      if standard not in json_grade:
        contents = data[item]
        formatted_content = ''      
        for content in contents:        
          formatted_content += format(content)
        json_grade[standard] = formatted_content
        json_strand[grade] = json_grade
        json_tree[strand] = json_strand
        core_json[tree] = json_tree


#Dump out structured dictionary into a somewhat human-readable json file
with open('usable_data.json', 'wb') as ff:
  json.dump(core_json, ff,sort_keys=True, indent=2)
ff.closed

