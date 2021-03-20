# Overview Document for TweetGuard

This file gives a breakdown of the folder structure of the project and a summary of what each file contains&#46; It's purpose is to determine if a file is of interest without needing to view the contents of the file&#46; Each description of code and pdf files contain a link to the specified file.

## Table of Contents

- [Top-level Directory][1]
    - documents
    - webapp
    - &#46;gitignore
    - Dockerfile
    - README&#46;md
    - requirements&#46;txt
- [documents Directory][2]
    - Product Document&#46;pdf
    - Project Evolution&#46;pdf
    - Project Brief&#46;pdf
- [webapp Directory][3]
    - static
    - templates
    - \_\_init\_\_&#46;py
    - forms&#46;py
    - models&#46;py
    - scanning&#46;py
    - site&#46;db
    - views&#46;py
- [webapp/static Directory][4]
    - mr_clean&#46;jpg
    - site&#46;css
    - site&#46;js
    - twitter-bird-pixy&#46;png
- [webapp/templates Directory][5]
    - admin
    - database_search&#46;html
    - database&#46;html
    - index&#46;html
    - layout&#46;html
    - report_ranked&#46;html
    - report&#46;html
    - scan_all&#46;html
    - scan_choose&#46;html
    - scan_user&#46;html
    - scan&#46;html

## Top-Level Directory

**documents** - This directory holds the documentation files such as the Product Brief, Product Documentation and Project Evolution&#46;

**webapp** - The directory containing source code files including HTML, CSS, Javascript as well as Flask and Python code&#46;

**&#46;gitignore** - The file Git uses to exclude files from commits&#46;

[**Dockerfile**][6] - The file used to build a Docker container of the project&#46;

[**README&#46;md**][7] - Includes the names of the developers, a very brief overview of the project, installation instructions and possible limitations&#46;

[**requirements&#46;txt**][8] - Used by PIP (The Python Package Manager) to install dependencies with one command (pip install -r requirements&#46;txt)&#46;

[**run&#46;py**][32] - The file that is used to start running the server&#46;



## documents Directory

[**Product Document&#46;pdf**][9] - Details each page in the application and how to interact with them&#46;

[**Project Evolution&#46;pdf**][10] - Gives a breakdown of work done each week, decisions made, and limitations that materialised&#46;

[**Project Brief&#46;pdf**][11] - Gives a detailed description of what the product is, why it's relevant, how it works and desctiptions of the team roles and architecture&#46;

## webapp Directory

**static** - The directory that holds images and user-defined HTML and CSS&#46;

**templates** - The directory that holds the HTML layout files for each page&#46;

[**\_\_init\_\_&#46;py**][12] - Assembles the application files and creates the database connection and Twitter API connection to pass to run&#46;py&#46;

[**forms&#46;py**][14] - Used by Flask to construct forms programatically rather than in the HTML templates&#46;

[**models&#46;py**][15] - Used to construct the schemas of the database tables&#46;

[**scanning&#46;py**][16] - Contains all the functions for the scan functionality&#46;

**site&#46;db** - Contains the actual data within the database&#46;

[**views&#46;py**][17] - Contains the URL routes and their actions&#46;

## webapp/static Directory

[**mr_clean&#46;jpg**][18] - The image used when no threatening tweets were found&#46;

[**site&#46;css**][19] - User-defined CSS styles&#46;

[**site&#46;js**][20] - User-defined Javascript functions&#46;

[**twitter-bird-pixy&#46;png**][21] - The Twitter logo for the header&#46;

## webapp/templates Directory

[**admin**][22] - Layout file for the admin homepage&#46;

[**database_search&#46;html**][22] - Layout file for the results page of a database search&#46;

[**database&#46;html**][23] - Layout file for the database homepage&#46;

[**index&#46;html**][24] - Layout file for the homepage of the application&#46;

[**layout&#46;html**][25] - Base layout file for all pages that holds common elements such as the navigation bar and footer&#46;

[**report_ranked&#46;html**][26] - Layout file for the total reports page&#46;

[**report&#46;html**][27] - Layout file for the report user form&#46;

[**scan_all&#46;html**][28] - Layout file for the results of scanning multiple users for dangerous tweets&#46;

[**scan_choose&#46;html**][29] - Layout file for the page where the user can pick which followers to scan or use the slider to select an amount of specific followers&#46;

[**scan_user&#46;html**][30] - Layout file for the result of scanning a specific user on the scan homepage&#46;

[**scan&#46;html**][31] - Layout file for the scan homepage&#46;

[1]: <#top-level-directory>
[2]: <#documents-directory>
[3]: <#webapp-directory>
[4]: <#webapp/static-directory>
[5]: <#webapp/templates-directory>
[6]: <Dockerfile>
[7]: <README.md>
[8]: <requirements.txt>
[9]: <documents/product_document.pdf>
[10]: <documents/product_evolution.pdf>
[11]: <documents/product_brief.pdf>
[12]: <webapp/__init__.py>
[13]: <webapp/forms.py>
[14]: <webapp/models.py>
[15]: <webapp/scanning.py>
[16]: <webapp/views.py>
[17]: <webapp/static/mr_clean.jpg>
[18]: <webapp/static/site.css>
[19]: <webapp/static/site.js>
[20]: <webapp/static/twitter-bird-pixy.png>
[21]: <webapp/templates/database_search.html>
[22]: <webapp/templates/database.html>
[23]: <webapp/templates/index.html>
[24]: <webapp/templates/layout.html>
[25]: <webapp/templates/report_ranked.html>
[26]: <webapp/templates/report.html>
[27]: <webapp/templates/scan_all.html>
[28]: <webapp/templates/scan_choose.html>
[29]: <webapp/templates/scan_user.html>
[30]: <webapp/templates/scan.html>
[31]: <run.py>
