import os
import asyncio
import importlib
import logging
from aiohttp import web
from colorama import Fore, Style, init

from ShrutiCHATBOT import (
    ShrutiCHATBOT,
    userbot,
    LOGGER,
    load_clone_owners,
)
from ShrutiCHATBOT.modules import ALL_MODULES
from config import OWNER_ID, STRING1
from pyrogram.types import BotCommand
from pyrogram import idle

# ─────── Initialize colorama ───────
init(autoreset=True)

# ─────── Custom Logger ───────
class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Fore.CYAN + "🐞 [DEBUG] " + Style.RESET_ALL + "%(message)s",
        logging.INFO: Fore.GREEN + "ℹ️ [INFO] " + Style.RESET_ALL + "%(message)s",
        logging.WARNING: Fore.YELLOW + "⚠️ [WARNING] " + Style.RESET_ALL + "%(message)s",
        logging.ERROR: Fore.RED + "❌ [ERROR] " + Style.RESET_ALL + "%(message)s",
        logging.CRITICAL: Fore.MAGENTA + "💥 [CRITICAL] " + Style.RESET_ALL + "%(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

# ─────── Keepalive Web Server ───────
PORT = int(os.environ.get("PORT", 10000))  # Render or UptimeRobot port

async def handle(request):
    return web.Response(text="✅ Shruti ChatBot is alive!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    LOGGER.info(f"✅ Web server running on port {PORT}")
    return runner

# ─────── Bot Startup ───────
async def start_bots():
    try:
        # Start main bot
        await ShrutiCHATBOT.start()
        LOGGER.info(f"🚀 @{ShrutiCHATBOT.username} Started Successfully ✅")

        # Notify owner
        try:
            await ShrutiCHATBOT.send_message(
                int(OWNER_ID),
                f"✨ {ShrutiCHATBOT.mention} is now <b>Alive & Running ✅</b>",
            )
        except Exception:
            LOGGER.warning("⚡ Could not notify owner (start bot from owner account).")

        # Start userbot if STRING1 is set
        if STRING1:
            try:
                await userbot.start()
                LOGGER.info("🤖 Id-Chatbot started successfully ✅")
                try:
                    await ShrutiCHATBOT.send_message(int(OWNER_ID), "🤖 Id-Chatbot Also Started ✅")
                except Exception:
                    LOGGER.warning("⚡ Could not notify owner about Id-Chatbot")
            except Exception as ex:
                LOGGER.error(f"❌ Failed to start userbot: {ex}")

        # Load all modules
        for module in ALL_MODULES:
            importlib.import_module("ShrutiCHATBOT.modules." + module)
            LOGGER.info(f"📦 Loaded Module: {Fore.CYAN}{module}{Style.RESET_ALL}")

        # Import commands.py explicitly so handlers register
        try:
            import ShrutiCHATBOT.commands
            LOGGER.info("📌 Commands module loaded ✅")
        except ModuleNotFoundError:
            LOGGER.warning("⚠️ No commands.py found, command handlers won't work!")

        # Set bot commands
        try:
            await ShrutiCHATBOT.set_bot_commands(
                [
                    BotCommand("start", "Start the bot"),
                    BotCommand("help", "Get the help menu"),
                    BotCommand("clone", "Make your own chatbot"),
                    BotCommand("idclone", "Make your id-chatbot"),
                    BotCommand("cloned", "Get List of all cloned bot"),
                    BotCommand("ping", "Check if the bot is alive or dead"),
                    BotCommand("lang", "Select bot reply language"),
                    BotCommand("chatlang", "Get current using lang for chat"),
                    BotCommand("resetlang", "Reset to default bot reply lang"),
                    BotCommand("id", "Get users user_id"),
                    BotCommand("stats", "Check bot stats"),
                    BotCommand("gcast", "Broadcast message to groups/users"),
                    BotCommand("chatbot", "Enable or disable chatbot"),
                    BotCommand("status", "Check chatbot enable/disable in chat"),
                    BotCommand("shayri", "Get random shayri for love"),
                    BotCommand("ask", "Ask anything from ChatGPT"),
                ]
            )
            LOGGER.info("✅ Bot commands set successfully.")
        except Exception as ex:
            LOGGER.error(f"❌ Failed to set bot commands: {ex}")

        LOGGER.info(f"🎉 @{ShrutiCHATBOT.username} is fully up & running! 🚀")

        # Keep bot running
        await idle()

    except Exception as ex:
        LOGGER.critical(f"🔥 Bot failed to start: {ex}")

# ─────── Main Runner ───────
async def main():
    # Start web server and bot concurrently
    web_runner = await start_web_server()
    await start_bots()
    # Cleanup when idle ends
    await web_runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER.info("Bot stopped.")
