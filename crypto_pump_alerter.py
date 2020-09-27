#This code imports data from coinmarketcap and does mathematical calulations to predict when a pump is going to happen and sends a notification through telegram
from bs4 import BeautifulSoup
from unidecode import unidecode
from urllib.request import Request, urlopen
import time
import matplotlib.pyplot as plt
import math
import numpy as np
from coinmarketcap import Market
from datetime import datetime
import telegram


starttime=time.time()

def strip_comma(list_wcomma):
    list_float_no_comma=[]
    for elem in list_wcomma:
        no_comma_str=elem.replace(",", "")
        no_comma_float=float(no_comma_str)
        list_float_no_comma.append(no_comma_float)
    return list_float_no_comma


def get_dataList(url_data_list,first_element_index,step_size):  #works on the html file to return lists based on the html header
    some_array=[]
    data_array=[]
    for sub_heading in url_data_list:
        rows_txt= sub_heading.text;
        rows_txt_nowhitespace=rows_txt.strip()
        some_array.append(rows_txt_nowhitespace)

    array_length=len(some_array)

    for ind0 in range(first_element_index, array_length,step_size):
        data_array.append(some_array[ind0])     

    return data_array


def get_coin_historical_data(coin_id):   #Gets historical data from coinmarketcap from coin_id
    url_basic="https://coinmarketcap.com/currencies/"
    url=url_basic + coin_id+ "/historical-data/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    web_byte = urlopen(req).read();
    
    webpage = web_byte.decode('utf-8');
    
    soup = BeautifulSoup(webpage, 'html.parser')
    
    html_header_search=soup.find_all('td');
    
    url_data_list=html_header_search;
    Coin_dates_orig=get_dataList(url_data_list, 0, 7)
    Coin_openprices_orig=get_dataList(url_data_list,1,7)
    Coin_closeprices_orig=get_dataList(url_data_list, 4,7)
    Coin_volumes_orig=get_dataList(url_data_list, 5,7)
    
    Coin_openprices_no_comma=strip_comma(Coin_openprices_orig)
    Coin_closeprices_no_comma=strip_comma(Coin_closeprices_orig)
    Coin_volumes_no_comma=strip_comma(Coin_volumes_orig)
    
    date_index=list(range(0, len(Coin_dates_orig)))
    
    coin_historical_data=[Coin_dates_orig,Coin_openprices_no_comma,Coin_closeprices_no_comma,Coin_volumes_no_comma, date_index]
    return coin_historical_data


def read_user_IDs(ID_File):
    
    idfile_ref=open(ID_File)
    idfile_lines=idfile_ref.readlines()
    return idfile_lines

#*****************BOT INITIALIZATION*******************
bot_token_str=''  # Telegram Bot Token
bot = telegram.Bot(token=bot_token_str)

ID_Filename='Message_ID_File.txt'
#******************MAIN*************************
num_coins=130

R=4
loop_wait_time = 1800  # wait time in seconds
mute_period=4 #list resets every multiple of 4 day of the month



#*****************COIN INIT*****************************

coin_buy_list=[]
xyz=1
while xyz !=32:  # random variable/number so that the loop runs continuously (can be stopped by ctrl + c)
  
     # Get current coin information
    coinmarketcap = Market()
    coinmarketcap.ticker(start=0, limit=3)
    cmc_data_full=coinmarketcap.ticker(start=0, limit=num_coins)
    for ind0 in range(num_coins):
        ind0=ind0+1
        cmc_coin_data=cmc_data_full[ind0]
        coin_id=cmc_coin_data["id"]
        current_coin_price=float(cmc_coin_data["price_usd"])
        current_24vol=float(cmc_coin_data["24h_volume_usd"])
        coin_rank=float(cmc_coin_data["rank"])
        
    
        
        Signal_Threshold=1.6*math.pow(coin_rank, 0.2)  #Based on curve fitting (rank 0: 1.22, rank 20: 2.9...etc)
        
    #******************MAIN *************************
    
        coin_data_lists=get_coin_historical_data(coin_id)   # Get coin information from CMC
        
        historical_dates=coin_data_lists[0]
        historical_open_prices=coin_data_lists[1]
        historical_close_prices=coin_data_lists[2]
        historical_volumes=coin_data_lists[3]
        historical_indices=coin_data_lists[4]
        
    
        VN_avg=sum(historical_volumes[0:R])/R
        
        PN_avg=sum(historical_close_prices[0:R])/R # taking the last price or volume of the last R days
        
        if (VN_avg or PN_avg)!=0:
            VSI=current_24vol/VN_avg
            PSI=current_coin_price/PN_avg
        elif (VN_avg or PN_avg)==0:
            VSI=1
            PSI=1
        
        Current_Price_MA=(sum(historical_close_prices[0:R-1])+current_coin_price)/(R) # R-1 because we want to keep the same MA size, and dividing by R because we added the current element
        Previous_Price_MA=PN_avg
        PMA_Slope=Current_Price_MA-Previous_Price_MA
        
        VPSI=VSI/PSI * np.sign(PMA_Slope)    # multiplying it by slope so that we don't signal a buy when the price is declining (negative) and signal when price is increasing (positive)
        

    
    
    
        if VPSI > Signal_Threshold: 
            #send alert 
            print("buy " + coin_id + " at " + str(current_coin_price))   
            if coin_id not in coin_buy_list:
            
                if VPSI> (2*Signal_Threshold):
                    buy_signal_str="Strong Buy Signal"
                elif VPSI< (2*Signal_Threshold):
                    buy_signal_str="Buy Signal"
                #print("vn_avg=" + str(VN_avg) + "current volume= "+ str(current_24vol))
                #print("Past last 4 volume list="+ str(historical_volumes[0:R]))
                #print("pn_avg="+ str(PN_avg) + "Current price=" + str(current_coin_price))
                tel_message_string= "*******Pump Alert********* \n" + "Coin:" + coin_id + ", Current Price= " + str(current_coin_price)+"$"+ " Signal: " + buy_signal_str
            
                #bot.sendMessage(chat_id=490833773, text=tel_message_string)
                user_id_list=read_user_IDs(ID_Filename)
                for user_id_line in user_id_list:
                    bot.sendMessage(chat_id=user_id_line, text=tel_message_string)                
                coin_buy_list.append(coin_id)
                
    print(coin_buy_list)

    today = datetime.now()
    day_num=today.day
    hour_num=today.hour
    if day_num % mute_period ==0:  # resets the muted coins list every mute_period [days]
        if hour_num >0 and hour_num <3:
            coin_buy_list=[]
                
 
    print("Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') +"Coin: "+ coin_id + "Coin price=" + str(current_coin_price)+"$")
    
    time.sleep(loop_wait_time - ((time.time() - starttime) % loop_wait_time))












