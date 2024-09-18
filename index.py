import streamlit as st

# 한글 초성, 중성, 종성 리스트
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
    'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
    'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
    'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
    'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]

JONGSUNG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
    'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
    'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
    'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

def decompose_hangul(syllable):
    """한글 음절을 초성, 중성, 종성으로 분리"""
    code = ord(syllable)
    if not (0xAC00 <= code <= 0xD7A3):
        return None, None, None  # 한글 음절이 아님
    syllable_index = code - 0xAC00
    jong = syllable_index % 28
    jung = ((syllable_index - jong) // 28) % 21
    cho = ((syllable_index - jong) // 28) // 21
    return CHOSUNG_LIST[cho], JUNGSUNG_LIST[jung], JONGSUNG_LIST[jong]

def compose_hangul(cho, jung, jong):
    """초성, 중성, 종성을 합쳐 한글 음절 생성"""
    try:
        cho_index = CHOSUNG_LIST.index(cho)
        jung_index = JUNGSUNG_LIST.index(jung)
        jong_index = JONGSUNG_LIST.index(jong)
    except ValueError:
        return ''  # 유효하지 않은 초성, 중성, 종성
    syllable_code = 0xAC00 + (cho_index * 21 + jung_index) * 28 + jong_index
    return chr(syllable_code)

def shift_list(lst, shift=1):
    """리스트를 오른쪽으로 shift (암호화)"""
    return lst[-shift:] + lst[:-shift]

def unshift_list(lst, shift=1):
    """리스트를 왼쪽으로 shift (복호화)"""
    return lst[shift:] + lst[:shift]

def encrypt(sentence):
    """입력된 문장을 암호화"""
    decomposed = []
    for s in sentence:
        cho, jung, jong = decompose_hangul(s)
        if cho is None:
            # 한글이 아닌 문자는 그대로 유지
            decomposed.append({'cho': None, 'jung': None, 'jong': None, 'char': s})
        else:
            decomposed.append({'cho': cho, 'jung': jung, 'jong': jong, 'char': s})
    
    # 중성과 종성 리스트 추출
    jungs = [d['jung'] for d in decomposed if d['jung'] is not None]
    jongs = [d['jong'] for d in decomposed if d['jong'] is not None]
    
    if not jungs or not jongs:
        return "암호화할 수 있는 한글 음절이 충분하지 않습니다."
    
    # 중성과 종성을 시계 방향으로 한 칸 밀기 (오른쪽 shift)
    shifted_jungs = shift_list(jungs, shift=1)
    shifted_jongs = shift_list(jongs, shift=1)
    
    # 인덱스 추적
    jung_idx = 0
    jong_idx = 0
    
    # 새로운 음절 조합
    new_sentence = []
    for d in decomposed:
        if d['cho'] is None:
            # 한글이 아닌 문자는 그대로 추가
            new_sentence.append(d['char'])
        else:
            cho = d['cho']
            jung = shifted_jungs[jung_idx]
            jong = shifted_jongs[jong_idx]
            new_syllable = compose_hangul(cho, jung, jong)
            if not new_syllable:
                # 유효하지 않은 조합인 경우 원래 음절 유지
                new_sentence.append(d['char'])
            else:
                new_sentence.append(new_syllable)
            jung_idx += 1
            jong_idx += 1
    
    return ''.join(new_sentence)

def decrypt(sentence):
    """입력된 문장을 복호화"""
    decomposed = []
    for s in sentence:
        cho, jung, jong = decompose_hangul(s)
        if cho is None:
            # 한글이 아닌 문자는 그대로 유지
            decomposed.append({'cho': None, 'jung': None, 'jong': None, 'char': s})
        else:
            decomposed.append({'cho': cho, 'jung': jung, 'jong': jong, 'char': s})
    
    # 중성과 종성 리스트 추출
    jungs = [d['jung'] for d in decomposed if d['jung'] is not None]
    jongs = [d['jong'] for d in decomposed if d['jong'] is not None]
    
    if not jungs or not jongs:
        return "복호화할 수 있는 한글 음절이 충분하지 않습니다."
    
    # 중성과 종성을 시계 반대 방향으로 한 칸 밀기 (왼쪽 shift)
    shifted_jungs = unshift_list(jungs, shift=1)
    shifted_jongs = unshift_list(jongs, shift=1)
    
    # 인덱스 추적
    jung_idx = 0
    jong_idx = 0
    
    # 새로운 음절 조합
    new_sentence = []
    for d in decomposed:
        if d['cho'] is None:
            # 한글이 아닌 문자는 그대로 추가
            new_sentence.append(d['char'])
        else:
            cho = d['cho']
            jung = shifted_jungs[jung_idx]
            jong = shifted_jongs[jong_idx]
            new_syllable = compose_hangul(cho, jung, jong)
            if not new_syllable:
                # 유효하지 않은 조합인 경우 원래 음절 유지
                new_sentence.append(d['char'])
            else:
                new_sentence.append(new_syllable)
            jung_idx += 1
            jong_idx += 1
    
    return ''.join(new_sentence)

def main():
    st.set_page_config(
        page_title="한글 시계 암호기",
        page_icon="⏰",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    st.title("⏰ 한글 시계 암호기")
    st.markdown("""
        이 애플리케이션은 한글 문장을 **암호화**하거나 **복호화**합니다.
        - **암호화**: 각 한글 음절의 중성과 종성을 시계 방향으로 한 칸씩 이동합니다.
        - **복호화**: 암호화의 반대로, 중성과 종성을 시계 반대 방향으로 한 칸씩 이동하여 원래의 문장으로 복원합니다.
    """)
    
    # 입력 섹션
    st.header("📥 입력")
    sentence = st.text_area("문장을 입력하세요:", height=100, placeholder="여기에 암호화하거나 복호화할 한글 문장을 입력하세요.")
    
    # 버튼 섹션
    st.header("🔧 작업 선택")
    col1, col2 = st.columns(2)
    with col1:
        encrypt_btn = st.button("🔒 암호화")
    with col2:
        decrypt_btn = st.button("🔓 복호화")
    
    # 결과 섹션
    st.header("📤 결과")
    if encrypt_btn:
        if not sentence.strip():
            st.error("암호화할 문장을 입력해주세요.")
        else:
            encrypted = encrypt(sentence)
            st.success(f"**암호화된 문장:** {encrypted}")
    
    if decrypt_btn:
        if not sentence.strip():
            st.error("복호화할 문장을 입력해주세요.")
        else:
            decrypted = decrypt(sentence)
            st.success(f"**복호화된 문장:** {decrypted}")
    
    # 예시 섹션
    st.header("📚 사용 예시")
    st.markdown("""
        **원문:** `이 시계 만큼은 넘겨줄수 없다`  
        **암호화:** `의 시거 믄킴은 넘겨줄수 없다`  
        **복호화:** `이 시계 만큼은 넘겨줄수 없다`
    """)
    import streamlit as st

# 한글 초성, 중성, 종성 리스트
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
    'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
    'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
    'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
    'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]

JONGSUNG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
    'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
    'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
    'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

def decompose_hangul(syllable):
    """한글 음절을 초성, 중성, 종성으로 분리"""
    code = ord(syllable)
    if not (0xAC00 <= code <= 0xD7A3):
        return None, None, None  # 한글 음절이 아님
    syllable_index = code - 0xAC00
    jong = syllable_index % 28
    jung = ((syllable_index - jong) // 28) % 21
    cho = ((syllable_index - jong) // 28) // 21
    return CHOSUNG_LIST[cho], JUNGSUNG_LIST[jung], JONGSUNG_LIST[jong]

def compose_hangul(cho, jung, jong):
    """초성, 중성, 종성을 합쳐 한글 음절 생성"""
    try:
        cho_index = CHOSUNG_LIST.index(cho)
        jung_index = JUNGSUNG_LIST.index(jung)
        jong_index = JONGSUNG_LIST.index(jong)
    except ValueError:
        return ''  # 유효하지 않은 초성, 중성, 종성
    syllable_code = 0xAC00 + (cho_index * 21 + jung_index) * 28 + jong_index
    return chr(syllable_code)

def shift_list(lst, shift=1):
    """리스트를 오른쪽으로 shift (암호화)"""
    return lst[-shift:] + lst[:-shift]

def unshift_list(lst, shift=1):
    """리스트를 왼쪽으로 shift (복호화)"""
    return lst[shift:] + lst[:shift]

def encrypt(sentence):
    """입력된 문장을 암호화"""
    decomposed = []
    for s in sentence:
        cho, jung, jong = decompose_hangul(s)
        if cho is None:
            # 한글이 아닌 문자는 그대로 유지
            decomposed.append({'cho': None, 'jung': None, 'jong': None, 'char': s})
        else:
            decomposed.append({'cho': cho, 'jung': jung, 'jong': jong, 'char': s})
    
    # 중성과 종성 리스트 추출
    jungs = [d['jung'] for d in decomposed if d['jung'] is not None]
    jongs = [d['jong'] for d in decomposed if d['jong'] is not None]
    
    if not jungs or not jongs:
        return "암호화할 수 있는 한글 음절이 충분하지 않습니다."
    
    # 중성과 종성을 시계 방향으로 한 칸 밀기 (오른쪽 shift)
    shifted_jungs = shift_list(jungs, shift=1)
    shifted_jongs = shift_list(jongs, shift=1)
    
    # 인덱스 추적
    jung_idx = 0
    jong_idx = 0
    
    # 새로운 음절 조합
    new_sentence = []
    for d in decomposed:
        if d['cho'] is None:
            # 한글이 아닌 문자는 그대로 추가
            new_sentence.append(d['char'])
        else:
            cho = d['cho']
            jung = shifted_jungs[jung_idx]
            jong = shifted_jongs[jong_idx]
            new_syllable = compose_hangul(cho, jung, jong)
            if not new_syllable:
                # 유효하지 않은 조합인 경우 원래 음절 유지
                new_sentence.append(d['char'])
            else:
                new_sentence.append(new_syllable)
            jung_idx += 1
            jong_idx += 1
    
    return ''.join(new_sentence)

def decrypt(sentence):
    """입력된 문장을 복호화"""
    decomposed = []
    for s in sentence:
        cho, jung, jong = decompose_hangul(s)
        if cho is None:
            # 한글이 아닌 문자는 그대로 유지
            decomposed.append({'cho': None, 'jung': None, 'jong': None, 'char': s})
        else:
            decomposed.append({'cho': cho, 'jung': jung, 'jong': jong, 'char': s})
    
    # 중성과 종성 리스트 추출
    jungs = [d['jung'] for d in decomposed if d['jung'] is not None]
    jongs = [d['jong'] for d in decomposed if d['jong'] is not None]
    
    if not jungs or not jongs:
        return "복호화할 수 있는 한글 음절이 충분하지 않습니다."
    
    # 중성과 종성을 시계 반대 방향으로 한 칸 밀기 (왼쪽 shift)
    shifted_jungs = unshift_list(jungs, shift=1)
    shifted_jongs = unshift_list(jongs, shift=1)
    
    # 인덱스 추적
    jung_idx = 0
    jong_idx = 0
    
    # 새로운 음절 조합
    new_sentence = []
    for d in decomposed:
        if d['cho'] is None:
            # 한글이 아닌 문자는 그대로 추가
            new_sentence.append(d['char'])
        else:
            cho = d['cho']
            jung = shifted_jungs[jung_idx]
            jong = shifted_jongs[jong_idx]
            new_syllable = compose_hangul(cho, jung, jong)
            if not new_syllable:
                # 유효하지 않은 조합인 경우 원래 음절 유지
                new_sentence.append(d['char'])
            else:
                new_sentence.append(new_syllable)
            jung_idx += 1
            jong_idx += 1
    
    return ''.join(new_sentence)

def main():
    st.set_page_config(
        page_title="⏰ 한글 시계 암호기",
        page_icon="⏰",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    st.title("⏰ 한글 시계 암호기")
    st.markdown("""
        이 애플리케이션은 한글 문장을 **암호화**하거나 **복호화**합니다.
        - **암호화**: 각 한글 음절의 중성과 종성을 시계 방향으로 한 칸씩 이동합니다.
        - **복호화**: 암호화의 반대로, 중성과 종성을 시계 반대 방향으로 한 칸씩 이동하여 원래의 문장으로 복원합니다.
    """)
    
    # 탭 생성
    tab_encrypt, tab_decrypt = st.tabs(["🔒 암호화", "🔓 복호화"])
    
    with tab_encrypt:
        st.header("📥 암호화 입력")
        sentence = st.text_area(
            "암호화할 문장을 입력하세요:",
            height=150,
            placeholder="여기에 암호화할 한글 문장을 입력하세요."
        )
        
        if st.button("🔒 암호화"):
            if not sentence.strip():
                st.error("암호화할 문장을 입력해주세요.")
            else:
                encrypted = encrypt(sentence)
                st.success(f"**암호화된 문장:** {encrypted}")
    
    with tab_decrypt:
        st.header("📥 복호화 입력")
        encrypted_sentence = st.text_area(
            "복호화할 문장을 입력하세요:",
            height=150,
            placeholder="여기에 복호화할 암호화된 한글 문장을 입력하세요."
        )
        
        if st.button("🔓 복호화"):
            if not encrypted_sentence.strip():
                st.error("복호화할 문장을 입력해주세요.")
            else:
                decrypted = decrypt(encrypted_sentence)
                st.success(f"**복호화된 문장:** {decrypted}")
    
    # 예시 섹션
    st.header("📚 사용 예시")
    example_plain = "이 시계 만큼은 넘겨줄수 없다"
    example_encrypted = encrypt(example_plain)
    example_decrypted = decrypt(example_encrypted)
    
    st.markdown(f"""
    **원문:** `{example_plain}`  
    **암호화:** `{example_encrypted}`  
    **복호화:** `{example_decrypted}`
    """)
    
    st.markdown("---")
    st.markdown("©️ 2024 brainer. 모든 권리 보유.")

if __name__ == "__main__":
    main()
    