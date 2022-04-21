import disnake
from disnake import TextInputStyle
from disnake.ext import commands
import sqlite3
import os.path
from brawlstats import Client

try:
    client = Client('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY2ZDBlOGJlLTdlY2UtNGZjMi1hYjZiLTQ2YjgzODE3ODY4NCIsImlhdCI6MTY1MDUyNTU1Mywic3ViIjoiZGV2ZWxvcGVyL2NkNzI3NGQ2LTlhNzItOTk4Zi03MDM3LTM0OGI4NzY0MmQ3ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTg1LjE4NS43MC4yMzYiXSwidHlwZSI6ImNsaWVudCJ9XX0.b5E6HjBFDI5b7IpRF09-ABhJF3CIXveLUdXRHSXq3TSonrOuHSus9r7z1Sh6tU9NWlObQP_2MpwMU7yUvBBOcw')
except:
    #try:
    #    print("[WARN] Не удалось подключиться к BS API по основному токену. Пробуем другой...")
    #    client = Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmYWEyMTM4LWExZjEtNDZmOS04MWZlLWU0ODYxZGVmMWI0MiIsImlhdCI6MTY0ODgxMTU1Nywic3ViIjoiZGV2ZWxvcGVyL2NkNzI3NGQ2LTlhNzItOTk4Zi03MDM3LTM0OGI4NzY0MmQ3ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTg1LjIxMC4xNDIuODUiXSwidHlwZSI6ImNsaWVudCJ9XX0.0rT1Oi_wCuiu61w54dM-n2RJBWphrUF2LcWjF7X9Su3goqcK7yPtSYQxoLsEPAGRlZmhaj2PyfHJ5SM_G-YVVw")
    #except:
    print("[ERROR] Не удалось подключиться к BS API")

class link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.slash_command(name='привязать', description="Команда для привязывания тега Brawl Stars-аккаунта к Discord", guild_ids=[])
    async def link(self, inter, tag: str = commands.Param(name='тег', description="Тэг от Вашего Brawl Stars-аккаунта. Записывайте без # и букв O")):
        await inter.response.defer(ephemeral = True)
        if tag.startswith('#'):
            tag = tag.replace('#', '')
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        checkid = cur.execute(f"SELECT id FROM usersbs WHERE tag = '{tag}'").fetchone()
        checktag = cur.execute(f"SELECT tag FROM usersbs WHERE id = '{inter.author.id}'").fetchone()
        if checktag == None:
            try:
                player = client.get_profile(tag.upper())
                if checkid == None:
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
                    await inter.send(embed=embed, ephemeral = False)
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
                embed.add_field(name = "Советы по исправлению:", value = " • Проверьте тег на содержание букв `O` и замените на `0`\n • Уберите `#` из тега")
                await inter.send(embed=embed, ephemeral=True)
        elif checktag == tag:
            embed = disnake.Embed(
                title="Привязка тега Brawl Stars. Ошибка",
                description=f"Данный тег уже стоит у пользователя",
                color=0xED4245
            )
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
            embed.set_footer(text="Если вы уверены, что тег от вашего аккаунта, то обратитесь в поддержку.")
            await inter.send(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(
                title="Привязка тега Brawl Stars. Ошибка",
                description=f"{inter.author.mention} у вас уже есть тег!\nВоспользуйтесь командой **/unlink**, чтобы отвязать старый аккаунт, а затем воспользуйтесь **/link** снова",
                color=0xED4245
            )
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
            await inter.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(link(bot))
