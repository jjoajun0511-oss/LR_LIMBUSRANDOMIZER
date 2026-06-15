import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="림버스 수감자 조합기 V2",
    page_icon="logo.png",
    layout="centered"
)
# 1. 초기 데이터 기입 (세션 상태에 저장하여 추가/삭제 데이터가 유지되도록 함)
if "identity_pool" not in st.session_state:
    st.session_state.identity_pool = {
        "이상": ["[0] LCB 수감자 이상", "[000] 거미집 검지 아비 이상", "[000] 흑수 - 오 필두 이상", "[000] 로보토미 E.G.O :: 엄숙한 애도 이상", "[000] 약지 점묘파 스튜던트 이상", "[000] W사 3등급 정리 요원 이상", "[000] 검계 살수 이상", "[000] 남부 리우 협회 3과 이상"],
        "파우스트": ["[0] LCB 수감자 파우스트", "[000] 거미집 약지 제자 파우스트", "[000] 검지 수행자: 【쪽지】파우스트", "[000] 흑수 - 묘 필두 파우스트", "[000] 로보토미 E.G.O :: 후회 파우스트", "[00] 살아남은 로보토미 직원 파우스트", "[00] 워더링하이츠 버틀러 파우스트"],
        "돈키호테": ["[0] LCB 수감자 돈키호테", "[000] 검지 대행자 - 개화 E.G.O :: 대행 돈키호테", "[000] 흑수 - 미 돈키호테", "[000] 라만차랜드 실장 돈키호테", "[000] 중지 작은 아우 돈키호테", "[000] W사 3등급 정리 요원 돈키호테"],
        "료슈": ["[0] LCB 수감자 료슈", "[000] 거미집의 검 료슈", "[000] 로보토미 E.G.O :: 잔향 • 외로움 료슈", "[000] 홍원 방랑무사 료슈", "[000] N사 E.G.O :: 경멸 • 경외 료슈"],
        "뫼르소": ["[0] LCB 수감자 뫼르소", "[000] 약지 야수파 스튜던트 뫼르소", "[000] 동부 엄지 카포IIII 뫼르소", "[000] 서부 섕크 협회 3과 뫼르소", "[00] 중지 작은 아우 뫼르소", "[000] R사 제 4무리 코뿔소팀 뫼르소", "[000] 검계 우두머리 <착영휘도> 뫼르소", "[000] 검계 우두머리 뫼르소"],
        "홍루": ["[0] LCB 수감자 홍루", "[000] 거미집 약지 아비 홍루", "[000] 홍원 군주 홍루", "[000] K사 3등급 적출직 직원 홍루", "[00] 송곳니 사냥 사무소 해결사 홍루", "[00] 남부 리우 협회 5과 홍루", "[000] S사 추노꾼 홍루"],
        "히스클리프": ["[0] LCB 수감자 히스클리프", "[000] 중지 작은 형님 히스클리프", "[000] 흑수 - 유 필두 히스클리프", "[000] 흑운회 와카슈 히스클리프", "[000] 남부 외우피 협회 3과 히스클리프"],
        "이스마엘": ["[0] LCB 수감자 이스마엘", "[000] 거미집 중지 제자 이스마엘", "[000] 정사무소 대표 이스마엘", "[000] 흑운회 부조장 이스마엘", "[00] LCCB 대리 이스마엘", "[00] 에드가 가문 버틀러 이스마엘", "[000] LCD 현장추리팀 이스마엘"],
        "로쟈": ["[0] LCB 수감자 로쟈", "[000] 약지 야수파 도슨트 로쟈", "[000] 흑수 - 사 로쟈", "[000] 라만차랜드 공주 로쟈", "[000] 북부 제뱌찌 협회 3과 로쟈"],
        "싱클레어": ["[0] LCB 수감자 싱클레어", "[000] 거미집 소지 제자 싱클레어", "[000] 흑수 - 유 싱클레어", "[000] 중지 작은 아우 싱클레어", "[000] 북부 제뱌찌 협회 3과 싱클레어", "[000] 쥐어들 자 싱클레어", "[00] 로보토미 E.G.O :: 홍적 싱클레어", "[00] 마리아치 보스 싱클레어", "[000] 검계 살수 싱클레어"],
        "오티스": ["[0] LCB 수감자 오티스", "[000] LCA 우제트 선봉 3팀 팀장 오티스", "[000] T사 3등급 강력징수직 직원 오티스", "[000] 흑수 - 묘 오티스", "[00] 약지 점묘파 스튜던트 오티스", "[000] 거미집 중지 아비 오티스", "[00] 검계 살수 오티스"],
        "그레고르": ["[0] LCB 수감자 그레고르", "[000] LCE E.G.O :: AEDD 그레고르", "[000] 로보토미 E.G.O :: 램프 그레고르", "[000] 불주먹 사무소 생존자 그레고르", "[000] 라만차랜드 신부 그레고르", "[000] G사 1등대리 그레고르", "[000] 쌍갈고리 해적단 부선장 그레고르"]
    }

keywords = ["화상", "출혈", "진동", "파열", "침잠", "호흡", "충전", "참격", "관통", "타격"]

# 기본 선택 인원수 세션 등록 (기본 7명)
if "pick_count" not in st.session_state:
    st.session_state.pick_count = 7

