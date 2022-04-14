import disnake
from disnake.ext import commands
import sqlite3
import os.path
from brawlstats import Client

try:
    client = Client('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZjYzZkZDg2LWIxZjktNDdmYy04ZDk0LTU1YWNkNzU1YzE4MiIsImlhdCI6MTY0Nzk0ODE1Miwic3ViIjoiZGV2ZWxvcGVyL2NkNzI3NGQ2LTlhNzItOTk4Zi03MDM3LTM0OGI4NzY0MmQ3ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTkzLjE0My4xMTkuMjM4IiwiMTkzLjE0My4xMTkuMjM3Il0sInR5cGUiOiJjbGllbnQifV19.eNDlAGv0krmr1PK6Vyo4nln1_JQI2aXKkACvDiq0EA9GA0BGvuWiiHJLAnXm9dH_Qe83uRXLug2X58VpE-XFQA')
except:
    try:
        print("[WARN] Не удалось подключиться к BS API по основному токену. Пробуем другой...")
        client = Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmYWEyMTM4LWExZjEtNDZmOS04MWZlLWU0ODYxZGVmMWI0MiIsImlhdCI6MTY0ODgxMTU1Nywic3ViIjoiZGV2ZWxvcGVyL2NkNzI3NGQ2LTlhNzItOTk4Zi03MDM3LTM0OGI4NzY0MmQ3ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTg1LjIxMC4xNDIuODUiXSwidHlwZSI6ImNsaWVudCJ9XX0.0rT1Oi_wCuiu61w54dM-n2RJBWphrUF2LcWjF7X9Su3goqcK7yPtSYQxoLsEPAGRlZmhaj2PyfHJ5SM_G-YVVw")
    except:
        print("[ERROR] Не удалось подключиться к BS API")

class unlink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass


    @commands.slash_command(name='отвязать', description="Отвязать аккаунт Brawl Stars от аккаунта Discord", guild_ids=[])
    async def unlink(self, inter):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()

        row = cur.execute(f'SELECT tag FROM usersbs WHERE id = {inter.author.id}').fetchone()
        if row is None:
            embed = disnake.Embed(
                title="Отвязка тега Brawl Stars. Ошибка",
                description=f"У вас не обнаружено привязанного тега",
                color=0xED4245
            )
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955758311326761060/2118-unable-to-load.png")
            embed.set_footer(text="Если вы уверены, что тег привязан к аккаунту Discord, но вы всё равно получаете ошибку, то обратитесь в поддержку.")
            await inter.send(embed=embed, ephemeral=True)
        else:
            cur.execute(f"DELETE FROM usersbs WHERE id = {inter.author.id}")
            embed = disnake.Embed(
                title="Отвязка тега Brawl Stars. Успешно",
                description=f"Вы успешно отвязали тег от аккаунта",
                color=0x5865F2
            )
            embed.set_author(name = inter.author.name, icon_url=inter.author.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955795973127434281/9884-blurple-delete.png")
            await inter.send(embed=embed, ephemeral = True)
            con.commit()
            con.close


def setup(bot):
    bot.add_cog(unlink(bot))

