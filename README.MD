# vista-signage

##### Usage
```bash
./generate_html_pages.py [4-digit-location-code] [theater-number]
./generate_html_pages.py 0009 1
```

##### Results
```bash
$ ./generate_html_pages.py 0337 1
Theater  Location ScheduledFilmId ShowtimeStart        ShowtimeEnd          RunTime  Title                                    URL                                                         
1        0337     HO00001662      2018-07-26T11:00:00  2018-07-26T12:38:00  98       HOTEL TRANSYLVANIA 3: SUMMER VACATION    http://srv001.vista.smg337.studiomoviegrill.com/Cinema-CDN/Image/Entity/FilmTitleGraphic/h-HO00001662
1        0337     HO00001662      2018-07-26T13:45:00  2018-07-26T15:23:00  98       HOTEL TRANSYLVANIA 3: SUMMER VACATION    http://srv001.vista.smg337.studiomoviegrill.com/Cinema-CDN/Image/Entity/FilmTitleGraphic/h-HO00001662
1        0337     HO00001662      2018-07-26T16:30:00  2018-07-26T18:08:00  98       HOTEL TRANSYLVANIA 3: SUMMER VACATION    http://srv001.vista.smg337.studiomoviegrill.com/Cinema-CDN/Image/Entity/FilmTitleGraphic/h-HO00001662
1        0337     HO00001710      2018-07-26T19:15:00  2018-07-26T21:16:00  121      EQUALIZER 2                              http://srv001.vista.smg337.studiomoviegrill.com/Cinema-CDN/Image/Entity/FilmTitleGraphic/h-HO00001710
1        0337     HO00001652      2018-07-26T22:15:00  2018-07-27T00:23:00  128      JURASSIC WORLD: FALLEN KINGDOM           http://srv001.vista.smg337.studiomoviegrill.com/Cinema-CDN/Image/Entity/FilmTitleGraphic/h-HO00001652
```

##### Installation OSX
```bash
brew install python3
pip3 install requests
```

##### Installation Linux
```bash
sudo apt-get install python3
pip3 install requests
```