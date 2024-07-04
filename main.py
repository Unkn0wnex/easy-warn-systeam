import discord
from discord.ext import commands
import json
import os

bot = discord.Bot()

WARNINGS_FILE = 'warnings.json'

if os.path.exists(WARNINGS_FILE) and os.path.getsize(WARNINGS_FILE) > 0:
    with open(WARNINGS_FILE, 'r') as f:
        warnings = json.load(f)
else:
    warnings = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

def save_warnings():
    with open(WARNINGS_FILE, 'w') as f:
        json.dump(warnings, f, indent=4)

@bot.command(name='warn', help='Выдать предупреждение пользователю')
async def warn(ctx, member: discord.Member, *, reason: str):
    if ctx.author.guild_permissions.kick_members:
        if str(member.id) not in warnings:
            warnings[str(member.id)] = []
        warnings[str(member.id)].append({'issuer_id': ctx.author.id, 'reason': reason})
        save_warnings()
        embed = discord.Embed(title=f"{member.display_name} было выдано предупреждение", description=f"Причина {reason}", color=discord.Color.red())
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("У вас нет прав для выполнения этой команды.")

@bot.command(name='warnings', help='Посмотреть все предупреждения пользователя')
async def get_warnings(ctx, member: discord.Member):
    if str(member.id) in warnings:
        embed = discord.Embed(title=f"Предупреждения пользователя {member.display_name}", color=discord.Color.red())
        for index, warning in enumerate(warnings[str(member.id)]):
            issuer = ctx.guild.get_member(warning['issuer_id'])
            embed.add_field(name=f"Ситуация #{index + 1}", value=f"Выдал: {issuer.mention}\nПричина: {warning['reason']}", inline=False)
        await ctx.respond(embed=embed)
        embdnone = discord.Embed(title=f"Предупреждения пользователя {member.display_name}", description="Предупреждения отсуствуют.", color=discord.Color.red())
    else:
        await ctx.respond(embed=embdnone)

bot.run('')
