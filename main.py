import os
import discord
from discord.ext import commands
from datetime import datetime
from config import *
from myserver import keep_alive

# Start Flask server สำหรับ Render
keep_alive()

# ----- Intents -----
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----- Verify Form / View -----
class VerifyForm(discord.ui.Modal, title="🌸 แบบฟอร์มยืนยันตัวต้นจ้าา.."):
    # ... (โค้ด Modal เดิมของคุณ) ...
    async def on_submit(self, interaction: discord.Interaction):
        try:
            # โค้ดเดิมทั้งหมด
            user = interaction.user
            guild = interaction.guild
            role = guild.get_role(ROLE_ID)
            if role in user.roles:
                await interaction.response.send_message(
                    "⚠️ คุณยืนยันไปแล้ว อย่ากดเล่นเดะโดนซัดหน้า👊",
                    ephemeral=True
                )
                return
            await interaction.response.send_message(
                "✅ ยืนยันตัวต้นเรียบร้อย...",
                ephemeral=True
            )
            await user.add_roles(role)
            fetched = await bot.fetch_user(user.id)
            avatar = user.display_avatar.url
            banner = fetched.banner.url if fetched.banner else None
            log = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
            if not log:
                return
            embed = discord.Embed(
                title="📄 キャラクター覚醒",
                description=f"```fix\n✔ {user} ได้ยืนยันตัวต้นแล้ว\n```",
                color=AURA_COLOR,
                timestamp=datetime.utcnow()
            )
            if banner:
                embed.set_image(url=banner)
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="🧑‍🎤 ชื่อเล่น", value=self.name.value, inline=True)
            embed.add_field(name="🎂 อายุ", value=self.age.value, inline=True)
            embed.add_field(name="📜 เจอดิสนี้จาก..", value=self.reason.value, inline=False)
            embed.add_field(name="✨ Server", value="```diff\n+ ยินดีต้อนรับสมาชักใหม่\n+ ทำตามกฎด้วยละ ฮา ฮา\n```", inline=False)
            embed.add_field(name="🏅 ยศที่ได้รับ", value=role.mention, inline=False)
            embed.set_footer(text="ข้อมูลของคุณ 🌸 • New Member", icon_url=avatar)
            await log.send(embed=embed)
        except Exception as e:
            print("❌ ERROR in Modal on_submit:", e)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="情報を入力してください。 (Verify)", style=discord.ButtonStyle.blurple, emoji="🎀")
    async def awaken(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerifyForm())

# ----- Command -----
@bot.command()
async def verify(ctx):
    try:
        embed = discord.Embed(
            title="🌸 アニメ・認証システム",
            description=(
                "```yaml\n"
                "STATUS: Identity verification is required.\n"
                "WORLD: ૮₍亗𝓢𝓣𝓘𝓝𝓚𝓨亗₎ა\n"
                "```"
                "✨ กดปุ่มด้านล่างเพื่อปลดผนึกพลัง\n"
                "⚠️ ผู้ที่ไม่ยืนยันจะไม่สามารถเข้าโลกนี้ได้"
            ),
            color=ANIME_COLOR
        )
        embed.add_field(name="🎎 กฎของโลกนี้", value="<#1446834998912225410>", inline=False)
        embed.set_footer(text="แบบฟอร์มกรอกข้อมูล • 夜桜 Verification",
                         icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        await ctx.send(embed=embed, view=VerifyView())
    except Exception as e:
        print("❌ ERROR in verify command:", e)

# ----- Ready -----
@bot.event
async def on_ready():
    try:
        bot.add_view(VerifyView())
        print(f"🟢 Bot Online | {bot.user}")
    except Exception as e:
        print("❌ ERROR in on_ready:", e)

# ----- Run Bot -----
bot.run(os.getenv("TOKEN"))
