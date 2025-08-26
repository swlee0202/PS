import discord
import json
import os
import random
import asyncio
import time

# 업글 추가하는 방법:
# 2. default_data 추가
# 3. upgtypes 추가
# 4. chk_mes 추가
# 5. 업그레이드에 요소 추가

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ---------------------------
# 유저 데이터 관리
# ---------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_FILE = os.path.join(BASE_DIR, "userdata.json")

# # 기존 데이터 불러오기
# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         users = json.load(f)
#         users = {int(k): v for k, v in users.items()}
# else:
#     users = {}

# def save_data():
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(users, f, ensure_ascii=False, indent=2)
import redis

REDIS_URL = "redis://default:nECqwNkLHVKjNYzgQERmztnrRxgjQBie@centerbeam.proxy.rlwy.net:53835"
r = redis.from_url(REDIS_URL, decode_responses=True)

default_data = {
    "affection": 0,
    "reinforce": 0,
    "coin": 100,
    "prot": 0,
    "selllv": 0,
    "reinlv": 0,
    "critlv": 0,
    "cointime": 0,
    "reintime": 0
}

def get_user(user_id: int):
    key = f"user:{user_id}"
    data = r.get(key)
    if data:
        return json.loads(data)
    else:
        u = default_data.copy()
        save_user(user_id, u)
        return u

def save_user(user_id: int, data: dict):
    key = f"user:{user_id}"
    r.set(key, json.dumps(data))







# ---------------------------
# 명령어 리스트
# ---------------------------
welcome = ['테토야 ㅎㅇ','ㅌ ㅎㅇ','테토야 안녕','ㅌ 안녕']
affec   = ['테토야 호감도','ㅌ 호감도']
rein    = ['테토야 강화','ㅌ 강화']
sell    = ['테토야 판매','ㅌ 판매']
check   = ['테토야 내정보', 'ㅌ 내정보', '테토야 현황', 'ㅌ 현황']
upgrade = ['테토야 업그레이드', 'ㅌ 업그레이드', '테토야 업글', 'ㅌ 업글']
hlp     = ['테토야 도움말', 'ㅌ 도움말']
gimmecoin = ['테토야 코인','ㅌ 코인']
protect = ['테토야 보호', 'ㅌ 보호']
buy     = ['테토야 상점','ㅌ 상점']
mes = ['검 강화에 성공했습니다','검이 파괴되었습니다','검 강화에 실패했습니다','검 강화 크리티컬! :tada:']
color = [0xFFAD3B, 0x000000, 0xFF0000, 0xFFFF10]
spos=[
    100, 94, 88, 83, 78, 74, 70, 67, 64, 61,
    59, 57, 55, 53, 51, 49, 47, 45, 43, 41,
    39, 37, 36, 34, 33, 31, 30, 28, 27, 25,
    24, 22, 21, 19, 18, 16, 15, 14, 13, 12,
    11, 10, 9, 8, 7, 6, 5, 4, 3, 2,
    1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9
]
bpos=[
    0, 0, 0, 1, 1, 1, 2, 2, 2, 3,
    3, 3, 4, 4, 4, 5, 5, 5, 6, 6,
    6, 7, 7, 8, 8, 9, 9, 10, 10, 10,
    10, 10, 11, 11, 11, 11, 12, 12, 12, 12,
    13, 13, 13, 14, 14, 14, 15, 15, 15, 15,
    16, 16, 16, 17, 17, 17, 18, 18, 18, 18,
    19, 19, 19, 20, 20, 20, 21, 21, 22, 22
]
default_data= {
    "affection": 0,
    "reinforce": 0,
    "coin": 100,
    "prot": 0,
    "selllv": 0,
    "reinlv": 0,
    "critlv": 0,
    "cointime": 0,
    "reintime": 0
}
toprot=False

MAXLV=min(len(spos),len(bpos))
upgtypes={"reinlv":"성공 확률 강화","selllv":"판매 가격 강화","critlv":"크리티컬 확률 강화"}

# ---------------------------
# 함수
# ---------------------------
def rnd(i,j):
    return random.randint(i,j)


# ---------------------------
# 이벤트 핸들러
# ---------------------------
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    
    
    if message.author == client.user:
        return
    user_id = message.author.id
    input = message.content
    global toprot
