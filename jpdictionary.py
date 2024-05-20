#! python3
# jpdictionary.py - web scrape goojp dictionary and convert the data into a single csv file that can be easily imported to Anki
import requests
import bs4
import sys
import os
import csv
from ankicsvimporter import send_to_anki_connect, invoke_ac
from dotenv import load_dotenv
from elevenlabs import Voice, VoiceSettings, save
from elevenlabs.client import ElevenLabs

os.makedirs('anki_csv', exist_ok=True) # creates a folder to hold csv file

load_dotenv()

client = ElevenLabs(
  api_key=os.getenv("ELEVEN_LAB_API_KEY"), # insert api key
)


if len(sys.argv) > 1:
    try:
        for word in sys.argv[1:]:

            url = f'https://dictionary.goo.ne.jp/word/{word}/'
            res = requests.get(url)
            res.raise_for_status()
            wordSoup = bs4.BeautifulSoup(res.text, 'html.parser')
            jp_text = wordSoup.select('.text')

            full_sentence = ''.join(str(s) for s in jp_text)

            audio = client.generate(
                text = full_sentence,
                model="eleven_multilingual_v2",
                voice=Voice(
                    voice_id="j210dv0vWm7fCknyQpbA", #Japanese Voice ID
                    settings=VoiceSettings(stability=0.50, similarity_boost=0.65, style=0, use_speaker_boost=True),
                )
            )

            save(audio, f"/home/vboxuser/.local/share/Anki2/ユーザー 1/collection.media/{word}.wav") #May be different from yours, but this saves audio to Anki's media collection folder. Must do this or else not able to get media files

            location = os.path.join('anki_csv', os.path.basename('words.csv'))

            with open(location, 'a', newline='') as textfile: #Adds in at the last row of CSV
                file_is_empty = os.stat(location).st_size == 0
                csvwriter = csv.DictWriter(textfile, delimiter=',', fieldnames=['表面', '裏面', 'Audio']) # you must include fieldnames and must be correct for anki-csv-importer program to work
                if file_is_empty:
                    csvwriter.writeheader() # writes fieldname if empty however limitation is that it's only work if
                csvwriter.writerow({'表面': f'{word}', '裏面': f'{full_sentence}', 'Audio': f'[sound:{word}.wav]'})


            send_to_anki_connect( #import csv file and sync anki. Must install ankiconnect addon. Please read anki-csv-importer documentation
                location, #path to csv file
                'デフォルト', # deckname
                '基本') # note type
            print('[+] Syncing')
            invoke_ac("sync")

        print('Done')
    except Exception as err:
        print('エラー! 確認して下さい: %s' % (err))
