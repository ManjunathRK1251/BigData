from fastapi import FastAPI,Response, status,HTTPException
from fastapi.responses import JSONResponse
# from recomm.recomsystem import get_recommendations_new
from recomm import recomsystem as rec
from recomm import disney_recomm as dsrec
import json
from fastapi.responses import UJSONResponse
application = FastAPI()
app=application
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

@app.get("/recommend/{show_name}",status_code=200)
async def read_item(show_name:str):
    try:
        pdsr=rec.get_recommendations_new(show_name)
    except:
        Response.status_code=status.HTTP_403_FORBIDDEN
        # return {"message":"Movie Not Found in Database"}
        raise HTTPException(status_code=404, detail="Item not found")
    lst=list(pdsr.values)
    print(lst)
    return JSONResponse(content=lst,media_type="application/json")


@app.get("/disney_recommend/{show_name}",status_code=200,response_class=UJSONResponse)
async def read_item(show_name:str,):
    try:
        pdsr=dsrec.extended_recommender(show_name)
    except:
        Response.status_code=status.HTTP_403_FORBIDDEN
        return {"message":"Movie Not Found in Database"}
    lst=list(pdsr.values)
    print(lst)
    jsondata=json.dumps(lst)
    # return JSONResponse(content=lst,media_type="application/json")
    return Response(content=jsondata, media_type="application/json")