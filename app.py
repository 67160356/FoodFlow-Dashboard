import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
st.set_page_config(page_title="FoodFlow Thailand",page_icon="🍜",layout="wide")
@st.cache_data
def load():
    d=pd.read_csv("data/foodflow_orders_thailand.csv"); d["order_date"]=pd.to_datetime(d["order_date"]); return d
df=load()
st.title("🍜 FoodFlow — Thailand Food & Beverage Dashboard")
st.caption("ภาพรวมตลาดอาหารและเครื่องดื่ม ครอบคลุม 77 จังหวัดทั่วประเทศไทย | Synthetic Data สำหรับโครงงาน")
with st.sidebar:
    st.header("ตัวกรองข้อมูล")
    rs=sorted(df.region.unique()); ps=sorted(df.province.unique()); cs=sorted(df.category.unique()); ts=sorted(df.customer_type.unique())
    regions=st.multiselect("ภูมิภาค",rs,rs); provinces=st.multiselect("จังหวัด",ps,ps); cats=st.multiselect("หมวดสินค้า",cs,cs); types=st.multiselect("ประเภทลูกค้า",ts,ts)
    f=df[df.region.isin(regions)&df.province.isin(provinces)&df.category.isin(cats)&df.customer_type.isin(types)]
a,b,c,d=st.columns(4)
a.metric("ยอดขายรวม",f"฿{f.sales.sum():,.0f}"); b.metric("จำนวนออเดอร์",f"{len(f):,}"); c.metric("ยอดเฉลี่ย/ออเดอร์",f"฿{f.sales.mean():,.0f}" if len(f) else "฿0"); d.metric("คะแนนเฉลี่ย",f"{f.rating.mean():.2f}/5" if len(f) else "0/5")
st.divider()
st.subheader("🗺️ ยอดขายรายจังหวัด — ครบ 77 จังหวัด")
prov=f.groupby(["province","region"],as_index=False).agg(sales=("sales","sum"),orders=("order_id","count"))
coords={"กรุงเทพมหานคร":(13.7563,100.5018),"เชียงใหม่":(18.7883,98.9853),"เชียงราย":(19.9105,99.8406),"ภูเก็ต":(7.8804,98.3923),"ชลบุรี":(13.3611,100.9847),"ระยอง":(12.6814,101.2816),"ขอนแก่น":(16.4322,102.8236),"นครราชสีมา":(14.9799,102.0977),"อุดรธานี":(17.4138,102.7875),"อุบลราชธานี":(15.2287,104.8564),"สงขลา":(7.1898,100.5954),"นครศรีธรรมราช":(8.4304,99.9631),"สุราษฎร์ธานี":(9.1382,99.3217),"กระบี่":(8.0863,98.9063),"นครปฐม":(13.8199,100.0622),"นนทบุรี":(13.8621,100.5144),"ปทุมธานี":(14.0208,100.5250),"สมุทรปราการ":(13.5991,100.5998),"กาญจนบุรี":(14.0228,99.5328),"ราชบุรี":(13.5283,99.8134),"เพชรบุรี":(13.1119,99.9398)}
centers={"ภาคเหนือ":(17.8,99.0),"ภาคกลาง":(14.5,100.3),"ภาคตะวันออก":(13.2,101.4),"ภาคตะวันออกเฉียงเหนือ":(16.2,103.5),"ภาคตะวันตก":(13.0,99.0),"ภาคใต้":(8.5,99.5)}
lat=[];lon=[]
for _,r in prov.iterrows():
    if r.province in coords: la,lo=coords[r.province]
    else:
        la0,lo0=centers[r.region]; h=int(hashlib.md5(r.province.encode()).hexdigest()[:8],16); la=la0+((h%1000)/1000-.5)*3; lo=lo0+(((h//1000)%1000)/1000-.5)*4
    lat.append(la);lon.append(lo)
m=px.scatter_geo(prov.assign(lat=lat,lon=lon),lat="lat",lon="lon",size="sales",color="sales",hover_name="province",hover_data={"region":True,"sales":":,.0f","orders":":,d","lat":False,"lon":False},scope="asia",projection="mercator",title="ขนาดจุด = ยอดขายของจังหวัด")
m.update_geos(center={"lat":13.5,"lon":100.5},projection_scale=5.2,showland=True); m.update_layout(height=600,margin=dict(l=0,r=0,t=50,b=0)); st.plotly_chart(m,use_container_width=True)
x,y=st.columns(2)
with x:
    st.subheader("📊 ยอดขายตามภูมิภาค"); r=f.groupby("region",as_index=False).sales.sum().sort_values("sales",ascending=False); st.plotly_chart(px.bar(r,x="region",y="sales",text_auto=".2s"),use_container_width=True)
with y:
    st.subheader("🏆 10 จังหวัดยอดขายสูงสุด"); t=prov.sort_values("sales",ascending=False).head(10); st.plotly_chart(px.bar(t.sort_values("sales"),x="sales",y="province",orientation="h",text_auto=".2s"),use_container_width=True)
x,y=st.columns(2)
with x:
    st.subheader("🛒 ยอดขายตามหมวดสินค้า"); c=f.groupby("category",as_index=False).sales.sum().sort_values("sales",ascending=False); st.plotly_chart(px.pie(c,names="category",values="sales",hole=.45),use_container_width=True)
with y:
    st.subheader("📈 แนวโน้มยอดขายรายเดือน"); mo=f.assign(month=f.order_date.dt.to_period("M").astype(str)).groupby("month",as_index=False).sales.sum(); st.plotly_chart(px.line(mo,x="month",y="sales",markers=True),use_container_width=True)
st.subheader("💡 Insight")
if len(prov): st.write(f"• จังหวัดยอดขายสูงสุดจากตัวกรองปัจจุบันคือ **{prov.sort_values('sales',ascending=False).iloc[0].province}**")
st.write("• ใช้ข้อมูลระดับจังหวัดเพื่อวางแผนโปรโมชั่น การขยายร้านค้า และการจัดส่ง")
st.write("• ข้อมูลเป็น Synthetic Data สำหรับการเรียน/สาธิต")
