import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
# .env 파일을 로드합니다.


# standard.json파일 읽어오는 함수
import json
import time
import random


def connect_db():
    load_dotenv()
    host=os.getenv('DB_HOST')
    user=os.getenv('DB_USER')
    password=os.getenv('DB_PASSWORD')
    database=os.getenv('DB_NAME')
    
    # print(f"Host: {host}, User: {user}, Password: {password}, Database: {database}")  # 환경 변수 확인용
    
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
def insert_quote(quote_id, name, email, contact_name, contact, product, biz_type, employee, standards, audit_type, locale, all_support, documents_support, internal_auditor, response_support, audit_fee):
    try:
        db = connect_db()
        cursor = db.cursor()
        query = """
        INSERT INTO sb (quote_id, name, email, contact_name, contact, product, biz_type, employee, standards, audit_type, locale, all_support, documents_support, internal_auditor, response_support, audit_fee)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (quote_id, name, email, contact_name, contact, product, biz_type, employee, ', '.join(standards), audit_type, locale, all_support, documents_support, internal_auditor, response_support, audit_fee))
        db.commit()
        cursor.close()
        db.close()
        # st.success("견적 정보가 성공적으로 데이터베이스에 저장되었습니다.")
        print("견적 정보가 성공적으로 데이터베이스에 저장되었습니다.")
    except Exception as e:
        st.error("데이터베이스 저장 중 오류 발생: " + str(e))

st.set_page_config(page_title="ISO인증취득 온라인 견적", page_icon=":sports_medal:")
st.title('ISO인증취득 온라인 견적 문의')
# st.write(':rainbow[2,000건 이상의 사례를 분석한 인공지능]:sparkles:이 귀사의 상황에 가장 적합한 견적을 제시합니다. ')
st.subheader(':rainbow[인증지원센터는 효율적인 인증프로세스, 합리적인 비용을 기반으로 기업의 성장을 지원합니다.] ')
st.write('사업성장의 시작, 합리적인 비용과 효과적인 인증프로세스로 인증지원센터가 기업 맞춤형 서비스를 제공합니다. 견적문의를 통해 인증비용을 확인하세요.')
# HTML을 사용하여 글자 크기 조정
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.color {
    color: #FF0000;
}

</style>
""", unsafe_allow_html=True)
# st.markdown('<p class="big-font">안심하세요! &#x1F33B;</p> 1원도 들지 않습니다. 견적만 확인해보세요.', unsafe_allow_html=True)
# st.markdown("귀사의 :blue[**목표 달성**]과 :blue[**비용절감**]을 동시에 달성할 수 있을 것이라 확신합니다.;\
# ...             :fire::fire::fire:")

# # st.markdown('<p class="color">아래 질문에 진지하게 응답하기만 하면 됩니다!</p>', unsafe_allow_html=True)
# st.markdown('아래 질문에 :red[진지하게 응답하기만 하면] 됩니다!', unsafe_allow_html=True)

st.divider()

# col1, col2 = st.columns(2)
# st.columns(1)
st.subheader("기업정보")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("기업명*" )
    email = st.text_input("Email*")
    contact_name = st.text_input("담당자명", placeholder='나담당/과장')

with col2:
    contact = st.text_input("담당자 연락처*", placeholder="010-1234-5678")
    product = st.text_input('주요 제품 또는 서비스*', placeholder='ex) 종합건설공사, 가구의 제조, 경영컨설팅 등')
    biz_type = st.radio("업종*", ["제조업", "건설업", "기타"], horizontal=True)
    # st.write('업종:', biz_type)
st.divider()

st.subheader("인증표준정보")
st.caption('견적산출을 위해 정확히 입력해주세요.')
employee =st.number_input("종업원 수*", min_value=1, format='%d', step=1, placeholder='1인 기업은 1명으로 입력하세요.')

# 표준 이름과 식별자 매핑
standards_mapping = {
    'ISO9001': 'qms',
    'ISO14001': 'ems',
    'ISO45001': 'ohsms',
    'ISO22716': 'cms'
}
# 인증표준 선택 위젯
selected_standards = st.multiselect(
    '인증표준*',
    options=list(standards_mapping.keys()),  # 사용자에게 보여질 옵션
    default=['ISO9001', 'ISO14001']  # 초기 선택 옵션 설정
)

# 선택된 표준의 식별자 추출
standards = [standards_mapping[standard] for standard in selected_standards]
# st.write('선택하신 표준:', standards)

