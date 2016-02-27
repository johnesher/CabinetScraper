Cabinet
=======
Cabinet is a demonstration application to scrape certain required information from Sainsbury's Ripe Fruits web page and return a JSON array containing the information.

Why the name Cabinet? - One of my hobbies is woodwork and one of the specialist tools that I use is a cabinet scraper and so I named this application Cabinet as a reminder of happy days spent working with fine tools sucn as Python.

The objective of this application is to demonstrate solid coding practices suitable for a much more complex application. 

Requirements
------------
This is a Python 2.7 application and depends on the Python packages requests, beautifulsoup4 and json. If these Python packages are not installed on your system you can install them with the following commands.
```
pip install beautifulsoup4
pip install requests
```

Installation
------------
Copy the files cabinet.py and test_cabinet.py to a directory on your PC (Windows or Linux). There is no need to run setup.

Testing
-------
To run the test suite, open a command prompt, change to the Cabinet directory and at the command prompt type 
`python test_cabinet.py`

Running the Application
-----------------------
To run Cabinet, open a command prompt, change to the Cabinet directory and at the command prompt type 
`python cabinet.py <url>`
where `<url>` is the url of the web page to scrape.

The results are printed to stdout so you can redirect the output to a file if you want to keep them or pipe them through other commands for further processing.

Note that this application assumes that the user is an IT professional and so any problems are reported in technical language so that the problem can be understood and resolved.

Limitations
-----------
Cabinet is designed to match the format of a particular web site and will not work on sites which use a different html structure. To work with a different web page you will have to modify this application to match the format of the page.

Design
------
This section is intended for developers who wish to extend or modify Cabinet.

Cabinet uses the requests package to fetch the contents of a url and beautifulSoup4 to parse the html. The requests package is simpler to use than the standard urllib package. BeautifulSoup was chosen as it is easy to install and use (lxml is faster but harder to install and the speed difference would be negligible on the target pages).

The application consists of functions rather than a class aas there is no persistent data to share between methods. The style adopted is almost functional, but a simple loop is used to build the results list by appending to it (rather than a more complex copy&append functional approach).

The title, url to linked html and unit_price information is contained within a `<div class='productInner'>` tag which is itself contained within multiple enclosing tags. Cabinet navigates to the class=productInner tag without reference to the containing hierachy. This was a deliberate design decision as it means that Cabinet will work if the outer tags are changed, although it carries a risk of cabinet finding the wrong information if productInner tags are ever used to contain other information on the page.

Within the productInner tag the `<div class="productInfo">` tag contains the title and href to the linked html in an `<a>` tag. These are easy to extract with beautifulSoup methods.

The unit_price is a little more awkward to reach with beautifultsoup methods as the `<p class="pricePerUnit">` tag containing it contains other `<abbr>` tags so a helper function is used to extract the price as a float.

A helper function parses the description from the linked html page. The description is within a class=productText tag, a sibling of a class=productDataItemHeader tag. 

Error messages are sent to stderr as it is likely the output from the appplication will be redirected to a file. 

The application was created using TDD methodology - the tests were written first and then the code second. I recommend this approach is used for any modifications.

Where possible the tests use local data, but some of them rely on the Sainsbury's test site.

John, Feb2016