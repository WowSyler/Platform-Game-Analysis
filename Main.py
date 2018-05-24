import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import time

import TwetConnet as tc

site1 = "https://www.bolumsonucanavari.com/?pidx=13&pgidx="
site2 = "&f1id=0&f2id=0&f3id=0&mod="
data = []
dataa = []

for allpage in range(0, 10000, 1):
    url = site1 + str(allpage) + site2
    print("\nPage:" + str(allpage))
    url_oku = requests.get(url)
    soup = BeautifulSoup(url_oku.content, 'html.parser')

    gelenveri = soup.find_all('div', {'class':'listeleme'})
    icerik = (gelenveri[0].contents)[len(gelenveri[0].contents) - 9]
    tamammi = len(icerik)
    if tamammi == 3:
        break
    elif gelenveri != "":
        platform = (gelenveri[0].contents)[len(gelenveri[0].contents)-9]

        platform = platform.find_all('div', {'class':'tek'})

        for game in platform:
            data = game.find_all("a", {"class":"platform"})
            data = data[0].text
            data = data.strip()
            dataa.append(data)
            print(data)

counter = Counter(dataa)
pc = counter['PC']
ps4 = counter['PS4']
ps3 = counter['PS3']
x360 = counter['XBOX 360']
x = counter['XBOX ONE']
mobil = counter['Mobil']
ds3 = counter['3DS']
ds = counter['DS']
psp = counter['PSP']
vita = counter['VITA']
swch = counter['SWITCH']
wiiu = counter['Wii U']
wi = counter['Wii']

labels = ['PC', 'PS4', 'PS3', '360', 'XBOX1', 'Mobil', '3DS', 'DS', 'PSP', 'VITA', 'SWTCH', 'WiU', 'Wii']
sizes = [pc, ps4, ps3, x360, x, mobil, ds3, ds, psp, vita, swch, wiiu, wi]
colors = ['green', 'red', 'grey', 'black', 'yellow', 'blue', 'purple', 'pink', 'brown', 'orange', 'maroon', 'grey','pink']

y_post = np.arange(len(labels))
plt.bar(y_post, sizes, color=colors, align='center', alpha=0.7)
plt.xticks(y_post, labels)
plt.ylabel('Game Count')
plt.xlabel('Platform')
plt.title("Platform Game Count")
plt.show()

print("\n Total Game Count: ", len(dataa))
print("Total Pc Count: ", int(pc), "\n Total Ps4 Count: ", int(ps4), "\n Total Ps3 Count: ", int(ps3))
print("Total Xbox one Count: ", int(x), "\n Total xbox360 Count: ", int(x360), "\n Total mobil Count: ", int(mobil))
print("Total ds3 Count: ", int(ds3), "\n Total ds Count: ", int(ds), "\n Total psp Count: ", int(psp))
print("Total vita Count: ", int(vita), "\n Total swcih Count: ", int(swch), "\n Total wiiu Count: ", int(wiiu))
print("Total wii Count: ", int(wi), "\n")





searchTwetTag = ["pc -#PC -#ps4 -#mobil -ps4 -xbox",'mobil game -#ps4 -#pc -#xbox360 -pc -ps4', 'xbox one -#pc -#ps4 -#mobil -pc -ps4', 'ps4 -#PS4 -#pc -#mobil -pc -xbox']
title = ["PC Game Platform", "Mobil game platform","Xbox One game platform","Ps4 Game Platform"]
grapTitle = ["Current PC - Negative / Positive  Tweet","Current Mobil - Negative / Positive  Tweet","Current Xbox One - Negative / Positive  Tweet", "Current PS4 - Negative / Positive  Tweet"]
grapTitleall = ["PC - Negative / Positive  Tweet","Mobil - Negative / Positive  Tweet","Xbox One - Negative / Positive  Tweet", "PS4 - Negative / Positive  Tweet"]
platformPoz = ["pc-poz.txt","Mobil-poz.txt","Xbox1-poz.txt","Ps4-poz.txt"]
platformNeg = ["pc-neg.txt","Mobil-neg.txt","Xbox1-neg.txt","Ps4-neg.txt"]
grapColor = ['black','grey','green','blue']
index = 0

