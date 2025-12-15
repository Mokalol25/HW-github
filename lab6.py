import logging
import os
import xml.etree.ElementTree as ET


class FileNotFound(Exception):
    """
    Custom exception raised when a file is not found.
    """
    pass


class FileCorrupted(Exception):
    """
    Custom exception raised when the XML file is corrupted or in an invalid format.
    """
    pass


def setup_logger(func_name, mode="console"):
    logger = logging.getLogger(func_name)
    logger.setLevel(logging.ERROR)

    if mode == "console":
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler("log.txt", encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Avoid adding multiple handlers if it's already added
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger


def logged(exception, mode="console"):
    def decorator(func):
        # Set up the logger once when the decorator is applied
        logger = setup_logger(func.__name__, mode)

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                logger.error(f"An exception occurred: {str(e)}")
                raise

        return wrapper

    return decorator


class XMLFileManager:
    """
    A class for managing an XML file of books, allowing reading, adding, and deleting books.
    """

    @logged(FileNotFound, mode="console")
    def __init__(self, filepath):
        self.filepath = filepath

        if not os.path.exists(filepath):
            raise FileNotFound(f"File '{filepath}' does not exist")

        try:
            self.tree = ET.parse(filepath)
            self.root = self.tree.getroot()
        except Exception:
            raise FileCorrupted("The XML file is corrupted or in an invalid format.")

    @logged(FileCorrupted, mode="console")
    def read(self):
        try:
            return ET.tostring(self.root, encoding="unicode")
        except Exception:
            raise FileCorrupted("Unable to read the XML file.")

    @logged(FileCorrupted, mode="console")
    def append_book(self, book_id, title, author, year):
        try:
            new_book = ET.SubElement(self.root, "book")
            new_book.set("id", str(book_id))

            ET.SubElement(new_book, "title").text = title
            ET.SubElement(new_book, "author").text = author
            ET.SubElement(new_book, "year").text = str(year)

            self.tree.write(self.filepath, encoding="utf-8", xml_declaration=True)
        except Exception:
            raise FileCorrupted("Unable to add a new book to the XML file.")

    @logged(FileCorrupted, mode="console")
    def delete_book(self, book_id):
        try:
            for book in self.root.findall("book"):
                if book.get("id") == str(book_id):
                    self.root.remove(book)
                    self.tree.write(self.filepath, encoding="utf-8", xml_declaration=True)
                    return True
            return False
        except Exception:
            raise FileCorrupted("Unable to delete the book from the XML file.")


if __name__ == "__main__":
    manager = XMLFileManager("lab6.xml")

    print("\n----INITIAL CONTENT")
    print(manager.read())

    print("\n----ADDING NEW BOOK")
    manager.append_book(4, "title_4", "name_4", 2025)
    print(manager.read())

    print("\n----DELETING BOOK ID = 3")
    manager.delete_book(3)
    print(manager.read())

    print("\n----Grouped books by year")

    books_by_year = {}

    for book in manager.root.findall("book"):
        year = book.find("year").text
        title = book.find("title").text

        if year not in books_by_year:
            books_by_year[year] = []

        books_by_year[year].append(title)

    for year in sorted(books_by_year.keys()):
        print(f"\nYear {year}:")
        for title in books_by_year[year]:
            print(f"- {title}")



# <?xml version="1.0" encoding="UTF-8"?>
# <catalog>
#     <book id="1">
#         <title>title_1</title>
#         <author>name_1</author>
#         <year>1991</year>
#     </book>

#     <book id="2">
#         <title>title_2</title>
#         <author>name_2</author>
#         <year>2003</year>
#     </book>

#     <book id="3">
#         <title>title_3</title>
#         <author>name_3</author>
#         <year>2010</year>
#     </book>

# </catalog>

