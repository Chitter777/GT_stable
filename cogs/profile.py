import io
import disnake
import requests
from disnake import TextInputStyle
from disnake.ext import commands
import sqlite3
import os.path
from brawlstats import Client
from PIL import Image, ImageFont, ImageDraw
import requests
from datetime import datetime
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'

try:
    class bsclient():
        client = Client(os.getenv("BSCLIENT1"))
        status = 200
        print("[INFO] profile.py: Успешное подключение к BS API")
except:
    try:
        print("[WARN] profle.py: Не удалось подключиться к BS API по основному токену. Пробуем другой...")
        class bsclient():
            client = Client(os.getenv("BSCLIENT2"))
            status = 200
    except:
        class bsclient():
            status = 401
        print("[ERROR] profile.py: Не удалось подключиться к BS API")

developers = (403829627753070603, 450229150217797633,)


class tool():
    class icon():
        dev = "<:chitty_developer:924980296632397854> "
        exp = "<:chitty_experienced:958762170097762314> "
        bh1 = "<:chitty_bughunter1:925311594408312865> "
        love = "<:chitty_love:924986260899110932> "

    def card(self, usr):
        user = usr
        if user.id in developers:
            img = Image.open('devcard.png')
        else:
            img = Image.new('RGBA', (900, 200), '#5865F2')
        avatar = str(user.avatar)[:-10]
        response = requests.get(avatar, stream=True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((160, 160), Image.ANTIALIAS)
        img.paste(response, (20, 20, 180, 180))
        idraw = ImageDraw.Draw(img)
        if user.nick is not None:
            name = user.nick
        else:
            name = user.name
        # disc = user.discriminator
        headline = ImageFont.truetype('Pusia-Bold.ttf', size=36)
        # undertext = ImageFont.truetype('Pusia-Bold.ttf', size=24)
        # idraw.text((210, 50), f"{name}#{disc}", font=headline)
        idraw.text((210, 50), f"{name}", font=headline)
        # if teamId != None:
        #    idraw.text((180, 25), f"Команда {teamna}", font=undertext)
        img.save('user_card.png')

    def icons(self, icons):
        match icons:
            case "1000":
                return tool.icon.dev
            case "0111":
                return tool.icon.exp + tool.icon.bh1 + tool.icon.love
            case "0101":
                return tool.icon.exp
            case "0001":
                return tool.icon.love
            case "0010":
                return tool.icon.bh1
            case _:
                return None

    def isblocked(self, cur, inter):
        try:
            banReason, = cur.execute("SELECT banReason FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
            return banReason
        except:
            return None

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LOAD] Ког profile загружен успено!")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        embed = disnake.Embed(
            title="❌ Ошибка",
            description="Во время исполнения команды произошла ошибка",
            color=0xED4245
        )
        embed.add_field(name="Код ошибки:", value=f"```{error}```")
        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name='профиль', description="Просмотреть свой или чей-нибудь профиля")
    async def profile(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author, name='юзер', description="Выберите пользователя, чей профиль вы хотите получить")):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        bnRsn = tool.isblocked(self, cur = cur, inter=inter)
        try:
            teamId, = cur.execute("SELECT teamId FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
        except:
            teamId = None
        if bnRsn is not None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            embed.add_field(name="Причина отказа:", value=f"{bnRsn}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
        elif user.bot is True:
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
            usr = user
            tool.card(self, usr = usr)
            embed.set_image(file = disnake.File("user_card.png"))
            dr = user.created_at
            drts = str(dr.timestamp() * 1000)
            embed.add_field(name="Информация об аккаунте Discord:", value=f"Дата регистрации: <t:{drts[:-5]}:f>(<t:{drts[:-5]}:R>)", inline=True)
            if tag is not None:
                try:
                    player = bsclient.client.get_profile(tag)
                    embed.add_field(name="<:bsinfo:957947143153397760> Информация об аккаунте Brawl Stars:", value=f"Никнейм: `{player.name}`\nТэг: `{tag}`\nКоличество трофеев: `{player.trophies}/{player.highest_trophies}`\nБойцов: `{str(len(player.brawlers))}/55`", inline=False)
                    embed.add_field(name="<:bsaccount:957946769713561630> Статистика Brawl Stars-аккаунта: ", value=f"Побед в 3 на 3: `{player.x3vs3_victories}`\nПобед в одиночном ШД: `{player.solo_victories}`\nПобед в парном ШД: `{player.duo_victories}`", inline = True)
                except:
                    embed.add_field(name=":warning: Проблемы с Brawl Stars API", value="Сейчас наблюдаются проблемы с BS API. Возможно, сейчас проводятся тенические работы.", inline=True)
            else:
                if inter.author == user:
                    embed.add_field(name="Совет:", value="Вы можете привязать тег с помощью `/привязать`, чтобы получить доступк статистике", inline=False)

            icnstring = tool.icons(self, icons)
            if icnstring is not None:
                embed.add_field(name="Значки:", value=icnstring, inline=False)

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
        bnRsn = tool.isblocked(self, cur=cur, inter=inter)
        try:
            teamId, = cur.execute("SELECT teamId FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
        except:
            teamId = None
        if bnRsn is not None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            embed.add_field(name="Причина отказа:", value=f"{bnRsn}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
        elif user.bot is True:
            embed = disnake.Embed(
                title="Получение сведений. Ошибка",
                description=f"Аккаунт {user.mention} отмечен как <:chitty_bottagverif1:958998669208719361><:chitty_bottagverif2:958998711529242634>. Зачем получать сведения о ботах, если они не играют в бравл :D ?",
                color=0xED4245
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
            await inter.send(embed=embed, ephemeral=True)
        else:
            await inter.response.defer(ephemeral=True)
            icons = None
            banReason = None
            try:
                icons, banReason, = cur.execute(f"SELECT icons, banReason FROM usersd WHERE id == ?",
                                                (user.id,)).fetchone()
            except:
                cur.execute("INSERT INTO usersd VALUES(?, ?, ?, ?, ?, ?)", (user.id, None, '0000', 0, None, 3))
                con.commit()
            try:
                tag, = cur.execute(f"SELECT tag FROM usersbs WHERE id = '{user.id}'").fetchone()
            except:
                tag = None
            embed = disnake.Embed(description="Информация об участнике:", color=0x5865F2)
            embed.set_author(name=f"Профиль {user.name}#{user.discriminator}", icon_url=user.avatar)
            usr = user
            tool.card(self, usr=usr)
            embed.set_image(file=disnake.File("user_card.png"))
            dr = user.created_at
            drts = str(dr.timestamp() * 1000)
            embed.add_field(name="Информация об аккаунте Discord:",
                            value=f"Дата регистрации: <t:{drts[:-5]}:f>(<t:{drts[:-5]}:R>)", inline=True)
            if tag is not None:
                try:
                    player = bsclient.client.get_profile(tag)
                    embed.add_field(name="<:bsinfo:957947143153397760> Информация об аккаунте Brawl Stars:", value=f"Никнейм: `{player.name}`\nТэг: `{tag}`\nКоличество трофеев: `{player.trophies}/{player.highest_trophies}`\nБойцов: `{str(len(player.brawlers))}/55`", inline=False)
                    embed.add_field(name="<:bsaccount:957946769713561630> Статистика Brawl Stars-аккаунта: ", value=f"Побед в 3 на 3: `{player.x3vs3_victories}`\nПобед в одиночном ШД: `{player.solo_victories}`\nПобед в парном ШД: `{player.duo_victories}`", inline=True)
                except:
                    embed.add_field(name=":warning: Проблемы с Brawl Stars API", value="Сейчас наблюдаются проблемы с BS API. Возможно, сейчас проводятся тенические работы.", inline=True)
            else:
                if inter.author == user:
                    embed.add_field(
                        name="Совет:",
                        value="Вы можете привязать тег с помощью `/привязать`, чтобы получить доступк статистике",
                        inline=False
                    )

            icnstring = tool.icons(self, icons)
            if icnstring is not None:
                embed.add_field(name="Значки:", value=icnstring, inline=False)

            if banReason is not None:
                embed.add_field(
                    name="<:isBlocked:957961543910326284> Причина блокировки доступа:",
                    value=banReason, inline=True
                )
            try:
                teamname, = cur.execute("SELECT teamname FROM teams WHERE id == ?", (teamId,)).fetchone()
                embed.add_field(name="В команде:", value=f"{teamname}", inline=True)
            except Exception as e:
                print(e)
            con.close()
            embed.set_footer(text=f"ID участника: {user.id}")
            await inter.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(profile(bot))
