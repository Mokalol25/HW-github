import logging
import os
import xml.etree.ElementTree as ET


class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


def logged(exception, mode="console"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.ERROR)

            if mode == "console":
                handler = logging.StreamHandler()
            else:
                handler = logging.FileHandler("log.txt", encoding="utf-8")

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)

            logger.handlers.clear()
            logger.addHandler(handler)

            try:
                return func(*args, **kwargs)
            except exception as e:
                logger.error(f"Стався виняток {str(e)}")
                raise

        return wrapper

    return decorator


class XMLFileManager:

    @logged(FileNotFound, mode="console")
    def __init__(self, filepath):
        self.filepath = filepath

        if not os.path.exists(filepath):
            raise FileNotFound(f"Файл '{filepath}' не існує")

        try:
            self.tree = ET.parse(filepath)
            self.root = self.tree.getroot()
        except Exception:
            raise FileCorrupted("XML файл пошкоджено або має неправильний формат.")

    @logged(FileCorrupted, mode="console")
    def read(self):
        try:
            return ET.tostring(self.root, encoding="unicode")
        except Exception:
            raise FileCorrupted("неможливо прочитати XML файл.")

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
            raise FileCorrupted("неможливо додати елемент до XML файлу.")

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
            raise FileCorrupted("неможливо видалити елемент з XML файлу.")


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

print("\n----Відгруповані книги за роками")

books_by_year = {}

for book in manager.root.findall("book"):
    year = book.find("year").text
    title = book.find("title").text

    if year not in books_by_year:
        books_by_year[year] = []

    books_by_year[year].append(title)

for year in sorted(books_by_year.keys()):
    print(f"\nРік {year}:")
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