# 전체 새로 고침 함수
def reset_all():
    # 인격이 최소 1개 이상 등록된 수감자만 필터링 (에러 방지)
    valid_sinners = [k for k, v in st.session_state.identity_pool.items() if len(v) > 0]
    actual_count = min(st.session_state.pick_count, len(valid_sinners))
    
    st.session_state.current_sinners = random.sample(valid_sinners, actual_count)
    st.session_state.current_team = {sinner: random.choice(st.session_state.identity_pool[sinner]) for sinner in st.session_state.current_sinners}
    st.session_state.chosen_keyword = random.choice(keywords)
    st.session_state.num1 = random.randint(1, 3)
    st.session_state.num2 = random.randint(1, 3)
    st.session_state.new_commers = []

# 초기 앱 구동 시 자동 뽑기
if 'current_sinners' not in st.session_state:
    reset_all()

# 멤버 교체 함수 (뽑힌 인원이 적을 때를 대비해 유연하게 조절)
def change_three_members():
    valid_sinners = [k for k, v in st.session_state.identity_pool.items() if len(v) > 0]
    current_set = set(st.session_state.current_sinners)
    bench_sinners = list(set(valid_sinners) - current_set)

    # 교체할 명수 결정 (최대 3명, 대기 조가 부족하면 가능한 만큼만)
    change_count = min(3, len(st.session_state.current_sinners), len(bench_sinners))
    if change_count <= 0:
        return

    leavers = random.sample(st.session_state.current_sinners, change_count)
    joiners = random.sample(bench_sinners, change_count)

    for leave_sinner in leavers:
        st.session_state.current_sinners.remove(leave_sinner)
        if leave_sinner in st.session_state.current_team:
            del st.session_state.current_team[leave_sinner]

    for join_sinner in joiners:
        st.session_state.current_sinners.append(join_sinner)
        st.session_state.current_team[join_sinner] = random.choice(st.session_state.identity_pool[join_sinner])
    
    st.session_state.new_commers = joiners

# --- UI 레이아웃 시작 ---
st.title("🎲 림버스 수감자 커스텀 조합기")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 멤버 일부 교체하기", use_container_width=True, type="primary"):
        change_three_members()
with col2:
    if st.button("🔄 아예 새로 뽑기", use_container_width=True):
        reset_all()

st.markdown("---")

# 결과창 출력
st.subheader(f"★ 현재 수감자 엔트리 ({len(st.session_state.current_sinners)}명) ★")
for i, sinner in enumerate(st.session_state.current_sinners, 1):
    identity_name = st.session_state.current_team.get(sinner, "선택 가능한 인격 없음")
    if sinner in st.session_state.new_commers:
        st.markdown(f"**{i}. [{sinner}]** ➔ {identity_name} 🔴 **(새로 투입!)**")
    else:
        st.write(f"{i}. [{sinner}] ➔ {identity_name}")

st.markdown("---")
st.subheader("🎯 최초 지정 키워드 & 숫자")
st.info(f"▶ **[지정 키워드]** : {st.session_state.chosen_keyword}")
st.success(f"▶ **[보너스 숫자]** : {st.session_state.num1}, {st.session_state.num2}")

# --- 커스텀 데이터 관리 섹션 (접이식 메뉴로 모바일 가독성 업) ---
st.markdown("---")
with st.expander("⚙️ 데이터 관리 및 유저 설정 (인격 추가/삭제/인원 조절)"):
    
    # 1. 인원 수 설정
    new_count = st.slider("한 번에 몇 명을 뽑을까요?", min_value=1, max_value=12, value=st.session_state.pick_count)
    if new_count != st.session_state.pick_count:
        st.session_state.pick_count = new_count
        reset_all()
        st.rerun()

    st.markdown("---")
    
    # 2. 인격 추가 기능
    st.write("**➕ 새로운 인격 추가하기**")
    add_sinner = st.selectbox("수감자 선택 (추가용)", list(st.session_state.identity_pool.keys()), key="add_select")
    add_name = st.text_input("추가할 인격 이름을 적어주세요 (예: [000] 워더링하이츠 버틀러 오티스)")
    if st.button("인격 풀에 추가하기"):
        if add_name.strip():
            st.session_state.identity_pool[add_sinner].append(add_name.strip())
            st.toast(f"✅ {add_sinner} - '{add_name}' 추가 완료!")
        else:
            st.error("인격 이름을 입력해 주세요.")

    st.markdown("---")

    # 3. 인격 삭제 기능
    st.write("**❌ 마음에 안 드는 인격 삭제하기**")
    del_sinner = st.selectbox("수감자 선택 (삭제용)", list(st.session_state.identity_pool.keys()), key="del_select")
    
    # 선택한 수감자의 인격 목록 가져오기
    current_identities = st.session_state.identity_pool[del_sinner]
    if current_identities:
        del_name = st.selectbox("삭제할 인격 선택", current_identities)
        if st.button("선택한 인격 삭제하기"):
            st.session_state.identity_pool[del_sinner].remove(del_name)
            st.toast(f"🔥 {del_sinner} - '{del_name}' 삭제 완료!")
            st.rerun()
    else:
        st.caption("해당 수감자는 등록된 인격이 없습니다.")

