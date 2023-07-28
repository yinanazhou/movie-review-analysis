# -*- coding: utf-8 -*-

import imdb_scraper as scraper
import pandas as pd

driver_path = "./chromedriver_mac_arm64/"

df = scraper.get_reviews('https://www.imdb.com/', 'Barbie', 2023, driver_path, n_max=1000, verbose=True)

df.to_csv('reviews.csv', index=False)