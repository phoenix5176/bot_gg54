import os
from datetime import datetime
from threading import Thread

import discord
from discord.ext import commands
from flask import Flask

# =========================
# Flask keep-alive for Render
# =========================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

keep_alive()

# =========================
# Discord Bot setup
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# Config
# =========================
ROLE_ID = 1433683710212833330  # ใส่ role ที่จะให้ user
LOG_CHANNEL_NAME = "┊📜┊「𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧」"  # ชื่อ channel log
ANIME_COLOR = 0xFFC0CB
AURA_COLOR = 0xFF69B4

# =========================
# Modal for verification
# =========================
class VerifyForm(discord.ui.Modal, title="🌸 แบบฟอร์มยืนยันตัวต้น"):
    name = discord.ui.TextInput(label="ชื่อเล่น", placeholder="ใส่ชื่อเล่นของคุณ", required=True)
    age = discord.ui.TextInput(label="อายุ", placeholder="เช่น 18", required=True)
    reason = discord.ui.TextInput(label="เจอดิสนี้ทางที่ไหน", style=discord.TextStyle.long, placeholder="คุณเข้ามาในโลกนี้จากที่ไหน...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = interaction.user
            guild = interaction.guild
            role = guild.get_role(ROLE_ID)
            if not role:
                await interaction.response.send_message("⚠️ ไม่พบ role ที่กำหนด", ephemeral=True)
                return

            if role in user.roles:
                await interaction.response.send_message("⚠️ คุณยืนยันไปแล้วลืมหรือป่าว ถ้าลืมเดะจูนให้น้าา👊", ephemeral=True)
                return

            await interaction.response.send_message("✅ ยืนยันตัวต้นเรียบร้อยค้าบฟู้วววว😁", ephemeral=True)
            await user.add_roles(role)

            fetched = await bot.fetch_user(user.id)
            avatar = user.display_avatar.url
            banner = fetched.banner.url if fetched.banner else None

            log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
            if not log_channel:
                return

            embed = discord.Embed(
                title="📄 キャラクター覚醒",
                description=f"✔ {user.mention} ได้ยืนยันตัวต้นแล้ว",
                color=AURA_COLOR,
                timestamp=datetime.utcnow()
            )
            if banner:
                embed.set_image(url=banner)
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="🧑‍🎤 ชื่อเล่น", value=self.name.value, inline=True)
            embed.add_field(name="🎂 อายุ", value=self.age.value, inline=True)
            embed.add_field(name="📜 เจอดิสนี้จาก..", value=self.reason.value, inline=False)
            embed.add_field(
    name="✨ Server",
    value=(
        "🌸 ยินดีต้อนรับสมาชิกใหม่\n"
        "📜 ทำตามกฎของโลกนี้\n"
        "🎉 สนุกและมีความสุขในโลกของเรา!"
          ),
            inline=False
          )

            embed.add_field(name="🏅 ยศที่ได้รับ", value=role.mention, inline=False)
            embed.set_footer(text="ข้อมูลของคุณ 🌸 • New Member", icon_url=avatar)

            await log_channel.send(embed=embed)

        except Exception as e:
            print("❌ ERROR in Modal on_submit:", e)

# =========================
# Verify button
# =========================
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="情報を入力してください。 (Verify)", style=discord.ButtonStyle.blurple, emoji="🎀")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerifyForm())

# =========================
# Command
# =========================
@bot.command()
async def verify(ctx):
    try:
        embed = discord.Embed(
            title="🌸 アニメ・認証システム",
            description=(
                "STATUS: 𝗜𝗗𝗘𝗡𝗧𝗜𝗧𝗬 𝗩𝗘𝗥𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗜𝗦 𝗥𝗘𝗤𝗨𝗜𝗥𝗘𝗗.\n"
                "WORLD: ૮₍亗𝓢𝓣𝓘𝓝𝓚𝓨亗₎ა\n"
                "✨ กดปุ่มด้านล่างเพื่อปลดผนึกพลัง\n"
                "⚠️ ผู้ที่ไม่ยืนยันจะไม่สามารถเข้าโลกนี้ได้"
            ),
            color=ANIME_COLOR
        )
        embed.add_field(name="🎎 กฎของโลกนี้", value="<#1446834998912225410>", inline=False)
        embed.set_footer(text="แบบฟอร์มกรอกข้อมูล • 夜桜 Verification", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)

        view = VerifyView()
        await ctx.send(embed=embed, view=view)
        bot.add_view(view)  # add view ทันที
    except Exception as e:
        print("❌ ERROR sending verify:", e)

# =========================
# on_ready
# =========================
@bot.event
async def on_ready():
    try:
        bot.add_view(VerifyView())
        print(f"🟢 Bot Online | {bot.user}")
    except Exception as e:
        print("❌ ERROR in on_ready:", e)

# =========================
# Run Bot
# =========================
bot.run(os.getenv("TOKEN"))

