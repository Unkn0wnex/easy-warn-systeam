import discord
from discord.ext import commands
import json
import os

bot = discord.Bot()

WARNINGS_FILE = 'warnings.json'
LANG_FILE = 'lang.json'

if os.path.exists(WARNINGS_FILE) and os.path.getsize(WARNINGS_FILE) > 0:
    with open(WARNINGS_FILE, 'r') as f:
        warnings = json.load(f)
else:
    warnings = {}

if os.path.exists(LANG_FILE) and os.path.getsize(LANG_FILE) > 0:
    with open(LANG_FILE, 'r') as f:
        lang = json.load(f)
else:
    lang = {"language": "ru"}

def save_language():
    with open(LANG_FILE, 'w') as f:
        json.dump(lang, f, indent=4)

def save_warnings():
    with open(WARNINGS_FILE, 'w') as f:
        json.dump(warnings, f, indent=4)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(name='warn', description='Выдать предупреждение пользователю')
async def warn(ctx: discord.ApplicationContext, member: discord.Member, reason: str):
    if ctx.author.guild_permissions.kick_members:
        if str(member.id) not in warnings:
            warnings[str(member.id)] = []
        warnings[str(member.id)].append({'issuer_id': ctx.author.id, 'reason': reason})
        save_warnings()
        if lang["language"] == "ru":
            embed = discord.Embed(title="Предупреждение", description=f"Выдано предупреждение пользователю {member.mention}", color=discord.Color.red())
            embed.add_field(name="Причина", value=reason, inline=False)
            embed.set_footer(text=f"Выдал: {ctx.author.display_name}")
        else:
            embed = discord.Embed(title="Warning", description=f"Warning issued to {member.mention}", color=discord.Color.red())
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Issued by: {ctx.author.display_name}")
        await ctx.respond(embed=embed)
    else:
        if lang["language"] == "ru":
            embed = discord.Embed(title="Ошибка", description="У вас нет прав для выполнения этой команды.", color=discord.Color.red())
        else:
            embed = discord.Embed(title="Error", description="You do not have permission to execute this command.", color=discord.Color.red())
        await ctx.respond(embed=embed)

@bot.slash_command(name='warnings', description='Посмотреть все предупреждения пользователя')
async def get_warnings(ctx: discord.ApplicationContext, member: discord.Member):
    if str(member.id) in warnings:
        if lang["language"] == "ru":
            embed = discord.Embed(title=f"Предупреждения пользователя {member.display_name}", color=discord.Color.red())
        else:
            embed = discord.Embed(title=f"{member.display_name}'s Warnings", color=discord.Color.red())
        for index, warning in enumerate(warnings[str(member.id)]):
            issuer = ctx.guild.get_member(warning['issuer_id'])
            if lang["language"] == "ru":
                embed.add_field(name=f"Предупреждение #{index + 1}", value=f"Выдал: {issuer.mention}\nПричина: {warning['reason']}", inline=False)
            else:
                embed.add_field(name=f"Warning #{index + 1}", value=f"Issued by: {issuer.mention}\nReason: {warning['reason']}", inline=False)
        await ctx.respond(embed=embed)
    else:
        if lang["language"] == "ru":
            embed = discord.Embed(title="Предупреждения", description=f"У пользователя {member.mention} нет предупреждений.", color=discord.Color.green())
        else:
            embed = discord.Embed(title="Warnings", description=f"{member.mention} has no warnings.", color=discord.Color.green())
        await ctx.respond(embed=embed)

@bot.slash_command(name='removewarn', description='Снять предупреждение у пользователя')
async def removewarn(ctx: discord.ApplicationContext, member: discord.Member, index: int):
    if ctx.author.guild_permissions.kick_members:
        if str(member.id) in warnings and 1 <= index <= len(warnings[str(member.id)]):
            removed_warning = warnings[str(member.id)].pop(index - 1)
            save_warnings()
            issuer = ctx.guild.get_member(removed_warning['issuer_id'])
            if lang["language"] == "ru":
                embed = discord.Embed(title="Снятие предупреждения", description=f"Предупреждение от {issuer.mention} с причиной '{removed_warning['reason']}' было снято у пользователя {member.mention}.", color=discord.Color.green())
            else:
                embed = discord.Embed(title="Warning Removal", description=f"Warning from {issuer.mention} with reason '{removed_warning['reason']}' has been removed from {member.mention}.", color=discord.Color.green())
            await ctx.respond(embed=embed)
            if not warnings[str(member.id)]:
                del warnings[str(member.id)]
                save_warnings()
        else:
            if lang["language"] == "ru":
                embed = discord.Embed(title="Ошибка", description=f"У пользователя {member.mention} нет предупреждения с индексом {index}.", color=discord.Color.red())
            else:
                embed = discord.Embed(title="Error", description=f"{member.mention} does not have a warning with index {index}.", color=discord.Color.red())
            await ctx.respond(embed=embed)
    else:
        if lang["language"] == "ru":
            embed = discord.Embed(title="Ошибка", description="У вас нет прав для выполнения этой команды.", color=discord.Color.red())
        else:
            embed = discord.Embed(title="Error", description="You do not have permission to execute this command.", color=discord.Color.red())
        await ctx.respond(embed=embed)

@bot.slash_command(name='changelang', description='Сменить язык сообщений')
async def changelang(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        if lang["language"] == "ru":
            lang["language"] = "en"
            embed = discord.Embed(title="Language Change", description="Language has been changed to English.", color=discord.Color.green())
        else:
            lang["language"] = "ru"
            embed = discord.Embed(title="Смена языка", description="Язык был изменен на русский.", color=discord.Color.green())
        save_language()
        await ctx.respond(embed=embed)
    else:
        if lang["language"] == "ru":
            embed = discord.Embed(title="Ошибка", description="У вас нет прав для выполнения этой команды.", color=discord.Color.red())
        else:
            embed = discord.Embed(title="Error", description="You do not have permission to execute this command.", color=discord.Color.red())
        await ctx.respond(embed=embed)

bot.run("YOUR TOKEN HERE")