# -------------------------------------------------
# -------------------------------------------------
    def send_rein(type,lv,aft,user_id):
        sucpos=max(0,min(spos[lv]+user["reinlv"],100))
        critpos=min(1,max(0,(5+user["critlv"]-(lv//6))/100))
        brkpos=min(100,max(0,bpos[lv]))
        touse=int(((beflv/8)**2+1))*(lv-aft)
        basemes=f"""\
{message.author.name}님의 {mes[type]}
{lv}레벨 -> {aft}레벨
현재 보유 코인 : {user["coin"]}

**확률**
크리티컬: {round(sucpos*(critpos),4)}%
성공: {round(sucpos*(1-critpos),4)}%
실패: {round(100 - min(brkpos,100-sucpos) - sucpos,4)}%
파괴: {round(max(0,min(brkpos,100-sucpos)),4)}%"""
        if type in [1,2]:
            basemes+=f"""

**테토야 보호** 또는 **ㅌ 보호**로 보호권을 사용해 레벨을 복구할 수 있어요!
보호권은 총 {touse}개 필요해요
현재 보유 보호권 : {user["prot"]}개
"""
        embed = discord.Embed(
        description=basemes,
        color=color[type]
        )
        return embed
# -------------------------------------------------
    def chk_mes(user_id):
        embed = discord.Embed(
        description=f"""\
{message.author.name}님의 검 :
{user["reinforce"]}레벨

업그레이드 현황 :
1. {upgtypes["reinlv"]} : {user["reinlv"]} 레벨
2. {upgtypes["selllv"]} : {user["selllv"]} 레벨
3. {upgtypes["critlv"]} : {user["critlv"]} 레벨

현재 보유 코인 : {user["coin"]}코인
현재 보유 보호권 : {user["prot"]}개""",
        color=0x87CEEB
        )
        return embed
# -------------------------------------------------
    def whatupgprint(user_id):
        embed = discord.Embed(
        description=f"""\
무엇을 업그레이드 하실건가요? 원하는 업그레이드의 숫자를 입력해 주세요
1. {upgtypes["reinlv"]} : {user["reinlv"]}레벨, 업그레이드 비용 : {int((user["reinlv"]+1)**0.8*100+(user["reinlv"]+1)**2*3)} 코인
2. {upgtypes["selllv"]} : {user["selllv"]}레벨, 업그레이드 비용 : {int((user["selllv"]+1)**2*100+(user["selllv"]+1)**3*10)} 코인
3. {upgtypes["critlv"]} : {user["critlv"]}레벨, 업그레이드 비용 : {int((user["critlv"]+1)**2.5*30)} 코인

현재 보유 코인 : {user["coin"]}""",
        color=0x87CEEB
        )
        return embed
# -------------------------------------------------
    def upgprint(type,user_id):
        embed = discord.Embed(
        description=f"""\
업그레이드 성공!
{upgtypes[type]} : {user[type]-1}레벨 -> {user[type]} 레벨

현재 보유 코인 : {user["coin"]}""",
        color=0x87CEEB
        )
        return embed
# -------------------------------------------------
    def sucprot(user_id,beflv,used):
        embed = discord.Embed(
        description=f"""\
보호권 {used}개 사용 성공!
{beflv}레벨 -> {user["reinforce"]} 레벨

현재 보유 보호권 : {user["prot"]}""",
        color=0x87CEEB
        )
        return embed
# -------------------------------------------------
    def howmanybuy(user_id):
        mes = discord.Embed(description=f"""\
원하는 물건의 번호와 개수를 띄어쓰기로 구분해 입력해 주세요
1. 보호권 1개 가격 : 20코인
현재 보유 보호권 : {user["prot"]}

현재 보유 코인 : {user["coin"]}""",color=0x87CEEB)
        return mes
# -------------------------------------------------
# -------------------------------------------------

    
    # 코인 임의 추가
    # if message.content.startswith('테토야 add'):
    #     toadd_id = message.content.split()[2].strip()
    #     users[toadd_id]["coin"] += 100
    #     await message.reply('코인 지급 완료')
    
###################################################################################################################################
#################################################        명령어 구간         ########################################################
###################################################################################################################################

    if message.content.startswith('테토야') or message.content.startswith('ㅌ'):
        save_user(user_id, user)
        
        # 유저 정보 초기화 (처음 보는 유저라면)
        user = get_user(user_id)
        
        if input == '테토야':
            await message.reply('네?')
        
        if input in hlp:
            await message.reply(embed=discord.Embed(description="""안녕하세요! 저를 어떻게 쓰는지 알려드릴게요
    저를 부를 때는 '테토야' 하고 부를 수 있고, 줄여서 'ㅌ'이라고도 가능해요
    지금 사용할 수 있는 기능은 다음과 같아요
    강화, 판매, 내정보, 현황, 도움말, 업그레이드, 업글, 상점, 코인
    """,color=0x87CEEB))

        # 호감도 자동 누적
        user["affection"] += 1
        save_user(user_id, user)


        # 인사
        if input in welcome:
            await message.reply('안녕하세요!')

        # 호감도 확인
        if input in affec:
            score = user["affection"]
            await message.reply(f"{message.author.name}님의 호감도는 {score} 입니다!")

        # 정보확인
        if input in check:
            tosend=chk_mes(user_id)
            await message.reply(embed=tosend)

        # 돈내놔
        if input in gimmecoin:
            now = time.time()
            last_time = user["cointime"]
            if now - last_time < 180:  # 3분 = 180초
                remain = int(180 - (now - last_time))
                await message.reply(f"아직 쿨타임이에요! {remain}초 후에 다시 시도하세요.")
            else:
                user["coin"] += min(300,50*(user["reinlv"]+1))
                user["cointime"] = now
                await message.reply(f"{min(300,50*(user["reinlv"]+1))}코인을 드렸어요!\n현재 보유 금액: {user['coin']}코인")
        
        # 판매
        if input in sell:
            if user["reinforce"]>=5:
                toadd = int(user["reinforce"]**(2.2+1.9*(1-1.04**-user["selllv"])))
                user["coin"] += toadd
                embed = discord.Embed(
            description=f"""{message.author.name}님의 {user["reinforce"]}레벨 검이 판매되었습니다!
    코인 + {toadd}
    현재 보유 금액 : {user["coin"]}""",
            color=0x00ff00
        )
                await message.reply(embed=embed)
                user["reinforce"] = 0
            else:
                await message.reply("5레벨 이상부터 판매 가능해요!")
            save_user(user_id, user)


        # 구매
        if input in buy:
            if user["reinforce"] == 0:
                tosend = howmanybuy(user_id)
                await message.reply(embed=tosend)
                def checkk(m):
                    return m.author == message.author and m.channel == message.channel
                try:
                    reply = await client.wait_for("message", timeout=15.0, check=checkk)
                    q=list(reply.content.split())
                    if len(q)==2:
                        num,cnt=q[0],q[1]
                        if num == '1':
                            cnt=int(cnt)
                            price = 20*cnt
                            if user["coin"] < price:
                                await message.reply("코인이 부족해요")
                            else:
                                user["prot"] += cnt
                                user["coin"] -= price
                                await message.reply(f"보호권을 성공적으로 구매했어요!\n현재 보유 보호권 : {user["prot"]}\n현재 보유 코인 : {user["coin"]} ")
                        else:
                            await message.reply("물건 구매를 취소했어요")
                    else:
                        await message.reply("물건 구매를 취소했어요")
                except asyncio.TimeoutError:
                    await message.reply("물건 구매를 취소했어요")
            else:
                await message.reply("검 레벨이 0일때만 가능해요")
        
        # 강화
        if input in rein:
            now = time.time()
            last_time = user["reintime"]
            if now - last_time < 7:  # 10초
                remain = int(7 - (now - last_time))
                await message.reply(f"아직 쿨타임이에요! {remain}초 후에 다시 시도하세요.")
            else:
                user["reintime"] = now
                lv=user["reinforce"]
                if lv>=MAXLV:
                    await message.reply(
                        f"이미 최대 레벨입니다!"
                    )
                else:
                    price = int((user["reinforce"]*17)**0.6)
                    if user["coin"]<price:
                        await message.reply(f"코인이 부족합니다!\n현재 보유 코인 : {user["coin"]}  필요한 코인 : {price}")
                    else:
                        user["coin"] -= price
                        beflv=lv
                        pos=rnd(1,100)
                        sucpos=max(0,min(spos[lv]+user["reinlv"],100))
                        brkpos=min(bpos[lv],100-sucpos)
                        if pos<=sucpos:
                            pos=rnd(1,100)
                            if pos<=min(100,max(0,(5+user["critlv"]-(lv//6)))):#크리, type = 3
                                user["reinforce"] += 3
                                tosend=send_rein(3,beflv,user['reinforce'],user_id)
                                await message.reply(embed=tosend)
                            else:#성공, type = 0
                                user["reinforce"] += 1
                                tosend=send_rein(0,beflv,user['reinforce'],user_id)
                                await message.reply(embed=tosend)
                        elif pos<=sucpos+brkpos: # 파괴, type = 1
                            user["reinforce"] -= 3
                            if user["reinforce"]<0:
                                user["reinforce"] = 0
                            tosend=send_rein(1,beflv,user['reinforce'],user_id)
                            await message.reply(embed=tosend)
                        else: #실패, type = 2
                            user["reinforce"] -= 1
                            if user["reinforce"]<0:
                                user["reinforce"] = 0
                            tosend=send_rein(2,beflv,user['reinforce'],user_id)
                            await message.reply(embed=tosend)
                            
                        # 보호권 사용
                        if beflv>user["reinforce"]:
                            toprot=True
                            def checkk(m):
                                return m.author == message.author and m.channel == message.channel
                            try:
                                dec=beflv-user["reinforce"]
                                reply = await client.wait_for("message", timeout=60.0, check=checkk)
                                if reply.content in protect:
                                    touse = int(((beflv/8)**2+1))*dec
                                    if user["prot"]>=touse:
                                        user["prot"] -= touse
                                        user["reinforce"] += dec
                                        tosend = sucprot(user_id,beflv-dec,touse)
                                        await message.reply(embed=tosend)
                                    else:
                                        await message.reply("보호권이 부족해요")
                                    toprot=False
                                else:
                                    if toprot:
                                        await message.reply("보호권을 사용하지 않았어요")
                                        toprot=False
                            except asyncio.TimeoutError:
                                if toprot:
                                    toprot=False
                                    await message.reply("보호권을 사용하지 않았어요")
                    save_user(user_id, user)
        
        # 업그레이드
        
        if input in upgrade:
            tosend = whatupgprint(user_id)
            await message.reply(embed=tosend)

            def checkk(m):
                return m.author == message.author and m.channel == message.channel

            try:
                reply = await client.wait_for("message", timeout=15.0, check=checkk)
                if reply.content == "1":
                    price = int((user["reinlv"]+1)**0.8*100+(user["reinlv"]+1)**2*3)
                    if user["coin"] < price:
                        await message.reply("코인이 부족해요")
                    else:
                        user["reinlv"] += 1
                        user["coin"] -= price
                        tosend = upgprint("reinlv", user_id)
                        await message.reply(embed=tosend)
                elif reply.content == "2":
                    price = int((user["selllv"]+1)**2*100+(user["selllv"]+1)**3*10)
                    if user["coin"] < price:
                        await message.reply("코인이 부족해요")
                    else:
                        user["selllv"] += 1
                        user["coin"] -= price
                        tosend = upgprint("selllv", user_id)
                        await message.reply(embed=tosend)
                elif reply.content == "3":
                    price = int((user["critlv"]+1)**2.5*30)
                    if user["coin"] < price:
                        await message.reply("코인이 부족해요")
                    else:
                        user["critlv"] += 1
                        user["coin"] -= price
                        tosend = upgprint("critlv", user_id)
                        await message.reply(embed=tosend)
                else:
                    await message.reply("업그레이드를 취소했어요")
            except asyncio.TimeoutError:
                await message.reply("업그레이드를 취소했어요")

            
                
    save_user(user_id, user)


# client.run(os.getenv("DISCORD_TOKEN"))
client.run("MTQwOTM5MTk5OTYwMTA4NjUxNA.G8orEZ.hmF30yXEdFRK3ZFuRINgiLIXoOI-Ac_d5Np2EI")