import requests
from bs4 import BeautifulSoup

def get_links(n: int | list[int] = -1) -> tuple[list[str], list[str]]:
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        response = requests.get(url)
        parser = BeautifulSoup(response.text, 'html.parser')


        header = parser.find("h2", string=lambda t: t and "Top 100 EBooks yesterday" in t)
        ol = header.find_next_sibling("ol")
        all_items = ol.find_all("a", href=True)

        if n == -1:
            selected = all_items
        elif isinstance(n, int):
            selected = [all_items[n - 1]]
        else:
            selected = [all_items[i - 1] for i in n]

        links, titles = [], []
        for item in selected:
            title = item.get_text(strip=True)
            ebook_id = item["href"].split("/")[-1]
            links.append(f"https://www.gutenberg.org/ebooks/{ebook_id}.txt.utf-8")
            titles.append(title + ".txt")

        return links, titles


    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")

def download_file(url, name, directory):
    response = requests.get(url, stream=True)
    name = directory + name
    with open(name, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
    print(f"Downloaded file: {name}")

def store_files(links, names, directory='./'):
    for url, name in zip(links, names):
        download_file(url, name, directory)

def main(n=-1, directory='./'):
    links, titles = get_links(n)
    store_files(links, titles, directory)
    print("Done")

if __name__ == '__main__':
    directory = 'Books/'
    n = range(1, 51)
    main(n, directory)
