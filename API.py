import json
import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()


# Format of the response
class Info(BaseModel):

    isbn: str = Query(..., description="book identifier")
    title: str = Query(..., description="book title")
    publisher: str = Query(..., description="book publisher")
    published_date: int = Query(..., description="book published date; timestamp")
    description: str = Query(..., description="book description")
    page_count: int = Query(..., description="number of book pages")
    thumbnail_url: str = Query(..., description="a url to the book cover")
    language: str = Query(..., description="book language")
    average_rating: float = Query(..., description="book rating")
    authors: list[str] = Query(..., description="list of book authors")
    categories: list[str] = Query(..., description="list of book categories")
    is_ebook: bool = Query(..., description="is ebook version available")


# Get dir
with open("dir") as d:
    dirr = d.readline()


# Load JSON file
with open(str(dirr)) as f:
    data = json.load(f)


# Book by ISBN
@app.post("/api/book/{isbn}", response_model=Info, response_model_exclude_none=True)
async def isbn_book(answer: Info, isbn: str):
    """

    :param answer: instance of class Info returned in json format
    :param isbn: isbn number provided by user
    :return: json return with data from answer
    """
    for idx, value in enumerate(data['items']):
        try:
            if value['id'] == isbn or value['volumeInfo']['industryIdentifiers'][0]['identifier'] == isbn or \
                    value['volumeInfo']['industryIdentifiers'][1]['identifier'] == isbn:

                answer.isbn = isbn
                answer.title = value['volumeInfo'].get('title', "")
                answer.publisher = value['volumeInfo'].get('publisher', "")
                try:
                    dt = datetime.strptime(value['volumeInfo'].get('publishedDate', ""), "%Y-%m-%d")
                except ValueError:
                    dt = datetime.strptime(value['volumeInfo'].get('publishedDate', ""), "%Y")
                timestamp = datetime.timestamp(dt)
                answer.published_date = timestamp
                answer.description = value['volumeInfo'].get('description', "")
                answer.page_count = value['volumeInfo'].get('pageCount', 0)
                answer.thumbnail_url = value['volumeInfo']['imageLinks'].get('thumbnail', "")
                answer.language = value['volumeInfo'].get('language', "")
                answer.average_rating = value['volumeInfo'].get('averageRating', 0.0)
                answer.authors = value['volumeInfo'].get('authors', [])
                answer.categories = value['volumeInfo'].get('categories', [])
                answer.is_ebook = value['saleInfo'].get('isEbook', False)

            else:
                continue
        except IndexError:
            pass  # or some logging info
    if answer.title == "string":
        raise HTTPException(status_code=404, detail="No results found")
    else:
        return answer


# Book by category
@app.post("/api/category/{categoryName}/books", response_model=Info, response_model_exclude_unset=True)
async def category_book(answer: Info, categoryName: str, resp=None, i=None, lst=None):
    """

    :param answer: instance of class Info returned in json format
    :param categoryName: category name provided by user
    :param resp: dictionary used to store information from books.json
    :param i: iterator for dictionary
    :param lst: list used to create the response
    :return: json return with data lst
    """
    if resp is None or i is None:
        resp = {}
        i = 0
        lst = []
    for idx, value in enumerate(data['items']):
        try:
            category = str(value['volumeInfo']['categories'])
            if categoryName in category:

                answer.isbn = str(value['volumeInfo'].get('industryIdentifiers'))
                answer.title = value['volumeInfo'].get('title', "")
                answer.publisher = value['volumeInfo'].get('publisher', "")
                try:
                    dt = datetime.strptime(value['volumeInfo'].get('publishedDate', ""), "%Y-%m-%d")
                except ValueError:
                    dt = datetime.strptime(value['volumeInfo'].get('publishedDate', ""), "%Y")
                timestamp = datetime.timestamp(dt)
                answer.published_date = timestamp
                answer.description = value['volumeInfo'].get('description', "")
                answer.page_count = value['volumeInfo'].get('pageCount', 0)
                answer.thumbnail_url = value['volumeInfo']['imageLinks'].get('thumbnail', "")
                answer.language = value['volumeInfo'].get('language', "")
                answer.average_rating = value['volumeInfo'].get('averageRating', 0.0)
                answer.authors = value['volumeInfo'].get('authors', [])
                answer.categories = value['volumeInfo'].get('categories', [])
                answer.is_ebook = value['saleInfo'].get('isEbook', False)

                resp[str(i)] = str(answer)
                i += 1

        except KeyError:
            pass  # or some logging info

    for y in range(len(resp)):
        lst.append({resp[str(y)]})

    json_item = jsonable_encoder(lst)
    if answer.title == "string":
        raise HTTPException(status_code=404, detail="No results found")
    else:
        return JSONResponse(content=json_item)


# For category rating
def get_cat_lst(lst=None):
    """

    :param lst: list of categories in books.json
    :return: list of categories
    """
    for idx, value in enumerate(data['items']):
        try:
            if lst is None:
                lst = []
            cat = str(value['volumeInfo']['categories'])
            if cat not in lst:
                lst.append(cat)
            else:
                continue
            # print(lst)
        except KeyError:
            pass  # or some logging info
    print(lst)
    return lst


# Category rating
@app.post("/api/rating/category")
async def category_book(avg=None, tmp=None, ct=None):
    """

    :param avg: list of average values
    :param tmp: list for temporary storing averageRating and list for formatting json response
    :param ct: list of categories connected with avg list
    :return: json formatted response with category and average rating
    """
    if avg is None or tmp is None or ct is None:
        tmp = []
        avg = []
        ct = []
    lst = get_cat_lst()

    for i in range(0, len(lst), 1):
        for idx, value in enumerate(data['items']):
            try:
                if str(value['volumeInfo']['categories']) in lst[i]:
                    tmp.append(float(value['volumeInfo']['averageRating']))
                    if str(value['volumeInfo']['categories']) not in ct:
                        ct.append(str(value['volumeInfo']['categories']))
                        avg.append(round(sum(tmp) / len(tmp), 2))
            except KeyError:
                pass
    tmp = []
    for i in range(len(ct)):
        tmp.append({"category": ct[i], "averageRating": avg[i]})

    json_data = jsonable_encoder(tmp)
    return JSONResponse(content=json_data)


if __name__ == '__main__':
    uvicorn.run("API:app", host='127.0.0.1', port=4000, reload=True, log_level='info', debug=True)
