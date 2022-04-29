import disnake
from disnake import TextInputStyle
from disnake.ext import commands
from disnake.enums import ButtonStyle
import sqlite3

class buttons(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(label="Сервер поддержки", url="https://discord.gg/esaPCQvpwY", emoji="<:chitty_bughunter1:925311594408312865>"))


    @disnake.ui.button(emoji="<:chitty_rules:924980688531390506>", label="Условия использования", style=ButtonStyle.grey)
    async def terms(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Условия обслуживания Galka's Tournaments:",
            description="""**1. Пользователь**(т.е. Вы) при первом взаимодействии с ботом подтверждаете, что вы согласны со всеми положениями **Условий обслуживания Galka's Tournaments**.
  **2.** Вы обязуетесь не нарушать **[Условия использования Discord](https://discord.com/terms)** и правила **Supercell**.
            
  При нарушении вами **Условий обслуживания**, Мы __имеем полное право **лишить** вас **доступа к боту**__!""",
            colour=0x5865F2
        )
        embed.set_footer(text="CHIT SQD | (C) 2022 | Все права взломаны", icon_url="https://cdn.discordapp.com/icons/794400771662676009/a_ab67786efe3ceccc550f4127e1992176.gif")
        await interaction.send(embed=embed, ephemeral=True)

class about(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='обомне', description="Информация о боте")
    async def about(self, inter):
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
            embed = disnake.Embed(
                title="О боте:",
                description="Привет. Это приватный бот для турниров на сервере **Galka's Team**",
                colour=0x5865F2
            )
            embed.add_field(name="Разработчики:", value="<:chitter777:959425285470683158> Chitter777#0070\n<:kotik:959428879741780048> Кот? | kotik_nekot#9395", inline=True)
            embed.set_footer(text="CHIT SQD | (C) 2022 | Все права взломаны", icon_url="https://cdn.discordapp.com/icons/794400771662676009/a_ab67786efe3ceccc550f4127e1992176.gif")
            view = buttons()
            await inter.send(embed=embed, view=buttons())



def setup(bot):
    bot.add_cog(about(bot))
