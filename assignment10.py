from fastapi import FastAPI, Query
from typing import List

app = FastAPI()


movies = [
    {"id": i, "title": f"Movie {i}", "year": 2000 + i}
    for i in range(1, 101) 
]

@app.get("/movies", response_model=List[dict])
def get_movies(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
   
    start = (page - 1) * page_size
    end = start + page_size
    paginated_movies = movies[start:end]

    total_pages = (len(movies) + page_size - 1) // page_size

    return {
        "page": page,
        "page_size": page_size,
        "total_movies": len(movies),
        "total_pages": total_pages,
        "data": paginated_movies
    }
