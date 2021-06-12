# Robinhood-trading-journal

This project is python scripts, which uses mainly [Robinhood](https://robinhood.com)'s private API and [Dash feature from Plotly](https://plotly.com/dash/open-source/) for creating visualized trading journal. Inspired and based on pyhton projects, [Josh Fraser's robinhood-to-csv](https://github.com/joshfraser/robinhood-to-csv/), and [Rohan Pai & Adithya Balaji's Robinhood Unofficial](https://github.com/robinhood-unofficial/pyrh).

The reason behind creating is that new age invester's trading habits in robinhood is very risky and rewarding and there is no budget tool (there are some pricey tools that can extract robinhood trades and then some requering you to have csv from robinhood) that can calculute one's ongoing gains, the person doesn't actually know how much profit/loss is made in one week, month or quarter. Most useful case scenerio is paying your quarterly estimated tax based on your estimated calculated gain using this. Where as day trader or swing trader can analyze their trading habits using visulized trading journal, run the script on day's end to know net profit of the day. Most importantly I needed it for myself since I am robinhooder and also just wanted showcase my pyhton skills :)


# Pyhton scripts are in python3.

The defalts endpoints to access robinhood api is in [Robinhood_Base.py](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Robinhood_Base.py), one of the convienince I made in my script for login is that it is MFA app compatiable login, which means you can use your google code auth or duo to add MFA code to login. Although I haven't worked on more methods since that are not useful in regards to this project, but you can give it a try. 

The [Robin_hood.py](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Robin_hood.py) scripts have methods on accessing order history for stocks and options, will work on crypto later, current portfolio and dataframe of order history. I seen that many other methods do not account of splits while calculating for profit or loss but I have tried to account for splits in stocks orderBook and should account of spilts if security was bought before split and sold after split. Although calculation are based of FIFO basis as per [Robinhood's default cost basis](https://robinhood.com/us/en/support/articles/cost-basis/), Wash sale calculation are not accounted in it yet but will be soon. 

# This project is still "Work In Progress", I will try to finish workable trading journal ASAP. Meanwhile you can look into [RH_code.ipynb](https://github.com/virajkothari7/Robinhood-trading-journal/blob/main/Rh_Code.ipynb), it shows how can you use this scripts and also play around with plotly's Jupyter dash, eventually it will be dash app and will be running on local host.
# At this moment you can just downlaod scripts manually.
