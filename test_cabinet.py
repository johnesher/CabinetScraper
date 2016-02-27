# -*- coding: utf-8 -*-
"""
This module tests the cabinet.py module.
To run the tests type
python test_cabinet.py
at the command line.
"""
import unittest
import types

import requests
import json
import bs4

import cabinet

testUrl='http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html'

testLinkedUl='http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-avocado--ripe---ready-x2.html'

class TestCabinet(unittest.TestCase):

    def test_extract_price_returns_float(self):
        res = cabinet.extract_price(PRICE_NUMBERS_DATA[0][0])
        self.assertIsInstance(res,types.FloatType)

    def test_extract_price_handles_different_contents(self):
        for tc in PRICE_CONTENTS_DATA :
            res = cabinet.extract_price(tc)
            self.assertEqual(res,3.5, msg='Failed with %s' % tc)

    def test_extract_price_handles_different_numbers(self):
        for tc in PRICE_NUMBERS_DATA :
            res = cabinet.extract_price(tc[0])
            self.assertEqual(res,tc[1],msg='Failed with %s' % tc[0])

    def test_get_web_page_succeeds(self):
        res = cabinet.get_web_page(u'http://www.python.org/')
        self.assertEqual(res.status_code,200)

    @unittest.skip('Test fails as TalkTalk returns a valid page')
    def test_get_web_page_raises_fail(self):
        res = cabinet.get_web_page(u'HTTP://www.doesnotexist12789.org/')
        self.assertRaises(requests.exceptions.RequestException)
        self.assertNotEqual(res.status_code,200)

    def test_get_outer_tags_finds_all_matching_tags(self):
        counter = 0
        for tag in cabinet.get_outer_tags(TESTHTML) :
            self.assertEqual(tag[u'class'][0],u'productInner')
            counter += 1
        self.assertEqual(counter,7)

    def test_extract_description_finds_text(self):
        soup = bs4.BeautifulSoup(TEST_DESCRIPTION_HTML,'html5lib')
        res = cabinet.extract_description(soup)
        self.assertEqual(res,u'Avocados')

    def test_scrape_page(self):
        res = cabinet.scrape_page(TESTHTML)
        self.assertEqual( len(res),7 )
        for p in ['title', 'size', 'unit_price', 'description']:
            self.assertIn(p, res[0])

    def test_scrape_gives_help_message(self) :
        res = cabinet.scrape(['cabinet.py'])
        self.assertTrue( 'command' in res )

    def test_scrape_scrapes_url(self) :
        res = cabinet.scrape(['cabinet.py',testUrl])
        loaded = json.loads(res)
        self.assertIn('total', loaded)
        self.assertIn('title', loaded['results'][0])
        self.assertEqual( len(loaded['results']),7)


PRICE_CONTENTS_DATA = [ 
u'''<p class="pricePerUnit">£3.50</p>''',
u'''                <p class="pricePerUnit">
                 £3.50
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>

''',
u'''                <p class="pricePerUnit">
                 £3.50
                 <abbr title="per">
                  /
                 </abbr>
                </p>

''',
u'''                <p class="pricePerUnit">
                 $3.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>

''',
]

PRICE_NUMBERS_DATA = [ 
(u'''                <p class="pricePerUnit">
                 £3.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>

''',3.50),
(u'''                <p class="pricePerUnit">
                 £93.
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>

''',93.0),
(u'''                <p class="pricePerUnit">
                 £11.2
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>

''',11.2),
(u'''                <p class="pricePerUnit">
                 £56
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>

''',56.0),

]

