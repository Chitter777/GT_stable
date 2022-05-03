import io

import disnake
import requests
from disnake import TextInputStyle
from disnake.ext import commands
import sqlite3
#import os.path
from brawlstats import Client
#from PIL import Image, ImageFont, ImageDraw
import requests
from datetime import datetime
import time

try:
    client = Client('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY2ZDBlOGJlLTdlY2UtNGZjMi1hYjZiLTQ2YjgzODE3ODY4NCIsImlhdCI6MTY1MDUyNTU1Mywic3ViIjoiZGV2ZWxvcGVyL2NkNzI3NGQ2LTlhNzItOTk4Zi03MDM3LTM0OGI4NzY0MmQ3ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTg1LjE4NS43MC4yMzYiXSwidHlwZSI6ImNsaWVudCJ9XX0.b5E6HjBFDI5b7IpRF09-ABhJF3CIXveLUdXRHSXq3TSonrOuHSus9r7z1Sh6tU9NWlObQP_2MpwMU7yUvBBOcw')
#except:
#    print("[WARN] Не удалось подключиться к основному токену авторизации BS API. Идёт попытка подключения к резервному токену.")
#    client = Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmYWEyMTM4LWExZjEtNDZmOS04MWZlLWU0ODYxZGVmMWI0MiIsImlhdCI6MTY0ODgxMTU1Nywic3ViIjoiZGV2ZWxvcGVyL2NkNzI3NGQ2LTlhNzItOTk4Zi03MDM3LTM0OGI4NzY0MmQ3ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTg1LjIxMC4xNDIuODUiXSwidHlwZSI6ImNsaWVudCJ9XX0.0rT1Oi_wCuiu61w54dM-n2RJBWphrUF2LcWjF7X9Su3goqcK7yPtSYQxoLsEPAGRlZmhaj2PyfHJ5SM_G-YVVw")
except:
    print("[ERROR] Не удалось подключиться к BS API")

