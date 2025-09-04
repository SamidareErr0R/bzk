import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Googleスプレッドシート設定
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("文化祭在庫管理").sheet1

st.set_page_config(page_title="文化祭 在庫管理", layout="centered")

st.title("🍧 文化祭 在庫管理システム")
st.write("スマホから在庫をリアルタイムで管理できます。")

# データ取得
data = SHEET.get_all_records()

# 商品リスト作成
item_names = [row["商品名"] for row in data]
selected_item = st.selectbox("商品を選んでください", item_names)

# 選択した商品の在庫表示
item_row = next((row for row in data if row["商品名"] == selected_item), None)
current_stock = item_row["在庫数"] if item_row else 0

st.metric(label=f"{selected_item} の在庫数", value=f"{current_stock} 個")

# 販売数入力
qty = st.number_input("販売数を入力してください", min_value=1, max_value=100, value=1, step=1)

# 在庫更新
if st.button("在庫を更新"):
    new_stock = max(current_stock - qty, 0)
    cell = SHEET.find(selected_item)
    SHEET.update_cell(cell.row, cell.col + 1, new_stock)
    st.success(f"{selected_item} の在庫を {new_stock} 個に更新しました！")
    st.experimental_rerun()

# 在庫一覧表示
st.subheader("📦 在庫一覧")
for row in data:
    st.write(f"{row['商品名']}: {row['在庫数']} 個")