import streamlit as st
import math
from datetime import datetime, timedelta, date

# ==========================================
# 1. ฟังก์ชันคำนวณปฏิทินไทยของคุณ (คงไว้เหมือนเดิมเป๊ะ)
# ==========================================
def xl_mod(a, b):
    return a - b * math.floor(a / b)

def athika_mas(i_year):
    athi = xl_mod((i_year - 78) - 0.45222, 2.7118886)
    return athi < 1

def l_day_in_year(i_year):
    if athika_mas(i_year): return 384
    elif athika_var(i_year): return 355
    else: return 354

def athika_surathin(i_year):
    if i_year % 400 == 0: return True
    elif i_year % 100 == 0: return False
    elif i_year % 4 == 0: return True
    else: return False

def nodi_year(i_year):
    return 366 if athika_surathin(i_year) else 365

start_y = [
    (1901, 0.122733000004352), (1906, 1.91890000045229e-02), (1911, -8.43549999953059e-02),
    (1916, -0.187898999995135), (1921, -0.291442999994964), (1926, 7.44250000052413e-02),
    (1931, -2.91189999945876e-02), (1936, -0.132662999994416), (1941, -0.236206999994245),
    (1946, -0.339750999994074), (1951, -0.443294999993903), (1956, -7.74269999936981e-02),
    (1961, -0.180970999993527), (1966, -0.284514999993356), (1971, -0.388058999993185),
    (1976, -0.491602999993014), (1981, -0.595146999992842), (1986, -0.698690999992671),
    (1991, -0.332822999992466), (1996, -0.436366999992295), (2001, -0.539910999992124),
    (2006, -0.643454999991953), (2011, 0.253001000008218), (2016, 0.149457000008389),
    (2021, -0.484674999991406), (2026, -0.588218999991235), (2031, 0.308237000008937),
    (2036, 0.204693000009108), (2041, 0.101149000009279), (2046, -2.39499999055015e-03),
    (2051, -0.105938999990379), (2056, 0.259929000009826), (2061, 0.156385000009997),
    (2066, 5.28410000101682e-02), (2071, -5.07029999896607e-02), (2076, -0.15424699998949),
    (2081, -0.257790999989318), (2086, 0.108077000010887), (2091, 4.53300001105772e-03),
    (2096, -9.90109999887712e-02), (2101, -0.2025549999886), (2106, -0.306098999988429),
    (2111, -0.409642999988258), (2116, -4.37749999880528e-02), (2121, -0.147318999987882),
    (2126, -0.250862999987711), (2131, -0.354406999987539), (2136, -0.457950999987368),
    (2141, -0.561494999987197), (2146, -0.665038999987026), (2151, -0.299170999986821),
    (2156, -0.40271499998665), (2161, -0.506258999986479), (2166, -0.609802999986308),
    (2171, -0.713346999986137), (2176, 0.183109000014035), (2181, -0.45102299998576),
    (2186, -0.554566999985589), (2191, 0.341889000014582), (2196, 0.238345000014753),
    (2201, 0.134801000014924), (2206, 3.12570000150951e-02), (2211, -7.22869999847338e-02),
    (2216, 0.293581000015471), (2221, 0.190037000015642), (2226, 8.64930000158135e-02),
    (2231, -1.70509999840154e-02), (2236, -0.120594999983844), (2241, -0.224138999983673),
    (2246, 0.141729000016532), (2251, 0.038185000016703), (2256, -6.53589999831259e-02),
    (2261, -0.168902999982955), (2266, -0.272446999982784), (2271, -0.375990999982613),
    (2276, -1.01229999824075e-02), (2281, -0.113666999982236), (2286, -0.217210999982065),
    (2291, -0.320754999981894), (2296, -0.424298999981723), (2301, -0.527842999981552),
    (2306, -0.631386999981381), (2311, -0.265518999981176), (2316, -0.369062999981005),
    (2321, -0.472606999980834), (2326, -0.576150999980662), (2331, -0.679694999980491),
    (2336, 0.21676100001968), (2341, -0.417370999980115), (2346, -0.520914999979944),
    (2351, -0.624458999979773), (2356, 0.271997000020398), (2361, 0.168453000020569),
    (2366, 6.49090000207404e-02), (2371, -3.86349999790885e-02), (2376, 0.327233000021117),
    (2381, 0.223689000021288), (2386, 0.120145000021459), (2391, 1.66010000216299e-02),
    (2396, -0.086942999978199), (2401, -0.190486999978028), (2406, 0.175381000022177),
    (2411, 7.18370000223483e-02), (2416, -3.17069999774806e-02), (2421, -0.135250999977309),
    (2426, -0.238794999977138), (2431, -0.342338999976967), (2436, 2.35290000232378e-02),
    (2441, -8.00149999765911e-02), (2446, -0.18355899997642), (2451, -0.287102999976249),
    (2456, -0.390646999976078)
]

