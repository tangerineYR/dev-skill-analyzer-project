import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.ticker as mticker
from collections import Counter
import ast  
import platform 
import matplotlib.font_manager as fm 
import numpy as np

# 데이터 정규화 맵
SKILL_NORMALIZATION_MAP = {
    # C/C++ 통일
    'c++': 'C++', 'c / c++': 'C++', 'c/c++': 'C++',
    
    # Python 계열
    'python': 'Python', 'django': 'Django', 'flask': 'Flask', 'fastapi': 'FastAPI',
    
    # Java/Kotlin 계열
    'java': 'Java', 'spring': 'Spring', 'spring boot': 'Spring Boot', 'springboot': 'Spring Boot',
    'jpa': 'JPA', 'kotlin': 'Kotlin',

    # Front-end 계열
    'javascript': 'JavaScript', 'typescript': 'TypeScript', 'react': 'React', 'react.js': 'React',
    'vue.js': 'Vue.js', 'vue': 'Vue.js', 'next.js': 'Next.js', 'node.js': 'Node.js',
    'redux': 'Redux', 'recoil': 'Recoil', 'svelte': 'Svelte',
    
    # DB 계열
    'sql': 'SQL', 'mysql': 'MySQL', 'postgresql': 'PostgreSQL', 'oracle': 'Oracle',
    'redis': 'Redis', 'mongodb': 'MongoDB', 'mariadb': 'MariaDB',
    
    # Cloud/Infra 계열
    'aws': 'AWS', 'gcp': 'GCP', 'azure': 'Azure', 'docker': 'Docker', 'kubernetes': 'Kubernetes',
    'git': 'Git', 'github': 'Git',
    
    # Data Science 계열
    'r': 'R', 'pandas': 'Pandas', 'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch',
    'scikit-learn': 'Scikit-learn', 'keras': 'Keras', 'tableau': 'Tableau', 'power bi': 'Power BI',
}

# 폰트 설정
def set_korean_font():
    os_name = platform.system()
    if os_name == 'Windows':
        font_name = 'Malgun Gothic'
    elif os_name == 'Darwin': # macOS
        font_name = 'AppleGothic'
    else: # Linux
        font_name = 'NanumGothic' 
    
    try:
        plt.rc('font', family=font_name)
        plt.rcParams['axes.unicode_minus'] = False
        print(f"폰트가 '{font_name}'(으)로 설정되었습니다.")
    except Exception as e:
        print(f"폰트 설정 오류: {e}.")

# 1. 데이터 불러오기 및 정규화
def normalize_skills(skill_list):
    normalized_set = set() 
    for skill in skill_list:
        skill_low = skill.lower().strip() 
        standard_skill = SKILL_NORMALIZATION_MAP.get(skill_low)
        if standard_skill:
            normalized_set.add(standard_skill)
    return list(normalized_set)

def load_and_clean_data(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"[오류] '{csv_file}' 파일을 찾을 수 없습니다.")
        return None
    
    def safe_literal_eval(s):
        try: return ast.literal_eval(s)
        except: return []
            
    df['skills_raw'] = df['skills'].apply(safe_literal_eval)
    df['skills'] = df['skills_raw'].apply(normalize_skills) 
    print("데이터 로딩 및 정규화 완료:")
    print(df['job_role'].value_counts())
    return df

# 2. 직무별 기술 스택 분석
def analyze_skill_frequency(df, top_n=20):
    job_roles = df['job_role'].unique()
    all_skill_data = {}
    for role in job_roles:
        role_df = df[df['job_role'] == role]
        total_jobs_for_role = len(role_df)
        if total_jobs_for_role == 0: continue
        all_skills_list = [skill for sublist in role_df['skills'] for skill in sublist]
        skill_counts = Counter(all_skills_list)
        top_skills_df = pd.DataFrame(skill_counts.most_common(top_n), columns=['Skill', 'Count'])
        top_skills_df['Percentage'] = (top_skills_df['Count'] / total_jobs_for_role) * 100
        # 막대그래프를 위해 역순 정렬 (맨 위가 1위가 되도록)
        all_skill_data[role] = top_skills_df.sort_values(by='Percentage', ascending=True)
    return all_skill_data

