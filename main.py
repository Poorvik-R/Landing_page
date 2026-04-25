from fastapi import FastAPI , Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import gspread
from google.oauth2.service_account import Credentials

import os
import json
from google.oauth2.service_account import Credentials
import gspread

app=FastAPI()

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

client = gspread.authorize(creds)

sheet = client.open("Contact_details").sheet1

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)









@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )



@app.post("/submit")
async def submit_form(
    # here three dot means that the field is required and must be provided in the form data
    name: str = Form(...),   
    email: str = Form(...),
    message: str = Form(...)
):
    try:
        sheet.append_row([name, email, message])
        return RedirectResponse(url="/success", status_code=303)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request):
    return templates.TemplateResponse(
        request,
        "success.html",
        {"request": request})


from fastapi import Request

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    print("Webhook received:", data)

    return {"status": "received"}

