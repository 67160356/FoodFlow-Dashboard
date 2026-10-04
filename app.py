import hashlib
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FoodFlow | Business Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Style ----------
st.markdown(
    """
    <style>
    .stApp { background: #f7f8fa; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1450px; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e5e7eb; }
    .brand { font-size: 30px; font-weight: 800; color: #1f2937; margin-bottom: 0; }
    .brand span { color: #15803d; }
    .subtitle { color: #6b7280; font-size: 15px; margin-top: -6px; }
    .section-title { font-size: 21px; font-weight: 750; color: #1f2937; margin: 18px 0 4px 0; }
    .section-note { color: #6b7280; font-size: 13px; margin-bottom: 12px; }
    .story-card { background: white; border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px 20px; margin-bottom: 12px; }
    .story-card h4 { margin: 0 0 6px 0; color: #1f2937; }
    .story-card p { margin: 0; color: #4b5563; line-height: 1.55; }
    .insight { background: #ecfdf5; border-left: 4px solid #15803d; padding: 13px 16px; border-radius: 8px; margin: 8px 0; color: #1f2937; }
    div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e5e7eb; padding: 14px 16px; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Data ----------
@st.cache_data
def load_data():
    data = pd.read_csv("data/foodflow_orders_thailand.csv")
    data["order_date"] = pd.to_datetime(data["order_date"])
    return data


df = load_data()

# ---------- Header ----------
st.markdown('<div class="brand">🍽️ <span>FoodFlow</span> | Business Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Business Idea Creation • Executive view of Thailand food & beverage marketplace performance</div>',
    unsafe_allow_html=True,
)
st.divider()

# ---------- Filters ----------
with st.sidebar:
    st.markdown("### ตัวกรองข้อมูล")
    st.caption("เลือกข้อมูลเพื่อดูมุมมองทางธุรกิจที่ต้องการ")
    regions = st.multiselect("ภูมิภาค", sorted(df["region"].unique()), sorted(df["region"].unique()))
    provinces = st.multiselect("จังหวัด", sorted(df["province"].unique()), sorted(df["province"].unique()))
    categories = st.multiselect("หมวดสินค้า", sorted(df["category"].unique()), sorted(df["category"].unique()))
    customer_types = st.multiselect("ประเภทลูกค้า", sorted(df["customer_type"].unique()), sorted(df["customer_type"].unique()))
    st.divider()
    st.caption("ข้อมูลสำหรับการเรียน/สาธิต")
    st.caption("Synthetic Data • 77 จังหวัด")

filtered = df[
    df["region"].isin(regions)
    & df["province"].isin(provinces)
    & df["category"].isin(categories)
    & df["customer_type"].isin(customer_types)
].copy()

# ---------- Story 1: Executive summary ----------
st.markdown('<div class="section-title">1. Executive Summary — ภาพรวมธุรกิจ</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">เริ่มจากคำถามว่า FoodFlow มีผลการดำเนินงานและโอกาสทางตลาดอย่างไร</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("ยอดขายรวม", f"฿{filtered.sales.sum():,.0f}")
with m2:
    st.metric("จำนวนคำสั่งซื้อ", f"{len(filtered):,}")
with m3:
    avg = filtered.sales.mean() if len(filtered) else 0
    st.metric("ยอดขายเฉลี่ย / ออเดอร์", f"฿{avg:,.0f}")
with m4:
    rating = filtered.rating.mean() if len(filtered) else 0
    st.metric("คะแนนเฉลี่ย", f"{rating:.2f} / 5")

if len(filtered):
    top_province = filtered.groupby("province", as_index=False).sales.sum().sort_values("sales", ascending=False).iloc[0]
    top_category = filtered.groupby("category", as_index=False).sales.sum().sort_values("sales", ascending=False).iloc[0]
    st.markdown(
        f'<div class="story-card"><h4>Business Story</h4><p>จากข้อมูลที่เลือก จังหวัด <b>{top_province.province}</b> มียอดขายสูงสุด และหมวดสินค้า <b>{top_category.category}</b> เป็นหมวดที่สร้างยอดขายสูงสุด จึงสามารถใช้ข้อมูลนี้เป็นแนวทางในการวางแผนโปรโมชั่น การขยายร้านค้า และการจัดสรรทรัพยากรของ FoodFlow</p></div>',
        unsafe_allow_html=True,
    )

# ---------- Story 2: Geographic opportunity ----------
st.markdown('<div class="section-title">2. Market Opportunity — ตลาดอยู่ที่ไหน?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">วิเคราะห์การกระจายยอดขายเพื่อหาพื้นที่ที่ควรทำตลาดและขยายเครือข่ายร้านค้า</div>', unsafe_allow_html=True)

prov = filtered.groupby(["province", "region"], as_index=False).agg(
    sales=("sales", "sum"), orders=("order_id", "count")
)

coords = {
    "กรุงเทพมหานคร": (13.7563, 100.5018), "เชียงใหม่": (18.7883, 98.9853), "เชียงราย": (19.9105, 99.8406),
    "ภูเก็ต": (7.8804, 98.3923), "ชลบุรี": (13.3611, 100.9847), "ระยอง": (12.6814, 101.2816),
    "ขอนแก่น": (16.4322, 102.8236), "นครราชสีมา": (14.9799, 102.0977), "อุดรธานี": (17.4138, 102.7875),
    "อุบลราชธานี": (15.2287, 104.8564), "สงขลา": (7.1898, 100.5954), "นครศรีธรรมราช": (8.4304, 99.9631),
    "สุราษฎร์ธานี": (9.1382, 99.3217), "กระบี่": (8.0863, 98.9063), "นครปฐม": (13.8199, 100.0622),
    "นนทบุรี": (13.8621, 100.5144), "ปทุมธานี": (14.0208, 100.5250), "สมุทรปราการ": (13.5991, 100.5998),
    "กาญจนบุรี": (14.0228, 99.5328), "ราชบุรี": (13.5283, 99.8134), "เพชรบุรี": (13.1119, 99.9398)
}
centers = {
    "ภาคเหนือ": (17.8, 99.0), "ภาคกลาง": (14.5, 100.3), "ภาคตะวันออก": (13.2, 101.4),
    "ภาคตะวันออกเฉียงเหนือ": (16.2, 103.5), "ภาคตะวันตก": (13.0, 99.0), "ภาคใต้": (8.5, 99.5)
}
lat, lon = [], []
for _, row in prov.iterrows():
    if row.province in coords:
        la, lo = coords[row.province]
    else:
        la0, lo0 = centers[row.region]
        h = int(hashlib.md5(row.province.encode()).hexdigest()[:8], 16)
        la = la0 + ((h % 1000) / 1000 - .5) * 3
        lo = lo0 + (((h // 1000) % 1000) / 1000 - .5) * 4
    lat.append(la); lon.append(lo)

if len(prov):
    map_df = prov.assign(lat=lat, lon=lon)
    fig_map = px.scatter_geo(
        map_df, lat="lat", lon="lon", size="sales", color="sales", hover_name="province",
        hover_data={"region": True, "sales": ":,.0f", "orders": ":,d", "lat": False, "lon": False},
        scope="asia", projection="mercator", title="การกระจายยอดขายตามจังหวัด"
    )
    fig_map.update_geos(center={"lat": 13.5, "lon": 100.5}, projection_scale=5.2, showland=True)
    fig_map.update_layout(height=560, margin=dict(l=0, r=0, t=55, b=0), font=dict(family="Arial"))
    st.plotly_chart(fig_map, use_container_width=True)

r = filtered.groupby("region", as_index=False).sales.sum().sort_values("sales", ascending=False)
t = prov.sort_values("sales", ascending=False).head(10)
ca, cb = st.columns(2)
with ca:
    st.plotly_chart(px.bar(r, x="region", y="sales", text_auto=".2s", title="ยอดขายแยกตามภูมิภาค"), use_container_width=True)
with cb:
    st.plotly_chart(px.bar(t.sort_values("sales"), x="sales", y="province", orientation="h", text_auto=".2s", title="10 จังหวัดยอดขายสูงสุด"), use_container_width=True)

# ---------- Story 3: Customer and product ----------
st.markdown('<div class="section-title">3. Customer & Product — ลูกค้าซื้ออะไร?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">ใช้ข้อมูลลูกค้าและหมวดสินค้าเพื่อกำหนดสินค้า โปรโมชั่น และกลยุทธ์การขาย</div>', unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    cat = filtered.groupby("category", as_index=False).sales.sum().sort_values("sales", ascending=False)
    st.plotly_chart(px.pie(cat, names="category", values="sales", hole=.48, title="สัดส่วนยอดขายตามหมวดสินค้า"), use_container_width=True)
with cb:
    customer = filtered.groupby("customer_type", as_index=False).sales.sum().sort_values("sales", ascending=False)
    st.plotly_chart(px.bar(customer, x="customer_type", y="sales", text_auto=".2s", title="ยอดขายตามประเภทลูกค้า"), use_container_width=True)

# ---------- Story 4: Trend ----------
st.markdown('<div class="section-title">4. Business Trend — ธุรกิจเติบโตอย่างไร?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">ดูแนวโน้มรายเดือนเพื่อช่วยวางแผนแคมเปญ การจัดสินค้า และการขยายตลาด</div>', unsafe_allow_html=True)

monthly = filtered.assign(month=filtered.order_date.dt.to_period("M").astype(str)).groupby("month", as_index=False).sales.sum()
st.plotly_chart(px.line(monthly, x="month", y="sales", markers=True, title="แนวโน้มยอดขายรายเดือน"), use_container_width=True)

# ---------- Story 5: Decision ----------
st.markdown('<div class="section-title">5. Insight → Business Action — แล้วควรทำอะไรต่อ?</div>', unsafe_allow_html=True)
if len(prov):
    top = prov.sort_values("sales", ascending=False).iloc[0]
    top_region = r.iloc[0]["region"] if len(r) else "-"
    st.markdown(f'<div class="insight"><b>พื้นที่เป้าหมาย:</b> {top.province} เป็นจังหวัดที่มียอดขายสูงสุดจากตัวกรองปัจจุบัน → ควรพิจารณาเพิ่มร้านค้าและแคมเปญในพื้นที่นี้</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight"><b>ภูมิภาค:</b> {top_region} เป็นภูมิภาคที่มียอดขายสูงสุด → ใช้เป็นพื้นที่นำร่องสำหรับการขยายเครือข่าย FoodFlow</div>', unsafe_allow_html=True)
if len(cat):
    st.markdown(f'<div class="insight"><b>สินค้า:</b> {cat.iloc[0]["category"]} เป็นหมวดสินค้าที่สร้างยอดขายสูงสุด → สามารถนำไปวางแผนโปรโมชั่นและการแนะนำสินค้า</div>', unsafe_allow_html=True)
st.markdown('<div class="story-card"><h4>ความเชื่อมโยงกับ Business Idea Creation</h4><p>Dashboard นี้ทำหน้าที่เปลี่ยนข้อมูลคำสั่งซื้อของ FoodFlow ให้เป็นข้อมูลสำหรับตัดสินใจทางธุรกิจ เช่น การเลือกพื้นที่ขยายตลาด การวางโปรโมชั่น การคัดเลือกร้านค้า และการติดตามแนวโน้มยอดขาย</p></div>', unsafe_allow_html=True)

# ---------- Data submission ----------
st.divider()
st.caption("FoodFlow • Business Idea Creation • Synthetic Data สำหรับการเรียนและสาธิต ไม่ใช่ข้อมูลยอดขายจริง")
