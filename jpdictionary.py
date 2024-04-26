#! python3
# jpdictionary.py - web scrabe goojp of definition and convert the data into a single csv file that can be easily imported to Anki
import requests, bs4, sys, os, csv
from dotenv import load_dotenv
from elevenlabs import Voice, VoiceSettings, play, save
from elevenlabs.client import ElevenLabs

os.makedirs('anki_csv', exist_ok=True)

load_dotenv()

client = ElevenLabs(
  api_key=os.getenv("API_KEY"),
)


if len(sys.argv) > 1:
    try:
        for word in sys.argv[1:]:
            url = f'https://dictionary.goo.ne.jp/word/{word}/'
            res = requests.get(url)
            res.raise_for_status()
            wordSoup = bs4.BeautifulSoup(res.text, 'html.parser')
            jp_text = wordSoup.select('.text')

            full_sentence = ''

            for element in jp_text:
                full_sentence += element.text

            audio = client.generate(
                text = full_sentence,
                model="eleven_multilingual_v2",
                voice=Voice(
                    voice_id="j210dv0vWm7fCknyQpbA", #Japanese Voice ID
                    settings=VoiceSettings(stability=0.50, similarity_boost=0.65, style=0, use_speaker_boost=True),
                )
            )

            save(audio, f"/home/vboxuser/.local/share/Anki2/ユーザー 1/collection.media/{word}.wav") #May be different from yours, but this saves audio to Anki's media collection folder. Must do this or else not able to import media files


            with open(os.path.join('anki_csv', os.path.basename('words.csv')), 'a', newline='') as textfile: #Adds in at the last row of CSV
                csvwriter = csv.writer(textfile)
                csvwriter.writerow([f'{word}', f'{full_sentence}', f'[sound:{word}.wav]'])
            print(full_sentence)

        print('Done')
    except Exception as err:
        print('エラー! 確認して下さい: %s' % (err))
