# FoodFlow — Thailand Business Dashboard

> Business Dashboard สำหรับวิเคราะห์ธุรกิจอาหารและเครื่องดื่มในประเทศไทย

## 🌐 Live Dashboard

👉 **[เปิดใช้งาน FoodFlow Dashboard](https://foodflow-dashboard.streamlit.app/)**

## รายวิชา

Business Idea Creation

## แนวคิดของบริษัท
**FoodFlow** คือแพลตฟอร์ม Marketplace สำหรับสินค้าอาหารและเครื่องดื่มที่รวบรวมร้านค้าและผู้ขายหลายรายไว้ในระบบเดียว ช่วยให้ลูกค้าค้นหา เปรียบเทียบสินค้าและราคา ดูข้อมูลสินค้า รีวิว และตัดสินใจสั่งซื้อได้สะดวกขึ้น ขณะเดียวกันช่วยให้ร้านอาหารและผู้ประกอบการ SME เข้าถึงลูกค้าออนไลน์ได้มากขึ้น

## วัตถุประสงค์ของ Dashboard
Dashboard นี้ออกแบบเป็น **Dashboard เชิงเล่าเรื่อง (Storytelling Dashboard)** เพื่อเชื่อมโยงข้อมูลกับการทำธุรกิจของ FoodFlow โดยเรียงลำดับจาก

1. **Executive Summary** — ธุรกิจมีผลการดำเนินงานเป็นอย่างไร
2. **Market Opportunity** — ยอดขายอยู่ที่พื้นที่ใด และจังหวัดใดมีโอกาสทางตลาด
3. **Customer & Product** — ลูกค้ากลุ่มใดและหมวดสินค้าใดสร้างยอดขาย
4. **Business Trend** — ยอดขายมีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน
5. **Insight → Business Action** — นำข้อมูลไปใช้วางแผนโปรโมชั่น การขยายตลาด การเพิ่มร้านค้า และการจัดสินค้าอย่างไร

## ความเกี่ยวข้องกับงานในบริษัท
ข้อมูลใน Dashboard ถูกนำเสนอในมุมมองของบริษัท FoodFlow โดยใช้ข้อมูลคำสั่งซื้อเป็นฐานในการตอบคำถามทางธุรกิจ เช่น

- จังหวัดใดควรเป็นพื้นที่เป้าหมายในการขยายตลาด
- ภูมิภาคใดมียอดขายสูงและควรเพิ่มเครือข่ายร้านค้า
- หมวดสินค้าใดควรได้รับการส่งเสริมหรือจัดโปรโมชั่น
- ลูกค้าประเภทใดเป็นกลุ่มสำคัญของแพลตฟอร์ม
- ยอดขายมีแนวโน้มอย่างไร เพื่อช่วยวางแผนธุรกิจในช่วงถัดไป

## Data ที่ใช้
ไฟล์ข้อมูลที่ใช้ในการสร้าง Dashboard คือ:

`data/foodflow_orders_thailand.csv`

ข้อมูลเป็น **Synthetic Data สำหรับการเรียนและสาธิต** ไม่ใช่ข้อมูลยอดขายจริงของบริษัท โดยครอบคลุมข้อมูลคำสั่งซื้อใน **77 จังหวัดของประเทศไทย**

### ตัวแปรหลักใน Data
- `order_id` — รหัสคำสั่งซื้อ
- `order_date` — วันที่สั่งซื้อ
- `province` — จังหวัด
- `region` — ภูมิภาค
- `category` — หมวดสินค้า
- `customer_type` — ประเภทลูกค้า
- `sales` — ยอดขาย
- `rating` — คะแนนรีวิว

## โครงสร้างไฟล์
```text
FoodFlow-Dashboard/
├── app.py
├── README.md
├── requirements.txt
├── run_dashboard.bat
└── data/
    └── foodflow_orders_thailand.csv
```

## วิธีเปิดใช้งาน

1. ติดตั้ง Library
```bash
python -m pip install -r requirements.txt
```

2. เปิด Dashboard
```bash
python -m streamlit run app.py
```

3. เปิด URL ที่แสดงใน Terminal เช่น
```text
http://localhost:8501
```
ถ้า 8501 ถูกใช้งานอยู่ Streamlit อาจเปลี่ยนเป็น 8502 หรือพอร์ตอื่น ให้เปิด **Local URL ที่แสดงล่าสุดใน Terminal**

## เครื่องมือที่ใช้
- Python
- Streamlit
- Pandas
- Plotly
- CSV

## หมายเหตุ
Dashboard นี้จัดทำเพื่อประกอบรายวิชา **Business Idea Creation** และใช้ Synthetic Data เพื่อสาธิตแนวคิดการนำ Data Analytics มาช่วยสนับสนุนการตัดสินใจทางธุรกิจของ FoodFlow