api = tc.TwitterAnalysisApi()

while index < len(searchTwetTag):
    tweetss = api.get_tweets(query=searchTwetTag[index], count=150)
    print("\n  ############################# \n")
    # picking positive tweets from tweets
    ptweetss = [tweet for tweet in tweetss if tweet['sentiment'] == 'positive']
    # picking negative tweets from tweets
    ntweetss = [tweet for tweet in tweetss if tweet['sentiment'] == 'negative']
    nntweetss = [tweet for tweet in tweetss if tweet['sentiment'] == 'neutral']


    print("##### " + title[index] + " #####")
    print("\n\nHam tweets:")
    for tweet in tweetss[:4]:
        print(tweet['ham']+"\n #####\n")

    print("\n\nClear tweets:")
    for tweet in tweetss[:4]:
        print(tweet['text'])

    print("\n\nAnalysis tweets:")
    for tweet in tweetss[:4]:
        print(tweet['text'] + " = " + tweet['sentiment'])

    print("\n\nPositive tweets:")
    for tweet in ptweetss[:2]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweetss[:2]:
        print(tweet['text'])

    print("\n\nNuetral tweets:")
    for tweet in nntweetss[:2]:
        print(tweet['text'])


    try:
        txtPosR = open(platformPoz[index], "a+")
        txtNegR = open(platformNeg[index], "a+")
        txtNegR.seek(0)
        txtPosR.seek(0)
        dataPosW = txtPosR.readlines()
        dataNegW = txtNegR.readlines()

        for tweet in ptweetss:
            txtPosR.write(tweet['text'] + "\n")

        for tweet in ntweetss:
            txtNegR.write(tweet['text'] + "\n")


        txtNegR.seek(0)
        txtPosR.seek(0)
        dataPosNew = txtPosR.readlines()
        dataNegNew = txtNegR.readlines()


        totalOld = len(dataPosNew) + len(dataNegNew)

        print("\n #### All Data Tweet Analysïs ####")
        if totalOld != 0:
            print("Positive tweets percentage: {} %".format(100 * len(dataPosNew) / totalOld))
            print("Negative tweets percentage: {} %".format(100 * len(dataNegNew) / totalOld))
            print("Total positive tweet count: ", len(dataPosNew))
            print("Total negative tweet count: ", len(dataNegNew))
            print("Total tweet count: ", totalOld)

        pos = len(dataPosNew)
        neg = len(dataNegNew)
        labels = 'Positive', 'Negative'
        sizes = [pos, neg]
        colors = [grapColor[index], 'red']

        plt.pie(sizes, labels=labels, colors=colors, shadow=True, startangle=90)
        plt.title("All data " + grapTitleall[index])
        plt.show()

        txtPosR.flush()
        txtNegR.flush()
        txtNegR.close()
        txtPosR.close()
    except IOError:
        print(grapTitle[index] + " there is an error here.")

    print("\n ####  Current twet analysis, only max 150 twet  ####")
    print("Current Positive tweets percentage: {} %".format(100 * len(ptweetss) / len(tweetss)))
    print("Current Negative tweets percentage: {} %".format(100 * len(ntweetss) / len(tweetss)))
    print("Current Neutral tweets percentage: {} %".format(
        100 * (len(tweetss) - (len(ptweetss) + len(ntweetss))) / len(tweetss)))
    print("Current positive tweet count: ", len(ptweetss))
    print("Current negative tweet count: ", len(ntweetss))
    print("Current tweet count: ", len(tweetss))

    posss = len(ptweetss)
    neggg = len(ntweetss)
    labels = 'Positive', 'Negative'
    sizes = [posss, neggg]
    colors = [grapColor[index], 'red']

    plt.pie(sizes, labels=labels, colors=colors, shadow=True, startangle=90)
    plt.title(grapTitle[index])
    plt.show()
    index += 1

    print("\nWait 5 s.\n")
    time.sleep(3)







