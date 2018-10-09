# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

##INPUT QR CODE

#new_qr = "123123121212123"  

## DRAW DATA FROM GOOGLE SHEET

def access_gsheet():

    scope = ['https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project 3977-ed1ac165f75d.json',scope)
    
    gc = gspread.authorize(credentials)
    
    wks = gc.open('test').sheet1
    
    return(pd.DataFrame(wks.get_all_records()))     
        
## BASH WHETHER QR CODE HAS BEEN PREVIOUSLY ENTERED
    
#print(result)
    
## RECORD NEW ENTRY IF NECCESSARY
def record_qr(new_qr):
    scope = ['https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project 3977-ed1ac165f75d.json',scope)
    
    gc = gspread.authorize(credentials)
    
    wks = gc.open('test').sheet1
    
    new_row = len(wks.col_values(1))+1
    
    wks.update_cell(new_row, 1, new_qr)
    wks.update_cell(new_row, 2, str(datetime.datetime.now())) #timenow
    wks.update_cell(new_row, 3, 'Hong Kong Station') 
    print('Record Updated \n Please provide a ticket to this Client.')
    
## PRINT ALL RECORDS (IF YES)
def pipeline(new_qr):
    df = access_gsheet()
    result=[]
    
    for i in range(len(df["QR Code"])):
        if str((df["QR Code"].iloc[i])) == new_qr or ((df["QR Code"].iloc[i])) == int(new_qr):
            result.append(i)
        else:
            #print("no matched record in row {}".format(i))
            pass
    
    for i in range(len(result)):
        result [i] = [str(df.iloc[i,0]), str(df.iloc[i,1]), (df.iloc[i,2])]
    
    #print ((result)) 
    if len(result) == 2:
        print ("This Client has previously redeemed 2 tickets.\n This Client is no longer entitled to redeem any more tickets. \n First time: at {} at {}\n Second Time: at {} at {}.".format(result[0][0],result[0][2],result[1][0],result[1][2]))
    elif len(result) == 1:
        print ("This Client has previously redeemed 1 ticket.\n First time: at {} at {}.".format(result[0][0],result[0][2]))
        record_qr(new_qr)
    elif len(result) == 0:
        print ("This Client has NOT previously redeemed any ticket.")
        record_qr(new_qr)
    else:
        print ("Error! This Client has previously redeemed MORE THAN 2 tickets. \n First time: at {} at {}\n Second Time: at {} at {}. \n Please notify TDC staff on this.".format(result[0][0],result[0][2],result[1][0],result[1][2]))

## RECORD NEW ENTRY
while True:
    new_qr = str(input("Please enter the QR Code: "))
    #need to add a line to ensure all are digits
    if len(new_qr) is 15:
        pipeline(new_qr)
    elif new_qr == 'terminate':
        break
    elif new_qr == 'help':
        print('A. the QR code must be 15 digits \nB. Any questions please call TDC Staff at 2240 4622. \c ')
    else:
        print("Error!")
        





    