TESTHTML='''<!DOCTYPE html>
<html class="noJs" lang="en" xml:lang="en" xmlns:wairole="http://www.w3.org/2005/01/wai-rdf/GUIRoleTaxonomy#" xmlns:waistate="http://www.w3.org/2005/07/aaa">
 <!-- BEGIN CategoriesDisplay.jsp -->
 <head>
  <title>
   Ripe &amp; ready | Sainsbury's
  </title>
  <meta content="Buy Ripe &amp; ready online from Sainsbury's, the same great quality, freshness and choice you'd find in store. Choose from 1 hour delivery slots and collect Nectar points." name="description"/>
  <meta content="" name="keyword"/>
  <link href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ripe---ready" rel="canonical"/>
  <meta content="NOINDEX, FOLLOW" name="ROBOTS"/>
  <!-- BEGIN CommonCSSToInclude.jspf -->
  <!--[if IE 8]>
    <link type="text/css" href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/css/main-ie8.min.css" rel="stylesheet" media="all" />
	<![endif]-->
  <!--[if !IE 8]><!-->
  <link href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/css/main.min.css" media="all" rel="stylesheet" type="text/css"/>
  <!--<![endif]-->
  <link href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/groceries/css/espot.css" media="all" rel="stylesheet" type="text/css"/>
  <link href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/css/print.css" media="print" rel="stylesheet" type="text/css"/>
  <!-- END CommonCSSToInclude.jspf -->
  <!-- BEGIN CommonJSToInclude.jspf -->
  <meta content="storeId_10151" name="CommerceSearch"/>
  <script type="text/javascript">
   var _deliverySlotInfo = {                          
            expiryDateTime: '',
            currentDateTime: 'November 25,2015 16:53:57',
            ajaxCountDownUrl: 'CountdownDisplayView?langId=44&storeId=10151',
            ajaxExpiredUrl: 'DeliverySlotExpiredDisplayView?langId=44&storeId=10151&currentPageUrl=http%3a%2f%2fwww.sainsburys.co.uk%2fwebapp%2fwcs%2fstores%2fservlet%2fCategoryDisplay%3fmsg%3d%26categoryId%3d185749%26langId%3d44%26storeId%3d10151%26krypto%3ddwlvaeB6%252FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%250A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%252F%252BHeNnUqybiZXu%252FL47P9A658zhrWd08mA5Y%250Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%252BardwWtMA49XQA4Iqwf%252BSvFr8RJOHK%250Afp2%252Fk0F6LH6%252Fmq5%252FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%252FydqEDvTdI5qgO6sKl0Q%253D&AJAXCall=true'
        }
    var _amendOrderSlotInfo = {                          
            expiryDateTime: '',
            currentDateTime: 'November 25,2015 16:53:57',
            ajaxAmendOrderExpiryUrl: 'AjaxOrderAmendSlotExpiryView?langId=44&storeId=10151&currentPageUrl=http%3a%2f%2fwww.sainsburys.co.uk%2fwebapp%2fwcs%2fstores%2fservlet%2fCategoryDisplay%3fmsg%3d%26categoryId%3d185749%26langId%3d44%26storeId%3d10151%26krypto%3ddwlvaeB6%252FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%250A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%252F%252BHeNnUqybiZXu%252FL47P9A658zhrWd08mA5Y%250Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%252BardwWtMA49XQA4Iqwf%252BSvFr8RJOHK%250Afp2%252Fk0F6LH6%252Fmq5%252FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%252FydqEDvTdI5qgO6sKl0Q%253D'
        }    
    var _commonPageInfo = {
        currentUrl: 'http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D',
        storeId: '10151',
        langId: '44'
    }
  </script>
  <script type="text/javascript">
   var _rhsCheckPostCodeRuleset = {                          
	          postCode: {
	                isEmpty: {
	                      param: true,
	                      text: 'Sorry, this postcode has not been recognised - Please try again.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                },
	                minLength: {
	                      param: 5,
	                      text: 'Sorry, this entry must be at least 5 characters long.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                },
	                maxLength: {
	                      param: 8,
	                      text: 'Sorry, this postcode has not been recognised - Please try again.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                },
	                isPostcode: {
	                      param: true,
	                      text: 'Sorry, this postcode has not been recognised - Please try again.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                }
	          }
	    }
  </script>
  <script type="text/javascript">
   var _rhsLoginValidationRuleset = {
	        logonId: {
	            isEmpty: {
	                param: true,
	                text: 'Please enter your username in the space provided.',
	                msgPlacement: "fieldUsername",
	                elemToAddErrorClassTo: "fieldUsername"
	            },
	            notMatches: {
	                param: "#logonPassword",
	                text: 'Sorry, your details have not been recognised. Please try again.',
	                msgPlacement: "fieldUsername",
	                elemToAddErrorClassTo: "fieldUsername"
	            }
	        },
	        logonPassword: {
	            isEmpty: {
	                param: true,
	                text: 'Please enter your password in the space provided.',
	                msgPlacement: "fieldPassword",
	                elemToAddErrorClassTo: "fieldPassword"
	            },
	            minLength: {
	                param: 6,
	                text: 'Please enter your password in the space provided.',
	                msgPlacement: "fieldPassword",
	                elemToAddErrorClassTo: "fieldPassword"
	            }
	        }
	    }
  </script>
  <script type="text/javascript">
   var typeAheadTrigger = 2;
  </script>
  <!--<script type="text/javascript" data-dojo-config="isDebug: false, useCommentedJson: true,locale: 'en-gb', parseOnLoad: true, dojoBlankHtmlUrl:'/wcsstore/SainsburysStorefrontAssetStore/js/dojo.1.7.1/blank.html'" src="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/js/dojo.1.7.1/dojo/dojo.js"></script>-->
  <script src="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/js/sainsburys.js" type="text/javascript">
  </script>
  <script type="text/javascript">
   require(["dojo/parser", "dijit/layout/AccordionContainer", "dijit/layout/ContentPane", "dojox/widget/AutoRotator", "dojox/widget/rotator/Fade"]);
  </script>
  <script src="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/groceries/scripts/page/faq.js" type="text/javascript">
  </script>
  <style id="antiCJ">
   .js body{display:none !important;}
  </style>
  <script type="text/javascript">
   if (self === top) {var antiCJ = document.getElementById("antiCJ");antiCJ.parentNode.removeChild(antiCJ);} else {top.location = self.location;}
  </script>
  <!-- END CommonJSToInclude.jspf -->
 </head>
 <body class="shelfPage" id="shelfPage">
  <div id="page">
   <!-- BEGIN StoreCommonUtilities.jspf -->
   <!-- END StoreCommonUtilities.jspf -->
   <!-- Header Nav Start -->
   <!-- BEGIN LayoutContainerTop.jspf -->
   <!-- BEGIN HeaderDisplay.jspf -->
   <!-- BEGIN CachedHeaderDisplay.jsp -->
   <ul id="skipLinks">
    <li>
     <a href="#content">
      Skip to main content
     </a>
    </li>
    <li>
     <a href="#groceriesNav">
      Skip to groceries navigation menu
     </a>
    </li>
   </ul>
   <div id="globalHeaderContainer">
    <div class="header globalHeader" id="globalHeader">
     <div class="globalNav">
      <ul>
       <li>
        <a href="http://www.sainsburys.co.uk">
         <span class="moreSainsburysIcon">
         </span>
         Explore more at Sainsburys.co.uk
        </a>
       </li>
       <li>
        <a href="http://help.sainsburys.co.uk" rel="external">
         <span class="helpCenterIcon">
         </span>
         Help Centre
        </a>
       </li>
       <li>
        <a href="http://stores.sainsburys.co.uk">
         <span class="storeLocatorIcon">
         </span>
         Store Locator
        </a>
       </li>
       <li class="loginRegister">
        <a href="https://www.sainsburys.co.uk/sol/my_account/accounts_home.jsp">
         <span class="userIcon">
         </span>
         Log in / Register
        </a>
       </li>
      </ul>
     </div>
     <div class="globalHeaderLogoSearch">
      <!-- BEGIN LogoSearchNavBar.jspf -->
      <a class="mainLogo" href="http://www.sainsburys.co.uk/shop/gb/groceries">
       <img alt="Sainsbury's" src="http://www.sainsburys.co.uk/wcsstore/SainsburysStorefrontAssetStore/img/logo.png"/>
      </a>
      <div class="searchBox" role="search">
       <form action="SearchDisplay" id="globalSearchForm" method="get" name="sol_search">
        <input name="viewTaskName" type="hidden" value="CategoryDisplayView"/>
        <input name="recipesSearch" type="hidden" value="true"/>
        <input name="orderBy" type="hidden" value="RELEVANCE"/>
        <input name="skipToTrollyDisplay" type="hidden" value="false"/>
        <input name="favouritesSelection" type="hidden" value="0"/>
        <input name="level" type="hidden" value="2"/>
        <input name="langId" type="hidden" value="44"/>
        <input name="storeId" type="hidden" value="10151"/>
        <label class="access" for="search">
         Search for products
        </label>
        <input autocomplete="off" id="search" maxlength="150" name="searchTerm" placeholder="Search" type="search" value=""/>
        <button class="clearSearch hidden" id="clearSearch" type="button">
         Clear the search field
        </button>
        <input id="searchSubmit" name="searchSubmit" type="submit" value="Search"/>
       </form>
       <a class="findProduct" href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/ShoppingListDisplay?catalogId=10122&amp;action=ShoppingListDisplay&amp;urlLangId=&amp;langId=44&amp;storeId=10151">
        Search for multiple products
       </a>
       <!-- ul class="searchNav">
        <li class="shoppingListLink"><a href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/ShoppingListDisplay?catalogId=10122&action=ShoppingListDisplay&urlLangId=&langId=44&storeId=10151">Find a list of products</a></li>
        <li><a href="http://stores.sainsburys.co.uk">Store Locator</a></li>
        <li><a href="https://www.sainsburys.co.uk/sol/my_account/accounts_home.jsp">My Account</a></li>
        
                 <li><a href="https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/QuickRegistrationFormView?catalogId=10122&amp;langId=44&amp;storeId=10151" >Register</a></li>
        
    </ul-->
      </div>
      <!-- END LogoSearchNavBar.jspf -->
     </div>
     <div class="groceriesNav" id="groceriesNav">
      <ul class="mainNav">
       <li>
        <a class="active" href="http://www.sainsburys.co.uk/shop/gb/groceries">
         <strong>
          Groceries
         </strong>
        </a>
       </li>
       <li>
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/favourites">
         Favourites
        </a>
       </li>
       <li>
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/great-offers">
         Great Offers
        </a>
       </li>
       <li>
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/ideas-recipes">
         Ideas &amp; Recipes
        </a>
       </li>
       <li>
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/benefits">
         Benefits
        </a>
       </li>
      </ul>
      <hr/>
      <p class="access">
       Groceries Categories
      </p>
      <div class="subNav">
       <ul>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/Christmas">
          Christmas
         </a>
        </li>
        <li>
         <a class="active" href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg">
          <strong>
           Fruit &amp; veg
          </strong>
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/meat-fish">
          Meat &amp; fish
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/dairy-eggs-chilled">
          Dairy, eggs &amp; chilled
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/bakery">
          Bakery
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/frozen-">
          Frozen
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/food-cupboard">
          Food cupboard
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/drinks">
          Drinks
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/health-beauty">
          Health &amp; beauty
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/baby">
          Baby
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/household">
          Household
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/pet">
          Pet
         </a>
        </li>
        <li>
         <a href="http://www.sainsburys.co.uk/shop/gb/groceries/home-ents">
          Home
         </a>
        </li>
       </ul>
      </div>
     </div>
    </div>
   </div>
   <!-- Generated on: Wed Nov 25 16:53:57 GMT 2015  -->
   <!-- END CachedHeaderDisplay.jsp -->
   <!-- END HeaderDisplay.jspf -->
   <!-- END LayoutContainerTop.jspf -->
   <!-- Header Nav End -->
   <!-- Main Area Start -->
   <div id="main">
    <!-- Content Start -->
    <div class="article" id="content">
     <div class="nav breadcrumb" id="breadcrumbNav">
      <p class="access">
       You are here:
      </p>
      <ul>
       <li class="first">
        <span class="corner">
        </span>
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg">
         <span>
          Fruit &amp; veg
         </span>
        </a>
        <span class="arrow">
        </span>
        <div>
         <p>
          Select an option:
         </p>
         <ul>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/great-prices-on-fruit---veg">
            Great prices on fruit &amp; veg
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/flowers---seeds">
            Flowers &amp; plants
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/new-in-season">
            In season
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-fruit">
            Fresh fruit
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-vegetables">
            Fresh vegetables
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-salad">
            Fresh salad
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-herbs-ingredients">
            Fresh herbs &amp; ingredients
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/prepared-ready-to-eat">
            Prepared fruit, veg &amp; salad
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/organic">
            Organic
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/taste-the-difference-185761-44">
            Taste the Difference
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fruit-veg-fairtrade">
            Fairtrade
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/christmas-fruit---nut">
            Christmas fruit &amp; nut
           </a>
          </li>
         </ul>
        </div>
       </li>
       <li class="second">
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-fruit">
         <span>
          Fresh fruit
         </span>
        </a>
        <span class="arrow">
        </span>
        <div>
         <p>
          Select an option:
         </p>
         <ul>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/all-fruit">
            All fruit
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ripe---ready">
            Ripe &amp; ready
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/bananas-grapes">
            Bananas &amp; grapes
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/apples-pears-rhubarb">
            Apples, pears &amp; rhubarb
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/berries-cherries-currants">
            Berries, cherries &amp; currants
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/citrus-fruit">
            Citrus fruit
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/nectarines-plums-apricots-peaches">
            Nectarines, plums, apricots &amp; peaches
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/melon-pineapple-kiwi">
            Kiwi &amp; pineapple
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/melon---mango">
            Melon &amp; mango
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/mango-exotic-fruit-dates-nuts">
            Papaya, Pomegranate &amp; Exotic Fruit
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/dates--nuts---figs">
            Dates, Nuts &amp; Figs
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ready-to-eat">
            Ready to eat fruit
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/organic-fruit">
            Organic fruit
           </a>
          </li>
          <li>
           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-fruit-vegetables-special-offers">
            Special offers
           </a>
          </li>
         </ul>
        </div>
       </li>
       <li class="third">
        <a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ripe---ready">
         <span>
          Ripe &amp; ready
         </span>
        </a>
       </li>
      </ul>
     </div>
     <!-- BEGIN MessageDisplay.jspf -->
     <!-- END MessageDisplay.jspf -->
     <!-- BEGIN ShelfDisplay.jsp -->
     <div class="section">
      <h1 class="resultsHeading" id="resultsHeading">
       Ripe &amp; ready (7 products available)
      </h1>
      <!-- DEBUG: shelfTopLeftESpotName = Z:FRUIT_AND_VEG/D:FRESH_FRUIT/A:RIPE_AND_READY/Shelf_Top_Left -->
      <!-- DEBUG: shelfTopRightESpotName = Z:FRUIT_AND_VEG/D:FRESH_FRUIT/A:RIPE_AND_READY/Shelf_Top_Right -->
      <div class="eSpotContainer">
       <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_Z:FRUIT_AND_VEG/D:FRESH_FRUIT/A:RIPE_AND_READY/Shelf_Top_Left">
        Z:FRUIT_AND_VEG/D:FRESH_FRUIT/A:RIPE_AND_READY/Shelf_Top_Left
       </div>
       <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_Z:FRUIT_AND_VEG/D:FRESH_FRUIT/A:RIPE_AND_READY/Shelf_Top_Right">
        Z:FRUIT_AND_VEG/D:FRESH_FRUIT/A:RIPE_AND_READY/Shelf_Top_Right
       </div>
      </div>
     </div>
     <div class="section" id="filterContainer">
      <!-- FILTER SECTION STARTS HERE-->
      <!-- BEGIN BrowseFacetsDisplay.jspf-->
      <!-- Start Filter -->
      <h2 class="access">
       Product filter options
      </h2>
      <div class="filterSlither">
       <div class="filterCollapseBar">
        <div class="noFlexComponent">
         <a aria-controls="filterOptions" href="#filterOptions" id="showHideFilterSlither">
          Filter your list
         </a>
         <span aria-live="assertive" aria-relevant="text" class="quantitySelected" id="quantitySelected" role="status">
         </span>
         <a class="repressive" href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?pageSize=20&amp;catalogId=10122&amp;orderBy=FAVOURITES_FIRST&amp;facet=&amp;top_category=12518&amp;parent_category_rn=12518&amp;beginIndex=0&amp;categoryId=185749&amp;langId=44&amp;storeId=10151">
          Clear filters
         </a>
        </div>
       </div>
       <form action="" class="shelfFilterOptions " id="filterOptions" method="get" name="search_facets_form">
        <input name="langId" type="hidden" value="44"/>
        <input name="storeId" type="hidden" value="10151"/>
        <input name="catalogId" type="hidden" value="10122"/>
        <input name="categoryId" type="hidden" value="185749"/>
        <input name="parent_category_rn" type="hidden" value="12518"/>
        <input name="top_category" type="hidden" value="12518"/>
        <input name="pageSize" type="hidden" value="20"/>
        <input name="orderBy" type="hidden" value="FAVOURITES_FIRST"/>
        <input name="searchTerm" type="hidden" value=""/>
        <input name="beginIndex" type="hidden" value="0"/>
        <div class="wrapper" id="filterOptionsContainer">
         <div class="field options">
          <div class="indicator">
           <p>
            Options:
           </p>
          </div>
          <div class="checkboxes">
           <div class="input">
            <input aria-disabled="true" disabled="disabled" id="globalOptions0" name="facet" type="checkbox" value=""/>
            <label class="favouritesLabel" for="globalOptions0">
             Favourites
            </label>
           </div>
           <div class="input">
            <input id="globalOptions1" name="facet" type="checkbox" value="86"/>
            <label for="globalOptions1">
             New
            </label>
           </div>
           <div class="input">
            <input aria-disabled="true" disabled="disabled" id="globalOptions2" name="facet" type="checkbox" value=""/>
            <label class="offersLabel" for="globalOptions2">
             Offers
            </label>
           </div>
          </div>
         </div>
         <!-- BEGIN BrandFacetDisplay.jspf -->
         <div class="field topBrands">
          <div class="indicator">
           <p>
            Top Brands:
           </p>
          </div>
          <div class="checkboxes">
           <div class="input">
            <input id="topBrands0" name="facet" type="checkbox" value="887"/>
            <label for="topBrands0">
             Sainsbury's
            </label>
           </div>
          </div>
         </div>
         <!-- END BrandFacetDisplay.jspf -->
        </div>
        <!-- BEGIN DietaryFacetDisplay.jspf -->
        <div class="filterCollapseBarDietAndLifestyle">
         <a href="#dietAndLifestyle" id="showHideDietAndLifestyle">
          Dietary &amp; lifestyle options
         </a>
         <span class="misc">
          (such as vegetarian, organic and British)
         </span>
        </div>
        <div class="field dietAndLifestyle jsHide" id="dietAndLifestyle">
         <div class="checkboxes">
          <div class="input">
           <input id="dietAndLifestyle0" name="facet" type="checkbox" value="4294966755"/>
           <label for="dietAndLifestyle0">
            Keep Refrigerated
           </label>
          </div>
          <div class="input">
           <input id="dietAndLifestyle1" name="facet" type="checkbox" value="4294966711"/>
           <label for="dietAndLifestyle1">
            Organic
           </label>
          </div>
         </div>
        </div>
        <!-- END DietaryFacetDisplay.jspf -->
        <div class="filterActions">
         <input class="button primary" id="applyfilter" name="applyfilter" type="submit" value="Apply filter"/>
        </div>
       </form>
      </div>
      <!-- END BrowseFacetsDisplay.jspf-->
      <!-- FILTER SECTION ENDS HERE-->
     </div>
     <div class="section" id="productsContainer">
      <div class="areaOverlay" id="productsOverlay">
      </div>
      <div id="productLister">
       <h2 class="access">
        Product pagination
       </h2>
       <div class="pagination">
        <ul class="viewOptions">
         <li class="grid">
          <a href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?listView=false&amp;orderBy=FAVOURITES_FIRST&amp;parent_category_rn=12518&amp;top_category=12518&amp;langId=44&amp;beginIndex=0&amp;pageSize=30&amp;catalogId=10122&amp;searchTerm=&amp;categoryId=185749&amp;listId=&amp;storeId=10151&amp;promotionId=">
           <span class="access">
            Grid view
           </span>
          </a>
         </li>
         <li class="listSelected">
          <span class="access">
           List view
          </span>
         </li>
        </ul>
        <form action="CategoryDisplay" method="get" name="search_orderBy_form">
         <input name="langId" type="hidden" value="44"/>
         <input name="storeId" type="hidden" value="10151"/>
         <input name="catalogId" type="hidden" value="10122"/>
         <input name="categoryId" type="hidden" value="185749"/>
         <input name="pageSize" type="hidden" value="20"/>
         <input name="beginIndex" type="hidden" value="0"/>
         <input name="promotionId" type="hidden" value=""/>
         <input name="listId" type="hidden" value=""/>
         <input name="searchTerm" type="hidden" value=""/>
         <input name="hasPreviousOrder" type="hidden" value=""/>
         <input name="previousOrderId" type="hidden" value=""/>
         <input name="categoryFacetId1" type="hidden" value=""/>
         <input name="categoryFacetId2" type="hidden" value=""/>
         <input name="bundleId" type="hidden" value=""/>
         <div class="field">
          <div class="indicator">
           <label for="orderBy">
            Sort by:
           </label>
          </div>
          <input name="parent_category_rn" type="hidden" value="12518"/>
          <input name="top_category" type="hidden" value="12518"/>
          <div class="input">
           <div class="selectWrapper">
            <select id="orderBy" name="orderBy">
             <option selected="selected" value="FAVOURITES_FIRST">
              Favourites First
             </option>
             <option value="PRICE_ASC">
              Price - Low to High
             </option>
             <option value="PRICE_DESC">
              Price - High to Low
             </option>
             <option value="NAME_ASC">
              Product Name - A - Z
             </option>
             <option value="NAME_DESC">
              Product Name - Z - A
             </option>
             <option value="TOP_SELLERS">
              Top Sellers
             </option>
             <option value="RATINGS_DESC">
              Ratings - High to Low
             </option>
            </select>
            <span>
            </span>
           </div>
          </div>
         </div>
         <div class="actions">
          <input class="button" id="Sort" name="Sort" type="submit" value="Sort"/>
         </div>
        </form>
        <form action="CategoryDisplay" method="get" name="search_pageSize_form">
         <input name="langId" type="hidden" value="44"/>
         <input name="storeId" type="hidden" value="10151"/>
         <input name="catalogId" type="hidden" value="10122"/>
         <input name="categoryId" type="hidden" value="185749"/>
         <input name="orderBy" type="hidden" value="FAVOURITES_FIRST"/>
         <input name="beginIndex" type="hidden" value="0"/>
         <input name="promotionId" type="hidden" value=""/>
         <input name="listId" type="hidden" value=""/>
         <input name="searchTerm" type="hidden" value=""/>
         <input name="hasPreviousOrder" type="hidden" value=""/>
         <input name="previousOrderId" type="hidden" value=""/>
         <input name="categoryFacetId1" type="hidden" value=""/>
         <input name="categoryFacetId2" type="hidden" value=""/>
         <input name="bundleId" type="hidden" value=""/>
         <input name="parent_category_rn" type="hidden" value="12518"/>
         <input name="top_category" type="hidden" value="12518"/>
         <div class="field">
          <div class="indicator">
           <label for="pageSize">
            Per page
           </label>
          </div>
          <div class="input">
           <div class="selectWrapper">
            <select id="pageSize" name="pageSize">
             <option selected="selected" value="20">
              20
             </option>
             <option value="40">
              40
             </option>
             <option value="60">
              60
             </option>
             <option value="80">
              80
             </option>
             <option value="100">
              100
             </option>
            </select>
            <span>
            </span>
           </div>
          </div>
         </div>
         <div class="actions">
          <input class="button" id="Go" name="Go" type="submit" value="Go"/>
         </div>
        </form>
        <ul class="pages">
         <li class="previous">
          <span class="access">
           Go to previous page
          </span>
         </li>
         <li class="current">
          <span class="access">
           Current page
          </span>
          <span>
           1
          </span>
         </li>
         <li class="next">
          <span class="access">
           Go to next page
          </span>
         </li>
        </ul>
       </div>
       <h2 class="access">
        Products
       </h2>
       <ul class="productLister listView">
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error149117">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-apricot-ripe---ready-320g.html">
               Sainsbury's Apricot Ripe &amp; Ready x5
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/product_images/media_7572754_M.jpg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_149117">
               <div class="pricing">
                <p class="pricePerUnit">
                 £3.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £0.70
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_149117" method="post" name="OrderItemAddForm_149117">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="7572754"/>
                 <label class="access" for="quantity_149116">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_149116" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="149117"/>
                 <input name="productId" type="hidden" value="149116"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_149117" id="numberInTrolley_149117">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_149117">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error572163">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-avocado-xl-pinkerton-loose-300g.html">
               Sainsbury's Avocado Ripe &amp; Ready XL Loose 300g
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/51/0000000202251/0000000202251_M.jpeg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_572163">
               <div class="pricing">
                <p class="pricePerUnit">
                 £1.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £1.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_572163" method="post" name="OrderItemAddForm_572163">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="7678882"/>
                 <label class="access" for="quantity_572162">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_572162" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="572163"/>
                 <input name="productId" type="hidden" value="572162"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_572163" id="numberInTrolley_572163">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_572163">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <div class="coverage ranged">
         </div>
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error138041">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-avocado--ripe---ready-x2.html">
               Sainsbury's Avocado, Ripe &amp; Ready x2
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/22/0000001600322/0000001600322_M.jpeg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_138041">
               <div class="pricing">
                <p class="pricePerUnit">
                 £1.80
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £1.80
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_138041" method="post" name="OrderItemAddForm_138041">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="6834746"/>
                 <label class="access" for="quantity_138040">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_138040" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="138041"/>
                 <input name="productId" type="hidden" value="138040"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_138041" id="numberInTrolley_138041">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_138041">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error809817">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-avocados--ripe---ready-x4.html">
               Sainsbury's Avocados, Ripe &amp; Ready x4
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/15/0000000184915/0000000184915_M.jpeg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_809817">
               <div class="pricing">
                <p class="pricePerUnit">
                 £3.20
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £3.20
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_809817" method="post" name="OrderItemAddForm_809817">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="7718228"/>
                 <label class="access" for="quantity_809816">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_809816" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="809817"/>
                 <input name="productId" type="hidden" value="809816"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_809817" id="numberInTrolley_809817">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_809817">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error136679">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-conference-pears--ripe---ready-x4-%28minimum%29.html">
               Sainsbury's Conference Pears, Ripe &amp; Ready x4 (minimum)
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/08/0000001514308/0000001514308_M.jpeg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_136679">
               <div class="pricing">
                <p class="pricePerUnit">
                 £1.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £1.50
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_136679" method="post" name="OrderItemAddForm_136679">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="6621757"/>
                 <label class="access" for="quantity_136678">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_136678" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="136679"/>
                 <input name="productId" type="hidden" value="136678"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_136679" id="numberInTrolley_136679">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_136679">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error642875">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-golden-kiwi--taste-the-difference-x4-685641-p-44.html">
               Sainsbury's Golden Kiwi x4
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/41/0000000685641/0000000685641_M.jpeg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_642875">
               <div class="pricing">
                <p class="pricePerUnit">
                 £1.80
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £0.45
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_642875" method="post" name="OrderItemAddForm_642875">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="685641"/>
                 <label class="access" for="quantity_642874">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_642874" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="642875"/>
                 <input name="productId" type="hidden" value="642874"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_642875" id="numberInTrolley_642875">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_642875">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
        <li>
         <!-- BEGIN CatalogEntryThumbnailDisplay.jsp -->
         <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
         <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
         <!-- END MerchandisingAssociationsDisplay.jsp -->
         <div class="errorBanner hidden" id="error130231">
         </div>
         <div class="product ">
          <div class="productInner">
           <div class="productInfoWrapper">
            <div class="productInfo">
             <h3>
              <a href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/sainsburys-kiwi-fruit--ripe---ready-x4.html">
               Sainsbury's Kiwi Fruit, Ripe &amp; Ready x4
               <img alt="" src="http://c2.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/product_images/media_1116748_M.jpg"/>
              </a>
             </h3>
             <div class="ThumbnailRoundel">
              <!--ThumbnailRoundel -->
             </div>
             <div class="promoBages">
              <!-- PROMOTION -->
             </div>
             <!-- Review -->
             <!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf -->
             <!-- productAllowedRatingsAndReviews: false -->
             <!-- END CatalogEntryRatingsReviewsInfo.jspf -->
            </div>
           </div>
           <div class="addToTrolleytabBox">
            <!-- addToTrolleytabBox LIST VIEW-->
            <!-- Start UserSubscribedOrNot.jspf -->
            <!-- Start UserSubscribedOrNot.jsp -->
            <!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
            <div class="addToTrolleytabContainer addItemBorderTop">
             <!-- End AddToSubscriptionList.jsp -->
             <!-- End AddSubscriptionList.jspf -->
             <!-- 
	                        ATTENTION!!!
	                        <div class="addToTrolleytabContainer">
	                        This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
	                        -->
             <div class="pricingAndTrolleyOptions">
              <div class="priceTab activeContainer priceTabContainer" id="addItem_130231">
               <div class="pricing">
                <p class="pricePerUnit">
                 £1.80
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="unit">
                  <span class="pricePerUnitUnit">
                   unit
                  </span>
                 </abbr>
                </p>
                <p class="pricePerMeasure">
                 £0.45
                 <abbr title="per">
                  /
                 </abbr>
                 <abbr title="each">
                  <span class="pricePerMeasureMeasure">
                   ea
                  </span>
                 </abbr>
                </p>
               </div>
               <div class="addToTrolleyForm ">
                <form action="OrderItemAdd" class="addToTrolleyForm" id="OrderItemAddForm_130231" method="post" name="OrderItemAddForm_130231">
                 <input name="storeId" type="hidden" value="10151"/>
                 <input name="langId" type="hidden" value="44"/>
                 <input name="catalogId" type="hidden" value="10122"/>
                 <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
                 <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
                 <input name="SKU_ID" type="hidden" value="1116748"/>
                 <label class="access" for="quantity_130230">
                  Quantity
                 </label>
                 <input class="quantity" id="quantity_130230" name="quantity" size="3" type="text" value="1"/>
                 <input name="catEntryId" type="hidden" value="130231"/>
                 <input name="productId" type="hidden" value="130230"/>
                 <input name="page" type="hidden" value=""/>
                 <input name="contractId" type="hidden" value=""/>
                 <input name="calculateOrder" type="hidden" value="1"/>
                 <input name="calculationUsage" type="hidden" value="-1,-2,-3"/>
                 <input name="updateable" type="hidden" value="1"/>
                 <input name="merge" type="hidden" value="***"/>
                 <input name="callAjax" type="hidden" value="false"/>
                 <input class="button process" name="Add" type="submit" value="Add"/>
                </form>
                <div class="numberInTrolley hidden numberInTrolley_130231" id="numberInTrolley_130231">
                </div>
               </div>
              </div>
              <!-- END priceTabContainer Add container -->
              <!-- Subscribe container -->
              <!-- Start AddToSubscriptionList.jspf -->
              <!-- Start AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jsp -->
              <!-- End AddToSubscriptionList.jspf -->
             </div>
            </div>
           </div>
          </div>
         </div>
         <div class="additionalItems" id="additionalItems_130231">
          <!-- BEGIN MerchandisingAssociationsDisplay.jsp -->
          <!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
          <!-- END MerchandisingAssociationsDisplay.jsp -->
         </div>
         <!-- END CatalogEntryThumbnailDisplay.jsp -->
        </li>
       </ul>
       <h2 class="access">
        Product pagination
       </h2>
       <div class="pagination paginationBottom">
        <ul class="pages">
         <li class="previous">
          <span class="access">
           Go to previous page
          </span>
         </li>
         <li class="current">
          <span class="access">
           Current page
          </span>
          <span>
           1
          </span>
         </li>
         <li class="next">
          <span class="access">
           Go to next page
          </span>
         </li>
        </ul>
       </div>
      </div>
     </div>
     <!-- END ShelfDisplay.jsp -->
     <!-- ********************* ZDAS ESpot Display Start ********************** -->
     <div class="section eSpotContainer bottomESpots">
      <!-- Left POD ESpot Name = Z:FRUIT_AND_VEG/Espot_Left -->
      <!-- START ZDASPODDisplay.jsp -->
      <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_Z:FRUIT_AND_VEG/Espot_Left">
       Z:FRUIT_AND_VEG/Espot_Left
      </div>
      <div class="es es-border-box" style="width: 100%; height: 150px; padding-bottom: 15px; ">
       <div class="es-border-box-100 es-transparent-bg" dojotype="dojox.widget.AutoRotator" duration="" id="myAutoRotator1445437214786" suspendonhover="true" transition="dojox.widget.rotator.crossFade">
        <div class="es-border-box-100">
         <div class="es-border-box-100">
          <a href="/shop/gb/groceries/find-recipes/recipes/chicken-poultry-and-game/chicken--pea-and-leek-pie">
           <img alt="Recipe with all ingredients available to add to basket" src="http://www.sainsburys.co.uk/wcassets/2015_2016/cycle_13_18_nov/produce_recipe_leek_pie_847x135.jpg"/>
          </a>
         </div>
         <div class="es-border-box es-white-bg" style="width: 168px; height: 155px; position: absolute; left: 0px; top: 0px; opacity: 1; -ms-filter: progid:DXImageTransform.Microsoft.Alpha(100); filter: alpha(opacity=100);">
         </div>
         <div class="es-border-box" style="width: 168px; height: 155px; position: absolute; left: 0px; top: 0px; padding-left: 15px; padding-top: 10px; padding-right: 15px; padding-bottom: 15px; ">
          <div class="es-border-box" style="width: 100%; padding-top: px; ">
           <h3>
            Chicken, pea and leek pie
           </h3>
          </div>
          <div class="es-border-box" style="width: 100%; padding-top: px; ">
           <p>
            Fluffy potato tops a creamy chicken and veg filling
           </p>
          </div>
         </div>
        </div>
       </div>
      </div>
      <!-- end of if empty marketingSpotDatas loop-->
      <!-- END ZDASPODDisplay.jsp -->
      <!--  Middle POD Espot Name = Z_Default_Espot_Content -->
      <!-- START ZDASPODDisplay.jsp -->
      <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_Z_Default_Espot_Content">
       Z_Default_Espot_Content
      </div>
      <!-- end of if empty marketingSpotDatas loop-->
      <!-- END ZDASPODDisplay.jsp -->
      <!--  Right POD Espot Name = Z_Default_Espot_Content-->
      <!-- START ZDASPODDisplay.jsp -->
      <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_Z_Default_Espot_Content">
       Z_Default_Espot_Content
      </div>
      <!-- end of if empty marketingSpotDatas loop-->
      <!-- END ZDASPODDisplay.jsp -->
     </div>
     <!-- ********************* ZDAS ESpot Display End ********************** -->
    </div>
    <!-- content End -->
    <!-- auxiliary Start -->
    <div class="aside" id="auxiliary">
     <!-- BEGIN RightHandSide.jspf -->
     <div id="auxiliaryDock">
      <!-- BEGIN RightHandSide.jsp -->
      <div class="panel loginPanel">
       <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_NZ_Welcome_Back_RHS_Espot">
        NZ_Welcome_Back_RHS_Espot
       </div>
       <h2>
        Already a customer?
       </h2>
       <form action="LogonView" id="Rhs_signIn" method="post" name="signIn">
        <input name="storeId" type="hidden" value="10151"/>
        <input name="langId" type="hidden" value="44"/>
        <input name="catalogId" type="hidden" value="10122"/>
        <input name="URL" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
        <input name="logonCallerId" type="hidden" value="LogonButton"/>
        <input name="errorViewName" type="hidden" value="CategoryDisplayView"/>
        <input class="button process" type="submit" value="Log in"/>
       </form>
       <div class="panelFooter">
        <p class="register">
         Not yet registered?
         <a class="callToAction" href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/PostcodeCheckView?catalogId=10122&amp;currentPageUrl=http%3A%2F%2Fwww.sainsburys.co.uk%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2FCategoryDisplay%3Fmsg%3D%26categoryId%3D185749%26langId%3D44%26storeId%3D10151%26krypto%3DdwlvaeB6%252FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%250A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%252F%252BHeNnUqybiZXu%252FL47P9A658zhrWd08mA5Y%250Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%252BardwWtMA49XQA4Iqwf%252BSvFr8RJOHK%250Afp2%252Fk0F6LH6%252Fmq5%252FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%252FydqEDvTdI5qgO6sKl0Q%253D&amp;langId=44&amp;storeId=10151" name="register">
          Register Now
         </a>
        </p>
       </div>
      </div>
      <div class="panel imagePanel checkPostCodePanel" id="checkPostCodePanel">
       <div class="siteCatalystTag" id="sitecatalyst_ESPOT_NAME_NZ_Do_We_Deliver_To_You_Espot">
        NZ_Do_We_Deliver_To_You_Espot
       </div>
       <h2>
        New customer?
       </h2>
       <p>
        Enter your postcode to check we deliver in your area.
       </p>
       <div class="errorMessage" id="PostCodeMessageArea" style="display:none;">
       </div>
       <form action="/webapp/wcs/stores/servlet/CheckPostCode" id="Rhs_checkPostCode" method="post" name="CheckPostCode">
        <input name="langId" type="hidden" value="44"/>
        <input name="storeId" type="hidden" value="10151"/>
        <input name="currentPageUrl" type="hidden" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?msg=&amp;categoryId=185749&amp;langId=44&amp;storeId=10151&amp;krypto=dwlvaeB6%2FxULwIdnZBpXIWTi8eDrMLVBDvxz1SYU6pQ4HZ0p1fQ4WzDDbX58qo25joVKwiFFlmQW%0A0wrexmT0zSs9NxHPxri6CctBDvXHKi15cZntIRJRW%2F%2BHeNnUqybiZXu%2FL47P9A658zhrWd08mA5Y%0Azhm9vwQK7oLCWKF5VeQF9UiLmiVnffGVqRM76kUBxmRLDA%2BardwWtMA49XQA4Iqwf%2BSvFr8RJOHK%0Afp2%2Fk0F6LH6%2Fmq5%2FM97LMdaXyk0YneYUccDUWQUNnbztUkimdSo%2FydqEDvTdI5qgO6sKl0Q%3D"/>
        <input name="currentViewName" type="hidden" value="CategoryDisplayView"/>
        <input name="messageAreaId" type="hidden" value="PostCodeMessageArea"/>
        <div class="field">
         <div class="indicator">
          <label class="access" for="postCode">
           Postcode
          </label>
         </div>
         <div class="input">
          <input id="postCode" maxlength="8" name="postCode" type="text" value=""/>
         </div>
        </div>
        <div class="actions">
         <input class="button primary process" type="submit" value="Check postcode"/>
        </div>
       </form>
      </div>
      <!-- END RightHandSide.jsp -->
      <!-- BEGIN MiniShopCartDisplay.jsp -->
      <!-- If we get here from a generic error this service will fail so we need to catch the exception -->
      <div class="panel infoPanel">
       <span class="icon infoIcon">
       </span>
       <h2>
        Important Information
       </h2>
       <p>
        Alcohol promotions available to online customers serviced from our Scottish stores may differ from those shown when browsing our site. Please log in to see the full range of promotions available to you.
       </p>
      </div>
      <!-- END MiniShopCartDisplay.jsp -->
     </div>
     <!-- END RightHandSide.jspf -->
    </div>
    <!-- auxiliary End -->
   </div>
   <!-- Main Area End -->
   <!-- Footer Start -->
   <!-- BEGIN LayoutContainerBottom.jspf -->
   <!-- BEGIN FooterDisplay.jspf -->
   <div class="footer" id="globalFooter">
    <ul>
     <li>
      <a href="http://www.sainsburys.co.uk/privacy">
       Privacy policy
      </a>
     </li>
     <li>
      <a href="http://www.sainsburys.co.uk/cookies">
       Cookie policy
      </a>
     </li>
     <li>
      <a href="http://www.sainsburys.co.uk/terms">
       Terms &amp; conditions
      </a>
     </li>
     <li>
      <a href="http://www.sainsburys.co.uk/accessibility">
       Accessibility
      </a>
     </li>
     <li>
      <a href="http://help.sainsburys.co.uk/" rel="external" target="_blank" title="Opens in new window">
       Help Centre
      </a>
     </li>
     <li>
      <a href="http://www.sainsburys.co.uk/getintouch">
       Contact us
      </a>
     </li>
     <li>
      <a href="/webapp/wcs/stores/servlet/DeviceOverride?deviceId=-21&amp;langId=44&amp;storeId=10151">
       Mobile
      </a>
     </li>
    </ul>
   </div>
   <!-- END FooterDisplay.jspf -->
   <!-- END LayoutContainerBottom.jspf -->
   <!-- Footer Start End -->
  </div>
  <!--// End #page  -->
  <!-- Bright Tagger start -->
  <div class="siteCatalystTag" id="sitecatalyst_ws">
  </div>
  <script type="text/javascript">
   var brightTagStAccount = 'sp0XdVN';
  </script>
  <noscript>
   &lt;iframe src="//s.thebrighttag.com/iframe?c=sp0XdVN" width="1" height="1" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"&gt;&lt;/iframe&gt;
  </noscript>
  <!-- Bright Tagger End -->
 </body>
</html>
<!-- END CategoriesDisplay.jsp -->
'''

