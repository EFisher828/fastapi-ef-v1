from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import xarray as xr
import numpy as np

app = FastAPI()

origins = ["*"]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

# App decortator that defines method for HTTP get method
# / is the root directory
@app.get("/")
async def root():
    return {"message": "Welcome to the Explore Fall API"}

# Define route to extract data based on latitude and longitude
@app.get("/extract/")
async def extract_data(latitude: float = Query(...), longitude: float = Query(...), date: str = Query(...)):
    # Extract data based on provided latitude and longitude
    try:
        doy = int(datetime.strptime(date,"%Y%m%d").strftime("%j"))
        dataArr = []
        for day in np.arange(244,doy+1):
            dateStr = "2023" + str(datetime.strptime(str(day),"%j").strftime("%m%d"))
            data = xr.open_dataset(f"./foliagedata/{dateStr}.nc")
            value = float(data.sel(latitude=latitude, longitude=longitude, method="nearest")['stage'].values)
            dataArr.append(value)
    except:
        value = None
    return {"latitude": latitude, "longitude": longitude, "date": date, "value": dataArr}