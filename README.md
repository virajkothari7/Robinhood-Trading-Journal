# Robinhood-trading-journal

This project is python scripts, which uses mainly [Robinhood](https://robinhood.com)'s 
private API and [Dash feature from Plotly](https://plotly.com/dash/open-source/) for 
creating visualized trading journal. 

Inspired and based on python projects, [Josh Fraser's robinhood-to-csv](https://github.com/joshfraser/robinhood-to-csv/), and [Rohan Pai & Adithya Balaji's Robinhood Unofficial](https://github.com/robinhood-unofficial/pyrh).

The reason behind creating is that new age invester's trading habits in robinhood is very risky and rewarding and 
there is no budget tool (there are some pricey tools that can extract robinhood trades and then some requiering you to 
have csv from robinhood as robinhood doesn't give until asked from one of thier representive!), this can calculute one's ongoing gains, 
the person can actually know how much profit/loss is made in one week, month or quarter. 

Most useful case scenerio is paying one's quarterly estimated tax based on your estimated calculated gain using this. 
Where as day trader or swing trader can analyze their trading habits using visulized trading journal, run the script on day's end to know net profit of the day. 


# Python scripts are in python3.

The defalts endpoints to access robinhood api is in [Robinhood_Base.py](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Robinhood_Base.py), 
one of the convienince I made in my script for login is that it is MFA app compatiable login, which means you can use your google code auth or duo to add MFA code to login. 
Although I haven't worked on more methods since that are not useful in regards to this project, but you can give it a try. 

The [Robin_hood.py](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Robin_hood.py) scripts have methods on accessing order history for stocks and options, (will try to work on crypto later), current portfolio and dataframe of order history. 
Benefit of this script is that it accounts of stocks splits while calculating for profit/loss, if security was bought before split and sold after split. Although calculation are based of FIFO basis as per [Robinhood's default cost basis](https://robinhood.com/us/en/support/articles/cost-basis/). 
However, wash sale calculation are not accounted. Also options calculation were quite complicated so at moment it only accounts for bought and sold or expired. If there is covered sell meaning that you sold option contract based on stocks owned, and option excersiced will be not be accounted hence those entities are not included in calculations.

Each Layout file in apps in dashApp is each webpage layout python scripts, it consits dash bootstrap, container, and html components as well as callback methods of regarding each webpage are in same corresponding python script. For further understanding look [dash documentation](https://dash.plotly.com/)


# Getting github repo to local machine and installing dependency to run this app

You can manually download zip file from here, click on Code and select Download Zip

> **_Requirements:_**  python 3+ [Install Python](https://www.python.org/downloads/), Git [Install Git](https://git-scm.com/downloads).

"""
Cloning this repo:
Change directory to desired location!!!

>>>> cd Documents
>>>> git clone https://github.com/virajkothari7/Robinhood-trading-journal.git
>>>> cd Robinhood-trading-journal
>>>> pip3 instrall -r requirements.txt

"""

#Getting Started

"""

"""


#Final View


#Credits
