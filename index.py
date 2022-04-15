import disnake
from disnake.ext import commands
import sqlite3
import os
import http.client
import time

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
        start_time = int(time.time())
        ip = http.client.HTTPConnection("ifconfig.me")
        ip.request("GET", "ip")
        ips = str(ip.getresponse().read())
        ips = ips.replace("'", "")
        ips = ips.replace("b", "")
        dev1 = await self.get_user(450229150217797633)
        embed = disnake.Embed(
            title = "Запуск бота. Успешно",
            color=0x5865F2
        )
        embed.add_field(name="Время запуска:", value=f"<t:{start_time}:F>", inline = True)
        embed.add_field(name="IP-адрес хоста:", value=f"{ips}")
        await dev1.send(embed=embed)
        print('[STARTUP] Бот в строю!')

    async def on_guild_join(self, guild):
        log = self.get_channel(847748996302241792)
        if log is not None:
            embed = disnake.Embed(
                title="Бот был добавлен на сервер",
                color=0x57F287
            )
            if guild.icon.url is not None:
                embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="Название:", value=f"`{guild.name}`", inline=True)
            embed.add_field(name="Сервер создан:", value= f"<t:{str(guild.created_at.timestamp() * 1000) [:-5]}:F>", inline=True)
            try:
                own = await self.bot.fetch_user(guild.owner_id)
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

    async def on_slash_command_error(self, inter, error):
        embed = disnake.Embed(
            title="Произошла ошибка",
            color=0xED4245
        )
        embed.add_field(name="Код ошибки:", value = f"```{error}```")
        inter.send(embed=embed)


client = Login()


@client.command()
async def reload(ctx, extension):
    embed_wait = disnake.Embed(title="<:chitty_settings:924980025223155723> Менеджер загрузки когов. Ожидание перезагрузки", description=f"Идёт перезагрузка кога `{extension}`.", color=0xFEE75C)
    embed_successfully = disnake.Embed(title='<:chitty_settings:924980025223155723> Менеджер агрузки когов. Успех', description=f'Ког `{extension}` успешно перезагружен.', color=0x57F287)
    message = await ctx.send(embed=embed_wait)
    if (ctx.author.id in developers) and (extension is not None) and (extension != "all"):
        try:
            client.reload_extension(f"cogs.{extension}")
            await message.edit(embed=embed_successfully, delete_after=60)
            print(f"[INFO] Ког {extension} был успешно перезагружен")
        except Exception as e:
            embed_error = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер загрузки когов. Ошибка перезагрузки',
                description=f'Боту не удалось перезагрузить ког `{extension}`. Возможно, вы ошиблись с названием.\n\nВывод консоли:```{e}```',
                color=0xED4245
            )
            await message.edit(embed=embed_error, delete_after=30)
            print(f"[ERROR] Ког {extension} не был перезагружен: {e}")
    elif (ctx.author.id in developers) and (extension == "all"):
        try:
            for file in os.listdir("./cogs"):
                if file.endswith(".py"):
                    client.reload_extension("cogs." + file[:-3])
            print(f"[INFO] Все коги былы успешно перезагружены")
            embed_reloadAll = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер загрузки когов. Успех',
                description=f'Все коги были перезагружены.',
                color=0x57F287
            )
            await message.edit(embed=embed_reloadAll, delete_after=120)
        except Exception as e:
            embed_error = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер загрузки когов. Ошибка перезагрузки',
                description=f'Боту не удалось перезагрузить ког `{extension}`. Возможно, вы ошиблись с названием.\nВывод консоли:```{e}```',
                color=0xED4245
            )
            print(f"[ERROR] Ког {file[:-3]} не был перезагружен: {e}")
            await message.edit(embed=embed_error, delete_after=120)

@client.command()
async def load(ctx, extension):
    if (ctx.author.id in developers) and (extension is not None) and (extension != "all"):
        embed_wait = disnake.Embed(title="<:chitty_settings:924980025223155723> Менеджер загрузки когов. Ожидание загрузки", description=f"Идёт загрузка кога `{extension}`.", color=0xFEE75C)
        embed_successfully = disnake.Embed(title='<:chitty_settings:924980025223155723> Менеджер загрузки когов. Успех', description=f'Ког `{extension}` успешно загружен.', color=0x57F287)
        message = await ctx.send(embed=embed_wait)
        try:
            client.load_extension("cogs." + file[:-3])
            await message.edit(embed=embed_successfully, delete_after=60)
            print(f"[INFO] Ког {extension} был успешно перезагружен")
        except:
            embed_error = disnake.Embed(
                title='<:chitty_settings:924980025223155723> Менеджер загрузки когов. Ошибка перезагрузки',
                description=f'Боту не удалось перезагрузить ког `{extension}`. Возможно, вы ошиблись с названием.',
                color=0xED4245
            )
            embed_error.add_feld(name="Вывод консоли:", value=f"```{e}```")
            await message.edit(embed=embed_error, delete_after=30)
            print(f"[ERROR] Ког {extension} не был перезагружен: {e}")



for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        try:
            client.load_extension("cogs." + file[:-3])
            print(f"[STARTUP] Ког {file[:-3]} был успешно загружен")
        except Exception as e:
            print(f"[ERROR] Ког {file[:-3]} не был загружен: {e}")

client.run(TOKEN, reconnect=True)