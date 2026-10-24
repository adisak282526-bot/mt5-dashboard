import streamlit as st
import json
import os

# ตั้งค่าหน้าจอ Dashboard
st.set_page_config(
    page_title="EA ADIDAS Dashboard",
    page_icon="🎮",
    layout="centered"
)

# โหลดข้อมูลพอร์ตจากไฟล์ JSON
def load_data():
    file_path = "portfolio_status.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

st.title("🎮 EA ADIDAS Dashboard")
st.caption("ระบบติดตามเป้าหมายเกมการเทรดเรียลไทม์")

if data:
    balance = data.get("balance", 0.0)
    equity = data.get("equity", 0.0)
    floating_pl = equity - balance
    
    # 🎯 การคำนวณเป้าหมายเกม
    target_game = 20.0
    
    # รอบจบเกมสะสม (คำนวณจากกำไรพอร์ต)
    wins = int(floating_pl // target_game) if floating_pl > 0 else 0
    current_round_profit = floating_pl % target_game if floating_pl > 0 else floating_pl
    remaining = target_game - current_round_profit
    
    progress = max(0.0, min(1.0, current_round_profit / target_game)) if current_round_profit > 0 else 0.0

    st.markdown("---")
    
    # --- ส่วนที่ 1: เป้าหมายเกมหลัก ---
    st.subheader(f"🎯 เป้าหมายรอบนี้: ${target_game:.2f} USD")
    
    # กำหนดสีตามสถานการณ์
    if remaining <= target_game and floating_pl >= 0:
        rem_color = "#FFA500"  # สีส้มทอง (ปกติ/บวก)
    else:
        rem_color = "#FF4B4B"  # สีแดง (ติดลบ/โดนลาก)

    st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333;">
            <p style="margin: 0; color: #888; font-size: 16px;">🏁 ระยะทางจบเกม (เหลืออีก)</p>
            <h1 style="margin: 5px 0; color: {rem_color}; font-size: 42px;">${remaining:.2f} USD</h1>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write(f"📈 **ความคืบหน้ารอบปัจจุบัน:** {progress * 100:.1f}%")
    st.progress(progress)

    st.markdown("---")

    # --- ส่วนที่ 2: สรุปผลงานประจำวัน ---
    st.subheader("🏆 สรุปผลงานประจำวัน (Daily Tracker)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🥇 จบเกมวันนี้", value=f"{wins} รอบ")
    with col2:
        daily_target = 100.0
        st.metric(label="🚩 เป้าหมายใหญ่ประจำวัน", value=f"${daily_target:.2f}")

    st.markdown("---")

    # --- ส่วนที่ 3: ข้อมูลพอร์ตปัจจุบัน ---
    st.subheader("📊 ข้อมูลพอร์ตปัจจุบัน (Portfolio Status)")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="💳 Balance", value=f"${balance:,.2f}")
    col_b.metric(label="📈 Equity", value=f"${equity:,.2f}", delta=f"{floating_pl:,.2f}")
    col_c.metric(label="📊 Floating P/L", value=f"${floating_pl:,.2f}", delta_color="normal")

else:
    st.warning("⏳ รอข้อมูลจากระบบ... (กรุณาตรวจสอบการรันไฟล์ auto_push.py บนคอมพิวเตอร์)")
    
      
