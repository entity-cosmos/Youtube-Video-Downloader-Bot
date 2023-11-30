import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters
from pytube import YouTube
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

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

def main() -> None:
    global youtube_downloader_bot
    youtube_downloader_bot = YoutubeDownloaderBot()

    application = Application.builder().token("5385502733:AAEkgNIbNL9sTyguk---nDiS0c-JMX2rybw").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("yt", download_video))
    application.add_handler(CommandHandler("list", list_downloaded_videos))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