TEST_DESCRIPTION_HTML=\
'''<!DOCTYPE html>
<html class="noJs" xmlns:wairole="http://www.w3.org/2005/01/wai-rdf/GUIRoleTaxonomy#" xmlns:waistate="http://www.w3.org/2005/07/aaa" lang="en" xml:lang="en">
<!-- BEGIN ProductDisplay.jsp -->
<head>
    <title>Sainsbury&#039;s Avocado, Ripe &amp; Ready x2 | Sainsbury&#039;s</title>
    <meta name="description" content="Burgers are a summer must-have and these homemade ones are perfect for a barbecue, topped with cool avocado and served with oven-baked potato wedges. "/>
    <meta name="keyword" content=""/>
     
    
    <meta property="fb:app_id" content="258691960829999" /> 
    <meta property="og:type" content="product" /> 
    <meta property="og:url" content="http://www.sainsburys.co.uk/shop/gb/groceries/sainsburys-avocado--ripe---ready-x2" /> 
    <meta property="og:title" content="Sainsbury's Avocado, Ripe & Ready x2" /> 
    <meta property="og:image" content="http://www.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/22/0000001600322/0000001600322_L.jpeg" /> 
    <meta property="og:site_name" content="Sainsbury's" />
    
    <link rel="canonical" href="http://www.sainsburys.co.uk/shop/gb/groceries/sainsburys-avocado--ripe---ready-x2" />
    <!-- BEGIN CommonCSSToInclude.jspf --><!--[if IE 8]>
    <link type="text/css" href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/css/main-ie8.min.css" rel="stylesheet" media="all" />
	<![endif]-->

    <!--[if !IE 8]><!-->
    <link type="text/css" href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/css/main.min.css" rel="stylesheet" media="all" />
    <!--<![endif]-->
 
	
	<link type="text/css" href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/groceries/css/espot.css" rel="stylesheet" media="all" />
	<link type="text/css" href="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/css/print.css" rel="stylesheet" media="print"/>	
<!-- END CommonCSSToInclude.jspf --><!-- BEGIN CommonJSToInclude.jspf -->
<meta name="CommerceSearch" content="storeId_10151" />



<script type="text/javascript">  
    var _deliverySlotInfo = {                          
            expiryDateTime: '',
            currentDateTime: 'November 25,2015 17:00:23',
            ajaxCountDownUrl: 'CountdownDisplayView?langId=44&storeId=10151',
            ajaxExpiredUrl: 'DeliverySlotExpiredDisplayView?langId=44&storeId=10151&currentPageUrl=http%3a%2f%2fwww.sainsburys.co.uk%2fwebapp%2fwcs%2fstores%2fservlet%2f%2fProductDisplay%3fcatalogId%3d10122%26level%3d2%26errorViewName%3dProductDisplayErrorView%26langId%3d44%26categoryId%3d185749%26productId%3d138040%26storeId%3d10151&AJAXCall=true'
        }
    var _amendOrderSlotInfo = {                          
            expiryDateTime: '',
            currentDateTime: 'November 25,2015 17:00:23',
            ajaxAmendOrderExpiryUrl: 'AjaxOrderAmendSlotExpiryView?langId=44&storeId=10151&currentPageUrl=http%3a%2f%2fwww.sainsburys.co.uk%2fwebapp%2fwcs%2fstores%2fservlet%2f%2fProductDisplay%3fcatalogId%3d10122%26level%3d2%26errorViewName%3dProductDisplayErrorView%26langId%3d44%26categoryId%3d185749%26productId%3d138040%26storeId%3d10151'
        }    
    var _commonPageInfo = {
        currentUrl: 'http://www.sainsburys.co.uk/webapp/wcs/stores/servlet//ProductDisplay?catalogId=10122&amp;level=2&amp;errorViewName=ProductDisplayErrorView&amp;langId=44&amp;categoryId=185749&amp;productId=138040&amp;storeId=10151',
        storeId: '10151',
        langId: '44'
    }
</script>

        <script type="text/javascript">
	    var _rhsCheckPostCodeRuleset = {                          
	          postCode: {
	                isEmpty: {
	                      param: true,
	                      text: 'Sorry, this postcode has not been recognised - Please try again.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                },
	                minLength: {
	                      param: 5,
	                      text: 'Sorry, this entry must be at least 5 characters long.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                },
	                maxLength: {
	                      param: 8,
	                      text: 'Sorry, this postcode has not been recognised - Please try again.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                },
	                isPostcode: {
	                      param: true,
	                      text: 'Sorry, this postcode has not been recognised - Please try again.',
	                      msgPlacement: "#checkPostCodePanel #Rhs_checkPostCode .field",
	                      elemToAddErrorClassTo: "#checkPostCodePanel #Rhs_checkPostCode .field"
	                }
	          }
	    }
	    </script>
    
        <script type="text/javascript">
	    var _rhsLoginValidationRuleset = {
	        logonId: {
	            isEmpty: {
	                param: true,
	                text: 'Please enter your username in the space provided.',
	                msgPlacement: "fieldUsername",
	                elemToAddErrorClassTo: "fieldUsername"
	            },
	            notMatches: {
	                param: "#logonPassword",
	                text: 'Sorry, your details have not been recognised. Please try again.',
	                msgPlacement: "fieldUsername",
	                elemToAddErrorClassTo: "fieldUsername"
	            }
	        },
	        logonPassword: {
	            isEmpty: {
	                param: true,
	                text: 'Please enter your password in the space provided.',
	                msgPlacement: "fieldPassword",
	                elemToAddErrorClassTo: "fieldPassword"
	            },
	            minLength: {
	                param: 6,
	                text: 'Please enter your password in the space provided.',
	                msgPlacement: "fieldPassword",
	                elemToAddErrorClassTo: "fieldPassword"
	            }
	        }
	    }
	    </script>
    
<script type="text/javascript">
      var typeAheadTrigger = 2;
</script>

<script type="text/javascript" data-dojo-config="isDebug: false, useCommentedJson: true,locale: 'en-gb', parseOnLoad: true, dojoBlankHtmlUrl:'/wcsstore/SainsburysStorefrontAssetStore/js/dojo.1.7.1/blank.html'" src="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/js/dojo.1.7.1/dojo/dojo.js"></script>




<script type="text/javascript" src="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/js/sainsburys.js"></script>


<script type="text/javascript">require(["dojo/parser", "dijit/layout/AccordionContainer", "dijit/layout/ContentPane", "dojox/widget/AutoRotator", "dojox/widget/rotator/Fade"]);</script>
<script type="text/javascript" src="http://c1.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/groceries/scripts/page/faq.js"></script>


    <style id="antiCJ">.js body{display:none !important;}</style>
    <script type="text/javascript">if (self === top) {var antiCJ = document.getElementById("antiCJ");antiCJ.parentNode.removeChild(antiCJ);} else {top.location = self.location;}</script>
<!-- END CommonJSToInclude.jspf -->
    <script type="text/javascript" src="//sainsburysgrocery.ugc.bazaarvoice.com//static/8076-en_gb/bvapi.js"></script>
    <script type="text/javascript">
        $BV.configure("global", {
            submissionContainerUrl: "http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/BVReviewSubmitDisplay?catalogId=&langId=44&productId=138040&storeId=10151",
            submissionUnavailableMessage: "For technical reasons, we have not been able to connect you to the page you requested and we hope to be able to do so soon. Please try again."
        });
        $BV.ui("rr", "show_reviews", {
            productId: '6834746-P',
            displayCode: '8076-en_gb',
            doShowContent: function() { 
                var reviewTab = 'reviews';
                JS.objects.pdpTabs.showTab(reviewTab);    
                JS.SmoothScroll(reviewTab);
            }
        });
    </script>
    
    
</head>

<body id="productDetails">
  <div id="page">
    <!-- Header Nav Start --><!-- BEGIN LayoutContainerTop.jspf --><!-- BEGIN HeaderDisplay.jspf --><!-- BEGIN CachedHeaderDisplay.jsp -->

<ul id="skipLinks">
    <li><a href="#content">Skip to main content</a></li>
    <li><a href="#groceriesNav">Skip to groceries navigation menu</a></li>
    
</ul>

<div id="globalHeaderContainer">
    <div class="header globalHeader" id="globalHeader">
        <div class="globalNav">
	<ul>
		<li>
			<a href="http://www.sainsburys.co.uk">
			    <span class="moreSainsburysIcon"></span>
                Explore more at Sainsburys.co.uk 
			</a>
		</li>
		<li>
			<a href="http://help.sainsburys.co.uk" rel="external">
			    <span class="helpCenterIcon"></span>
                Help Centre 
			</a>
		</li>
		<li>
			<a href="http://stores.sainsburys.co.uk">
			    <span class="storeLocatorIcon"></span>
                Store Locator 
			</a>
		</li>
		<li class="loginRegister">
			  
					<a href="https://www.sainsburys.co.uk/sol/my_account/accounts_home.jsp">
						<span class="userIcon"></span>
                        Log in / Register 
					</a>
				
		</li>
	</ul>
</div>

	    <div class="globalHeaderLogoSearch">
	        <!-- BEGIN LogoSearchNavBar.jspf -->

<a href="http://www.sainsburys.co.uk/shop/gb/groceries" class="mainLogo"><img src="http://www.sainsburys.co.uk/wcsstore/SainsburysStorefrontAssetStore/img/logo.png" alt="Sainsbury's" /></a>
<div class="searchBox" role="search">
    

    <form name="sol_search" method="get" action="SearchDisplay" id="globalSearchForm">

        <input type="hidden" name="viewTaskName" value="ProductDisplayView" />
        <input type="hidden" name="recipesSearch" value="true" />
        <input type="hidden" name="orderBy" value="RELEVANCE" />

        
              <input type="hidden" name="skipToTrollyDisplay" value="false"/>
          
              <input type="hidden" name="favouritesSelection" value="0"/>
          
              <input type="hidden" name="langId" value="44"/>
          
              <input type="hidden" name="productId" value="138040"/>
          
              <input type="hidden" name="errorViewName" value="ProductDisplayErrorView"/>
          
              <input type="hidden" name="storeId" value="10151"/>
          

        <label for="search" class="access">Search for products</label>
        <input type="search" name="searchTerm" id="search" maxlength="150" value="" autocomplete="off" placeholder="Search" />
        <button type="button" id="clearSearch" class="clearSearch hidden">Clear the search field</button>
        <input type="submit" name="searchSubmit" id="searchSubmit" value="Search" />
    </form>

    <a class="findProduct" href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/ShoppingListDisplay?catalogId=10122&action=ShoppingListDisplay&urlLangId=&langId=44&storeId=10151">Search for multiple products</a>
    <!-- ul class="searchNav">
        <li class="shoppingListLink"><a href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/ShoppingListDisplay?catalogId=10122&action=ShoppingListDisplay&urlLangId=&langId=44&storeId=10151">Find a list of products</a></li>
        <li><a href="http://stores.sainsburys.co.uk">Store Locator</a></li>
        <li><a href="https://www.sainsburys.co.uk/sol/my_account/accounts_home.jsp">My Account</a></li>
        
                 <li><a href="https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/QuickRegistrationFormView?catalogId=10122&amp;langId=44&amp;storeId=10151" >Register</a></li>
        
    </ul-->

</div>
<!-- END LogoSearchNavBar.jspf -->
        </div>
        <div id="groceriesNav" class="groceriesNav">
            <ul class="mainNav">
                <li>
                    
                            <a class="active" href="http://www.sainsburys.co.uk/shop/gb/groceries"><strong>Groceries</strong></a>
                        
                </li>
                <li>
                    
                           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/favourites">Favourites</a>
                        
                </li>
                <li>
                    
                          <a href="http://www.sainsburys.co.uk/shop/gb/groceries/great-offers">Great Offers</a>
                        
                </li>
                <li>
                    
                           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/ideas-recipes">Ideas &amp; Recipes</a>
                        
                </li>
                <li>
                    
                           <a href="http://www.sainsburys.co.uk/shop/gb/groceries/benefits">Benefits</a>
                        
                </li>
            </ul>
            <hr />
            
                    <p class="access">Groceries Categories</p>
                    
                    <div class="subNav">
                        <ul>
                            
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/Christmas">Christmas</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a class="active" href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg"><strong>Fruit &amp; veg</strong></a>
                                             
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/meat-fish">Meat &amp; fish</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/dairy-eggs-chilled">Dairy, eggs &amp; chilled</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/bakery">Bakery</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/frozen-">Frozen</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/food-cupboard">Food cupboard</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/drinks">Drinks</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/health-beauty">Health &amp; beauty</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/baby">Baby</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/household">Household</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/pet">Pet</a>
                                         
                                   </li>
                              
                                <li>
                                    
                                            <a href="http://www.sainsburys.co.uk/shop/gb/groceries/home-ents">Home</a>
                                         
                                   </li>
                              
                        </ul>
                    </div>
                
        </div>    
    </div>
</div>
<!-- Generated on: Wed Nov 25 17:00:23 GMT 2015  -->
<!-- END CachedHeaderDisplay.jsp --><!-- END HeaderDisplay.jspf --><!-- END LayoutContainerTop.jspf --><!-- Header Nav End --><!-- Main Area Start -->
    <div id="main">
      <!-- Content Start -->
      <div class="article" id="content">

          <!--  Breadcrumb include to go here -->
                  <div class="nav breadcrumb" id="breadcrumbNav">
                    <p class="access">You are here:</p>  
                    <ul>
                        
<li class="first"><span class="corner"></span><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg"><span>Fruit & veg</span></a>
    
        <span class="arrow"></span>
    
    <div>
        <p>Select an option:</p>
        <ul>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/great-prices-on-fruit---veg">Great prices on fruit & veg</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/flowers---seeds">Flowers & plants</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/new-in-season">In season</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-fruit">Fresh fruit</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-vegetables">Fresh vegetables</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-salad">Fresh salad</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-herbs-ingredients">Fresh herbs & ingredients</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/prepared-ready-to-eat">Prepared fruit, veg & salad</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/organic">Organic</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/taste-the-difference-185761-44">Taste the Difference</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fruit-veg-fairtrade">Fairtrade</a></li>
            
                <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/christmas-fruit---nut">Christmas fruit & nut</a></li>
            
        </ul>
    </div>
</li>

            <li class="second"><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-fruit"><span>Fresh fruit</span></a> <span class="arrow"></span>
                <div>
                <p>Select an option:</p>
                    <ul>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/all-fruit">All fruit</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ripe---ready">Ripe & ready</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/bananas-grapes">Bananas & grapes</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/apples-pears-rhubarb">Apples, pears & rhubarb</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/berries-cherries-currants">Berries, cherries & currants</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/citrus-fruit">Citrus fruit</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/nectarines-plums-apricots-peaches">Nectarines, plums, apricots & peaches</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/melon-pineapple-kiwi">Kiwi & pineapple</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/melon---mango">Melon & mango</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/mango-exotic-fruit-dates-nuts">Papaya, Pomegranate & Exotic Fruit</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/dates--nuts---figs">Dates, Nuts & Figs</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ready-to-eat">Ready to eat fruit</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/organic-fruit">Organic fruit</a></li>
                        
                            <li><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/fresh-fruit-vegetables-special-offers">Special offers</a></li>
                        
                    </ul>
                </div>
            </li>
        
    <li class="third"><a href="http://www.sainsburys.co.uk/shop/gb/groceries/fruit-veg/ripe---ready"><span>Ripe & ready</span></a>
        
    </li>
    
                    </ul>
                  </div>
                
          
          <div class="section productContent">
              <!-- BEGIN MessageDisplay.jspf --><!-- END MessageDisplay.jspf -->
              <div class="errorBanner hidden" id="error138041"></div>
              <!-- BEGIN CachedProductOnlyDisplay.jsp -->


<div class="pdp">
    
	     
    <div class="productSummary">
        <div class="productTitleDescriptionContainer">
            <h1>Sainsbury's Avocado, Ripe & Ready x2</h1>
	 
            <div id="productImageHolder">
	             <img src="http://www.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/22/0000001600322/0000001600322_L.jpeg"  alt="Image for Sainsbury&#039;s Avocado, Ripe &amp; Ready x2 from Sainsbury&#039;s" class="productImage " id="productImageID" />
            </div>  
	
            
	
            <div class="reviews">   
				<!-- BEGIN CatalogEntryRatingsReviewsInfoDetailsPage.jspf --><!-- END CatalogEntryRatingsReviewsInfoDetailsPage.jspf -->
            </div>
        </div>
        
        
	   <div class="addToTrolleytabBox" >
	        <!-- Start UserSubscribedOrNot.jspf --><!-- Start UserSubscribedOrNot.jsp --><!-- 
			If the user is not logged in, render this opening 
			DIV adding an addtional class to fix the border top which is removed 
			and replaced by the tabs
		-->
		<div class="addToTrolleytabContainer addItemBorderTop">
	<!-- End AddToSubscriptionList.jsp --><!-- End AddSubscriptionList.jspf --><!-- 
		    ATTENTION!!!
		    <div class="addToTrolleytabContainer">
		    This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
		    -->
	        <div class="pricingAndTrolleyOptions">
	        
	        
	        <div class="priceTab activeContainer priceTabContainer" id="addItem_138041"> <!-- CachedProductOnlyDisplay.jsp -->
	            <div class="pricing">
	               
<p class="pricePerUnit">
&pound;1.80<abbr title="per">/</abbr><abbr title="unit"><span class="pricePerUnitUnit">unit</span></abbr>
</p>
 
    <p class="pricePerMeasure">&pound;1.80<abbr 
            title="per">/</abbr><abbr 
            title="each"><span class="pricePerMeasureMeasure">ea</span></abbr>
    </p>

	            </div>
	            
	            <div class="addToTrolleyForm "> 
	                
<form class="addToTrolleyForm" name="OrderItemAddForm_138041" action="OrderItemAdd" method="post" id="OrderItemAddForm_138041" class="addToTrolleyForm">
    <input type="hidden" name="storeId" value="10151"/>
    <input type="hidden" name="langId" value="44"/>
    <input type="hidden" name="catalogId" value="10122"/>
    <input type="hidden" name="URL" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet//ProductDisplay?catalogId=10122&amp;level=2&amp;errorViewName=ProductDisplayErrorView&amp;langId=44&amp;categoryId=185749&amp;productId=138040&amp;storeId=10151"/>
    <input type="hidden" name="errorViewName" value="ProductDisplayView"/>
    <input type="hidden" name="SKU_ID" value="6834746"/>
    
        <label class="access" for="quantity_138040">Quantity</label>
        
	        <input name="quantity" id="quantity_138040" type="text" size="3" value="1" class="quantity"   />
	        
        
        <input type="hidden" name="catEntryId" value="138041"/>
        <input type="hidden" name="productId" value="138040"/>
    
    <input type="hidden" name="page" value=""/>
    <input type="hidden" name="contractId" value=""/>
    <input type="hidden" name="calculateOrder" value="1"/>
    <input type="hidden" name="calculationUsage" value="-1,-2,-3"/>
    <input type="hidden" name="updateable" value="1"/>
    <input type="hidden" name="merge" value="***"/>
     
   	<input type="hidden" name="callAjax" value="false"/>
    
         <input class="button process" type="submit" name="Add" value="Add" />
     
</form>

	    <div class="numberInTrolley hidden numberInTrolley_138041" id="numberInTrolley_138041">
	        
	    </div>
	      
	            </div> 
	            
	        </div>            
	        <!-- Start AddToSubscriptionList.jspf --><!-- Start AddToSubscriptionList.jsp --><!-- End AddToSubscriptionList.jsp --><!-- End AddToSubscriptionList.jspf -->     
            </div><!-- End pricingAndTrolleyOptions -->  
        </div><!-- End addToTrolleytabContainer --> 
    </div>	
	
	<div class="BadgesContainer">    
	    
		<div class="roundelContainer">
		          
		 </div>
	    
    </div>
    	 
    
    <div id="sitecatalyst_ESPOT_NAME_WF_013_eSpot_1" class="siteCatalystTag">WF_013_eSpot_1</div>

</div> 

	
        
</div>
<div class="mainProductInfoWrapper">
    <div class="mainProductInfo">        
        <p class="itemCode">
            Item code: 6834746
        </p>
        
        <div class="socialLinks">
        <h2 class="access">Social Links (may open in a new window)</h2>
        
           <ul>
                                   
               <li class="twitter"><a href="https://twitter.com/share?text=Check this out&amp;url=http://www.sainsburys.co.uk/shop/gb/groceries/sainsburys-avocado--ripe---ready-x2" target="_blank"><span>Tweet</span> <span class="access">on Twitter</span></a></li>
                                  
                   <li class="facebook">
                       <iframe src="//www.facebook.com/plugins/like.php?href=http://www.sainsburys.co.uk/shop/gb/groceries/sainsburys-avocado--ripe---ready-x2&amp;send=false&amp;layout=button_count&amp;width=90&amp;show_faces=false&amp;action=like&amp;colorscheme=light&amp;font&amp;height=21" scrolling="no" frameborder="0" allowTransparency="true"></iframe>
                   </li>
               
           </ul>
        </div>
        
           
        <div class="tabs">
            
            <ul class="tabLinks">
                <li class="first">
                    <a href="#information" class="currentTab">Information</a>
                </li>
                
            </ul>

            
            
            <div class="section" id="information">
                <h2 class="access">Information</h2>
                <ProductContent xmlns:a="http://www.inspire-js.com/SOL">
<HTMLContent contentPath="/Content/media/html/products/label//_label_inspire.html" outputMethod="xhtml">
<h3 class="productDataItemHeader">Description</h3>
<div class="productText">
<p>Avocados</p>
<p>
<p></p>
</p>
</div>

<h3 class="productDataItemHeader">Nutrition</h3>
<div class="productText">
<div>
<p>
<strong>Table of Nutritional Information</strong>
</p>
<div class="tableWrapper">
<table class="nutritionTable">
<thead>
<tr class="tableTitleRow">
<th scope="col">Per 100g</th><th scope="col">Per 100g&nbsp;</th><th scope="col">% based on RI for Average Adult</th>
</tr>
</thead>
<tr class="tableRow1">
<th scope="row" class="rowHeader" rowspan="2">Energy</th><td class="">813kJ</td><td class="">-</td>
</tr>
<tr class="tableRow0">
<td class="">198kcal</td><td class="">10%</td>
</tr>
<tr class="tableRow1">
<th scope="row" class="rowHeader">Fat</th><td class="tableRow1">19.5g</td><td class="tableRow1">28%</td>
</tr>
<tr class="tableRow0">
<th scope="row" class="rowHeader">Saturates</th><td class="tableRow0">4.1g</td><td class="tableRow0">21%</td>
</tr>
<tr class="tableRow1">
<th scope="row" class="rowHeader">Mono unsaturates</th><td class="tableRow1">12.1g</td><td class="tableRow1">-</td>
</tr>
<tr class="tableRow0">
<th scope="row" class="rowHeader">Polyunsaturates</th><td class="tableRow0">2.2g</td><td class="tableRow0">-</td>
</tr>
<tr class="tableRow1">
<th scope="row" class="rowHeader">Carbohydrate</th><td class="tableRow1">1.9g</td><td class="tableRow1">1%</td>
</tr>
<tr class="tableRow0">
<th scope="row" class="rowHeader">Total Sugars</th><td class="tableRow0">&lt;0.5g</td><td class="tableRow0">-</td>
</tr>
<tr class="tableRow1">
<th scope="row" class="rowHeader">Fibre</th><td class="tableRow1">3.4g</td><td class="tableRow1">-</td>
</tr>
<tr class="tableRow0">
<th scope="row" class="rowHeader">Protein</th><td class="tableRow0">1.9g</td><td class="tableRow0">4%</td>
</tr>
<tr class="tableRow1">
<th scope="row" class="rowHeader">Salt</th><td class="tableRow1">0.02g</td><td class="tableRow1">-</td>
</tr>
</table>
</div>
<p>RI= Reference Intakes of an average adult (8400kJ / 2000kcal)</p>
</div>
</div>

<h3 class="productDataItemHeader">Country of Origin</h3>
<div class="productText"><p>Grown in Argentina, Brazil, Chile, Colombia, Dominican Republic, Israel, Kenya, Mexico, Morocco, Peru, South Africa, Spain, Swaziland, Tanzania</p></div>

<h3 class="productDataItemHeader">Size</h3>
<div class="productText">
<p>2Count</p>
</div>

<h3 class="productDataItemHeader">Storage</h3>
<div class="productText">
<p>At home refrigerate for freshness, prepare immediately prior to eating.</p>
</div>

<h3 class="productDataItemHeader">Packaging</h3>
<div class="productText">
<p>Plastic - LDPE film</p>
<p>Recycled paper punnet</p>
</div>

<h3 class="productDataItemHeader">Manufacturer</h3>
<div class="productText">
<p>We are happy to replace this item if it is not satisfactory</p>
<p>Sainsbury's Supermarkets Ltd.</p>
<p>33 Holborn, London EC1N 2HT</p>
<p>Customer services 0800 636262</p>
</div>

</HTMLContent>
</ProductContent>

                <p><h3>Important Information</h3><p>The above details have been prepared to help you select suitable products. Products and their ingredients are liable to change.</p><p><strong>You should always read the label before consuming or using the product and never rely solely on the information presented here.</p></strong><p>If you require specific advice on any Sainsbury's branded product, please contact our Customer Careline on 0800 636262. For all other products, please contact the manufacturer.</p><p>
This information is supplied for your personal use only. It may not be reproduced in any way without the prior consent of Sainsbury's Supermarkets Ltd and due acknowledgement.</p></p>
            </div>

               
        </div>    
        
            <p class="skuCode">6834746</p>
        
    </div>        
</div>
<div id="additionalItems_138041" class="additionalProductInfo">

      <!--  Left hand side column --><!-- BEGIN MerchandisingAssociationsDisplay.jsp --><!-- Start - JSP File Name:  MerchandisingAssociationsDisplay.jsp -->
    <div class="coverage ranged"></div>
<!-- BEGIN CatalogEntryThumbnailMerchandisingAssociation.jspf -->
                    <div id="sitecatalyst_SELL_TYPE_958706" class="siteCatalystTag">UPSELL</div>
                    <div class="crossSell">
                        <h2 class="crossSellTitle">
                            <!-- BEGIN ContentDisplay.jsp -->
	                    <a href="?errorViewName=ProductDisplayErrorView" >
	                
	                <img
	                    src='http://www.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/merchandising_associations/you_may_also_like_grid_202x32.gif'
	                    alt='wcassets/merchandising_associations/you_may_also_like_grid_202x32.gif'
	                    border="0"
	                />
	                
	                    </a>
	                <!-- end: ContentDisplay.jsp -->
                        </h2>
                        <div class="crossSellContent">                            
                        <div class="crossSellInfo">
                                <h3 class="crossSellName">
                                    <span class="access">Try this product with  </span>
	                                <a href="http://www.sainsburys.co.uk/shop/gb/groceries/pip---nut-almond-butter-250g">
	                                    Pip & Nut Almond Butter 250g
	                                    <img src="http://www.sainsburys.co.uk/wcsstore7.11.1.161/ExtendedSitesCatalogAssetStore/images/catalog/productImages/48/5060367180048/5060367180048_S.jpeg" alt="" />
	                                </a>
                                </h3>                                
                            </div>
                            <div class="pricingAndTrolleyFormWrapper">
                                <div class="pricingReviews">
                                    <div class="pricing">
                                        
<p class="pricePerUnit">
£3.45<abbr title="per">/</abbr><abbr title="unit"><span class="pricePerUnitUnit">unit</span></abbr>
</p>
 
    <p class="pricePerMeasure">£1.38<abbr 
            title="per">/</abbr>100<abbr 
            title="gram"><span class="pricePerMeasureMeasure">g</span></abbr>
    </p>

                                    </div>
                                </div>
                                <div class="addToTrolleyForm ">
                                    
                                    
<form class="addToTrolleyForm" name="OrderItemAddForm_958707_138040" action="OrderItemAdd" method="post" id="OrderItemAddForm_138040_958707" class="addToTrolleyForm">
    <input type="hidden" name="storeId" value="10151"/>
    <input type="hidden" name="langId" value="44"/>
    <input type="hidden" name="catalogId" value="10122"/>
    <input type="hidden" name="URL" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet//ProductDisplay?catalogId=10122&amp;level=2&amp;errorViewName=ProductDisplayErrorView&amp;langId=44&amp;categoryId=185749&amp;productInRange=true&amp;productId=138040&amp;storeId=10151"/>
    <input type="hidden" name="errorViewName" value="ProductDisplayView"/>
    <input type="hidden" name="SKU_ID" value="7771694"/>
    
        <label class="access" for="quantity_958706">Quantity</label>
        
	        <input name="quantity" id="quantity_958706" type="text" size="3" value="1" class="quantity"   />
	        
        
        <input type="hidden" name="catEntryId" value="958707"/>
        <input type="hidden" name="productId" value="958706"/>
    
    <input type="hidden" name="page" value=""/>
    <input type="hidden" name="contractId" value=""/>
    <input type="hidden" name="calculateOrder" value="1"/>
    <input type="hidden" name="calculationUsage" value="-1,-2,-3"/>
    <input type="hidden" name="updateable" value="1"/>
    <input type="hidden" name="merge" value="***"/>
     
   	<input type="hidden" name="callAjax" value="false"/>
    
         <input class="button process" type="submit" name="Add" value="Add" />
     
</form>

	    <div class="numberInTrolley hidden numberInTrolley_958707" id="numberInTrolley_958707">
	        
	    </div>
	
                                </div>
                            </div>
                            
    <div class="promotion">
        
            <p><a href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/PromotionDisplayView?catalogId=10122&amp;langId=44&amp;productId=958706&amp;storeId=10151&amp;promotionId=10155981">Introductory Offer:  Only £3.45</a></p>
            
    </div>

                        </div>
                    </div>
                <!-- END CatalogEntryThumbnailMerchandisingAssociation.jspf --><!-- END MerchandisingAssociationsDisplay.jsp -->
    
    <div class="badges">
        <ul>
            
                    
                    
                    
                     <li >

                        
                        
                        <img src="http://www.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/icons/ico_spacer.gif" alt="Vegan" />
                            
                        
                    </li>
                
                    
                    
                    
                     <li  class="lastchild" >

                        
                        
                        <img src="http://www.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/icons/ico_spacer.gif" alt="Vegetarian" />
                            
                        
                    </li>
                
        </ul>   
    </div>


  </div>    
    
<!-- END CachedProductOnlyDisplay.jsp -->
          </div><!-- productContent End -->
      </div>
      <!-- Content End --><!-- auxiliary Start -->
      <div class="aside" id="auxiliary">
        <!-- BEGIN RightHandSide.jspf -->
<div id="auxiliaryDock">
    <!-- BEGIN RightHandSide.jsp -->

<div class="panel loginPanel">
	
    <div id="sitecatalyst_ESPOT_NAME_NZ_Welcome_Back_RHS_Espot" class="siteCatalystTag">NZ_Welcome_Back_RHS_Espot</div>

                    
	<h2>Already a customer?</h2>
    <form name="signIn" method="post" action="LogonView" id="Rhs_signIn">
        <input type="hidden" name="storeId" value="10151"/>
        <input type="hidden" name="langId" value="44"/>
        <input type="hidden" name="catalogId" value="10122"/>
        <input type="hidden" name="URL" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet//ProductDisplay?catalogId=10122&level=2&errorViewName=ProductDisplayErrorView&langId=44&categoryId=185749&productInRange=true&productId=138040&storeId=10151"/>
        <input type="hidden" name="logonCallerId" value="LogonButton"/>
        <input type="hidden" name="errorViewName" value="ProductDisplayView"/>
        <input class="button process" type="submit" value="Log in" />
    </form>
    
	<div class="panelFooter">
		<p class="register">Not yet registered? 
		<a class="callToAction" name="register" href="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/PostcodeCheckView?catalogId=&currentPageUrl=http%3A%2F%2Fwww.sainsburys.co.uk%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2F%2FProductDisplay%3FcatalogId%3D10122%26level%3D2%26errorViewName%3DProductDisplayErrorView%26langId%3D44%26categoryId%3D185749%26productInRange%3Dtrue%26productId%3D138040%26storeId%3D10151&langId=44&storeId=10151"> Register Now</a></p>
	</div>
</div>
<div class="panel imagePanel checkPostCodePanel" id="checkPostCodePanel">
	
    <div id="sitecatalyst_ESPOT_NAME_NZ_Do_We_Deliver_To_You_Espot" class="siteCatalystTag">NZ_Do_We_Deliver_To_You_Espot</div>

	<h2>New customer?</h2>
    <p>Enter your postcode to check we deliver in your area.</p>
    
    
      <div id="PostCodeMessageArea" class="errorMessage" style="display:none;">
      </div>
    
	<form name="CheckPostCode" method="post" action="/webapp/wcs/stores/servlet/CheckPostCode" id="Rhs_checkPostCode">
		<input type="hidden" name="langId" value="44"/>
		<input type="hidden" name="storeId" value="10151"/>
		<input type="hidden" name="currentPageUrl" value="http://www.sainsburys.co.uk/webapp/wcs/stores/servlet//ProductDisplay?catalogId=10122&amp;level=2&amp;errorViewName=ProductDisplayErrorView&amp;langId=44&amp;categoryId=185749&amp;productInRange=true&amp;productId=138040&amp;storeId=10151"/>
         
            <input type="hidden" name="currentViewName" value="ProductDisplayView"/>
        
		<input type="hidden" name="messageAreaId" value="PostCodeMessageArea"/>
		
		<div class="field">
			<div class="indicator">
				<label class="access" for="postCode">Postcode</label>
			</div>
			<div class="input">
				<input type="text" name="postCode" id="postCode" maxlength="8" value="" />
			</div>
		</div>
		<div class="actions">
			<input class="button primary process" type="submit" value="Check postcode"/>
		</div>      
	</form>
</div>
<!-- END RightHandSide.jsp --><!-- BEGIN MiniShopCartDisplay.jsp --><!-- If we get here from a generic error this service will fail so we need to catch the exception -->
		<div class="panel infoPanel">
			<span class="icon infoIcon"></span>
		   	<h2>Important Information</h2>
			<p>Alcohol promotions available to online customers serviced from our Scottish stores may differ from those shown when browsing our site. Please log in to see the full range of promotions available to you.</p>
		</div>
	<!-- END MiniShopCartDisplay.jsp -->
</div>
<!-- END RightHandSide.jspf -->
      </div>
      <!-- auxiliary End -->
    </div>
    <!-- Main Area End --><!-- Footer Start Start --><!-- BEGIN LayoutContainerBottom.jspf --><!-- BEGIN FooterDisplay.jspf -->


<div id="globalFooter" class="footer">
    <ul>
	<li><a href="http://www.sainsburys.co.uk/privacy">Privacy policy</a></li>
	<li><a href="http://www.sainsburys.co.uk/cookies">Cookie policy</a></li>
	<li><a href="http://www.sainsburys.co.uk/terms">Terms &amp; conditions</a></li>
	<li><a href="http://www.sainsburys.co.uk/accessibility">Accessibility</a></li>
	<li><a href="http://help.sainsburys.co.uk/" rel="external" target="_blank" title="Opens in new window">Help Centre</a></li>
	<li><a href="http://www.sainsburys.co.uk/getintouch">Contact us</a></li>
	<li><a href="/webapp/wcs/stores/servlet/DeviceOverride?deviceId=-21&langId=44&storeId=10151">Mobile</a></li>
</ul>

</div>

<!-- END FooterDisplay.jspf --><!-- END LayoutContainerBottom.jspf --><!-- Footer Start End -->
        
  </div><!--// End #page  --><!-- Bright Tagger start -->

	<div id="sitecatalyst_ws" class="siteCatalystTag"></div>
	
    <script type="text/javascript">
        var brightTagStAccount = 'sp0XdVN';
    </script>
    <noscript>
        <iframe src="//s.thebrighttag.com/iframe?c=sp0XdVN" width="1" height="1" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
    </noscript>
	
<!-- Bright Tagger End -->
</body>
</html>
<!-- END ProductDisplay.jsp -->
'''
        
if __name__ == '__main__' :
    unittest.main()