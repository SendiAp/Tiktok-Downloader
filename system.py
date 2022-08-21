import json
import time
import requests
from requests import *
from datetime import datetime
from config import *
from tiktok_module import downloader

api = "https://api.telegram.org/bot" + token_bot
update_id = 0

def SendVideo(userid,msgid):
	tg_url = api + "/sendvideo"
	data = {
		"chat_id":userid,
		"caption":"<b>Upload By:</b> @smtiktokdownloaderbot",
		"parse_mode":"html",
		"reply_to_message_id":msgid,
		"reply_markup":json.dumps({
			"inline_keyboard":[
				[
					{
						"text":"SM•Project",
						"url":"t.me/smprojectID"
					}
				]
			]
		})
	}
	res = post(
		tg_url,
		data=data,
		files={
			"video":open("video.mp4","rb")
		}
	)

def SendMsg(userid,text,msgid):
	tg_url = api + "/sendmessage"
	post(
		tg_url,
		json={
			"chat_id":userid,
			"text":text,
			"parse_mode":"html",
			"reply_to_message_id":msgid
		}
	)

def get_time(tt):
	ttime = datetime.fromtimestamp(tt)
	return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"

def Bot(update):
	try:
		global last_use
		userid = update['message']['chat']['id']
		meseg = update['message']['text']
		msgid = update['message']['message_id']
		timee = update['message']['date']
		dl = downloader.tiktok_downloader()
		if update['message']['chat']['type'] != "private":
			SendMsg(
				userid,
				"Bot hanya berfungsi di obrolan pribadi !",
				msgid
			)
			return
		first_name = update['message']['chat']['first_name']
		print(f"{get_time(timee)}-> {userid} - {first_name} -> {meseg}")
		if meseg.startswith('/start'):
			SendMsg(
				userid,
				"Hai, bot ini dapat mengunduh video tanpa tanda air dari <b>TikTok.</b> Untuk memulai, kirimkan tautan ke bot.\n",
				msgid
			)
		elif "tiktok.com" in meseg and "https://" in meseg :
			getvid = dl.musicaldown(url=meseg,output_name="video.mp4")
			if getvid == False:
				SendMsg(
					userid,
					"<i>Gagal mengunduh video</i>\n\n<i>coba lagi nanti</i>",
					msgid
				)
				return
			elif getvid == "private/remove":
				SendMsg(
					userid,
					"<i>Failed to download video</i>\n\n<i>Video was private or removed</i>",
					msgid
				)
			elif int(len(open('video.mp4','rb').read()) / 1024) > 51200:
				SendMsg(
					userid,
					"<i>Failed to download video</i>\n\n<i>Video size to large</i>",
					msgid
				)
			elif getvid == 'url-invalid':
				SendMsg(
					userid,
					"<i>URL is invalid, send again !</i>",
					msgid)
			else:
				SendVideo(
					userid,
					msgid
				)
		elif "/help" in meseg:
			SendMsg(
				userid,
				"Kirimkan Saya Url Tiktok! Contoh: https://vt.tiktok.com/ZSRSCjoeW/",
				msgid
			)
	except KeyError:
		return
