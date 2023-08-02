from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def load_more(driver):
    # Loop to click on the "Load More" button until it's no longer present
    load_more_btn = driver.find_element(By.CLASS_NAME, 'ipl-load-more__button')
        
    while load_more_btn.is_displayed():
        # TODO: stop when n_max is met
        load_more_btn.click()
        load_more_btn = driver.find_element(By.CLASS_NAME, 'ipl-load-more__button')
        driver.execute_script("arguments[0].scrollIntoView();", load_more_btn)
        time.sleep(1)

def get_reviews(url, movie, year, driver_path, n_max=None, verbose=False):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.maximize_window()

    # Search the target movie
    driver.get(url)
    search_input = driver.find_element(By.ID, 'suggestion-search') 
    search_input.send_keys(movie)
    search_input.submit()
    time.sleep(1)

    # Go to the first in the list and check for year if provided
    titles = driver.find_element(By.XPATH, './/ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base"]')
    top = titles.find_element(By.TAG_NAME, 'li')
    if year: 
        if top.text != str(year):
            print('Error: Target movie not found!')
            return
    top.click()
    # TODO: check with the user

    # Go to the review block
    review_btn = driver.find_element(By.XPATH, "//ul[@data-testid='hero-subnav-bar-topic-links']//li//a[text()='User reviews']")
    review_btn.click()

    # Get #review
    n_review = int(driver.find_element(By.XPATH, "//div[@class='header']//div//span").text.split(' Reviews')[0])
    if n_max:
        if n_max > n_review:
            n_max = n_review
    else:
        n_max = n_review

    # Load all the reviews
    load_more(driver)

    # init review list
    reviews = []
    review_lst = driver.find_element(By.CLASS_NAME, 'lister-list')

    for review in review_lst.find_elements(By.XPATH, './*'):
        title = review.find_element(By.CLASS_NAME, 'title').text
        content = review.find_element(By.CLASS_NAME, 'text').text
        rating = review.find_element(By.TAG_NAME, 'span').text
        date = review.find_element(By.CLASS_NAME, 'review-date').text
        action = review.find_element(By.CLASS_NAME, 'actions').text
        reviews.append({"Title": title,
                        "Content": content,
                        "Rating": rating,
                        "Date": date,
                        "Action": action,
                        })
        if verbose:
            print(f'#{len(reviews)}: {title}') 
        if len(reviews) == n_max:
            break


    return pd.DataFrame(reviews)  # This line converts the dictionary object into a pandas DataFrame.

