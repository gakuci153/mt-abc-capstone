from bs4 import BeautifulSoup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
import json

# Strip the invalid characters for file name
def sanitize_filename(url):
    invalid_chars = ':/?<>\\|*\"'
    for char in invalid_chars:
        url = url.replace(char, "_")
    return url

def scrape_website(url, exclude_dirs=[], max_depth=5):
     # Instantiate the RecursiveUrlLoader
    loader = RecursiveUrlLoader(
        url=url, 
        extractor=lambda x: BeautifulSoup(x, "html.parser").get_text(separator='\n', strip=True),
        max_depth=max_depth,
        prevent_outside = True,
        check_response_status = True,
        continue_on_failure = True,
        base_url = url,
        exclude_dirs=exclude_dirs
    )

    # Load the data from the website
    docs = loader.load()

    # Define the file path to store the data
    file_name = sanitize_filename(url)
    output_file = f'./data/{file_name}.json'

    output = []
    
    # Write metadata and content for each document to the file
    for doc in docs:
        output_dic = {}
        title = doc.metadata.get("title")
        source = doc.metadata.get("source")
        content = doc.page_content

        if isinstance(title, str) and isinstance(source, str) and isinstance(content, str):
            output_dic['title'] = title
            output_dic['source'] = source
            output_dic['content'] = content

            output.append(output_dic)
        else:
            print("Skipped a document due to non-string content.")

        json_output = json.dumps(output)

    # Open the file in write mode with UTF-8 encoding
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_output)

    print("Data has been successfully written to", output_file)