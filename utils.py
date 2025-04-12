import pandas as pd
import numpy as np

def load_data(file_path):
    """
    CSV 파일을 불러오는 함수
    
    Args:
        file_path (str): CSV 파일 경로
        
    Returns:
        pandas.DataFrame: 불러온 데이터
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"데이터 로딩 중 오류 발생: {e}")
        return pd.DataFrame()

def filter_videos(df, age_group=None, gender=None):
    """
    선택된 나이 그룹과 성별에 따라 동영상을 필터링하는 함수
    
    Args:
        df (pandas.DataFrame): 동영상 데이터
        age_group (str, optional): 선택된 나이 그룹. 기본값은 None.
        gender (str, optional): 선택된 성별. 기본값은 None.
        
    Returns:
        pandas.DataFrame: 필터링 및 정렬된 데이터
    """
    if df.empty:
        return df
    
    # 점수 계산 컬럼 초기화
    df['score'] = 0
    
    # 나이 그룹 필터링
    if age_group:
        age_column = f'age_{age_group}'
        if age_column in df.columns:
            df['score'] += df[age_column]
    
    # 성별 필터링
    if gender:
        gender_column = f'gender_{gender}'
        if gender_column in df.columns:
            df['score'] += df[gender_column]
    
    # 점수가 0인 경우 (필터링이 없는 경우) 모든 나이 및 성별 점수의 합으로 계산
    if age_group is None and gender is None:
        age_columns = [col for col in df.columns if col.startswith('age_')]
        gender_columns = [col for col in df.columns if col.startswith('gender_')]
        df['score'] = df[age_columns + gender_columns].sum(axis=1)
    
    # 점수로 정렬하고 상위 10개 반환
    result = df.sort_values(by='score', ascending=False).head(10)
    return result

def get_youtube_embed_html(video_id):
    """
    YouTube 영상 임베드 HTML을 생성하는 함수
    
    Args:
        video_id (str): YouTube 영상 ID
        
    Returns:
        str: YouTube 임베드 HTML 코드
    """
    return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'