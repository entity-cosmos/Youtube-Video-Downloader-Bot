import os
from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters
from pytube import YouTube
import os

TOKEN = os.environ.get("TOKEN")

app = FastAPI()

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

class YoutubeDownloaderBot:
    def __init__(self):
        self.downloaded_videos = {}

    def download_video(self, video_url):
        try:
            youtube = YouTube(video_url)
            video = youtube.streams.get_highest_resolution()
            file_path = video.download()
            self.downloaded_videos[video.title] = file_path
            return f"Video '{video.title}' downloaded successfully.", file_path
        except Exception as e:
            return f"Error: {str(e)}", None

    def get_downloaded_videos(self):
        return list(self.downloaded_videos.keys())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Welcome To Cosmos YT Videos Downloader.\n"
        "Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/yt <youtubeVideoUrl> - Download a YouTube video\n"
        "/list - List downloaded videos\n"
        "Only Small Videos are supported for now.\n"
        "Made with ❤️ by @Srajan_B_Shetty\n"
    )
    await update.message.reply_text(text)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        bot = context.bot
        args = context.args
        video_url = " ".join(args)

        if not video_url:
            await update.message.reply_text("Please provide a YouTube video URL.")
            return

        response, file_path = youtube_downloader_bot.download_video(video_url)
        await update.message.reply_text(response)
        if file_path:
            with open(file_path, 'rb') as video_file:
                await bot.send_video(chat_id=update.message.chat_id, video=video_file)
        #delete the video after sending it on telegram
        os.remove(file_path)
    except Exception as e:
        os.remove(file_path)
        await update.message.reply_text(f"Error: {str(e)}")


async def list_downloaded_videos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    downloaded_videos = youtube_downloader_bot.get_downloaded_videos()
    if downloaded_videos:
        text = "Downloaded Videos:\n" + "\n".join(downloaded_videos)
    else:
        text = "No videos downloaded yet."
    await update.message.reply_text(text)

app = FastAPI()

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook Endpoint
    '''
    app = Application(token="5385502733:AAEkgNIbNL9sTyguk---nDiS0c-JMX2rybw")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yt", download_video))
    app.add_handler(CommandHandler("list", list_downloaded_videos))
    app.run_webhook(webhook_data.dict())
    return {"message": "Webhook received successfully"}



@app.get("/")
def index():
    return {"message": "Hello World"}