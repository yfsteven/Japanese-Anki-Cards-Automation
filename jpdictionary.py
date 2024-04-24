#! python3
# jpdictionary.py - web scrabe goojp of definition and convert the data into csv file
import requests, bs4, sys, os, csv

os.makedirs('anki_csv', exist_ok=True)

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

            with open(os.path.join('anki_csv', os.path.basename(f'{word}.csv')), 'w', newline='') as textfile:
                csvwriter = csv.writer(textfile)
                csvwriter.writerow([f'{word}', f'{full_sentence}'])



        print(full_sentence)
    except Exception as err:
        print('エラー! 確認して下さい: %s' % (err))