audit_type_options = {
    "최초": "initial",
    "사후": "surveillance",
    "갱신": "renewal"
}
audit_type_label = st.radio("심사유형*", list(audit_type_options.keys()), horizontal=True)
audit_type = audit_type_options[audit_type_label]
locale = st.radio("지역*", ["서울/경기", "충청", "강원", "경북", "경남", "전북", "전남", "제주", "베트남", "캄보디아", "인도네시아", "필리핀"], horizontal=True)

st.divider()
st.subheader("선택정보")
st.caption('보다 빠르고 편리하게 인증을 취득하세요.')
# default_support = st.checkbox("심사만 진행(기본)", value=True)
# documents_support = st.checkbox("시스템 문서 준비 포함 (+ 50,000원)")
# nc_support = st.checkbox("부적합 시정 조치 대응 포함 (+ 50,000원)") 
all_support = st.checkbox("시스템 구축 지도/자문 (+ 100,000원)")
if all_support:
    st.caption(" ** 시스템 구축 지도/자문은 시스템 문서 준비, 심사 대응(요청 시), 부적합 시정 조치 대응을 포함하여 인증서 발행 시까지 모든 지원을 포함합니다.")

# if all_support:
#     documents_support = False
#     nc_support = False
#     response_support = False
    # st.warning('인증보장 패키지는 시스템 문서 준비와 부적합 시정 조치 대응을 포함합니다.')

documents_support = st.checkbox("시스템 문서 지원 (+ 50,000원)")
response_support = st.checkbox("심사 대응 지원 (+ 100,000원)")
internal_auditor = st.checkbox("내부심사원 교육  (+ 150,000원)")

# st.write('name:', name, 'email:', email, 'biz_type:', biz_type, 'contactor:', contactor, 'product:', product)
# st.write('employee:', employee, 'standards:', standards, 'audit_type:', audit_type, 'locale:', locale)
# st.write('system_level:', system_level, 'system_prepare:', system_prepare, 'system_goal:', system_goal)


# JSON 파일 로드함수
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("표준 정보 파일을 찾을 수 없습니다. 관리자에게 문의하세요.")
        return {}


# 해당조건에 맞는 md추출 함수
def find_md(standards, audit_type, employee):
    json_data = load_json('standard.json')
    total_md = 0
    risk_level = 'medium' # 항상 medium리스크 레벨을 사용
    
    for standard in standards:
        standard_data = json_data.get(standard, {})
        if not standard_data:
            print(f"경고: {standard}에 대한 데이터가 없습니다.")
            continue # 해당 표준이 없으면 다음 표준으로 넘어감
        
        # print(f"{standard} 표준 처리 중...")
        
        # 종업원 수에 따라 적절한 범위 찾기
        found = False  # 범위 찾았는지 여부 확인용
        for range_key in standard_data.keys():
            low, high = map(int, range_key.split('-'))
            # print(f"범위 확인: {low} - {high}")
            
            if low <= employee <= high:
                found = True
                md_value = standard_data[range_key][risk_level][audit_type]
                total_md += md_value
                # print(f"적용 범위: {low}-{high}, md: {md_value}, 현재 총 md: {total_md}")
                break # 해당 범위에 대한 심사일수를 찾으면 더 이상의 범위는 확인하지 않음.
            
        if not found:
            print(f"경고: 종업원 수 {employee}명에 대한 범위가 없습니다.")
    return total_md


# # JSON 파일 로드
# json_data = load_json('standard.json')

# 총 MD 계산
total_md = find_md(standards, audit_type, employee)
# st.write('total_md:', total_md)

# 견적산출함수
def calculate_quote(standards, audit_type, employee ):
    
    # # json_data 불러오기
    # json_data = load_json('standard.json')
    
    # 총 MD 계산
    total_md = find_md(standards, audit_type, employee)
    print(f"계산된 총 심사일수(md): {total_md}")
    
    # 기본 MD 요율
    base_day_rate = 600000 # 1일당 50만원
    
    # 관리수준에 따라 요율 적용. 50인이하 일때는 
    count_standards = len(standards)
    try:
        if employee < 50:
            if count_standards == 1:
                if audit_type == 'initial':
                    estimated_quote = 600000
                    return estimated_quote
                elif audit_type == 'surveillance':
                    estimated_quote = 500000
                    return estimated_quote
                else:
                    estimated_quote = 600000
                    return estimated_quote
            elif count_standards == 2:
                if audit_type == 'initial':
                    estimated_quote = 1200000
                    return estimated_quote
                elif audit_type == 'surveillance':
                    estimated_quote = 1000000
                    return estimated_quote
                else:
                    estimated_quote = 1200000
                    return estimated_quote
            elif count_standards == 3:
                if audit_type == 'initial':
                    estimated_quote = 1800000
                    return estimated_quote
                elif audit_type == 'surveillance':
                    estimated_quote = 1500000
                    return estimated_quote
                else:
                    estimated_quote = 1800000
                    return estimated_quote
            else:
                if audit_type == 'initial':
                    estimated_quote = 2400000
                    return estimated_quote
                elif audit_type == 'surveillance':
                    estimated_quote = 2000000
                    return estimated_quote
                else:
                    estimated_quote = 2400000
                    return estimated_quote
        else:
            # 50인 이상 기업들에게 심사비 50%를 할인해주는 정책
            normal_price = total_md * base_day_rate
            return normal_price
    except:
        st.write('견적산출에 실패했습니다. 관리자에게 문의하세요.')
        return 0
        
               