dev1 = 450229150217797633
dev2 = 403829627753070603

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass


    @commands.slash_command(name='профиль', description="Просмотреть свой или чей-нибудь профиля")
    async def profile(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author, name='юзер', description="Выберите пользователя, чей профиль вы хотите получить")):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        try:
            banReason, = cur.execute("SELECT banReason FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
        except:
            banReason = None
        try:
            teamId, = cur.execute("SELECT teamId FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
        except:
            teamId = None
        if banReason is not None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            embed.add_field(name="Причина отказа:", value=f"{banReason}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
        elif user.bot == True:
            embed = disnake.Embed(
                title="Получение сведений. Ошибка",
                description=f"Аккаунт {user.mention} отмечен как <:chitty_bottagverif1:958998669208719361><:chitty_bottagverif2:958998711529242634>. Зачем получать сведения о ботах, если они не играют в бравл :D ?",
                color=0xED4245
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
            await inter.send(embed = embed, ephemeral=True)
        else:
            await inter.response.defer()
            icons = None
            banReason = None
            try:
                icons, banReason, = cur.execute(f"SELECT icons, banReason FROM usersd WHERE id == ?", (user.id,)).fetchone()
            except:
                cur.execute("INSERT INTO usersd VALUES(?, ?, ?, ?, ?, ?)", (user.id, None, '0000', 0, None, 3))
                con.commit()
            try:
                tag, = cur.execute(f"SELECT tag FROM usersbs WHERE id = '{user.id}'").fetchone()
            except:
                tag = None
            embed = disnake.Embed(description="Информация об участнике:", color=0x5865F2)
            embed.set_author(name=f"Профиль {user.name}#{user.discriminator}", icon_url=user.avatar)
            #img = Image.new('RGBA', (900, 200), '#5865F2')
            #avatar = str(user.avatar)[:-10]
            #response = requests.get(avatar, stream = True)
            #response = Image.open(io.BytesIO(response.content))
            #response = response.convert('RGBA')
            #response = response.resize((160, 160), Image.ANTIALIAS)
            #img.paste(response, (20, 20, 180, 180))
            #idraw = ImageDraw.Draw(img)
            #if user.nick is not None:
                #name = user.nick
            #else:
                #name = user.name
            #disc = user.discriminator
            #headline = ImageFont.truetype('Pusia-Bold.ttf', size=36)
            #undertext = ImageFont.truetype('Pusia-Bold.ttf', size=24)
            # idraw.text((210, 50), f"{name}#{disc}", font=headline)
            #idraw.text((210, 50), f"{name}", font=headline)
            #if teamId != None:
            #    idraw.text((180, 25), f"Команда {teamna}", font=undertext)
            #img.save('user_card.png')
            #embed.set_image(file = disnake.File("user_card.png"))
            dr = user.created_at
            drts = str(dr.timestamp() * 1000)
            embed.add_field(name="Информация об аккаунте Discord:", value=f"Дата регистрации: <t:{drts[:-5]}:f>(<t:{drts[:-5]}:R>)", inline=True)

            if tag is not None:
                try:
                    player = client.get_profile(tag)
                    embed.add_field(name="<:bsinfo:957947143153397760> Информация об аккаунте Brawl Stars:", value=f"Никнейм: `{player.name}`\nТэг: `{tag}`\nКоличество трофеев: `{player.trophies}/{player.highest_trophies}`\nБойцов: `{str(len(player.brawlers))}/55`", inline=False)
                    embed.add_field(name="<:bsaccount:957946769713561630> Статистика Brawl Stars-аккаунта: ", value=f"Побед в 3 на 3: `{player.x3vs3_victories}`\nПобед в одиночном ШД: `{player.solo_victories}`\nПобед в парном ШД: `{player.duo_victories}`", inline = True)
                except:
                    embed.add_field(name=":warning: Проблемы с Brawl Stars API", value="Сейчас наблюдаются проблемы с BS API. Возможно, сейчас проводятся тенические работы.", inline=True)
            else:
                if inter.author == user:
                    embed.add_field(name="Совет:", value="Вы можете привязать тег с помощью `/привязать`, чтобы получить доступк статистике", inline=False)

            if icons == '1000':
                icons = "<:chitty_developer:924980296632397854>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            elif icons == "0111":
                icons = "<:chitty_experienced:958762170097762314> <:chitty_bughunter1:925311594408312865> <:chitty_love:924986260899110932>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            elif icons == "0101":
                icons = "<:chitty_experienced:958762170097762314> <:chitty_love:924986260899110932>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            elif icons == "0001":
                icons = "<:chitty_love:924986260899110932>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            else:
                pass
            if banReason is not None:
                embed.add_field(name="<:isBlocked:957961543910326284> Причина блокировки доступа:", value=banReason, inline=True)
            try:
                teamname, = cur.execute("SELECT teamname FROM teams WHERE id == ?", (teamId,)).fetchone()
                embed.add_field(name="В команде:", value=f"{teamname}", inline=True)
            except Exception as e:
                print(e)
            con.close()
            embed.set_footer(text = f"ID участника: {user.id}")
            await inter.send(embed=embed)

    @commands.user_command(name="Профиль участника", guild_ids=[])
    async def profile_usrcmd(self, inter: disnake.AppCmdInter, user: disnake.User):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        try:
            banReason, = cur.execute(f"SELECT banReason FROM usersd WHERE id = '{inter.author.id}'").fetchone()
        except:
            banReason = None
        try:
            teamId, = cur.execute(f"SELECT teamId FROM usersd WHERE id = '{inter.author.id}'").fetchone()
        except:
            teamId = None
        if banReason is not None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            # embed.set_thumbnail(url="")
            embed.add_field(name="Причина отказа:", value=f"{banReason}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
        elif user.bot == True:
            embed = disnake.Embed(
                title="Получение сведений. Ошибка",
                description=f"Аккаунт {user.mention} отмечен как <:chitty_bottagverif1:958998669208719361><:chitty_bottagverif2:958998711529242634>. Зачем получать сведения о ботах, если они не играют в бравл :D ?",
                color=0xED4245
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
            await inter.send(embed=embed, ephemeral=True)
        else:
            await inter.response.defer(ephemeral = True)
            icons = None
            banReason = None
            try:
                icons, banReason, = cur.execute(f"SELECT icons, banReason FROM usersd WHERE id = '{user.id}'").fetchone()
            except:
                cur.execute("INSERT INTO usersd VALUES(?, ?, ?, ?, ?, ?)", (user.id, None, '0000', 0, None, 3))
                con.commit()
            try:
                tag, = cur.execute(f"SELECT tag FROM usersbs WHERE id = '{user.id}'").fetchone()
            except:
                tag = None
            embed = disnake.Embed(description="Информация об участнике:", color=0x5865F2)
            embed.set_author(name=f"Профиль {user.name}", icon_url=user.avatar)
            #img = Image.new('RGBA', (900, 200), '#5865F2')
            #avatar = str(user.avatar)[:-10]
            #response = requests.get(avatar, stream=True)
            #response = Image.open(io.BytesIO(response.content))
            #response = response.convert('RGBA')
            #response = response.resize((160, 160), Image.ANTIALIAS)
            #img.paste(response, (20, 20, 180, 180))
            #idraw = ImageDraw.Draw(img)
            #if user.nick is not None:
                #name = user.nick
            #else:
                #name = user.name
            #disc = user.discriminator
            #headline = ImageFont.truetype('Pusia-Bold.ttf', size=36)
            #undertext = ImageFont.truetype('Pusia-Bold.ttf', size=24)
            #idraw.text((210, 50), f"{name}#{disc}", font=headline)
            idraw.text((210, 50), f"{name}", font=headline)
            # if teamId != None:
            #    idraw.text((180, 25), f"Команда {teamna}", font=undertext)
            #img.save('user_card.png')
            #embed.set_image(file=disnake.File("user_card.png"))
            dr = user.created_at
            drts = str(dr.timestamp() * 1000)
            embed.add_field(name="Информация об аккаунте Discord:", value=f"Дата регистрации: <t:{drts[:-5]}:f>(<t:{drts[:-5]}:R>)", inline=True)

            if tag is not None:
                try:
                    player = client.get_profile(tag)
                    embed.add_field(name="<:bsinfo:957947143153397760> Информация об аккаунте Brawl Stars:", value=f"Никнейм: `{player.name}`\nТэг: `{tag}`\nКоличество трофеев: `{player.trophies}/{player.highest_trophies}`\nБойцов: `{str(len(player.brawlers))}/55`", inline=False)
                    embed.add_field(name="<:bsaccount:957946769713561630> Статистика Brawl Stars-аккаунта: ", value=f"Побед в 3 на 3: `{player.x3vs3_victories}`\nПобед в одиночном ШД: `{player.solo_victories}`\nПобед в парном ШД: `{player.duo_victories}`", inline=True)
                except:
                    embed.add_field(name=":warning: Проблемы с Brawl Stars API", value="Сейчас наблюдаются проблемы с BS API. Возможно, сейчас проводятся тенические работы.", inline=True)
            else:
                if inter.author == user:
                    embed.add_field(name="Совет:", value="Вы можете привязать тег с помощью `/привязать`, чтобы получить доступк статистике", inline=False)
            if icons == '1000':
                icons = "<:chitty_developer:924980296632397854>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            elif icons == "0111":
                icons = "<:chitty_experienced:958762170097762314> <:chitty_bughunter1:925311594408312865> <:chitty_love:924986260899110932>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            elif icons == "0101":
                icons = "<:chitty_experienced:958762170097762314> <:chitty_love:924986260899110932>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            elif icons == "0001":
                icons = "<:chitty_love:924986260899110932>"
                embed.add_field(name="Значки:", value=icons, inline=False)
            else:
                pass
            if banReason != None:
                embed.add_field(name="<:isBlocked:957961543910326284> Причина блокировки доступа:", value=banReason, inline=True)
            try:
                teamname, = cur.execute(f"SELECT teamname FROM teams WHERE id = '{teamId}'").fetchone()
                embed.add_field(name="В команде:", value=f"{teamname}", inline=True)
            except Exception as e:
                print(e)
            con.close()
            embed.set_footer(text=f"ID участника: {user.id}")
            await inter.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(profile(bot))
