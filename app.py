import streamlit as st
import json
import os

# ตั้งค่าหน้าจอ Dashboard
st.set_page_config(
    page_title="EA ADIDAS Dashboard",
    page_icon="📊",
    layout="centered"
)

st.title("📊 EA ADIDAS Dashboard")
st.caption("ระบบติดตามพอร์ตเรียลไทม์")

# อ่านไฟล์ข้อมูล
file_path = "portfolio_status.json"

if os.path.exists(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        balance = data.get("balance", 0.0)
        equity = data.get("equity", 0.0)
        floating_pl = data.get("floating_pl", 0.0)
        target = data.get("target", 20.0)
        
        # แสดงเป้าหมาย
        st.subheader("🎯 เป้าหมายกำไรสุทธิ")
        progress = min(max((floating_pl / target) if target > 0 else 0.0, 0.0), 1.0)
        st.progress(progress)
        st.caption(f"ความคืบหน้า: {progress*100:.1f}% (เป้าหมาย: ${target:.2f})")
        
        st.divider()
        
        # แสดง Balance & Equity
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="💳 Balance", value=f"${balance:,.2f}")
        with col2:
            st.metric(label="📈 Equity", value=f"${equity:,.2f}")
            
        st.write("")
        
        # แสดง Floating P/L
        pl_color = "#00C853" if floating_pl >= 0 else "#FF3D00"
        st.markdown(
            f"""
            <div style="
                background-color: #1E1E1E;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #333;
            ">
                <span style="color: #AAAAAA; font-size: 18px;">Current P/L</span><br>
                <span style="color: {pl_color}; font-size: 36px; font-weight: bold;">
                    ${floating_pl:,.2f} USD
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านข้อมูล: {e}")
else:
    st.info("กำลังรอข้อมูลจากระบบ MT5...")
      
