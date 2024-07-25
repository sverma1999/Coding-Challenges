import requests
import pandas as pd


# Task 1: Parse Available Datasets------------------------------------------


def load_books(title):
    try:
        # Fetches books from the Open Library API
        url = f"https://openlibrary.org/search.json"
        # Parameters for the API request: we are searching for books with the title
        params = {"title": title}
        # Make the request and get the response data
        response = requests.get(url, params=params)
        # Convert the response data to a dictionary
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return {}


def parse_books(data):
    # We will store the parsed books in a list. Each book will be a dictionary with keys: title, author, publish_date, and number_of_pages
    books = []

    # Loop through the list of books in the response data
    for doc in data.get("docs", []):
        book = {
            "Title": doc.get("title"),
            "Author": doc.get("author_name", ["Unknown"])[0],
            "First Published": doc.get("first_publish_year"),
            "Ratings (out of 5)": doc.get("ratings_average", 0),
            "Number of Ratings": doc.get("ratings_count", 0),
        }
        books.append(book)
    return books


# Task 2: Retrieve a Specific Dataset------------------------------------------


def laod_books_by_subject(subject):
    try:
        # Fetches books by subject from the Open Library API
        url = f"https://openlibrary.org/subjects/{subject}.json"

        # Make the request and get the response data
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()

        # Convert the response data to a dictionary
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return {}


def parse_books_by_subject(data):
    # We will store the parsed books in a list. Each book will be a dictionary with keys: title, authors, and first_published
    books = []

    # Loop through the list of works in the response data
    for work in data.get("works", []):
        book = {
            "Title": work.get("title"),
            "Authors": ", ".join(
                author.get("name") for author in work.get("authors", [])
            ),
            "First Published": work.get("first_publish_year"),
        }
        books.append(book)
    return books


# Save the parsed data to a CSV file
def save_locally(books, filename):
    df = pd.DataFrame(books)
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    # Task 1: Parse Available Datasets------------------------------------------
    title = "lord of the rings"
    books_data = load_books(title)
    if books_data:
        books = parse_books(books_data)
        # Save the parsed books data to CSV files
        save_locally(books, "lord_of_the_rings_books.csv")
    else:
        print("No books data found")

    # Task 2: Retrieve a Specific Dataset------------------------------------------
    subject = "machine learning"
    books_by_subjects_data = laod_books_by_subject(subject)
    if books_by_subjects_data:
        books_by_subject = parse_books_by_subject(books_by_subjects_data)

        # Save the parsed books by subject data to a CSV file
        save_locally(books_by_subject, "ml_books.csv")
    else:
        print("No books data found")
