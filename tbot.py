# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import altair
import pandas as pd
from altair import Chart
from flask import Flask, request
import telegram
import json
import datetime 
from datetime import timedelta
import mysql.connector
from mysql.connector import errorcode
import pygal    
from pygal.style import DarkStyle                                                   # First import pygal



app = Flask(__name__)
app.debug = True
TOKEN = '*******'
configdb = {
  'user': '****',
  'password': '****',
  'host': '127.0.0.1',
  'database': 'botstat',
  'raise_on_warnings': True,}

useru  = []
dlina = []

global bot 
bot = telegram.Bot(token=TOKEN)

URL = '******'



def our_time():
    common_our_time = ct = str(datetime.datetime.now() - datetime.datetime(2017,3,14,20,14)).partition('.')[0]
    return common_our_time


def sql_text_insert(date, chatid, userid, username, textlen, wordc):
    cnx = mysql.connector.connect(**configdb)
    cursor = cnx.cursor()
    add_dat = ("INSERT INTO groupstat "
               "(date, chatid, userid, username, textlen, wordc) "
               "VALUES ( %s, %s, %s, %s, %s, %s)")
    data_test = ( date, chatid, userid, username, textlen, wordc)
    cursor.execute(add_dat , data_test)
    cnx.commit()
    cursor.close()
    cnx.close()

def sql_sticker_insert(chatid, userid, username):
    cnx = mysql.connector.connect(**configdb)
    cursor = cnx.cursor()
    add_dat = ("INSERT INTO sticker "
               "(chatid, userid, username) "
               "VALUES ( %s, %s, %s )")
    data_test = (chatid, userid, username)
    cursor.execute(add_dat , data_test)
    cnx.commit()
    cursor.close()
    cnx.close()

def sql_pictures_insert(chatid, userid, username):
    cnx = mysql.connector.connect(**configdb)
    cursor = cnx.cursor()
    add_dat = ("INSERT INTO pic "
               "(chatid, userid, username) "
               "VALUES ( %s, %s, %s )")
    data_test = (chatid, userid, username)
    cursor.execute(add_dat , data_test)
    cnx.commit()
    cursor.close()
    cnx.close()

def sql_voice_insert(chatid, userid, username,voice_len):
    cnx = mysql.connector.connect(**configdb)
    cursor = cnx.cursor()
    add_dat = ("INSERT INTO voice "
               "(chatid, userid, username ,voicelen) "
               "VALUES ( %s, %s, %s, %s )")
    data_test = (chatid, userid, username,voice_len)
    cursor.execute(add_dat , data_test)
    cnx.commit()
    cursor.close()
    cnx.close()




def sql_text_zapros(lol):
    useru = []
    cnx = mysql.connector.connect(**configdb)
    cursor = cnx.cursor(buffered=True)
    query = ("SELECT userid , sum(textlen) as textsum,   sum(wordc) as wordsum , count(chatid) as msgsum  FROM "
    "(SELECT chatid,userid,textlen,wordc FROM groupstat WHERE chatid = %s )"
    "AS results GROUP BY userid")
    
    cursor.execute(query , (lol,))
    #cursor.execute("SELECT userid , sum(textlen) as textsum,   sum(wordc) as wordsum , count(chatid) as msgsum  FROM ( SELECT chatid,userid,textlen,wordc FROM groupstat WHERE chatid=%s ) AS results GROUP BY userid" , (40590037) )
    for  ( userid , textsum, wordsum,msgsum) in cursor:
        useru.append(userid)
        useru.append(int(textsum))
        useru.append(int(wordsum))
        useru.append(msgsum)
    cursor.close()
    cnx.close()
    print(useru)
    a = int(len(useru) /4)
    b = 0
    pie_chart = pygal.Pie(print_values=True,style=DarkStyle(value_font_family='googlefont:Raleway',value_font_size=30,value_colors=('white',)))
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    for i in range(int(len(useru) /4)):
      pie_chart.add(useru[b], useru[b+1])
      b += 4
    pie_chart.render_to_png('/home/devorn/tbot/tbotp/plz.png')
   

    

    


# def ch_stick(chatid, userid, username):
#     cnx = mysql.connector.connect(**configdb)
#     cursor = cnx.cursor()
#     add_dat = ("INSERT INTO pic "
#                "(chatid, userid, username) "
#                "VALUES ( %s, %s, %s)")
#     data_test = ( chatid, userid, username)
#     cursor.execute(add_dat , data_test)
#     cnx.commit()
#     cursor.close()
#     cnx.close()

def sql_voice_stat():
    global useru_voice
    useru_voice = []
    global dlina_voice
    dlina_voice = [] 
    cnx = mysql.connector.connect(**configdb)
    cursor = cnx.cursor(buffered=True)
    query = ("SELECT userid,  sum(voicelen) AS kol FROM voice WHERE chatid = '-286266472' GROUP BY userid;")
    cursor.execute(query)
    for userid , dlina in cursor:
        useru_voice.append(userid.format())
        dlina_voice.append(int(dlina))
    cursor.close()
    cnx.close()


#set_webhook 
@app.route('/set_webhook', methods=['GET', 'POST']) 
def set_webhook(): 
    s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/server.crt', 'rb')) 
    if s:
        print(s)
        return "webhook setup ok" 
    else: 
        return "webhook setup failed" 

@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
    if request.method == "POST": 
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        #chart.savechart('/homde/devorn/test_loooh.png')
        try:
            chat_id = update.message.chat.id
            date = update.message.date
            userid = update.message.from_user.id
            username = update.message.from_user.username
            if update.message.text != None:
                text = update.message.text
                text_len = str(len(text))
                text_word = str(len(str(text).split(' ')))
                if text == "/timetogether@DrQueen_bot" or text == "/timetogether":    
                    bot.send_message(chat_id=chat_id, text=str(our_time()))
                elif text == "/getstat":
                    sql_text_zapros(chat_id)
                    bot.send_photo(chat_id=chat_id, photo=open('/home/devorn/tbot/tbotp/plz.png', 'rb'))               
                else:
                    sql_text_insert(date,chat_id,userid,username,text_len,text_word)
            elif update.message.text == None :
                if update.message.sticker != None:
                    sql_sticker_insert(chat_id, userid, username)
                elif update.message.voice != None:
                    voice_len = update.message.voice.duration
                    sql_voice_insert(chat_id, userid, username, voice_len)
                elif update.message.photo[0] != None:
                    sql_pictures_insert(chat_id, userid, username)
                    bot.send_message(chat_id=chat_id, text='')


        except Exception as e:
            print(e)
    return 'ok'






