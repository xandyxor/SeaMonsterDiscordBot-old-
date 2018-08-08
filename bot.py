import discord
from discord.ext import commands
from discord.utils import get
import datetime
import pandas as pd
import time,datetime
from datetime import datetime,timezone,timedelta

# 1.目前戰利品數量未與本地端csv文件同步(已同步)
# 2.很多地方有優化空間
# 3.尚未加入每個禮拜重製資料表的功能
# 4.目前只抓取discord的暱稱，並未與id同步，所以無密語查詢功能
# 5.大數處理上還是有問題= =
# 6.數字加上,方便瀏覽
# 7.目前將採取數字過大異常判斷


week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期日',
}
def whatdayistoday(n): 
    """n=0回傳年月日，n=其他數字，回傳星期幾""" 
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    local_dt = dt.astimezone(tzutc_8)
    today = (str(local_dt)[:10])#今天幾月幾號  '2018-08-08'
    if (n == 0):
        return today
    day = local_dt.weekday()
    return week_day_dict[day] #星期三


def updata2csv(name,day,val):
    """把金額存到csv檔案"""
    # df.set_value(name,dat,money)
    df = pd.read_csv("output.csv", delimiter=",",encoding='utf-8')
    df.fillna(0,inplace=True) #把nan取代成0
    # df.fillna(0)
    # print(df)

    for index, row in df.iterrows():#檢查表格上是否已經有使用者
        # print(row)
        if (row['name'] == name):   #如果已經存在表格上
            # df.loc[df['name'] == 'andy', "星期一"] = 12345  
            #查詢當天金額
            # int(df.loc[df['name'] == "Serapin", "星期一"])  
            # print("使用者已經存在表格上")

            temp = (df.loc[df['name'] == name, day])     
            # 這裡開始註解，因為已經採用替代所有nan的模式了，因此不需要再判斷是否是nan(省資源)
            # if (temp == temp).bool():#nan永不等於nan，因此拿如果自己不等於自己就代表此數為nan
            #     #不等於nan
            #     # val += int(df.loc[df['name'] == name, day])
            #     val += int(temp)
            #     # print("不等於nan")
            # else:
            #     #等於nan   就順便補0(實際上並不需要，因為下一步就是替他增加)(等待優化)
            #     df.loc[df['name'] == name, day] = 0
            #     # print("等於nan")            
            # df.loc[df['name'] == name, day] = val
            # 註解結束
            # print(df)

            print("int(val) + int(temp)",int(val), int(temp))

            df.loc[df['name'] == name, day] = (int(val) + int(temp))
            df.to_csv('output.csv',index=False,header=True,encoding='utf-8')
            print("使用者　"+name+"　於"+day+" 收入登記 "+ int(val) + int(temp)+" 進行存檔")
            return
    #迴圈跑完都沒有return 代表使用者未在表格上
    # marks.append({'name':"andy",'星期二':2468},ignore_index=True)
    # print(name,day,val)
    df = df.append({'name':name,day:val},ignore_index=True) #新增row
    # print(df)
    print("新增使用者　"+name+"　於"+day+" 收入登記 "+str(val)+" 進行存檔")
    df.to_csv('output.csv',index=False,header=True,encoding='utf-8')


# updata2csv('andy','星期二',5487)

def sum_money(user):
    """計算total金額"""
    df = pd.read_csv("output.csv", delimiter=",",encoding='utf-8')
    df.fillna(0,inplace=True) #把nan取代成0
    # df.fillna(0)
    # print(df)
    # print (df[['星期日','星期一','星期二','星期三','星期四','星期五','星期六']].sum(axis=1))
    # print(df.sum(axis=1))
    # df[df['name']=='Serapin'][['星期日','星期一','星期二','星期三','星期四','星期五','星期六']].sum(axis=1)

    # 不能直接使用sum()，因為pandes使用sum時用float運算，所以數字過大時會變成科學記號，造成python取值時資料爆裂
    # total = df[df['name'] == user][['星期日','星期一','星期二','星期三','星期四','星期五','星期六']].sum(axis=1)
    total = 0
    for column in df:
        if(column == 'name' or column == 'total'):
            continue
        # print(column)
        # print(int(df.loc[df['name'] == user,  column ]))
        total += int(df.loc[df['name'] == user,  column ])
    # print(total)
    # print(int(total))
    df.loc[df['name'] == user, 'total'] = str(total)
    # print(df)
    df.to_csv('output.csv',index=False,header=True,encoding='utf-8')

