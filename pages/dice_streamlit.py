import random
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

# Streamlit UI 설정
st.title("주사위 시뮬레이션")
st.write("슬라이더를 사용해 시행 횟수를 조정하세요. 기댓값과 표준편차가 수렴하는 과정을 관찰할 수 있습니다.")

# 슬라이더를 통해 시행 횟수 선택
selected_trials = st.slider("시행 횟수를 선택하세요:", min_value=1, max_value=1500, value=100)

# 최대 시행 횟수 설정 (최적화를 위해 고정된 최대값으로 데이터 준비)
max_trials = 1500

# 데이터 캐싱: 최대 횟수까지 한 번만 계산
@st.cache_data
def simulate_dice_rolls(max_trials):
    averages = []
    std_devs = []
    values = []

    for trial in range(1, max_trials + 1):
        values.append(random.randint(1, 6))  # 새로운 주사위 값 추가
        averages.append(np.mean(values))  # 평균 업데이트
        std_devs.append(np.std(values))  # 표준편차 업데이트

    data = pd.DataFrame({
        "시행 횟수": np.arange(1, max_trials + 1),
        "표본 평균": averages,
        "표본 표준편차": std_devs,
    })
    return data

# 데이터 계산
data = simulate_dice_rolls(max_trials)

# 선택된 범위의 데이터만 필터링
filtered_data = data[data["시행 횟수"] <= selected_trials]

# 수학적 기대값과 표준편차
expected_value = 3.5
expected_std_dev = np.sqrt(sum([(i - expected_value) ** 2 / 6 for i in range(1, 7)]))

# Altair 그래프: 기댓값
mean_chart = (
    alt.Chart(filtered_data)
    .mark_line(color="blue")
    .encode(
        x="시행 횟수",
        y="표본 평균",
    )
    .properties(
        title="기댓값 수렴 과정"
    )
    + alt.Chart(pd.DataFrame({"y": [expected_value]}))
    .mark_rule(color="red", strokeDash=[5, 5])
    .encode(y="y:Q")
)

# Altair 그래프: 표준편차
std_dev_chart = (
    alt.Chart(filtered_data)
    .mark_line(color="green")
    .encode(
        x="시행 횟수",
        y="표본 표준편차",
    )
    .properties(
        title="표준편차 수렴 과정"
    )
    + alt.Chart(pd.DataFrame({"y": [expected_std_dev]}))
    .mark_rule(color="red", strokeDash=[5, 5])
    .encode(y="y:Q")
)

# Streamlit에 그래프 출력
st.altair_chart(mean_chart, use_container_width=True)
st.altair_chart(std_dev_chart, use_container_width=True)