st.divider()
if st.button('견적보기'):
    if not name or not email or not contact or not biz_type or not product or not employee or not standards or not audit_type or not locale:
        st.warning('필수입력 항목을 모두 입력해주세요.', icon="🚨")
        st.stop()
    with st.spinner('기쁜 소식을 준비 중입니다... 잠시만 기다려주세요'):
        time.sleep(3)
        # 견적을 구분하기 위한 고유번호 생성. standards의 첫글자_contact 끝 4자리_년월일_랜덤 2자리 숫자로 구성
        current_time = time.strftime('%H%M')
        first_letter = ''.join([standard[0].upper() for standard in standards if standard])
        quote_id = first_letter+contact[-4:] + '_' + time.strftime('%y%m%d') + '_' + current_time

        # print('견적번호:', quote_id)
        
        if employee < 50:
            result = calculate_quote(standards, audit_type, employee)
            audit_fee = int(result)
            # st.write('심사비 견적:', f"{int(audit_fee):,}원")
            if documents_support:
                audit_fee += 50000
            if internal_auditor:
                audit_fee += 150000
            if response_support:
                audit_fee += 100000
            if all_support:
                audit_fee += 100000
            audit_fee = int(audit_fee)
            # st.write(quote_id, name, email, contact_name, contact, product, biz_type, employee, standards, audit_type, locale, all_support, documents_support, nc_support, response_support, audit_fee)

            insert_quote(quote_id, name, email, contact_name, contact, product, biz_type, employee, standards, audit_type, locale, all_support, documents_support, internal_auditor, response_support, audit_fee)    
            formatted_fee = f"{int(audit_fee):,}원"  # 천 단위로 콤마를 추가하고, 끝에 '원'을 붙입니다.
            st.markdown(f'<p class="big-font">최종 견적: {formatted_fee}</p>', unsafe_allow_html=True) 
            st.write(f"접수코드: **{quote_id}**  **:blue[(접수코드를 꼭 메모해두세요!])")
            if locale in ["베트남", "캄보디아", "인도네시아", "필리핀"]:
                st.markdown(':triangular_flag_on_post: ***해외심사는 원격심사 원칙이며, 방문심사의 경우 항공료 및 숙박비 실비 별도.***', unsafe_allow_html=True)
        else:
            result = calculate_quote(standards, audit_type, employee)
            audit_fee = int(result)
            formatted_audit_fee = f"{int(audit_fee):,}원"
            # st.write('정상가:', formatted_audit_fee)
            # st.markdown(f'<p class="big-font">정상가: {formatted_audit_fee}</p>', unsafe_allow_html=True) 
            discount_fee = audit_fee * 0.5
            # st.write(name, email, contact_name, contact, product, biz_type, employee, standards, audit_type, locale, audit_fee, documents_support, nc_support, response_support, all_support)
            insert_quote(quote_id, name, email, contact_name, contact, product, biz_type, employee, standards, audit_type, locale, all_support, documents_support, internal_auditor, response_support, audit_fee)    
            audit_fee = f"{audit_fee:,}원"
            st.markdown(f'<p class="big-font">최종 견적: {audit_fee}</p>', unsafe_allow_html=True) 
            st.write(':triangular_flag_on_post: 해외심사는 원격심사 원칙이며, 방문심사의 경우 항공료 및 숙박비 실비 별도.')
            st.write('견적번호:', quote_id)
            
    st.success('견적산출이 완료되었습니다! 만족하셨다면 인증심사를 신청해보세요.')
    # HTML과 JavaScript를 사용하여 버튼에 링크 적용
    st.markdown("""
    <a href="https://iso-application.streamlit.app" target="_blank">
        <button style="color: white; background-color: red; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 10px;">
            심사신청하기
        </button>
    </a>
    """, unsafe_allow_html=True)
    st.info('견적에 대한 상담이 필요하시면 인증지원센터(02-2661-8505)로 연락주세요.^^')