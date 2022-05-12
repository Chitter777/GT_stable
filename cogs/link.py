import disnake
from disnake.ext import commands
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv
from brawlstats import Client

load_dotenv()
env_path = Path('.')/'.env'

try:
    class bsclient():
        client = Client(os.getenv("BSCLIENT1"))
        status = 200
        print("[INFO] link.py: Успешное подключение к BS API")
except:
    try:
        print("[WARN] link.py: Не удалось подключиться к BS API по основному токену. Пробуем другой...")
        class bsclient():
            client = Client(os.getenv("BSCLIENT2"))
            status = 200
    except:
        class bsclient():
            status = 401
        print("[ERROR] link.py: Не удалось подключиться к BS API")

class tool():
    def isblocked(self, cur, inter):
        try:
            banReason, = cur.execute("SELECT banReason FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
            return banReason
        except:
            return None

class linkclass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LOAD] Ког link загружен успено!")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        embed = disnake.Embed(
            title="❌ Ошибка",
            description="Во время исполнения команды произошла ошибка",
            color=0xED4245
        )
        embed.add_field(name="Код ошибки:", value=f"```{error}```")
        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name='привязать', description="Команда для привязывания тега Brawl Stars-аккаунта к Discord")
    async def link(self, inter, tag: str = commands.Param(name='тег', description="Тэг от Вашего Brawl Stars-аккаунта. Записывайте без # и букв O")):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        bnRsn = tool.isblocked(self, cur=cur, inter=inter)
        if bnRsn is not None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            embed.add_field(name="Причина отказа:", value=f"{bnRsn}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
        else:
            tag = str(tag)
            await inter.response.defer(ephemeral=True)
            cktag = tag
            if cktag.startswith('#'):
                cktag = cktag.replace('#', '')
            class checkin():
                tag = cktag
                checkid = cur.execute("SELECT id FROM usersbs WHERE tag == ?", (inter.author.id,)).fetchone()
                checktag = cur.execute("SELECT tag FROM usersbs WHERE id == ?", (inter.author.id,)).fetchone()

            match checkin.checktag:
                case None:
                    try:
                        if bsclient.status == 200:
                            player = bsclient.client.get_profile(tag.upper())
                        if checkin.checkid is None:
                            cur.execute("INSERT INTO usersbs VALUES (?, ?)", (inter.author.id, tag.upper()))
                            con.commit()
                            con.close()
                            embed = disnake.Embed(
                                title="Привязка тега Brawl Stars. Успешно!",
                                description=f"Вы привязали тег `{tag.upper()}` к аккаунту {inter.author.mention}",
                                color=0x57F287
                            )
                            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
                            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955807001496154122/4847-blurple-check.png")
                            await inter.send(embed=embed, ephemeral=False)
                        else:
                            embed = disnake.Embed(
                            title="Привязка тега Brawl Stars. Ошибка",
                            description=f"Данный тег уже стоит у пользователя",
                            color=0xED4245
                            )
                            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
                            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
                            embed.set_footer(text="Если вы уверены, что тег от вашего аккаунта, то обратитесь в поддержку.")
                            await inter.send(embed=embed, ephemeral=True)
                    except:
                        embed = disnake.Embed(
                            title="Привязка тега Brawl Stars. Ошибка",
                            description=f"Такого тега, как `{tag.upper()}`, не существует! Проверьте его написание.",
                            color=0xED4245
                        )
                        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
                        embed.add_field(name="⚠ Обратите внимание!", value="Проверьте тег на содержание букв `O` и замените на `0`")
                        await inter.send(embed=embed, ephemeral=True)
                case checkin.tag:
                    embed = disnake.Embed(
                        title="Привязка тега Brawl Stars. Ошибка",
                        description=f"Данный тег уже стоит у пользователя",
                        color=0xED4245
                    )
                    embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
                    embed.set_footer(text="Если вы уверены, что тег от вашего аккаунта, то обратитесь в поддержку.")
                    await inter.send(embed=embed, ephemeral=True)
                case _:
                    embed = disnake.Embed(
                        title="Привязка тега Brawl Stars. Ошибка",
                        description=f"{inter.author.mention} у вас уже есть тег!\nВоспользуйтесь командой **/unlink**, чтобы отвязать старый аккаунт, а затем воспользуйтесь **/link** снова",
                        color=0xED4245
                    )
                    embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
                    await inter.send(embed=embed, ephemeral=True)
        con.close()


def setup(bot):
    bot.add_cog(linkclass(bot))