def total_money_search(name): #需要注意的是 目前此函數查詢總收入時是直接查詢total欄位
    """查詢該使用者的總金額"""
    df = pd.read_csv("output.csv", delimiter=",",encoding='utf-8')
    df.fillna(0,inplace=True) #把nan取代成0
    print("查詢該使用者的總金額",int(df.loc[df['name'] == name, "total"]))
    return int(df.loc[df['name'] == name, "total"])
    # 因為直接使用把nan取代成0的函數了，所以不需再重新判斷是否等於nan
    # temp = (df.loc[df['name'] == name, "total"])    
    # if (temp == temp).bool():#nan永不等於nan，因此拿如果自己不等於自己就代表此數為nan
    #     #不等於nan
    #     return int(df.loc[df['name'] == name, "total"])
    #     # print("不等於nan")
    # else:
    #     return -1

Trophydict = {'<:1000g:476274938395885568>': 0,'<:blue:476262599177011240>': 0, '<:red:476262607335063552>': 0, '<:skin:476262626519941120>': 0 ,'<:tooth:476262644287012865>': 0 ,'<:nashark:476262658669281294>' : 0,'<:Carapace:476262683189182464>' : 0,'<:coin:476262700532367371>':0}
#rows ('<:blue:476262599177011240>', '10', '<:red:476262607335063552>', '20')
Trophydict_2_ch = {
    '<:1000g:476274938395885568>' : '金塊1000g',
    '<:blue:476262599177011240>' : '怪獸內丹',
    '<:red:476262607335063552>' : '赫卡魯的突起',
    '<:skin:476262626519941120>' : '漂流追蹤者的外皮',
    '<:tooth:476262644287012865>' : '幽冥鐵牙的顎骨',
    '<:nashark:476262658669281294>' : '納恩薩克的角破片',
    '<:Carapace:476262683189182464>' : '坎迪杜姆的甲殼',
    '<:coin:476262700532367371>' : '古德蒙特海賊團的金幣'
}
Trophydict_2_em = {
    '金塊1000g' :'<:1000g:476274938395885568>' ,
    '怪獸內丹'  :'<:blue:476262599177011240>' ,
    '赫卡魯的突起':'<:red:476262607335063552>',
    '漂流追蹤者的外皮'  :'<:skin:476262626519941120>',
    '幽冥鐵牙的顎骨' :'<:tooth:476262644287012865>' ,
    '納恩薩克的角破片'  :'<:nashark:476262658669281294>' ,
    '坎迪杜姆的甲殼':'<:Carapace:476262683189182464>',
    '古德蒙特海賊團的金幣'  :'<:coin:476262700532367371>'
}

def sysnTrophy(day):
    """把csv檔案上面的海怪物品傳到Trophydict裡面"""
    df = pd.read_csv("Trophy.csv", delimiter=",",encoding='utf-8')
    df.fillna(0,inplace=True) #把nan取代成0
    for column in df:        
        if(column == 'day'):
            continue
        # print(Trophydict_2_em[column])
        # print(df[column].sum())
        # Trophydict[Trophydict_2_em[column]]=df[column].sum()
        # pandas的sum()是用float計算的因此數字過大時會變成科學記號取出來就強轉int時會出錯垃圾東西
        Trophydict[Trophydict_2_em[column]] = int(df.loc[df['day'] == day, column ])

def addTrophy(rows):  #登記戰利品
    """登記戰利品"""
    df = pd.read_csv("Trophy.csv", delimiter=",",encoding='utf-8')   
    df.fillna(0,inplace=True) #把nan取代成0
    today = whatdayistoday(0)   # today = '2018-08-08'
    for i in range(0,len(rows)):
#         print(rows[i])    
        if(i%2==0):#戰利品
            Trophydict[rows[i]] = rows[i+1]
            # print(today,rows[i],rows[i+1])
            addTrophy2csv(today,rows[i],rows[i+1])
            # 2018-08-07 <:blue:476262599177011240> 10
            # 2018-08-07 <:red:476262607335063552> 20
        # df.set_value(name,dat,money)不好用
#     print(df)

def addTrophy2csv(today,id,num): #把戰利品存到csv檔
    """把戰利品存到csv檔"""
    df = pd.read_csv("Trophy.csv", delimiter=",",encoding='utf-8')  
    df.fillna(0,inplace=True) #把nan取代成0

    for index, row in df.iterrows():#檢查表格上是否有當日紀錄
        # print(row)
        if (row['day'] == today):   #如果已經存在表格上
            #查詢戰利品數量
            # int(df.loc[df['day'] == "2018-08-07", "怪獸內丹"])  
            temp = (df.loc[df['day'] == today,  Trophydict_2_ch[id]])
