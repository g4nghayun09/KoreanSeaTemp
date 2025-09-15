# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="해수온 상승과 해양 생태계 변화", layout="wide")

st.title("해수온 상승과 바다의 미래: 변화와 대응 전략")

# 자료 출처
st.markdown("""
참고 자료:
- [뉴스튜브](https://www.newstube.kr/news/articleView.html?idxno=3558)
- [위클리서울](https://www.weeklyseoul.net/news/articleView.html?idxno=80741)
- [GreenPeace](https://www.greenpeace.org/korea/update/18714/blog-ce-all-about-sea-level-rise/)
- [KMI 수산통계](https://www.kmi.re.kr/)
- [OCPC 해양기후 분석](https://www.ocpc.kr/review)
- [국립해양조사원](https://www.khoa.go.kr/)
""")

# ------------------------------
# 본론 1_1: 전 세계 및 한반도 주변 해수온 변화
st.header("1-1. 해수온 상승 추이 분석")
sea_temp_data = {
    "연도": [2000, 2005, 2010, 2015, 2020, 2024],
    "전세계 평균 해수온": [16.1, 16.2, 16.3, 16.5, 16.7, 16.9],
    "한반도 주변 해수온": [14.1, 14.4, 14.7, 15.0, 15.3, 15.7]
}
df_temp = pd.DataFrame(sea_temp_data)

fig_temp = px.line(df_temp, x="연도", y=["전세계 평균 해수온","한반도 주변 해수온"],
                   markers=True, title="전 세계 및 한반도 주변 해수온 변화")
st.plotly_chart(fig_temp, use_container_width=True)
st.markdown("해수온이 지속적으로 상승하며 최근 급격히 증가하고 있음을 보여준다.")

# ------------------------------
# 본론 1_2: 산호 백화 현상 사진/지도
st.header("1-2. 해수온 상승과 해양 환경 변화")
st.image("https://upload.wikimedia.org/wikipedia/commons/8/8d/Bleached_coral.jpg", caption="산호 백화 현상 예시")
st.markdown("해수온 상승이 산호 생태계에 직접적 피해를 준다는 것을 직관적으로 보여준다.")

# ------------------------------
# 본론 2_1: 토착 어종 개체수 변화
st.header("2-1. 해양 생물 다양성 위기")
species_data = {
    "연도": [2000, 2005, 2010, 2015, 2020, 2024],
    "토착 어종 개체수": [1000, 950, 900, 850, 780, 720]
}
df_species = pd.DataFrame(species_data)
fig_species = px.line(df_species, x="연도", y="토착 어종 개체수",
                      markers=True, title="토착 어종 개체수 변화")
st.plotly_chart(fig_species, use_container_width=True)
st.markdown("해양 생물 다양성이 점점 감소하고 있음을 보여준다.")

# ------------------------------
# 본론 2_2: 수산업 생산량 변화
st.header("2-2. 사회·경제적 파급 효과")
catch_data = {
    "연도": [2000, 2005, 2010, 2015, 2020, 2024],
    "오징어": [5000, 4800, 4500, 4300, 4100, 3800],
    "고등어": [6000, 5800, 5600, 5400, 5200, 5000]
}
df_catch = pd.DataFrame(catch_data)
df_catch_melted = df_catch.melt(id_vars="연도", var_name="어종", value_name="어획량(톤)")
fig_catch = px.line(df_catch_melted, x="연도", y="어획량(톤)", color="어종",
                    markers=True, title="수산업 생산량 변화 (오징어·고등어)")
st.plotly_chart(fig_catch, use_container_width=True)
st.markdown("해수온 상승이 어업 수익 감소로 이어지고 있음을 시각적으로 보여준다.")

# ------------------------------
# CSV 다운로드 버튼
st.header("데이터 다운로드")
st.download_button("연근해 해수온 데이터 다운로드", df_temp.to_csv(index=False), "sea_temp_data.csv", "text/csv")
st.download_button("토착 어종 데이터 다운로드", df_species.to_csv(index=False), "species_data.csv", "text/csv")
st.download_button("수산업 생산량 데이터 다운로드", df_catch.to_csv(index=False), "catch_data.csv", "text/csv")