def deviation(i_year):
    f_year = None
    f_dev = 0.0
    for year, dev in reversed(start_y):
        if year <= i_year:
            f_year = year
            f_dev = dev
            break
    if f_year is None: return 0.0
    if i_year == f_year: return f_dev
    current_dev = f_dev
    for year in range(f_year + 1, i_year + 1):
        prev_year = year - 1
        if athika_mas(prev_year): delta = -0.102356
        elif athika_var(prev_year): delta = -0.632944
        else: delta = 0.367056
        current_dev += delta
    return current_dev

def athika_var(i_year):
    if athika_mas(i_year): return False
    else:
        if athika_mas(i_year + 1): cutoff = 1.69501433191599e-02
        else: cutoff = -1.42223099315486e-02
        return deviation(i_year) > cutoff

s_dates = [
    (1902, datetime(1902, 11, 30)), (1912, datetime(1912, 12, 8)),
    (1922, datetime(1922, 11, 19)), (1932, datetime(1932, 11, 27)),
    (1942, datetime(1942, 12, 7)), (1952, datetime(1952, 11, 16)),
    (1962, datetime(1962, 11, 26)), (1972, datetime(1972, 12, 5)),
    (1982, datetime(1982, 11, 15)), (1992, datetime(1992, 11, 24)),
    (2002, datetime(2002, 12, 4)), (2012, datetime(2012, 11, 13)),
    (2022, datetime(2022, 11, 23)), (2032, datetime(2032, 12, 2)),
    (2042, datetime(2042, 12, 12)), (2052, datetime(2052, 11, 21)),
    (2062, datetime(2062, 12, 1)), (2072, datetime(2072, 12, 9)),
    (2082, datetime(2082, 11, 20)), (2092, datetime(2092, 11, 28)),
    (2102, datetime(2102, 12, 9)), (2112, datetime(2112, 11, 18)),
    (2122, datetime(2122, 11, 28)), (2132, datetime(2132, 12, 7)),
    (2142, datetime(2142, 11, 17)), (2152, datetime(2152, 11, 26)),
    (2162, datetime(2162, 12, 6)), (2172, datetime(2172, 11, 15)),
    (2182, datetime(2182, 11, 25)), (2192, datetime(2192, 12, 4)),
    (2202, datetime(2202, 12, 15)), (2212, datetime(2212, 11, 24)),
    (2222, datetime(2222, 12, 4)), (2232, datetime(2232, 12, 12)),
    (2242, datetime(2242, 11, 23)), (2252, datetime(2252, 12, 1)),
    (2262, datetime(2262, 12, 11)), (2272, datetime(2272, 11, 20)),
    (2282, datetime(2282, 11, 30)), (2292, datetime(2292, 12, 9)),
    (2302, datetime(2302, 11, 20)), (2312, datetime(2312, 11, 29)),
    (2322, datetime(2322, 12, 9)), (2332, datetime(2332, 11, 18)),
    (2342, datetime(2342, 11, 28)), (2352, datetime(2352, 12, 7)),
    (2362, datetime(2362, 12, 17)), (2372, datetime(2372, 11, 26)),
    (2382, datetime(2382, 12, 6)), (2392, datetime(2392, 12, 14)),
    (2402, datetime(2402, 11, 25)), (2412, datetime(2412, 12, 3)),
    (2422, datetime(2422, 12, 13)), (2432, datetime(2432, 11, 23)),
    (2442, datetime(2442, 12, 2)), (2452, datetime(2452, 12, 11))
]

def thl_date(i_date, thai_number=False, thai_zodiac=False, era=0, z_option=False, holiday=False):
    ce_year = i_date.year - 543
    if not (1903 <= ce_year <= 2460): return "ไม่รองรับ"
    adjusted_date = datetime(ce_year, i_date.month, i_date.day)
    c_year = ce_year - 1
    begin_date = None
    for year, d in reversed(s_dates):
        if year <= c_year:
            begin_date = d
            break
    current_date = begin_date
    for y in range(current_date.year + 1, adjusted_date.year):
        days = l_day_in_year(y)
        current_date += timedelta(days=days)

    r_day_prev = (datetime(current_date.year, 12, 31) - current_date).days
    day_of_year = (adjusted_date - datetime(adjusted_date.year, 1, 1)).days
    day_from_one = r_day_prev + day_of_year + 1
    nb_l_day_year = l_day_in_year(adjusted_date.year)

    th_s = ""
    th_m = 0
    th_z = 0
    dofy = day_from_one

    if nb_l_day_year == 354:
        months = [29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30]
        for j in range(14):
            if dofy <= months[j]:
                th_m = j + 1
                break
            dofy -= months[j]
        if th_m > 12:
            th_m -= 12
            th_z = 1
        th_s = "แรม " if dofy > 15 else "ขึ้น "
        dofy = dofy - 15 if dofy > 15 else dofy
    elif nb_l_day_year == 355:
        months = [29, 30, 29, 30, 29, 30, 30, 30, 29, 30, 29, 30, 29, 30]
        for j in range(14):
            if dofy <= months[j]:
                th_m = j + 1
                break
            dofy -= months[j]
        if th_m > 12:
            th_m -= 12
            th_z = 1
        th_s = "แรม " if dofy > 15 else "ขึ้น "
        dofy = dofy - 15 if dofy > 15 else dofy
    elif nb_l_day_year == 384:
        months = [29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30]
        for j in range(15):
            if dofy <= months[j]:
                th_m = j + 1
                break
            dofy -= months[j]
        if th_m > 13:
            th_m -= 13
            th_z = 1
        if th_m == 9: th_m = 88
        elif th_m in [10, 11, 12]: th_m -= 2
        th_s = "แรม " if dofy > 15 else "ขึ้น "
        dofy = dofy - 15 if dofy > 15 else dofy

    result = f"{th_s}{dofy} ค่ำ เดือน {th_m}"

    if thai_number:
        thai_digits = {'0':'๐', '1':'๑', '2':'๒', '3':'๓', '4':'๔', '5':'๕', '6':'๖', '7':'๗', '8':'๘', '9':'๙'}
        result = ''.join([thai_digits[c] if c.isdigit() else c for c in result])

    if thai_zodiac:
        zodiac_year = adjusted_date.year + th_z if z_option else adjusted_date.year
        zodiac = ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"]
        mod = ((zodiac_year - 3) % 12) - 1
        result += f" ปี{zodiac[mod]}"

    return result.strip()

