# A Common Core State Standards (CCSS) Parser
*Copyright (C) 2013 Quentin Donnellan*
*http://qdonnellan.appspot.com*

## What is this?
This is a python parser for the Common Core State Standards (CCSS). It's function is quite simple: Read the XML data from the CCSS websites, then turn it into useful json which can be iterated by your webapp. Feel free to download remix, etc. as I've attached an MIT license to this thing.

## How to use?

### First: fetch.py
Run fetch.py. This will scrape the XML from the two CCSS trees (Math and ELA-Literacy) located at: http://www.corestandards.org/ELA-Literacy.xml, and http://www.corestandards.org/Math.xml

fetch.py will then populate an unstructured json file named **data.json**

### Second: create.py
Run create.py. This will scrape the **data.json** file and create a structured json file, with a hierarchy similar to the proposed hierarchy published by CCSS (with some changes to make it user-friendly, because it is a little ridiculous)

### Third: You're done!
Now you have a human-readable json file with all of the core standards, go you! Please note that because the CCSS people thought it was a good idea to include html in these standards (my thought: WHY WHY WHY????) you will notice some html in your standards like italic and supescrips. Don't blame me.

Also, since the CCSS is riddled with Windows-1252 encoded unicode characters (which are not mapped in ascii) I've had to scrape them and replace with usable substitutes. It should be easy to figure out where I've changed those things in my code. 

That's it, have fun!

### Not allergic to bitcoin
Whiskey donation fund: 1MraDxM8gywuiQeTNdMaLB7U4xhpUQ9YeJ