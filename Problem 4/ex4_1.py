from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import unicodedata
def remove_diacritics(text):
    if pd.isna(text):
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ) 
def crawl_data(url):
    chromedriver_path = "D:\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    try:
        service = Service(chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(3) 
        soup = bs(driver.page_source, 'html.parser')
        table = soup.find('table')  

        if table:
            data = []
            rows = table.find_all('tr')

            for row in rows:
                player = row.find_all('span', attrs={'class': 'd-none'})
                price = row.find_all('td', attrs={'class': 'text-center'})
                price = [p.text.strip() for p in price]
                player = [p.text.strip() for p in player]
                cols = player + price
                if cols:
                    data.append(cols)
            data = data[2:]
            df = pd.DataFrame(data)
            return df
        driver.quit()

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        driver.quit()

if __name__ == '__main__':
    df = crawl_data('https://www.footballtransfers.com/us/players/uk-premier-league')
    for i in range(2,23):
        url = 'https://www.footballtransfers.com/us/players/uk-premier-league' + '/' + str(i)
        df = pd.concat([df, crawl_data(url)],ignore_index=False)
    df = df[[0, 2]]
    df = df.rename(columns={
        0: 'Player',
        2: 'Price',
    })
    df['Player'] = df['Player'].replace('Rasmus Winther Højlund', 'Rasmus Højlund')
    df['Player'] = df['Player'].replace('Idrissa Gueye', 'Idrissa Gana Gueye')
    df['Player'] = df['Player'].replace('Manuel Ugarte', 'Manuel Ugarte Ribeiro')
    df['Player'] = df['Player'].replace('Omari Giraud-Hutchinson', 'Omari Hutchinson')
    df['Player'] = df['Player'].replace('Rayan Aït Nouri', 'Rayan Ait-Nouri')
    df['Player'] = df['Player'].replace('Heung-min Son', 'Son Heung-min')
    df['Player'] = df['Player'].replace('Victor Kristiansen', 'Victor Bernth Kristiansen')
    df['Player'] = df['Player'].apply(remove_diacritics)
    df_epl = pd.read_csv('Problem 1/results.csv', na_values='N/a')
    df_epl.drop(columns='Unnamed: 0', inplace=True)
    df_epl['Player'] = df_epl['Player'].apply(remove_diacritics)
    df = df.merge(df_epl, on='Player', how='outer')
    df = df[df['Playing_time: Min'] > 900]
    df = df[['Player', 'Price', 'Playing_time: Min']]
    df.dropna(subset=['Price'],inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('D:/file python/bài tập lớn/Problem 4/results.csv',index = True)