#             print(int(temp),num)

            #從這裡開始(此為自行判斷是否nan的程式碼)
            # if (temp == temp).bool():#nan永不等於nan，因此拿如果自己不等於自己就代表此數為nan
            #     #不等於nan
            #     # num += int(df.loc[df['name'] == name, day])
            #     # print("num:",int(num),"temp",int(temp))
            #     num = int(num) + int(temp)
            #     # print("不等於nan")
            # else:
            #     #等於nan   就順便補0(實際上並不需要，因為下一步就是替他增加)(等待優化)
            #     df.loc[df['day'] == today, Trophydict_2_ch[id]] = 0
            #     # print("等於nan")                
            # df.loc[df['day'] == today, Trophydict_2_ch[id]] = num
            #結束註解
            print("把戰利品存到csv檔",(int(num) + int(temp)))
            df.loc[df['day'] == today, Trophydict_2_ch[id]] = (int(num) + int(temp)) #原本的加上新增的
            # print(df)
            df.to_csv('Trophy.csv',index=False,header=True,encoding='utf-8')
            # print(day+"+" 戰利品登記 "+str(num)+" 進行存檔中")
            return
    #迴圈跑完都沒有return 代表當日未在表格上有任何紀錄
    # print(name,day,num)
    # df = df.append({'day':'2018-08-07', '怪獸內丹': 10 },ignore_index=True) #新增row
    df = df.append({'day':today, Trophydict_2_ch[id]:num},ignore_index=True) #新增row
    # print(df)
    # print("新增使用者　"+name+"　於"+day+" 收入登記 "+str(num)+" 進行存檔中")
    df.to_csv('Trophy.csv',index=False,header=True,encoding='utf-8')




TOKEN = '{ur TOKEN}'

description = '''Bot in Python'''
bot = commands.Bot(command_prefix='$', description=description)

print (whatdayistoday(0), whatdayistoday(1)) #2018-08-08 星期三
print("hi 你好 本呆呆機器人將為您服務")


sysnTrophy(whatdayistoday(0))   #把csv上當天的海怪物品數量更新到字典上

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def hello(ctx):
    """Says world"""    
    await bot.say('hi {}'.format(ctx.message.author.display_name))    
    # await bot.say('hi {}'.format(ctx.message.channel))    #hi bot-test測試頻道


@bot.command(pass_context=True)
async def test(ctx,*args):
    print(ctx.message.author.display_name)
    print('{} arguments: {}'.format(len(args), ', '.join(args)))
    await bot.say('{} arguments: {}'.format(len(args), ', '.join(args)))
    total = 0 #輸入總金額
    print(args)

    
@bot.command(pass_context=True)
async def check(ctx):
    """輸出當天總戰利品數量""" 
    sysnTrophy(whatdayistoday(0))   #把csv檔案上的海怪物品更新到字典上
    await bot.say('hi {}'.format(ctx.message.author.display_name))    
    send_msg_text=""
    for i in Trophydict:
        send_msg_text += Trophydict_2_ch[i] +" "+ i +" "+ str(Trophydict[i])+'\n'
    await bot.say(send_msg_text)
    print(ctx.message.author.display_name+"使用本系統查詢了當日目前的戰利品總數量")

# @bot.command(pass_context=True)
# async def ckday(ctx,*args):
#     """輸出某一天總戰利品數量""" 
#     if (len(args)!=1 or args[0]>7 or args[0]<0):
#         await bot.say('請在ckday(這裡)輸入要查詢的天數喔,0~6分別代表星期日~星期六')   
#         return
#     #
#     sysnTrophy(week_day_dict[args[0]])   #把csv檔案上的海怪物品更新到字典上 
#     send_msg_text=""
#     for i in Trophydict:
#         send_msg_text += Trophydict_2_ch[i] +" "+ i +" "+ str(Trophydict[i])+'\n'
#     await bot.say(send_msg_text)
#     print(ctx.message.author.display_name+"使用本系統查詢了當日目前的戰利品總數量")
#     sysnTrophy(whatdayistoday(0))   #把csv檔案上的海怪物品更新到字典上 

