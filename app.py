import streamlit as st
import json
import os

# ตั้งค่าหน้าจอ Dashboard แบบกระชับ
st.set_page_config(
    page_title="EA ADIDAS Dashboard",
    page_icon="🎮",
    layout="centered"
)

def load_data():
    file_path = "portfolio_status.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

data = load_data()

# หัวข้อแบบกระชับลดพื้นที่ว่าง
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🎮 EA ADIDAS Dashboard</h2>", unsafe_allow_html=True)

if data:
    balance = data.get("balance", 0.0)
    equity = data.get("equity", 0.0)
    floating_pl = equity - balance
    
    target_game = 20.0
    daily_target = 100.0
    
    wins = int(floating_pl // target_game) if floating_pl > 0 else 0
    current_round_profit = floating_pl % target_game if floating_pl > 0 else floating_pl
    remaining = target_game - current_round_profit
    progress = max(0.0, min(1.0, current_round_profit / target_game)) if current_round_profit > 0 else 0.0
    daily_progress = max(0.0, min(1.0, floating_pl / daily_target)) if floating_pl > 0 else 0.0

    # สีตัวเลขระยะทางจบเกม
    if remaining <= target_game and floating_pl >= 0:
        rem_color = "#FFA500"  # สีส้มทอง
    else:
        rem_color = "#FF4B4B"  # สีแดง

    # --- ส่วนที่ 1: การ์ดหลัก (ระยะทางจบเกม + เป้าหมายรอบ) ---
    st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #333; margin-top: 5px;">
            <p style="margin: 0; color: #888; font-size: 14px;">🎯 เป้าหมายรอบนี้ (${target_game:.0f}) | เหลือระยะทางจบเกม</p>
            <h1 style="margin: 2px 0; color: {rem_color}; font-size: 36px;">${remaining:.2f} USD</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)

    # --- ส่วนที่ 2: สรุปผลงานประจำวันแบบ 2 คอลัมน์กระชับ ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🥇 จบเกม:** `{wins} รอบ`")
    with col2:
        st.markdown(f"**🚩 เป้าใหญ่:** `{daily_progress * 100:.1f}%`")
    
    st.progress(daily_progress)

    # --- ส่วนที่ 3: สถานะพอร์ตแบบบรรทัดเดียวจบ ---
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric(label="💳 Bal", value=f"${balance:,.0f}")
    c2.metric(label="📈 Eq", value=f"${equity:,.1f}")
    c3.metric(label="📊 P/L", value=f"${floating_pl:,.2f}")

else:
    st.warning("⏳ รอข้อมูลจากระบบ (auto_push.py)...")
    
    
      
