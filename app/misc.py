'''
import psycopg2
from psycopg2.extras import RealDictCursor
import fastapi

app = fastapi.FastAPI()
my_posts = [
     {"title": "Title of Post 1", "content": "Content of post 1", "id": 1},
     {"title": "Title of Post 2", "content": "Content of post 2", "id": 2},
     ]

# my_posts_sorted = {post["id"]: post for post in my_posts_list}

def find_post(id: int):
     for post in my_posts:
          if post["id"] == id:
               return post

def find_post_index(id: int):
     for i, p in enumerate(my_posts):
          if p["id"] == id:
               return i

@app.get("/")
async def welcome():
     # await asyncio.sleep(10)
     return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
     posts = cursor.execute("""SELECT * FROM posts""")
     posts = cursor.fetchall()
     return {"data": posts}

# @app.get("/posts/latest") # Needs to be above /posts/id because FastAPI looks topdown and posts/id matches
# def get_post_latest():
#      return my_posts[-1]

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
     post = find_post(id)
     if not post:
          # response.status_code = status.HTTP_404_NOT_FOUND
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id: {id} was not found")
     return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
     guid = random.randint(1, 1000000)
     post_dict = post.dict()
     post_dict["id"] = guid
     my_posts.append(post_dict)
     return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
     index = find_post_index(id)
     if index == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id: {id} does not exist")
     my_posts.pop(index)
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post: Post):
     # post_to_update = find_post(id)
     # if not post_to_update:
     #      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
     #                          detail=f"post with id: {id} was not found")
     # index = find_post_index(id)
     index = find_post_index(id)
     if index == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id: {id} does not exist")
     my_posts[index] = post
     return {"data" : post}

# Misc

class CarPost(BaseModel): # Inherit from pydantic -> Json Schema
     make: str
     model: str
     acquired: bool = False
     rating: Optional[int] = None

@app.get("/cars")
def getCars():
     car_map = {
          1: "Lotus Elise",
          2: "Lotus Esprit",
          3: "Lotus Exige"
     }
     randomInt = random.randint(1,len(car_map))
     return {randomInt: car_map[randomInt]}

@app.post("/cars")
def create_cars(received_payload: CarPost): # Automatic validation with the Post model
     # print(received_payload)
     return f"{received_payload.make} {received_payload.model} - {received_payload.acquired} - {received_payload.rating}"


try:
     conn = psycopg2.connect(host='', database='', user='',
     password='', cursor_factory=RealDictCursor)
     cursor = conn.cursor()
     print(f"Database connection was successful.")
except Exception as error:
     # time.sleep(5)
     print(f"Database connection has failed - {error}")

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
     posts = db.query(models.Post).all()
     print(posts)
     return {"data": posts}

while True:
     try:
          conn = psycopg2.connect(host="", database="", user="postgress",
                                  password="", cursor_factory=RealDictCursor)
          cursor = conn.cursor()
          print("Database connection successful")
          break
     except Exception as error:
          print("Connecting to database failed")
          print("Error: ", error)
          time.sleep(2)
'''