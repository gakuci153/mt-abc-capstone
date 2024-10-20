from helper import scraper, utility

DATA_FILES = {
    "acra" : "./data/https___www.acra.gov.sg.txt", 
    "gobusiness" : "./data/https___www.gobusiness.gov.sg.txt",
    "iras" : "./data/https___www.iras.gov.sg.txt"
}

def load_data(website_name):

    data_source = utility.load_ds_file()

    if website_name in data_source.keys():
        
        url = data_source[website_name]["base_url"]
        exclude_dirs = data_source[website_name]["exclude_urls"]

        # iras website thorws exception for max_depth = 5
        max_depth= 4 if 'iras' == website_name else 5
        
        print(f"Scraping started for {url}")
        scraper.scrape_website(url, exclude_dirs, max_depth)
        print(f"Scraping for {url} completed.")
        print("---------------------")

    else:
        print(f"{website_name} not found. Skip loading...")


def prepare_data(data_files):

    for key in data_files:
        if not utility.check_file(data_files[key]):
            load_data(key)
        else:
            print(f"{data_files[key]} already exist. Skip loading.")


if __name__ == "__main__":

    load_data("all1")