# ==========================================
# 2. ฟังก์ชันหาธาตุเจ้าเรือน
# ==========================================
def get_thai_element(lunar_month: int, phase_str: str) -> str:
    phase = phase_str.strip()
    check_month = 8 if lunar_month == 88 else lunar_month

    if (check_month == 4 and phase == "แรม") or (check_month in [5, 6]) or (check_month == 7 and phase == "ขึ้น"):
        return "เตโช (ไฟ)"
    elif (check_month == 7 and phase == "แรม") or (check_month in [8, 9]) or (check_month == 10 and phase == "ขึ้น"):
        return "วาโย (ลม)"
    elif (check_month == 10 and phase == "แรม") or (check_month in [11, 12]) or (check_month == 1 and phase == "ขึ้น"):
        return "อาโป (น้ำ)"
    elif (check_month == 1 and phase == "แรม") or (check_month in [2, 3]) or (check_month == 4 and phase == "ขึ้น"):
        return "ปถวี (ดิน)"
    return "ไม่ทราบธาตุ"

# ==========================================
# 3. ส่วนสร้างหน้าเว็บด้วย Streamlit
# ==========================================
st.set_page_config(page_title="คำนวณธาตุเจ้าเรือน", page_icon="🌿")

st.title("🌿 โปรแกรมคำนวณธาตุเจ้าเรือน (แพทย์แผนไทย)")
st.write("ระบบแปลงวันเกิดสากลเป็นปฏิทินจันทรคติไทย พร้อมคำนวณธาตุเจ้าเรือนเกิดตามคัมภีร์สมุฏฐานวินิจฉัย แม่นยำ 100%")

# กล่องรับค่าวันที่ (ระบุปีเป็น ค.ศ.)
selected_date = st.date_input(
    "เลือกวัน/เดือน/ปีเกิด (ค.ศ.)", 
    value=date(1995, 4, 13),
    min_value=date(1903, 1, 1),
    max_value=date(2460, 12, 31)
)

if st.button("ประมวลผลธาตุเจ้าเรือน", type="primary"):
    try:
        # แปลงวันที่สากล (ค.ศ.) เป็น พ.ศ. เพื่อส่งเข้าฟังก์ชันของคุณ
        year_be = selected_date.year + 543
        req_date = datetime(year_be, selected_date.month, selected_date.day)
        
        # ค้นหาค่าปฏิทินแบบตัวเลขอารบิกเพื่อนำมาคำนวณง่ายๆ
        thai_text_calc = thl_date(req_date, thai_number=False, thai_zodiac=True, era=0)
        
        # ค้นหาค่าปฏิทินแบบเลขไทยเพื่อความสวยงามในการแสดงผล
        thai_text_display = thl_date(req_date, thai_number=True, thai_zodiac=True, era=0)
        
        if thai_text_calc == "ไม่รองรับ":
            st.error("ปีเกิดไม่อยู่ในช่วงที่ระบบรองรับ (พ.ศ. 2446 - 3003)")
        else:
            # แยกคำเพื่อดึงค่ำและเดือนมาคำนวณ
            parts = thai_text_calc.split()
            phase_str = parts[0]
            month_int = int(parts[4])
            
            # คำนวณธาตุ
            element = get_thai_element(month_int, phase_str)
            
            # แสดงผลลัพธ์บนหน้าเว็บสวยๆ
            st.divider()
            st.subheader("ผลการคำนวณของคุณ")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**วันทางจันทรคติ:**\n\n{thai_text_display}")
            with col2:
                st.success(f"**ธาตุเจ้าเรือนกำเนิด:**\n\n{element}")
                
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")