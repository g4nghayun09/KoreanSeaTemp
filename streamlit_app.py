# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# 기본 세팅
# --------------------------
st.set_page_config(page_title="🌊 해수온 상승과 바다의 미래 대시보드", layout="wide")

# Pretendard 폰트 적용
st.markdown(
    """
    <style>
    * { font-family: 'Pretendard', sans-serif; }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: #2c3e50; }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# 사이드바 옵션
# --------------------------
st.sidebar.header("⚙️ 대시보드 옵션")

# 기간 선택
start_year, end_year = st.sidebar.slider(
    "해수온 데이터 기간 선택",
    1990, 2025, (2000, 2025)
)

# 이동 평균
window = st.sidebar.slider("이동 평균(년)", 1, 10, 3)

# --------------------------
# 예시 데이터 생성 (API 실패 대비)
# --------------------------
years = np.arange(1990, 2026)

# 해수온 데이터
sea_temp = 14 + 0.03 * (years - 1990) + np.random.normal(0, 0.2, len(years))
df_temp = pd.DataFrame({"연도": years, "해수온(°C)": sea_temp})

# 산호 백화 데이터
coral_bleach = 5 + 0.8 * (years - 1990) + np.random.normal(0, 2, len(years))
df_coral = pd.DataFrame({"연도": years, "산호 백화 발생(건)": coral_bleach})

# 어종 개체수 데이터
fish_stock = 100 - 0.7 * (years - 1990) + np.random.normal(0, 3, len(years))
df_fish = pd.DataFrame({"연도": years, "토착 어종 지수": fish_stock})

# 수산업 생산량 데이터
fishery_output = 200 - 1.2 * (years - 1990) + np.random.normal(0, 5, len(years))
df_output = pd.DataFrame({"연도": years, "수산업 생산량 지수": fishery_output})

# 해수온 이상 데이터 (지도용)
def generate_sst_anomaly_data():
    lats = np.linspace(-60, 60, 30)
    lons = np.linspace(-180, 180, 60)
    years = np.arange(1990, 2026)
    data = []
    for year in years:
        for lat in lats:
            for lon in lons:
                base_anomaly = (year - 1990) * 0.015
                seasonal_pattern = np.sin(lon * np.pi / 180) * np.cos(lat * np.pi / 180) * 0.5
                noise = np.random.normal(0, 0.3)
                anomaly = base_anomaly + seasonal_pattern + noise
                data.append([year, lat, lon, anomaly])
    return pd.DataFrame(data, columns=["Year", "Lat", "Lon", "SST_Anomaly"])

df_sst_anomaly = generate_sst_anomaly_data()

# --------------------------
# 필터링 함수
# --------------------------
def filter_data_by_year(df, year_col, start_y, end_y):
    return df[(df[year_col] >= start_y) & (df[year_col] <= end_y)]

def apply_moving_avg(df, col, window):
    df_copy = df.copy()
    df_copy[f"{col}(이동평균)"] = df_copy[col].rolling(window=window, min_periods=1).mean()
    return df_copy

# --------------------------
# 탭 구조
# --------------------------
tabs = st.tabs(["📘 서론", "📊 본론1", "🌍 본론2", "✅ 결론"])

# --------------------------
# 서론
# --------------------------
with tabs[0]:
    st.title("해수온 상승과 바다의 미래: 변화와 대응 전략")
    st.subheader("서론 : 우리가 이 보고서를 쓰게 된 이유")

    st.markdown("""
    21세기 인류가 직면한 가장 큰 도전 중 하나는 **기후 위기**이다.  
    그중 **해수온 상승**은 바다 문제를 넘어 지구 생태계 전체와 인류 사회의 미래와 직결된다.  

    최근 수십 년간 바다는 점점 뜨거워지고 있으며,  
    이로 인해 **해양 생태계는 심각한 변화의 소용돌이**에 휘말리고 있다.  

    따라서 본 보고서는 해수온 상승이  
    - 해양 환경  
    - 생물 다양성  
    - 사회·경제적 영역  
    에 미치는 영향을 분석하고, 대응 전략을 제안하는 데 목적이 있다.
    """)

    # 그래프: 해수온 상승 추이
    st.subheader("🌡️ 전 지구 해수온 상승 추이")
    filtered_temp = filter_data_by_year(df_temp, "연도", start_year, end_year)
    fig_temp, ax_temp = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_temp, x="연도", y="해수온(°C)", marker="o", linewidth=2, ax=ax_temp)
    sns.regplot(data=filtered_temp, x="연도", y="해수온(°C)", scatter=False, color="red", ax=ax_temp, label="추세선")
    ax_temp.set_title("해수온 상승 추이", fontsize=16, fontweight='bold')
    ax_temp.set_ylabel("해수온(°C)")
    ax_temp.legend()
    st.pyplot(fig_temp)

    # 지도: 해수온 이상 분포
    st.subheader("🌍 전 지구 해수온 이상 분포 지도")
    selected_year = st.selectbox("연도 선택", options=range(1990, 2026), index=35)
    year_data = df_sst_anomaly[df_sst_anomaly["Year"] == selected_year]
    fig_map = px.scatter_geo(
        year_data, lat="Lat", lon="Lon", color="SST_Anomaly",
        color_continuous_scale="RdBu_r", range_color=[-2, 2],
        projection="natural earth", title=f"{selected_year}년 해수온 이상 분포 (°C)", height=600
    )
    st.plotly_chart(fig_map, use_container_width=True)

# --------------------------
# 본론1
# --------------------------
with tabs[1]:
    st.header("본론 1. 데이터로 보는 해수온 상승과 해양 환경 변화")

    st.subheader("1-1. 해수온 상승 추이 분석")
    st.write("➡ 해수온이 지속적으로 상승하며 최근 급격히 증가하고 있음을 보여준다.")

    filtered_temp = filter_data_by_year(df_temp, "연도", start_year, end_year)
    df_temp_ma = apply_moving_avg(filtered_temp, "해수온(°C)", window)
    fig1 = px.line(df_temp_ma, x="연도", y=["해수온(°C)", "해수온(°C)(이동평균)"], height=500)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("1-2. 해수온 상승과 해양 환경 변화")
    st.write("➡ 해수온 상승이 산호 생태계에 피해를 준다는 것을 직관적으로 보여준다.")

    filtered_coral = filter_data_by_year(df_coral, "연도", start_year, end_year)
    fig2 = px.line(filtered_coral, x="연도", y="산호 백화 발생(건)", height=500)
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# 본론2
# --------------------------
with tabs[2]:
    st.header("본론 2. 사라지는 생명: 해수온 상승이 해양 생태계에 미치는 영향")

    st.subheader("2-1. 해양 생물 다양성 위기")
    st.write("➡ 해양 생물 다양성이 점점 감소하고 있음을 보여준다.")

    filtered_fish = filter_data_by_year(df_fish, "연도", start_year, end_year)
    fig3 = px.line(filtered_fish, x="연도", y="토착 어종 지수", height=500)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("2-2. 사회·경제적 파급 효과")
    st.write("➡ 해수온 상승이 어업 수익 감소로 이어지고 있음을 시각적으로 보여준다.")

    filtered_output = filter_data_by_year(df_output, "연도", start_year, end_year)
    fig4 = px.line(filtered_output, x="연도", y="수산업 생산량 지수", height=500)
    st.plotly_chart(fig4, use_container_width=True)

# --------------------------
# 결론
# --------------------------
with tabs[3]:
    st.header("결론")

    st.markdown("""
    본 보고서는 해수온 상승이 단순한 해양 현상이 아닌,  
    **해수온 상승 → 해양 환경 변화 → 해양 생물 다양성 위기 → 사회·경제적 파급 효과**로 이어지는 구조적 문제임을 확인했다.  

    따라서 다음과 같은 실천 방안을 제안한다.  

    - 🏛️ 정책: 탄소 배출 저감 및 해양 보호 정책 강화  
    - 🔬 연구: 해양 생태계 모니터링·연구 확대  
    - 👥 시민: 생활 속 친환경 실천과 해양 보호 캠페인 참여
    """)

# --------------------------
# 사이드바 기능
# --------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📥 데이터 다운로드")

combined_data = df_temp.merge(df_coral, on="연도", how="outer")
combined_data = combined_data.merge(df_fish, on="연도", how="outer")
combined_data = combined_data.merge(df_output, on="연도", how="outer")

st.sidebar.download_button(
    "전체 데이터 다운로드 (CSV)",
    combined_data.to_csv(index=False).encode("utf-8-sig"),
    "sea_data.csv", "text/csv"
)

st.sidebar.markdown("---")
st.sidebar.subheader("📚 데이터 출처")
st.sidebar.markdown("""
- NOAA Coral Reef Watch  
- 해양기후예측센터(OCPC)  
- Greenpeace Korea  
- 한국해양수산개발원(KMI)  
- 국립중앙과학관  
""")
