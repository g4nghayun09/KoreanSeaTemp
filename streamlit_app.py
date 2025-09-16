# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from io import StringIO
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Pretendard 폰트 적용 시도
plt.rcParams['font.family'] = 'Pretendard'

st.set_page_config(page_title="해수온 상승과 바다의 미래", layout="wide")
st.title("🌊 해수온 상승과 바다의 미래 대시보드")

# =====================================
# 서론
# =====================================
st.header("서론: 우리가 이 보고서를 쓰게 된 이유")
st.markdown("""
21세기 인류가 직면한 가장 큰 도전 중 하나는 기후 위기입니다.  
기후 위기의 다양한 현상 중에서도 해수온 상승은 단순히 바다만의 문제가 아니라,  
지구 생태계 전체와 인류 사회의 미래와도 직결됩니다.
최근 수십 년간 바다는 점점 뜨거워지고 있으며, 해양 생태계는 심각한 변화의 소용돌이에 휘말리고 있습니다.
본 보고서는 해수온 상승이 해양 환경과 생물 다양성, 사회·경제적 영역에 미치는 영향을 분석하고, 대응 전략을 제안합니다.
""")

# =====================================
# 1️⃣ 공식 공개 데이터 기반 대시보드
# =====================================
st.header("1️⃣ 공개 데이터 기반 해수온 상승 분석")

@st.cache_data
def load_noaa_data():
    url = "https://coralreefwatch.noaa.gov/satellite/data/sea_surface_temperature.csv"  # 예시 URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] <= pd.Timestamp(datetime.now().date())]
        df = df.drop_duplicates()
        df = df.fillna(method='ffill')
        return df
    except:
        st.warning("공식 데이터 불러오기 실패. 예시 데이터를 표시합니다.")
        dates = pd.date_range(start="2000-01-01", periods=240, freq='M')
        values = np.linspace(24, 28, 240) + np.random.randn(240)*0.2
        df = pd.DataFrame({'date': dates, 'value': values})
        return df

noaa_df = load_noaa_data()

st.subheader("📊 전 세계 평균 해수온 변화")
st.markdown("최근 수십 년간 전 세계 평균 해수온은 꾸준히 상승하고 있으며, 한반도 주변 해역은 더 빠른 상승을 보이고 있습니다.")
fig1 = px.line(noaa_df, x='date', y='value', title='전 세계 평균 해수온 (°C)',
               labels={'date':'연도', 'value':'해수온(°C)'})
st.plotly_chart(fig1, use_container_width=True)

# CSV 다운로드
csv = noaa_df.to_csv(index=False).encode('utf-8')
st.download_button("공식 데이터 CSV 다운로드", data=csv, file_name="noaa_sea_temp.csv", mime='text/csv')

# =====================================
# 2️⃣ 보고서 기반 데이터 대시보드
# =====================================
st.header("2️⃣ 보고서 기반 해수온·생태계 영향 분석")

# 사용자 보고서 데이터 예시 생성
dates = pd.date_range(start="2000-01-01", periods=20, freq='Y')
korea_temp = np.linspace(15, 18, 20) + np.random.randn(20)*0.2
world_temp = np.linspace(14, 16, 20) + np.random.randn(20)*0.2
fish_yield = np.linspace(1000, 700, 20) + np.random.randn(20)*20
native_species = np.linspace(500, 300, 20) + np.random.randn(20)*10

user_df = pd.DataFrame({
    '연도': dates.year,
    '한반도 평균 수온(°C)': korea_temp,
    '전 세계 평균 수온(°C)': world_temp,
    '수산업 생산량(톤)': fish_yield,
    '토착 어종 개체수(마리)': native_species
})

# UI: 연도 범위 선택
year_range = st.slider("연도 범위 선택", int(dates.year.min()), int(dates.year.max()),
                       (int(dates.year.min()), int(dates.year.max())))
user_df_filtered = user_df[(user_df['연도'] >= year_range[0]) & (user_df['연도'] <= year_range[1])]

# 본론 1-1
st.subheader("1-1. 해수온 상승 추이 분석")
st.markdown("""
지난 수십 년간 한반도와 전 세계 평균 해수온은 꾸준히 상승했습니다.  
최근에는 '해양 열파(marine heatwave)' 현상이 빈번하게 발생하고 있습니다.
""")
fig2 = px.line(user_df_filtered, x='연도',
               y=['한반도 평균 수온(°C)','전 세계 평균 수온(°C)'],
               labels={'value':'해수온(°C)', 'variable':'지역'})
st.plotly_chart(fig2, use_container_width=True)

# 본론 1-2
st.subheader("1-2. 해수온 상승과 해양 환경 변화")
st.markdown("""
해수온 상승은 산호 백화, 해양 산성화, 해류 변화를 유발합니다.  
열대·아열대 산호초는 수온 변화에 민감하여 단 몇 도 상승만으로도 백화가 발생합니다.
""")
st.markdown("지도 시각화로 산호 분포를 예시로 보여드립니다.")
m = folium.Map(location=[0, 150], zoom_start=2)
st_folium(m, width=700, height=400)

# 본론 2-1
st.subheader("2-1. 해양 생물 다양성 위기")
st.markdown("""
해수온 상승은 토착 어종 감소와 특정 종의 이동을 불러오며,  
플랑크톤과 저서생물 변화가 먹이사슬에 영향을 주어 해양 생태계 균형을 흔듭니다.
""")
fig3 = px.line(user_df_filtered, x='연도', y='토착 어종 개체수(마리)',
               labels={'토착 어종 개체수(마리)':'개체수(마리)'})
st.plotly_chart(fig3, use_container_width=True)

# 본론 2-2
st.subheader("2-2. 사회·경제적 파급 효과")
st.markdown("""
해수온 상승으로 수산업 생산량이 감소하고, 어업 수익이 줄며,  
지역사회 경제와 식량 안보에 직접적인 영향을 줍니다.
""")
fig4 = px.line(user_df_filtered, x='연도', y='수산업 생산량(톤)',
               labels={'수산업 생산량(톤)':'생산량(톤)'})
st.plotly_chart(fig4, use_container_width=True)

# CSV 다운로드
csv2 = user_df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("보고서 기반 CSV 다운로드", data=csv2, file_name="user_report_data.csv", mime='text/csv')

# 결론
st.header("결론")
st.markdown("""
해수온 상승은 해양 환경 변화 → 해양 생물 다양성 위기 → 사회·경제적 파급 효과로 이어지는 구조적 문제입니다.  
바다의 변화는 인류 삶과 직결되며, 미래 세대의 지속 가능한 생존 조건과도 맞닿아 있습니다.
- 정책 차원: 탄소 배출 저감 및 해양 보호 정책 강화  
- 연구 차원: 해양 생태계 모니터링 시스템 확충 및 기후 변화 대응 연구 확대  
- 시민 차원: 생활 속 친환경 실천 (플라스틱 사용 줄이기, 해양 보호 캠페인 참여 등)
""")
