import streamlit as st

def is_balanced(input_string):
    stack = []
    flag = 0

    for char in input_string:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack:
                return "아니요"
            top = stack.pop()
            if (char == ")" and top != "(") or (char == "}" and top != "{") or (char == "]" and top != "["):
                return "아니요"

    if len(stack) == 0:
        return "예"
    return "아니요"

# Streamlit UI
st.title("괄호 균형 확인기")
st.write("괄호로 이루어진 문자열을 입력하고 균형 여부를 확인하세요.")

# 입력 필드
input_string = st.text_input("문자열을 입력하세요:", "")

if st.button("확인"):
    if input_string:
        result = is_balanced(input_string)
        st.write(f"결과: **{result}**")
    else:
        st.write("문자열을 입력해주세요.")