# Tämä on esimerkkiohjelma miten aikataulusta sijaitsevasta pdf:stä saadaan
# irti csv jonka voi ladata Google Kalenteriin.
# Valititettavasti koodi on ehkä suuremmilta osilta kertakäyttöinen, sillä seuraava aikataulu
# on eheämpi tai rikkonaisempi. 
# Helpontuntuinen teksti ei ollutkaan niin helppo varsinkin kun on ensimmäinen koodi
# Jos nyt satut lukemaan tämän, niin kommentoi ihmeessä miten tekisit tämän paremmin
# TODO: Universaalimpi toteutus jos mahdollista? 
# Juha Halmu 19.4.2022  


# pdf:n muuttaminen käsiteltävään muotoon
import camelot

#pandalla tehdään DataFrame jota on helpompi muokata
import pandas as pd

# luetaan pdf objektiivisempaan muotoon
tables = camelot.read_pdf('Aikataulu.pdf', flavor='stream')

# tällä saadaan oikea kohta ja tehdään siitä dataframe 
df = tables[0].df

# karsitaan turhia rönsyjä tiedosta eli siistitään
df = df.iloc[3:,1:]

# irroitetaan tekstistä päivämäärä ja otsikoksi tuleva
df1 = df[1].str.split("2022").str.get(0)
df2 = df[1].str.split("2022").str.get(1)

# purkalla laitetaan vuosi perään kun sitä käytettiin splittaamisessa
df1 = df1+"2022"

# muutetaan päivä google kalenterin muotoon
df1 = pd.to_datetime(df1).dt.strftime('%m/%d/%Y')

# yhdistellään palasia
df3 = pd.concat([df1,df2], axis=1)
df4 = pd.concat([df3,df[2],df[3]], axis=1)

# resetoidaan indexi että näyttää kauniimmalta
df4 = df4.reset_index(drop=True)

# lisätään otsikot Google kalenterin mukaan
df4 = df4.set_axis(['Start Date','Subject','Description','Location'], axis='columns')

# leivotaan pandalla csv-muotoon googleen ladattavaksi
df4.to_csv('foo.csv', index=False)

#  tällä voi tarkastella tulostetta terminaalissa
#print(df4)