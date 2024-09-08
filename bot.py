import os
import requests
from telethon import TelegramClient, events
import yt_dlp

# إعدادات API من Telegram
api_id = '29147240'
api_hash = '0fe85fc806f0e22291b804262404d273'
bot_token = '7492476383:AAE-stROYDC9TA2dxV_kTP8Je46-VCKpCBs'
target_bot_token = '7492476383:AAE-stROYDC9TA2dxV_kTP8Je46-VCKpCBs'  # التوكن الخاص بالبوت المستلم للفيديو

# إعدادات البوتين
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
target_bot_url = f'https://api.telegram.org/bot{target_bot_token}/sendVideo'

# دالة لتحميل الفيديوهات
def download_video(url, output_dir='downloads'):
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'best',  # تحميل أفضل صيغة متاحة
        'noplaylist': True,
        'postprocessors': []  # تجنب الدمج التلقائي
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info)
        return video_file

# دالة لإرسال الفيديو إلى بوت آخر
def send_video_to_another_bot(video_file, chat_id):
    with open(video_file, 'rb') as video:
        response = requests.post(
            target_bot_url,
            data={'chat_id': chat_id},
            files={'video': video}
        )
        return response

# التعامل مع أمر /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("يا اهلين وسهلين في  بوت تحميل فيديوهات من مواقع التواصل  الاجتماعي")
    await event.respond("تم صنع البوت بواسطة  المطور ياسين")
    await event.respond("Insta : y30_s")
    await event.respond("telegram : dev_yassin")
# التعامل مع الرسائل التي تحتوي على الروابط
@client.on(events.NewMessage)
async def handle_message(event):
    url = event.raw_text

    # تحقق ما إذا كان النص المُرسل رابطاً صالحاً
    if not (url.startswith("http://") or url.startswith("https://")):
        await event.respond("دز رابط فيديو بعد كلبي انت /انتِ " )
        return

    await event.respond("صبرك علينه شوي ويجيك فيديو يا بعد عمري انت ")
    try:
        video_file = download_video(url)
        # إرسال الفيديو إلى بوت آخر
        response = send_video_to_another_bot(video_file, event.chat_id)
        if response.status_code == 200:
            await event.respond("جاك فديو بعد عمري")
        else:
            await event.respond(f"حدث خطأ أثناء إرسال الفيديو: {response.text}")
        # حذف الملف بعد الإرسال
        os.remove(video_file)
    except Exception as e:
        await event.respond(f"حدث خطأ أثناء تحميل الفيديو: {str(e)}")

# بدء العميل
if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    print("Bot is running...")
    client.run_until_disconnected()