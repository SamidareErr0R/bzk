import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# StreamlitのSecretsからcredentialsを取得
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("文化祭在庫管理").sheet1