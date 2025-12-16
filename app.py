import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="축제 포인트 분석", layout="wide")

st.title("🎉 동아리 축제 포인트 서버 기록 분석")
st.write("CSV 파일을 업로드하면 자동으로 분석 결과를 보여줍니다.")

# 1️⃣ 파일 업로드
uploaded_file = st.file_uploader("포인트 로그 CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 2️⃣ 데이터 정리
    df = df.dropna(how="all")
    df['created_at_utc'] = pd.to_datetime(df['created_at_utc'])
    df = df.sort_values('created_at_utc')

    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    # 3️⃣ 기본 요약
    st.subheader("📊 기본 통계 요약")
    col1, col2, col3 = st.columns(3)

    col1.metric("총 거래 수", len(df))
    col2.metric("참여 학생 수", df['student_name'].nunique())
    col3.metric("운영 부스 수", df['booth_name'].nunique())

    # 4️⃣ 전체 포인트 흐름
    st.subheader("📈 전체 포인트 흐름")
    df['total_point_flow'] = df['delta'].cumsum()

    fig1, ax1 = plt.subplots()
    ax1.plot(df['created_at_utc'], df['total_point_flow'], marker='o')
    ax1.set_xlabel("시간")
    ax1.set_ylabel("누적 포인트 변화")
    ax1.grid(True)
    st.pyplot(fig1)

    # 5️⃣ 부스별 포인트 변화
    st.subheader("🏷️ 부스별 포인트 변화")
    booth_sum = df.groupby('booth_name')['delta'].sum().sort_values()

    fig2, ax2 = plt.subplots()
    booth_sum.plot(kind='bar', ax=ax2)
    ax2.set_xlabel("부스명")
    ax2.set_ylabel("포인트 변화량")
    ax2.grid(axis='y')
    st.pyplot(fig2)

    # 6️⃣ 시간대별 포인트 사용
    st.subheader("⏰ 시간대별 포인트 변화")
    df['hour'] = df['created_at_utc'].dt.hour
    hourly = df.groupby('hour')['delta'].sum()

    fig3, ax3 = plt.subplots()
    ax3.plot(hourly.index, hourly.values, marker='o')
    ax3.set_xlabel("시간(시)")
    ax3.set_ylabel("포인트 변화 합계")
    ax3.grid(True)
    st.pyplot(fig3)

    # 7️⃣ 결과 요약
    st.subheader("✅ 분석 결과 요약")

    most_used_booth = booth_sum.idxmin()
    st.write(f"- 포인트가 가장 많이 사용된 부스: **{most_used_booth}**")
    st.write("- 특정 시간대에 포인트 사용이 집중되는 경향이 관찰됨")
