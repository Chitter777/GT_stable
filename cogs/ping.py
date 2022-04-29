import disnake
from disnake import TextInputStyle
from disnake.ext import commands
import sqlite3
import os.path


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if os.path.exists('bsdb.db'):
            pass
        else:
            con = sqlite3.connect('bsdb.db')
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS bsbdt (id INT UNIQUE, tag TEXT UNIQUE)''')
            con.commit()

    @commands.slash_command(name='пинг', description = "Измеряет задержку между ботом и серверами Discord")
    async def ping(self, inter):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        banReason, = cur.execute(f"SELECT banReason FROM usersd WHERE id = '{inter.author.id}'").fetchone()
        if banReason != None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            # embed.set_thumbnail(url="")
            embed.add_field(name="Причина отказа:", value=f"{banReason}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
        else:
            try:
                ping = self.bot.latency
                embed = disnake.Embed(
                    title="Проверка задержки",
                    description="Подождите, идёт измерение задержки...",
                    colour=0xFEE75C)
                embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/satellite-antenna_1f4e1.png")
                embed.set_footer(text="Измерение происходит слишком долго? Обратитесь к Chitter777#0070")
                await inter.send(embed=embed)
                embed = disnake.Embed(
                    title="Проверка задержки",
                    colour=0x5865F2)
                embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/satellite-antenna_1f4e1.png")
                embed.add_field(
                    name="Задержка:",
                    value=f'`{ping * 1000:.0f}` мс',
                    inline=True
                )
                if (ping * 1000) > 200:
                    embed.set_footer(text="Большая задержка? Обратитесь к Chitter777#0070")
                await inter.edit_original_message(embed=embed)
                print(f'[CMDEXEC] На данный момент пинг == `{ping * 1000:.0f} ms | ping')
            except Exception as e:
                await inter.send(e, ephemeral=True)

def setup(bot):
    bot.add_cog(ping(bot))
