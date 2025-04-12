import streamlit as st
import pandas as pd
import utils
import os
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="YouTube Prediction Result",
    layout="wide"
)
# 앱 제목
st.title("YouTube Prediction Result")
st.write("인구 그룹(성별 및 연령대)에 따라 예측된 YouTube 동영상을 보여줍니다.")
# 데이터 로드
@st.cache_data
def get_data():
    # 현재 디렉토리 기준으로 data 폴더 내의 youtubes.csv 파일 경로 구성
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "youtubes.csv")
    return utils.load_data(data_path)

df = get_data()

if df.empty:
    st.error("데이터 파일을 불러올 수 없습니다. 'data/youtubes.csv' 파일이 존재하는지 확인해주세요.")
    st.stop()

# 사이드바에 필터 추가
st.sidebar.header("필터 옵션")

# 연령대 선택 옵션
age_options = {
    "": None,  # 선택 안함
    "0-9세": "0_9",
    "10대": "10s",
    "20대": "20s",
    "30대": "30s",
    "40대": "40s",
    "50대 이상": "50plus"
}
selected_age = st.sidebar.selectbox("연령대 선택", options=list(age_options.keys()))
age_group = age_options[selected_age]

# 성별 선택 옵션
gender_options = {
    "": None,  # 선택 안함
    "남성": "male",
    "여성": "female"
}
selected_gender = st.sidebar.selectbox("성별 선택", options=list(gender_options.keys()))
gender = gender_options[selected_gender]

# 필터 적용 버튼
if st.sidebar.button("적용"):
    # 선택한 필터에 맞게 동영상 필터링
    filtered_videos = utils.filter_videos(df, age_group, gender)
    
    # 필터링 결과가 없는 경우
    if filtered_videos.empty:
        st.warning("선택한 조건에 맞는 동영상이 없습니다.")
    else:
        # 필터링 결과 표시
        st.subheader("선택한 조건에 맞는 상위 10개 동영상:")
        
        # 동영상 표시를 위한 그리드 생성
        cols = st.columns(2)  # 한 행에 2개의 동영상 배치
        
        for i, (_, row) in enumerate(filtered_videos.iterrows()):
            # 각 동영상에 대한 컬럼 선택
            col = cols[i % 2]
            
            with col:
                # 동영상 제목 또는 ID
                st.write(f"**동영상 {i+1}** (점수: {row['score']:.2f})")
                
                # YouTube 임베드 코드 생성 및 표시
                video_id = row['video_id']
                embed_html = utils.get_youtube_embed_html(video_id)
                st.markdown(embed_html, unsafe_allow_html=True)
                
                # 인구통계 점수 표시
                st.write("**인구통계 점수**")
                
                demographic_data = []
                
                # 연령대 점수
                age_display_map = {
                    '0_9': '0-9세', '10s': '10대', '20s': '20대', 
                    '30s': '30대', '40s': '40대', '50plus': '50대 이상'
                }
                
                for col in row.index:
                    if col.startswith('age_'):
                        age_name = col.replace('age_', '')
                        demographic_data.append({
                            '구분': '연령대',
                            '항목': age_display_map.get(age_name, age_name),
                            '점수': f'{row[col]:.2f}'
                        })
                    elif col.startswith('gender_'):
                        gender_name = col.replace('gender_', '')
                        demographic_data.append({
                            '구분': '성별',
                            '항목': '남성' if gender_name == 'male' else '여성',
                            '점수': f'{row[col]:.2f}'
                        })
                
                st.table(pd.DataFrame(demographic_data))
                st.write("---")
else:
    # 처음 페이지 로드 시 안내 메시지 표시
    st.info("👈 사이드바에서 필터 옵션을 선택하고 '적용' 버튼을 클릭하세요.")
    
    # 데이터 미리보기 표시
    st.subheader("데이터 미리보기:")
    st.dataframe(df.head())