@bot.command(pass_context=True)
async def total(ctx):
    """查詢玩家一個禮拜以來的總收入"""    
    # await bot.say('hi {}'.format(ctx.message.author.display_name))
    display_name = str(ctx.message.author.display_name)
    total_money = total_money_search(display_name)

    if (total_money <= 0):
        print(display_name+" 查詢收入失敗，因為當天為有收入")
        await bot.say("還沒有收入喔")
    elif (total_money > 0):
        print(display_name+" 的收入是:"+str(total_money))
        await bot.say("hi "+display_name+" 你的收入是:"+str(total_money))


@bot.command(pass_context=True)
async def Backup(ctx):
    """檔案備份指令"""    
    print(ctx.message.author.display_name+"使用了備份指令")
    await bot.say('hi {} start Backup'.format(ctx.message.author.display_name))
    await bot.send_file(ctx.message.channel, 'output.csv')
    await bot.send_file(ctx.message.channel, 'Trophy.csv')

@bot.command(pass_context=True)
async def eat(ctx,*args):
    bot_message_channel = str(ctx.message.channel) #判斷是否在指定伺服器頻道裡面
    display_name = str(ctx.message.author.display_name)

    if( bot_message_channel == "bot-test測試頻道") or (bot_message_channel == "bot公開測試頻道"):   #判斷是否在指定伺服器頻道裡面
        print(display_name)
        print('{} arguments: {}'.format(len(args), ', '.join(args)))
        await bot.say('{} arguments: {}'.format(len(args), ', '.join(args)))
    else:
        await bot.say('不好意思喔 這裡不是授權的頻道')
        print('這裡不是授權的頻道',str(ctx.message.channel))
        return

    if(len(args)%2 != 0):
        print("輸入錯誤 資料不對襯")
        await bot.say("輸入錯誤 別亂餵我好嗎?")
        return

    total = 0 #輸入總金額
    for i in range(0,len(args)):
        # print(args[i])
        if( len(args) >= 2):
            # if(i < len(args)-1): #意義不明 先註解好了
            if ((i % 2) == 0):  # i%2==0 代表戰利品欄位(單數0,2,4,6,8) i+1代表數量(雙數1,3,5,7)
                if(args[i+1].isdigit()):    #如果數量欄位(1,3,5,7)是數字  

                    if( int(args[i+1]) > 1000000 or int(args[i+1]) <= 0 ):
                        print("數量異常")
                        await bot.say("數量異常 最好別亂輸入喔")
                        return             

                    if (emojis2money(args[i]) == -1):
                        print("戰利品欄位錯誤")
                        await bot.say("戰利品欄位錯誤，必須是戰利品表情符號")
                        return
                    elif (emojis2money(args[i]) != -1):
                        total += emojis2money(args[i])*int(args[i+1]) #物品價錢*數量
                elif(args[i+1].isdigit() == False): #如果數量欄位(1,3,5,7)不是數字
                    print("數量錯誤，必須是數字"+args[i]+args[i+1])
                    await bot.say("數量錯誤，必須是數字")
                    return
        else:
            print('len(args) 必須大於 2')
            await bot.say("別耍我喔ˋˊ")
            return

    addTrophy(args)#把戰利品存入Trophy.csv
    print(display_name+" today("+ whatdayistoday(1) +") ur inpurt money:"+str(total))
    await bot.say("hi "+display_name+" today("+ whatdayistoday(1) +") ur inpurt money:"+str(total))
    updata2csv(display_name,whatdayistoday(1),total)#把收入存入output.csv
    sum_money(display_name)#計算總收入

def emojis2money(emojis):
    if emojis =="<:1000g:476274938395885568>":
        return 100000000
    if emojis == "<:blue:476262599177011240>":
        return 100000
    if emojis == "<:red:476262607335063552>":
        return 82000
    if emojis == "<:skin:476262626519941120>":
        return 42800
    if emojis == "<:tooth:476262644287012865>":
        return 52400
    if emojis == "<:nashark:476262658669281294>":
        return 53700
    if emojis == "<:Carapace:476262683189182464>":
        return 409200
    if emojis == "<:coin:476262700532367371>":
        return 100000

    # print("戰利品欄位錯誤!")
    return -1

bot.run(TOKEN)

# ('<:1000g:476274938395885568>', 
# '<:blue:476262599177011240>', 
# '<:Carapace:476262683189182464>', 
# '<:coin:476262700532367371>', 
# '<:nashark:476262658669281294>', 
# '<:nashark:476262658669281294>', 
# '<:red:476262607335063552>', 
# '<:skin:476262626519941120>', 
# '<:tooth:476262644287012865>')