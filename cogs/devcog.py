import disnake
from disnake.ext import commands
import sqlite3
import time

developers = [450229150217797633, 403829627753070603]
galka = 845550813119512589


class devcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def icons(self, ctx, user: disnake.User, icons):
        if ctx.author.id in developers:
            # id = user.id
            con = sqlite3.connect('bsdb.db')
            cur = con.cursor()
            try:
                cur.execute("UPDATE usersd SET icons == ? WHERE id == ?", (icons, user.id))
                con.commit()
                embed = disnake.Embed(
                    title="Обновление статуса значков. Успешно",
                    description=f"У участника {user.mention} была обновлена информация о значках.",
                    color=0x57F287
                )
            except Exception as e:
                embed = disnake.Embed(
                    title="",
                    description=f"Произошла ошибка во время обновления статуса значков у пользователя {user.mention}",
                    color=0x57F287
                )
                embed.add_field(name="Код ошибки:", value=f"```{e}```")
            con.close()
            await ctx.send(embed=embed)

    @commands.command()
    async def block(self, ctx, user: disnake.User, *, message: str):
        if ctx.author.id in developers:
            log = self.bot.get_channel(847748996302241792)
            con = sqlite3.connect('bsdb.db')
            cur = con.cursor()
            cur.execute("UPDATE usersd SET banReason == ? WHERE id == ?", (message, user.id))
            con.commit()
            con.close()
            embed = disnake.Embed(
                title="Блокировка пользователя. Успешно",
                description=f"К пользователю {user.mention} были применены штрафные санкции. Теперь он не сможет использовать бота",
                color=0xED4245
            )
            embed.add_field(name="Причина блокировки:", value=message)
            embed_log = disnake.Embed(
                title=f"Участник {user.name} был заблокирован.",
                color = 0xFEE75C
            )
            if user.avatar.url is not None:
                embed_log.set_thumbnail(url=user.avatar.url)
                embed_log.add_field(name="ID заблокированного:", value=f"`{user.id}`", inline=False)
                embed_log.add_field(name="Причина:", value=f"`{message}`")
                embed_log.add_field(name="Время блокировки:", value=f"<t:{int(time.time())}:F>(<t:{int(time.time())}:R>)")
                embed_log.set_footer(text=f"Модератор: {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar.url)
                await log.send(embed=embed_log)
            except Exception as e:
                embed = disnake.Embed(
                    title="Блокировка пользователя. Провал",
                    description=f"К пользователю {user.mention} не были применены штрафные санкции.",
                    color=0xFEE75C
                )
                embed.add_field(name="Ошибка:", value=f"```{e}```")
            await ctx.send(embed=embed)

    @commands.command()
    async def unblock(self, ctx, user: disnake.User):
        if ctx.author.id in developers:
            try:
                log = self.bot.get_channel(847748996302241792)
                con = sqlite3.connect('bsdb.db')
                cur = con.cursor()
                cur.execute("UPDATE usersd SET banReason == ? WHERE id == ?", (None, user.id))
                con.commit()
                con.close()
                embed = disnake.Embed(
                    title="Снятие блокировки с пользователя. Успешно",
                    description=f"С пользователя {user.mention} были сняты штрафные санкции. Теперь он сможет использовать бота",
                    color=0x5865F2
                )
                embed_log = disnake.Embed(
                    title=f"Участник {user.name} был разблокирован.",
                    color=0x57F287
                )
                if user.avatar.url != None:
                    embed_log.set_thumbnail(url=user.avatar.url)
                embed_log.add_field(name="Время снятия блокировки:", value=f"<t:{int(time.time())}:F>(<t:{int(time.time())}:R>)")
                embed_log.set_footer(text=f"Модератор: {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar.url)
                await log.send(embed=embed_log)
            except Exception as e:
                embed = disnake.Embed(
                    title="Снятие блокировки с пользователя. Провал",
                    description=f"С пользователя {user.mention} не были сняты штрафные санкции.",
                    color=0xFEE75C
                )
                embed.add_field(name="Ошибка:", value=f"```{e}```")
            await ctx.send(embed=embed)

    @commands.command()
    async def maintenance(self, ctx, arg1: str = "help", arg2: int = 0, arg3: int = 3600):
        if ctx.author.id in developers:
            if arg1 == "annonc":
                annonc_time = int(time.time())
                maint_start = annonc_time + arg2
                maint_end = maint_start + arg3
                log = self.bot.get_channel(847748996302241792)
                update = self.bot.get_channel(955850230472007701)
                dev1 = await self.bot.fetch_user(450229150217797633)
                embed_info = disnake.Embed(
                    title="Объявлено техническое обслуживание!",
                    description="Боту сейчас необходимо техническое обслуживание. В это время бот будет недоступен.",
                    color=0x5865F2
                )
                embed_info.add_field(name="Начало обслуживания:", value=f"<t:{maint_start}:F>(<t:{maint_start}:R>)", inline=True)
                embed_info.add_field(name="Конец обслуживания:", value=f"<t:{maint_end}:F>(<t:{maint_end}:R>)", inline=True)
                embed_info.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955801105663664168/4323-blurple-verified-bot-developer.png")
                embed_log = disnake.Embed(
                    title="Объявлено техническое обслуживание",
                    description=f"Разработчик {ctx.author.mention} объявил о начале технического обслуживания.",
                    color=0x5865F2
                )
                embed_log.set_thumbnail(url="https://cdn.discordapp.com/attachments/952169641801834546/955801105663664168/4323-blurple-verified-bot-developer.png")
                embed_log.add_field(name="Начало обслуживания:", value=f"<t:{maint_start}:F>(<t:{maint_start}:R>)", inline=True)
                embed_log.add_field(name="Конец обслуживания:", value=f"<t:{maint_end}:F>(<t:{maint_end}:R>)", inline=True)
                embed_log.set_footer(text=f"Разработчик: {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed_info, delete_after=30)
                await log.send(embed=embed_log)
                await dev1.send(embed=embed_log)
                message = await update.send("<@&926846261355761745>, важное уведомление!", embed=embed_info)
                await message.add_reaction("✅")
        else:
            await ctx.send(f"Интерестный факт: {ctx.author.mention}(т.е. Вы) не разработчик!", delete_after=7)


def setup(bot):
    bot.add_cog(devcog(bot))
