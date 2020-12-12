from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button
import json,requests
from lxml import html
client = TelegramClient('api_creator', 1581224, 'bd891fcb8726cfbd64abc9ddbba2c8ff')
client.start()
a = dict()
def create_api(phone):
    body = 'phone={0}'.format(phone)
    try:
        response = requests.post('https://my.telegram.org/auth/send_password',data=body,headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
        s = json.loads(response.content)
        return s['random_hash']
    except:
        return False
def auth(phone,hash_code,pwd):
    data2 = "phone={0}&random_hash={1}&password={2}".format(phone,hash_code,pwd)
    responses = requests.post('https://my.telegram.org/auth/login',data=data2,headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
    try:
        return responses.cookies['stel_token']
    except:
        return False
def auth2(stel_token):
    resp = requests.get('https://my.telegram.org/apps',headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":"stel_token={0}".format(stel_token),"Cache-Control": "max-age=0",})
    tree = html.fromstring(resp.content)
    api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
    try:
        return '{0}:{1}'.format(api[0],api[1])
    except:
        s = resp.text.split('"/>')[0]
        value = s.split('<input type="hidden" name="hash" value="')[1]
        on = "hash={0}&app_title=Coded By Arash&app_shortname=Love Telegram&app_url=&app_platform=desktop&app_desc=".format(value)
        end1 = requests.post('https://my.telegram.org/apps/create',data=on,headers={"Cookie":"stel_token={0}".format(stel_token),"Origin": "https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*","Referer": "https://my.telegram.org/apps","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
        respv = requests.get('https://my.telegram.org/apps',headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":"stel_token={0}".format(stel_token),"Cache-Control": "max-age=0",})
        trees = html.fromstring(respv.content)
        apis = trees.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
        return '{0}:{1}'.format(apis[0],apis[1])
@client.on(events.NewMessage)
async def my_event_handler(event):
    if event.raw_text.lower() == '/start':
        await event.reply('**Welcome To My Bot Please Use Share Contact Button To Create API_ID and API_HASH :)**',buttons=[Button.request_phone('Send phone', resize=True, single_use=True)])
    elif event.raw_text.lower().startswith('code') and ':' in a[event.sender_id]:
        msg = await event.reply('**Please Wait ... **')
        key = a[event.sender_id]
        token = auth(key.split(':')[0],key.split(':')[1],event.raw_text.split('code ')[1])
        if token != False:
            api = auth2(token)
            await msg.edit('**Done Api Created Successfully !\nApi_ID : {}\nApi_Hash : {}**'.format(api.split(':')[0],api.split(':')[1]),buttons=[
         [Button.inline('Api_ID')],[Button.inline(api.split(':')[0])],
         [Button.inline('Api_Hash')],[Button.inline(api.split(':')[1])],
         [Button.inline('Account Phone')],[Button.inline(key.split(':')[0])],
         [Button.inline('Coded By @TelethonHelp')]
         ])
 
            a[event.sender_id] = None
        else:
            a[event.sender_id] = None
            await msg.edit('**Sorry We Have Some Errors Please Try Again Later ... **')
    elif event.media.phone_number != None:
        msg = await event.reply('**Please Wait...**')
        t_hash = create_api(event.media.phone_number)
        a[event.sender_id] = '{}:{}'.format(event.media.phone_number,t_hash)
        await msg.edit('**Done Code Sended Successfully ! Please Enter Code with this format\ncode** `YOURCODE`')
        
client.run_until_disconnected()






