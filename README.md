<h1>Peru News</h1>

The main site is [here](https://www.perunews.xyz).


<h2>Scrapper</h2>

Use it to scrap articles from Peruvian news websites. You will want to install redis
so that you don't scrap the same article twice.

Run the scrapper with

    python scrappy/app.py


<h2>Api</h2>

You can find the api [here](https://api.perunews.xyz).

<h4>Endpoints</h4>
There are 2 main endpoints:

 * Sources `/v1/sources` - returns all sources that are currently being scrapped.
 * Articles `/v1/articles?source=[SOURCE]` - returns all scrapped articles from a given source. See the 'supported sources'
     for a list of available sources. 

<h4>Request Parameters</h4>

 * **source** - A string of identifiers for the news sources you want information for. Use the `/sources` endpoint for a list
              of supported sources.
           
 * **pageSize** - The number of results to return per page (request). 20 is the default, 100 is the maximum.

 * **page** - Use this to page through the results if the total results found is greater than the page size.

<h4>Supported sources</h4>

 * rpp - RPP Noticias (http://www.rpp.pe).