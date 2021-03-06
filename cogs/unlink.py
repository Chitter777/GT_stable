import disnake
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

class unlink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LOAD] Ког unlink загружен успено!")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        embed = disnake.Embed(
            title="❌ Ошибка",
            description="Во время исполнения команды произошла ошибка",
            color=0xED4245
        )
        embed.add_field(name="Код ошибки:", value=f"```{error}```")
        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(name='отвязать', description="Отвязать аккаунт Brawl Stars от аккаунта Discord")
    async def unlink(self, inter):
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
                con.close()


def setup(bot):
    bot.add_cog(unlink(bot))
