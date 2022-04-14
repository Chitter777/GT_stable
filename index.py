import disnake
from disnake.ext import commands
import sqlite3
import os

botname = "Galka's tournaments"

client = commands.Bot(
    command_prefix = ':/',
    activity = disnake.Game("Работаю на слэш-командах"),
    intent = disnake.Intents.all(),
    test_guilds=[955497836680720435, 919606896778936380])
client.remove_command('help')
developers = [450229150217797633, 403829627753070603]
TOKEN = 'OTU1MDUyNDE3OTMyNzIyMTc2.YjcD4A.dQJPlhrCVnvQFOL_zXWgB2Ftd5Y'


class Login(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = ':/',
            activity = disnake.Game("Работаю на слэш-командах"),
            intent = disnake.Intents.all(),
            test_guilds=[955497836680720435, 919606896778936380]
        )

    async def on_ready(self):
        print('[STARTUP] Бот в строю!')

    async def on_guild_join(self, guild):
        log = self.get_channel(847748996302241792)
        if log != None:
            embed = disnake.Embed(
                title="Бот был добавлен на сервер",
                color=0x57F287
            )
            if guild.icon.url != None:
                embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="Название:", value=f"`{guild.name}`", inline=True)
            embed.add_field(name="Сервер создан:", value= f"<t:{str(guild.created_at.timestamp() * 1000) [:-5]}:F>", inline=True)
            try:
                own = guild.owner
                embed.add_field(name="Владелец:", value=f"{own.mention}({own.id})", inline=True)
            except:
                embed.add_field(name="Владелец:", value="`Отсутствует`", inline=True)
            embed.add_field(name="Количество участников:", value=f"`{guild.member_count}`", inline=True)
            embed.set_footer(text=f"ID сервера: {guild.id}")
            await log.send(embed=embed)
        else:
            print("[ERROR] Не удалось вывести эмбед...")

    async def on_guild_remove(self, guild):
        log = self.get_channel(847748996302241792)
        embed = disnake.Embed(
            title="Бот был удалён с серера",
            color=0xFEE75C
        )
        embed.add_field(name="Название:", value=f"`{guild.name}`", inline=True)
        embed.set_footer(text=f"ID сервера: {guild.id}")
        await log.send(embed=embed)


client = Login()


@client.command()
async def reload(ctx, extension):
    embed_wait = disnake.Embed(title="<:chitty_settings:924980025223155723> Менеджер перезагрузки когов. Ожидание", description=f"Идёт перезагрузка кога `{extension}`.", color=0xFEE75C)
    embed_successfully = disnake.Embed(title='<:chitty_settings:924980025223155723> Менеджер перезагрузки когов. Успех', description=f'Ког `{extension}` успешно перезагружен.', color=0x57F287)
    message = await ctx.send(embed=embed_wait)
    if (ctx.author.id in developers) and (extension != None) and (extension != "all"):
        try:
            client.reload_extension(f"cogs.{extension}")
            await message.edit(embed=embed_successfully, delete_after=120)
            print(f"[INFO] Ког {extension} был успешно перезагружен")
        except Exception as e:
            embed_error = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер перезагрузки когов. Ошибка',
                description=f'Боту не удалось перезагрузить ког `{extension}`. Возможно, вы ошиблись с названием.\n\nВывод консоли:```{e}```',
                color=0xED4245
            )
            await message.edit(embed=embed_error)
            print(f"[ERROR] Ког {extension} не был перезагружен: {e}")
    elif (ctx.author.id in developers) and (extension == "all"):
        try:
            for file in os.listdir("./cogs"):
                if file.endswith(".py"):
                    client.reload_extension("cogs." + file[:-3])
            print(f"[INFO] Ког {file[:-3]} был успешно перезагружен")
            embed_reloadAll = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер перезагрузки когов. Успех',
                description=f'Все коги были перезагружены.',
                color=0x57F287
            )
            await message.edit(embed=embed_reloadAll, delete_after=120)
        except Exception as e:
            embed_error = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер перезагрузки когов. Ошибка',
                description=f'Боту не удалось перезагрузить ког `{extension}`. Возможно, вы ошиблись с названием.\nВывод консоли:```{e}```',
                color=0xED4245
            )
            print(f"[ERROR] Ког {file[:-3]} не был перезагружен: {e}")
            await message.edit(embed=embed_error, delete_after=120)


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        try:
            client.load_extension("cogs." + file[:-3])
            print(f"[STARTUP] Ког {file[:-3]} был успешно загружен")
        except Exception as e:
            print(f"[ERROR] Ког {file[:-3]} не был загружен: {e}")

client.run(TOKEN, reconnect=True)