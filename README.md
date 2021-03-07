# Tweet Guard
## Credits:
### Group 2
* [Conor McGavin](https://github.com/conormcgavin)
* [Evan Dunbar](https://github.com/pkia)
* [Mark Daly](https://github.com/MarkDaly64)
* [Conor Heeney](https://github.com/ConorH99)
* Joel McKenna

## Overview:
Tweet Guard is a web app used to defend against inappropriate and threatening Twitter users. The app has two functions. A scan function and a report function. 

### Scan Function
The scan function is the main feature of the app. It provides a quick way to scan a number of your followers or a specific twitter user. This can help you decide quickly whether you want this user to follow you. The scan function uses Natural Language Processing to find tweets that would be considered inappropriate. You have the ability to filter the target tweets, based on parameters, such as racism, homophobia, etc.

### Report Function
The report function is the secondary feature of the app. This provides a way for users to report a certain account based on their experience. This report consists of the username of the account, and the type and a short description of the threat. This report is added to our database of reports. You can view all reports made which are sorted by the amount of reports made on each account.

## Installation
To download the code and run it on your local machine:

1. Clone this repository.
2. Change into the top-level directory of the repository.
3. To install the requirements, run the command:

Docker:

```
build:
cd webapp
python3 BERT_model.py
cd..
docker build -t threat .

run:
docker run -ti -p 5000:5000 threat
```

Windows:
``` shell
pip install -r requirements.txt
```

Linux:
``` shell
pip3 install -r requirements.txt
```

4. To begin the server, run the command:

Windows:
``` shell
cd webapp
python BERT_model.py
cd..
python run.py
```

Linux:
```shell
cd webapp
python3 BERT_model.py
cd..
python3 run.py
```

5. The local server runs on port 5000, so open your browser of choice and type `localhost:5000` in the address bar.

6. Enjoy the app!

## Possible Limitations

8gb+ RAM required to run efficiently or user may find the app to be resource intensive when running locally.


The fetching and scanning of an entire account with a very high amount of followers can be extremely slow from first impressions and this is something that must be looked at 
A maximum of 3000 tweets can be pulled per user at a time, however this should be ok as recent tweets are the most important.


### Deployment:
Deployed as a containerized web application
http://tweetguard.me

