# Robinhood-Trading-Journal

This project is python scripts, which uses mainly [Robinhood](https://robinhood.com)'s 
private API and [Dash feature from Plotly](https://plotly.com/dash/open-source/) for 
creating visualized trading journal. You can varify and download to use it as personal trading journal for Robinhood. 

Inspired and based on python projects, [Josh Fraser's robinhood-to-csv](https://github.com/joshfraser/robinhood-to-csv/), and [Rohan Pai & Adithya Balaji's Robinhood Unofficial](https://github.com/robinhood-unofficial/pyrh).

The reason behind creating is that new age invester's trading habits in robinhood is very risky and rewarding and 
there is no budget tool (there are some pricey tools that can extract robinhood trades and then some requiering you to 
have csv from robinhood as robinhood doesn't give until asked from one of thier representive!), this can calculute one's ongoing gains, 
the person can actually know how much profit/loss is made in one week, month or quarter. 

Most useful case scenerio is paying one's quarterly estimated tax based on your estimated calculated gain using this. 
Where as day trader or swing trader can analyze their trading habits using visulized trading journal, run the script on day's end to know net profit of the day. 
<br><br>

> **Note: Python scripts are in python3.** 
<br>

The defalts endpoints to access robinhood api is in [Robinhood_Base.py](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Robinhood_Base.py), 
one of the convienince I made in my script for login is that it is MFA app compatiable login, which means you can use your google code auth or duo to add MFA code to login. 
Although I haven't worked on more methods since that are not useful in regards to this project, but you can give it a try. 

The [Robin_hood.py](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Robin_hood.py) scripts have methods on accessing order history for stocks and options, (will try to work on crypto later), current portfolio and dataframe of order history. 
Benefit of this script is that it accounts of stocks splits while calculating for profit/loss, if security was bought before split and sold after split. Although calculation are based on FIFO basis as per [Robinhood's default cost basis](https://robinhood.com/us/en/support/articles/cost-basis/). 
However, wash sale calculation are not accounted. Also options calculation were quite complicated so at moment it only accounts for bought and sold or expired. If there is covered sell meaning that you sold option contract based on stocks owned, and option excersiced are not accounted. Hence those entities  are not included in calculations.

Each Layout file in dashApp/app folder is each webpage layout's python scripts, it consists dash bootstrap, container, and html components as well as callback methods regarding each webpage are in same corresponding python script. For further understanding look [dash documentation](https://dash.plotly.com/)
<br>


## Installing github repo to local machine and dependency to run this app

You can manually download zip file from here, click on Code and select Download Zip

> **_Requirements:_**  python 3+ [Install Python](https://www.python.org/downloads/)<br> **_Optional:_** Git [Install Git](https://git-scm.com/downloads). If zip downloaded then directly go to step 3 and 4

~~~
Cloning this repo:
Change directory to desired location!!!

>> cd Documents
>> git clone https://github.com/virajkothari7/Robinhood-trading-journal.git
>> cd Robinhood-trading-journal
>> pip install -r requirements.txt

~~~


## Getting Started 
For detailed instruction look Instruction.txt
~~~
Getting data from Robinhood and have visualize it on local server using a web browser!!

>> cd [PATH]/Robinhood-trading-journal/dashApp
>> python Robin_hood.py  #To get data from Robinhood
>> python index.py  #Will open a local server, for best view results, try using google chrome, safari or edge

~~~


## Final View

After getting data by running "Robin_hood.py" script, and running "index.py" to have local server running dash app.
Below is screen shots of final app, also stored in snapshots folder.
<br><br>
<table>
  <tr>
    <td><img src=https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/snapshots/snapshot_1.gif></td>
    <td><img src=https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/snapshots/snapshot_3.gif></td>
  </tr>
  <tr>
    <td><img src=https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/snapshots/snapshot_2.gif></td>
    <td><img src=https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/snapshots/snapshot_5.gif></td>
  </tr>
</table>
<br> 


## Technologies
- plotly==5.1.0
- dash==1.21.0
- dash_table==4.12.0
- dash_core_components==1.17.1
- dash_html_components==1.1.4
- dash_bootstrap_components==0.12.2
- numpy==1.20.3
- pandas==1.3.0
- requests==2.25.1
- yfinance==0.1.63
- datetime
<br>

  
# Credits/Acknowledgement

Project: [pyrh - Unofficial Robinhood API](https://github.com/robinhood-unofficial) <br>
Copyright (c) 2020 Unofficial Robinhood Python API Developers <br>
License (MIT) https://github.com/robinhood-unofficial/pyrh/blob/master/LICENSE 
<br>

Project: [Robinhood to CSV](https://github.com/joshfraser/robinhood-to-csv) <br>
Copyright (c) 2015 Josh Fraser <br>
Copyright (c) 2015 Rohan Pai <br>
License (MIT) https://github.com/joshfraser/robinhood-to-csv/blob/master/LICENSE 
<br>

Project: [Plotly-Dash](https://github.com/plotly/dash) <br>
Copyright (c) 2021 Plotly, Inc <br>
License (MIT) https://github.com/plotly/dash/blob/dev/LICENSE <br>
Documentation : https://dash.plotly.com/ 
<br>

Author: Charming Data <br>
Github Repo: [Coding-with-Adam/Dash-by-Plotly](https://github.com/Coding-with-Adam/Dash-by-Plotly)<br>
Youtube Link: https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ 
<br>

Author: Gil Yehuda (credit for Credits Template) <br>
Quora Link: https://www.quora.com/How-do-I-properly-credit-an-original-codes-developer-for-her-open-source-contribution <br>

Community Credits: Python Community, Stack Exchange Community, Plolty Community, Web-Developers Community

<br>

# License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/LICENSE)

This project is licensed under MIT. You are responsible for using robinhood's private api and all depending third-party libraries by running the scripts, look robinhood's and respective python libraries terms of use.

