# dev-skill-analyzer-project

신입 개발자 직무별 요구 기술 분석 프로젝트
데이터시각화(001) 기말 프로젝트 (데이터사이언스학과 23011816 황유리)

본 프로젝트는 실제 채용 공고 데이터를 수집, 분석, 시각화하여 신입 개발자 지망생의 합리적인 진로 선택의 기준을 제시하는 것을 목표로 합니다.

1. 프로젝트 개요: 문제 인식

데이터사이언스학을 전공하며 데이터를 통해 문제를 해결하는 방법을 배우고 있지만, 정작 우리 자신의 진로 문제 앞에서는 데이터가 아닌 막연한 소문에 의존하고 있음을 발견했습니다. 백엔드, 프론트엔드 등 각 개발 직무가 실제 기업에서 어떤 기술 스택을 요구하는지에 대한 객관적인 정보가 부족하기 때문입니다.

수백 개의 채용 공고는 그저 거대한 텍스트의 나열일 뿐, 그 안에서 직무별 차이를 한눈에 파악하기란 불가능합니다. 이처럼 복잡한 데이터를 직관적으로 비교하고 이해할 수 있는 유일한 방법이 바로 **‘데이터 시각화’**입니다.

본 프로젝트는 흩어진 채용 정보를 유의미한 시각적 자료로 재구성하여, 데이터에 기반한 합리적인 진로 선택의 기준을 제시합니다.

2. 분석 데이터 및 방법론

가. 데이터 소스

플랫폼: 국내 주요 IT 채용 플랫폼 중 하나인 ‘원티드(Wanted)’ (country=kr 필터 적용)

수집 대상: '신입(경력 1년 미만)' 필터를 적용한 3개 직무

서버 개발자 ('개발' 직군)

프론트엔드 개발자 ('개발' 직군)

데이터 사이언티스트 ('개발' 직군)

나. 파일 설명

scraper.py: Selenium과 BeautifulSoup을 활용해 원티드에서 3개 직무의 상세 공고 페이지를 스크레이핑합니다. '기술 스택 태그'와 '본문 텍스트'를 모두 검색하는 하이브리드 방식을 사용하며, "R&D"와 같은 노이즈를 re(정규표현식)로 필터링합니다.

visualizer_lecture_aligned.py: wanted_jobs_final.csv를 pandas로 로드합니다. 'C / C++' -> 'C++'와 같이 표기를 통일하는 **정규화(Normalization)**를 수행한 뒤, Matplotlib과 Seaborn을 사용해 2가지 핵심 차트(막대그래프, 히트맵)를 생성 및 저장합니다.

wanted_jobs_final.csv: scraper.py를 통해 수집된 최종 원본 데이터(CSV)입니다.

*.png: visualizer_lecture_aligned.py 실행 시 생성되는 최종 시각화 결과 이미지 파일입니다.

다. 프로젝트 파이프라인

데이터 수집 (Scraping): scraper.py

Python의 Selenium과 BeautifulSoup을 활용하여 각 직무별 채용 공고의 상세 페이지에 동적으로 접근합니다.

공고 본문 텍스트(DESCRIPTION_CLASS)와 기술 스택 태그(DETAIL_SKILL_CLASS)를 하이브리드 방식으로 수집하여 누락되는 데이터를 최소화했습니다.

"R&D"의 'R'과 같은 노이즈를 re(정규표현식)을 이용해 제거했습니다.

데이터 정제 (Cleaning): visualizer_lecture_aligned.py

pandas를 이용해 수집된 wanted_jobs_final.csv 파일을 로드합니다.

'C / C++' -> 'C++', 'github' -> 'Git' 등, 의미는 같지만 표기가 다른 기술 스택들을 **SKILL_NORMALIZATION_MAP**을 통해 표준화했습니다.

데이터 시각화 (Visualization): visualizer_lecture_aligned.py

Matplotlib과 Seaborn을 활용하여 분석 결과를 시각화했습니다.

강의 교안(dv.pdf)의 원칙을 준수하여, 순수 Matplotlib (ax.barh) 방식과 **Sequential Colormap (viridis, rocket_r)**을 적용했습니다.

3. 시각화 결과 및 분석

분석 결과 요약: 수집된 유효 공고 수(N)는 서버 개발자(N=44), 프론트엔드 개발자(N=46), 데이터 사이언티스트(N=29)로, 신입 DS 시장이 상대적으로 작음을 확인했습니다.

분석 1: 직무별 핵심 요구 기술 (가로 막대그래프)

각 직무의 '필수 기술'을 파악하기 위해 상위 기술 스택의 요구 비율을 시각화했습니다. (N=총 공고 수)

서버 개발자 (N=44)

프론트엔드 개발자 (N=46)

데이터 사이언티스트 (N=29)







**‘Java/AWS’**가 핵심. Python, SQL, Spring이 뒤를 이음.

**‘React/TypeScript’**가 압도적. Next.js, JavaScript가 주요 기술.

**‘Python/PyTorch’**가 핵심. TensorFlow, SQL이 뒤를 이음.

→ 발견한 점: 각 직무의 핵심 요구 기술이 **‘Java/AWS(서버)’, ‘React/TypeScript(프론트)’, ‘Python/PyTorch(DS)’**라는 명확한 '기술 조합'으로 구분됨을 확인했습니다.

분석 2: 직무 간 기술 스택 비교 (히트맵)

세 직무가 공유하는 기술(공통 교양)과 각 직무에 특화된 기술(전공 필수)을 비교하기 위해 히트맵을 생성했습니다.

공유 기반 기술 (Shared Skill): Git은 세 직무 모두에서 11~24%의 비율을 보이며, 직군 공통의 기본 소양임을 확인했습니다. SQL 역시 DS(20.7%)와 서버(22.7%) 직군에서 중요하게 요구되었습니다.

직무 특화 기술 (Specialized Skill):

React, TypeScript는 프론트엔드 개발자 행만 압도적으로 진한 색(높은 비율)을 보였습니다.

PyTorch, TensorFlow는 데이터 사이언티스트 행만 진한 색을 보였습니다.

Java, Spring은 서버 개발자 행이 가장 진한 색을 기록했습니다.

→ 발견한 점: Git과 같은 **'공유 기술'**과, 각 직무의 전문성을 정의하는 **'특화 기술'**이 명확히 분리됨을 발견했습니다. 이는 '문제 인식'에서 제기했던 ‘객관적인 정보 부재’ 문제를 해결하고, 데이터사이언스 전공생으로서 자신의 커리어맵을 합리적으로 설계하는 데 결정적인 근거 자료를 제공합니다.

4. 실행 방법 (How to Run)

본 프로젝트의 코드를 직접 실행하고 결과를 재현하는 방법입니다.

요구 사항 (Requirements)

본 스크립트를 실행하기 위해 다음 라이브러리들이 필요합니다:

python >= 3.10
pandas
selenium
beautifulsoup4
webdriver-manager
matplotlib
seaborn
