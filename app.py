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

# หัวข้อกระชับ
st.markdown("<h3 style='text-align: center; margin: 0 0 5px 0;'>🎮 EA ADIDAS Dashboard</h3>", unsafe_allow_html=True)

if data:
    balance = data.get("balance", 0.0)
    equity = data.get("equity", 0.0)
    floating_pl = equity - balance
    
    target_game = 200.0
    daily_target = 10000.0
    
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

    # --- ส่วนที่ 1: การ์ดระยะทางจบเกม ---
    st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #333; margin-bottom: 5px;">
            <p style="margin: 0; color: #888; font-size: 13px;">🎯 เป้าหมายรอบนี้ (${target_game:.0f}) | เหลือระยะทางจบเกม</p>
            <h1 style="margin: 0; color: {rem_color}; font-size: 34px;">${remaining:.2f} USD</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)

    # --- ส่วนที่ 2: สรุปผลงานประจำวัน ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='margin: 0; font-size: 14px;'>🥇 <b>จบเกม:</b> {wins} รอบ</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='margin: 0; font-size: 14px;'>🚩 <b>เป้าใหญ่:</b> {daily_progress * 100:.1f}%</p>", unsafe_allow_html=True)
    
    st.progress(daily_progress)

    # --- ส่วนที่ 3: สถานะพอร์ต บังคับบรรทัดเดียว (Bal / Eq / P/L) ---
    st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 8px 5px; border-radius: 8px; border: 1px solid #333; margin-top: 10px; display: flex; justify-content: space-around; text-align: center;">
            <div>
                <p style="margin:0; color:#888; font-size:11px;">💳 Bal</p>
                <p style="margin:0; font-size:15px; font-weight:bold;">${balance:,.0f}</p>
            </div>
            <div style="border-left: 1px solid #333; border-right: 1px solid #333; padding: 0 10px;">
                <p style="margin:0; color:#888; font-size:11px;">📈 Eq</p>
                <p style="margin:0; font-size:15px; font-weight:bold;">${equity:,.1f}</p>
            </div>
            <div>
                <p style="margin:0; color:#888; font-size:11px;">📊 P/L</p>
                <p style="margin:0; color:{'#FFA500' if floating_pl>=0 else '#FF4B4B'}; font-size:15px; font-weight:bold;">${floating_pl:,.2f}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    st.warning("⏳ รอข้อมูลจากระบบ...")
        
