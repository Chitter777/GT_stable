import disnake
from disnake import TextInputStyle
from disnake.enums import ButtonStyle
from disnake.ext import commands
import sqlite3
import os.path


class buttons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=3600)

    @disnake.ui.button(emoji="<:chitty_info:958695250120036384>", style=ButtonStyle.grey)
    async def main(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Помощь с командами. Основные команды:",
            description="""**/обомне** - информация о боте;
**/отвязать** - отвязать аккаунт Brawl Stars от аккаунта Discord;
**/пинг** - проверка задержки между серверами Discord и сервером бота:
**/помощь** - справка обо всех командах;
**/привязать < #BS tag >** - привязать аккаунт Brawl Stars к аккаунту Discord
**/профиль [ пинг/id участника ]** - Просмотреть профиль участника""",
            colour=0x5865F2
        )
        embed.set_footer(text="CHIT SQD | (C) 2022 | Все права взломаны",
                         icon_url="https://cdn.discordapp.com/icons/794400771662676009/a_ab67786efe3ceccc550f4127e1992176.gif")
        await interaction.send(embed=embed, ephemeral=True)

    @disnake.ui.button(emoji="<:chitty_members:924981240875069480>", style=ButtonStyle.grey)
    async def tour(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Команды не сделаны",
            description="Команды находятся в разработке!",
            color=0x5865F2
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/952169641801834546/955801105663664168/4323-blurple-verified-bot-developer.png")
        await interaction.send(embed=embed, ephemeral=True)

    @disnake.ui.button(emoji="<:chitty_staff:924981410945720320>", style=ButtonStyle.danger)
    async def admin(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Команды не сделаны",
            description="Команды находятся в разработке!",
            color=0x5865F2
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/952169641801834546/955801105663664168/4323-blurple-verified-bot-developer.png")
        await interaction.send(embed=embed, ephemeral=True)

class tool():
    def isblocked(self, cur, inter):
        try:
            banReason, = cur.execute("SELECT banReason FROM usersd WHERE id == ?", (inter.author.id,)).fetchone()
            return banReason
        except:
            return None

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LOAD] Ког help загружен успено!")

    @commands.slash_command(
        name='помощь',
        description="Помощь со всеми командами"
    )
    async def help(self, inter):
        con = sqlite3.connect('bsdb.db')
        cur = con.cursor()
        bnRsn = tool.isblocked(self, cur = cur, inter=inter)
        if bnRsn is not None:
            embed = disnake.Embed(
                title=":no_entry_sign: Отказ в обслуживании",
                description=f"Вам отказано в обслуживании!",
                color=0xED4245
            )
            embed.add_field(name="Причина отказа:", value=f"{bnRsn}")
            embed.set_footer(text="Решение о блокировке обжалованию не подлежит!")
            await inter.send(embed=embed, ephemeral=True)
            con.close()
        else:
            embed = disnake.Embed(title="Помощь с командами. Все команды", colour=0x5865F2)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/952169641801834546/955411818975731712/1113-blurple-info.png")
            embed.add_field(name="Общие команды", value="Кнопка <:chitty_info:958695250120036384>", inline=True)
            embed.add_field(name="Турнирные команды:", value="<:chitty_developer:924980296632397854> В разработке", inline=False)
            embed.add_field(name="Команды для администрации):", value="<:chitty_developer:924980296632397854> В разработке", inline=False)
            embed.set_footer(text="CHIT SQD | (C) 2022 | Все права взломаны", icon_url="https://cdn.discordapp.com/icons/794400771662676009/a_ab67786efe3ceccc550f4127e1992176.gif")
            await inter.send(embed=embed, view=buttons())


def setup(bot):
    bot.add_cog(help(bot))
