from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Depends, HTTPExceprion, status
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel, EmailStr
from typing import List

from dotenv import dotenv_values

from src.models import SuperUser
import jwt

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smpt.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENATIALS=True,


)


class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(email: EmailSchema, instance: SuperUser):

    token_data = {
        "id": instance.id,
        # "username": instance.name,
    }
    token = jwt.encode(token_data, config_credentials["SECRET"])

    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
                
            </head>
            <body>
                <div style = "display: flex; align-items: center; justify-content: center;
                 flex-direction: column">
                    <h3>Account Verification </h2>
                    <br>
                    
                    <p> Thanks for choosing UES, please click on the button below 
                        to verify your account </p>
                    <a style="marign-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem;
                    text-decoration: none; background: #0275d8; 
                    color: white" href="http://localhost:8000/verifycation/?token={token}">
                    Verify your email
                    </a>
                    <p>Please kindly ignore this email if you did not register for UES and nothing will happend.
                     Thanks</p> 
                </div>
            </body>
        </html>
    """

    message = MessageSchema(
        subject="UES Account Verification Email",
        recipients=email,
        body=template,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message=message)