# 3. 시각화 1: 직무별 공고 수(시장 크기) 비교 (막대 그래프)
def plot_job_counts(df, filename='graph_job_role_counts.png'):
    print("직무별 공고 수 시각화 중...")
    
    job_counts = df['job_role'].value_counts().sort_values(ascending=True) # 오름차순 정렬
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Sequential Colormap
    cmap = cm.get_cmap('viridis')
    colors = cmap(np.linspace(0.4, 0.8, len(job_counts)))
    
    bars = ax.barh(job_counts.index, job_counts.values, color=colors)
    
    # 레이블 및 제목 설정
    ax.set_title("직무별 신입 채용 공고 수 비교 (시장 규모)", fontsize=16)
    ax.set_xlabel("수집된 공고 수 (N)", fontsize=12)
    ax.set_ylabel("직무 (Job Roles)", fontsize=12)
    
    # 축 서식 설정 (콤마)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    
    # 그리드 추가
    ax.grid(color='gray', linewidth=0.2, axis='x', linestyle='--')
    
    # 막대 위에 숫자 표시
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, # 막대 오른쪽에
                bar.get_y() + bar.get_height()/2, # 막대 중앙 높이에
                f'{width}건', # 표시할 텍스트
                va='center', 
                ha='left')
    
    plt.tight_layout()
    plt.savefig(filename)
    print(f"'{filename}' (Matplotlib) 그래프 저장 완료.")

# 4. 시각화 2: 직무별 요구 기술 topN (막대 그래프)
def plot_top_skills(skill_data, filename_prefix='graph_top_skills'):
    for role, data in skill_data.items():
        if data.empty:
            print(f"[{role}] 직무에 대한 데이터가 없어 막대 그래프를 건너뜁니다.")
            continue
            
        fig, ax = plt.subplots(figsize=(12, 10))
        
        skills = data['Skill']
        percentages = data['Percentage']
        
        # Colormap 설정
        cmap = cm.get_cmap('viridis')
        # 0.2 ~ 0.9 범위의 색상을 사용 (너무 연하거나 진한 색 제외)
        colors = cmap(np.linspace(0.2, 0.9, len(percentages)))
        
        # 가로 막대그래프(barh) 생성
        ax.barh(skills, percentages, color=colors)
        
        # 레이블 및 제목 설정
        total_n = int(round((data['Count'] / (data['Percentage'] / 100)).mean()))
        ax.set_title(f"'{role}' 직무 요구 기술 Top {len(data)} (N={total_n})", fontsize=16)
        ax.set_xlabel("공고 포함 비율 (%)", fontsize=12)
        ax.set_ylabel("기술 스택", fontsize=12)
        
        # 축 서식 설정
        ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=100.0))
        
        # 가독성을 위한 그리드 추가
        ax.grid(color='gray', linewidth=0.2, axis='x', linestyle='--')
        
        # 레이아웃 최적화
        plt.tight_layout()
        
        filename = f"{filename_prefix}_{role.replace(' ', '_')}.png"
        plt.savefig(filename)
        print(f"'{filename}' (Matplotlib) 그래프 저장 완료.")
 

# 5. 시각화 3: 직무 간 기술 스택 비교 히트맵
def plot_heatmap_comparison(df, skill_data, top_n=15, filename='graph_skill_heatmap.png'):
    all_top_skills = set()
    for data in skill_data.values():
        all_top_skills.update(data.head(top_n)['Skill'])
    
    all_top_skills = sorted(list(all_top_skills))
    
    heatmap_data = {}
    job_roles = df['job_role'].unique()
    
    for role in job_roles:
        role_df = df[df['job_role'] == role]
        total_jobs_for_role = len(role_df)
        if total_jobs_for_role == 0:
            continue
        
        all_skills_list = [skill for sublist in role_df['skills'] for skill in sublist]
        skill_counts = Counter(all_skills_list)
        
        skill_percentages = {}
        for skill in all_top_skills:
            percentage = (skill_counts.get(skill, 0) / total_jobs_for_role) * 100
            skill_percentages[skill] = percentage
            
        heatmap_data[role] = skill_percentages
    
    heatmap_df = pd.DataFrame(heatmap_data).T 
    
    plt.figure(figsize=(20, 10))

    sns.heatmap(
        heatmap_df, 
        annot=True,     
        fmt=".1f",      
        cmap='rocket_r', 
        linewidths=.5   
    )
    plt.title("직무별 주요 기술 스택 요구 비율(%) 비교", fontsize=18)
    plt.xlabel("기술 스택 (Skills)", fontsize=14)
    plt.ylabel("직무 (Job Roles)", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.savefig(filename)
    print(f"'{filename}' 히트맵 저장 완료.")

# 6. 메인 실행 함수
def main():
    INPUT_CSV_FILE = 'wanted_jobs.csv' 
    
    set_korean_font() 
    df = load_and_clean_data(INPUT_CSV_FILE)
    
    if df is not None:
        # 직무별 공고 수(시장 크기) 비교 막대 그래프 생성
        plot_job_counts(df)
        
        # 기술 스택 빈도 분석
        skill_data = analyze_skill_frequency(df, top_n=20)
        
        # 막대 그래프 생성
        plot_top_skills(skill_data)
        
        # 비교 히트맵 생성
        plot_heatmap_comparison(df, skill_data)

        # 모든 플롯이 생성된 후, 마지막에 show() 호출
        print("\n모든 시각화가 파일로 저장되었습니다. 이제 화면에 표시합니다.")
        plt.show()

if __name__ == "__main__":
    main()