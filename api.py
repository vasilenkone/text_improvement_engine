from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import uuid
import uvicorn
import os
from main import ImprovementSuggestor
import dataframe_image as dfi
import pandas as pd

pd.options.display.max_colwidth = 150
INPUTDIR = 'example_input/'
OUTPUTPATH = 'example_output/output.png'

app = FastAPI(
    title="Text_improvement_AI"
)
templates = Jinja2Templates(directory="htmlDirectory")

@app.post("/api/v1/upload_terms/")
async def upload_terms(file: UploadFile = File(...)):
    file.filename = f'{uuid.uuid4()}.csv'
    contents = await file.read()
    with open(f'{INPUTDIR}{file.filename}', 'wb') as f:
        f.write(contents)
    path = os.path.join(INPUTDIR, file.filename)
    return FileResponse(path)

@app.post("/api/v1/text_improvement")
async def text_improvement(request: Request, Check: str = Form(...)):
    files = os.listdir(INPUTDIR)
    full_list = [os.path.join(INPUTDIR, i) for i in files]
    time_sorted_list = sorted(full_list, key=os.path.getmtime)
    index = len(files) - 1
    terms_path = f'{time_sorted_list[index]}'
    dfi.export(ImprovementSuggestor().get_results(Check, terms_path), OUTPUTPATH, table_conversion="matplotlib")
    return FileResponse(OUTPUTPATH)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
