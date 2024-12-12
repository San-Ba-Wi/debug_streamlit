import streamlit as st
import altair as alt
import pandas as pd

def collatz(number):
    # 각 계산 단계를 저장할 리스트
    cv_list = []
    count = 0
    max_value = number  # 초기값을 max_value로 설정

    # Collatz 계산 반복
    while number != 1:
        cv_list.append({"단계": count, "값": number})  # 딕셔너리로 저장
        if number % 2 == 0:  # 짝수인 경우
            number //= 2
        else:  # 홀수인 경우
            number = number * 3 + 1
        count += 1
        if number > max_value:  # 최댓값 업데이트
            max_value = number
    cv_list.append({"단계": count, "값": number})  # 마지막 (1이 되는 값) 저장

    return cv_list, count, max_value

# Streamlit UI
st.title("콜라츠 추측 시각화")

# 사용자 입력
data_input = st.number_input("양의 정수를 입력하세요:", min_value=1, value=7, step=1)

if st.button("콜라츠 수열 실행"):
    # Collatz 계산 실행
    sequence, steps, max_value = collatz(data_input)

    # 결과 출력
    st.write(f"**총 단계 수:** {steps}")
    st.write(f"**최댓값:** {max_value}")

    # 데이터프레임 생성
    df = pd.DataFrame(sequence)

    # Altair 그래프 생성
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('단계:Q', title='단계'),
        y=alt.Y('값:Q', title='값'),
        tooltip=['단계', '값']
    ).properties(
        title="콜라츠 추측 시각화",
        width=700,
        height=400
    )

    # 그래프 표시
    st.altair_chart(chart, use_container_width=True)