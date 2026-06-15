import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 초기 데이터 세팅 (세션 상태 활용)
st.set_page_config(page_title="도서 대출/반납 시스템", layout="centered")

if 'book_list' not in st.session_state:
    st.session_state.book_list = ['어린왕자', '데미안', '드라큘라']
if 'status_list' not in st.session_state:
    st.session_state.status_list = ['대출가능', '대출가능', '대출가능']

# 제목
st.title("📚 도서 대출 관리 시스템")
st.write("현재 보유 중인 도서의 목록과 대출 상태입니다.")

# 2. 보유 도서 현황 출력 (st.dataframe 활용)
df = pd.DataFrame({
    '도서명': st.session_state.book_list,
    '상태': st.session_state.status_list
})
st.dataframe(df, use_container_width=True)

st.markdown("---")

# 3. 메뉴 선택 (Sidebar 또는 Radio 위젯 활용)
menu = st.radio("원하는 작업을 선택하세요", ('[1] 대출', '[2] 반납'), horizontal=True)

# --- [1] 대출 로직 ---
if menu == '[1] 대출':
    st.subheader("📖 도서 대출")
    
    # 대출 가능한 도서만 필터링
    available_books = [st.session_state.book_list[i] for i in range(len(st.session_state.book_list)) if st.session_state.status_list[i] == '대출가능']
    
    if not available_books:
        st.warning("현재 대출 가능한 도서가 없습니다.")
    else:
        # 대출할 도서 선택 (selectbox 위젯 사용)
        selected_book = st.selectbox("대출할 도서를 선택하세요", available_books)
        
        if st.button("대출 신청"):
            # 선택한 도서의 인덱스를 찾아 상태 변경
            idx = st.session_state.book_list.index(selected_book)
            st.session_state.status_list[idx] = '대출중'
            st.success(f"🎉 '{selected_book}' 도서가 성공적으로 대출되었습니다!")
            st.rerun() # 화면 즉시 갱신

# --- [2] 반납 로직 ---
elif menu == '[2] 반납':
    st.subheader("🔄 도서 반납")
    
    # 직접 입력받는 구조 (기존 코드의 의도 반영)
    return_book = st.text_input("반납할 도서명을 정확히 입력하세요:")
    
    if st.button("반납 신청"):
        if return_book in st.session_state.book_list:
            idx = st.session_state.book_list.index(return_book)
            
            # 이미 대출가능한 상태인 경우
            if st.session_state.status_list[idx] == '대출가능':
                st.info(f"'{return_book}'은(는) 이미 반납되어 있는 상태입니다.")
            else:
                # 반납 성공 처리
                st.session_state.status_list[idx] = '대출가능'
                st.success(f"✅ '{return_book}' 반납이 완료되었습니다. 감사합니다!")
                st.rerun() # 화면 즉시 갱신
        else:
            # 리스트에 없는 도서일 경우
            st.error("❌ 잘못된 도서명입니다. 보유 도서 목록을 확인해주세요.")