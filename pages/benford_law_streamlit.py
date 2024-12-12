import streamlit as st
import pandas as pd
import altair as alt

# Streamlit 앱 제목
st.title("벤포드 법칙 분석")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # CSV 파일 읽기 (UTF-8 인코딩 기본값)
        data = pd.read_csv(uploaded_file)
        st.write("데이터 미리보기:")
        st.dataframe(data.head())

        # 숫자로 변환 가능한 열 찾기
        numeric_columns = []
        for col in data.columns:
            try:
                pd.to_numeric(data[col].dropna(), errors='raise')  # 변환 시도
                numeric_columns.append(col)  # 성공하면 리스트에 추가
            except ValueError:
                continue

        # 숫자 열 확인
        if len(numeric_columns) == 0:
            st.error("데이터에 숫자로 변환 가능한 열이 없습니다. 분석할 수 없습니다.")
        else:
            column = st.selectbox("분석할 열을 선택하세요:", numeric_columns)

            if column:
                # 선택한 열 데이터 추출 및 결측값 제거
                valid_data = data[column].dropna()

                # 문자열 변환 및 첫 자리 숫자 추출
                valid_data = (
                    valid_data.astype(str)  # 문자열로 변환
                    .str.lstrip("-0.")  # 음수, 0, 소수점 제거
                )

                # 유효한 값 필터링 (숫자로 시작하는 데이터만)
                valid_data = valid_data[valid_data.str.match(r'^\d')]

                # 첫 자리 숫자만 추출
                first_digits = valid_data.str[0]

                # 각 첫 자리 숫자 빈도 계산
                first_digit_counts = first_digits.value_counts().sort_index()
                first_digit_distribution = (
                    first_digit_counts / first_digit_counts.sum()
                ).reset_index()
                first_digit_distribution.columns = ['숫자', '비율']

                # 분포 결과 출력
                st.write("첫자리 숫자 분포:")
                st.dataframe(first_digit_distribution)

                # Altair로 그래프 시각화 (퍼센트로 표시)
                chart = (
                    alt.Chart(first_digit_distribution)
                    .mark_bar()
                    .encode(
                        x=alt.X("숫자:O", title="첫자리 숫자"),
                        y=alt.Y("비율:Q", title="비율", axis=alt.Axis(format=".0%")),  # 축에 퍼센트 표시
                        tooltip=[
                            alt.Tooltip("숫자:O", title="숫자"),
                            alt.Tooltip("비율:Q", title="비율", format=".2%")  # 툴팁에 퍼센트 표시
                        ]
                    )
                    .properties(
                        title="첫자리 숫자 분포",
                        width=600,
                        height=400
                    )
                )
                st.altair_chart(chart)
    except UnicodeDecodeError as e:
        # 디코딩 오류 메시지와 해결 방법 출력
        st.error("⚠️ CSV 파일을 읽는 도중 디코딩 오류가 발생했습니다.")
        st.write("오류 메시지:")
        st.code(str(e), language="plaintext")
        st.warning("""
        이 문제는 파일이 UTF-8이 아닌 다른 인코딩(CP949, EUC-KR 등)으로 저장되어 있을 때 발생합니다.
        해결 방법:
        1. 파일이 UTF-8로 저장되어 있는지 확인하세요.
        2. 파일을 메모장에서 열어 다른 이름으로 저장할 때 인코딩을 UTF-8로 선택하세요.
        3. 또는 아래에 파일 인코딩을 입력하세요.
        """)

        # 사용자 입력을 통한 인코딩 지정
        encoding = st.text_input("파일 인코딩을 입력하세요 (예: cp949, euc-kr):", value="utf-8")

        if st.button("파일 다시 읽기"):
            try:
                data = pd.read_csv(uploaded_file, encoding=encoding)
                st.success(f"파일이 성공적으로 읽혔습니다! 사용한 인코딩: {encoding}")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"파일을 읽는 도중 오류가 발생했습니다: {str(e)}")