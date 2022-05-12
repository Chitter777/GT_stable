import disnake
from disnake import TextInputStyle
from disnake.ext import commands
import sqlite3
import os.path

class tool():
    def isblocked(self, cur, inter):
        try:
            banReason, = cur.execute("SELECT banReason FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
            return banReason
        except:
            return None

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LOAD] Ког ping загружен успено!")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        embed = disnake.Embed(
            title="❌ Ошибка",
            description="Во время исполнения команды произошла ошибка",
            color=0xED4245
        )
        embed.add_field(name="Код ошибки:", value=f"```{error}```")
        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name='пинг', description = "Измеряет задержку между ботом и серверами Discord")
    async def ping(self, inter):
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
            ping = self.bot.latency
            embed = disnake.Embed(
                title="Проверка задержки",
                colour=0x5865F2
            )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/satellite-antenna_1f4e1.png")
            embed.add_field(
                name="Задержка:",
                value=f'`{ping * 1000:.0f}` мс',
                inline=True
            )
            if (ping * 1000) > 200:
                embed.set_footer(text="Большая задержка? Обратитесь к Chitter777#0070")
            await inter.send(embed=embed)
            #print(f'[CMDEXEC] На данный момент пинг == `{ping * 1000:.0f} ms | ping')

def setup(bot):
    bot.add_cog(ping(bot))
