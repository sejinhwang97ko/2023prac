# sav 파일 로드
install.packages("foreign")
install.packages("readxl")

library(foreign)
library(readxl)

welfare = read.spss("csv/csv/Koweps_hpc10_2015_beta1.sav", to.data.frame=T)
View(welfare)

welfare = rename(welfare,
                 gender = h10_g3,
                 birth = h10_g4,
                 marriage = h10_g10,
                 religion = h10_g11,
                 income = p1002_8aq1,
                 code_job = h10_eco9,
                 code_region = h10_reg7)
welfare %>% 
  select(gender, birth, marriage, religion, income, code_job, code_region) -> welfare_copy


table(welfare_copy$gender)

ifelse(welfare_copy$gender == 1, 'male', 'female') -> welfare_copy$gender

table(welfare_copy$gender)
View(welfare_copy)
# 성별을 기준으로 월급이 평균이 어떻게 되는가?
# income이 0이면 수익이 존재하지 않는다. -> 결측치
# income이 9999면 극단치로 생각해서 결측치로 변경
ifelse(welfare_copy$income == 0 | welfare_copy$income == 9999, 
       NA, 
       welfare_copy$income) -> welfare_copy$income
# 결측치를 확인
table(is.na(welfare_copy$income))

# income의 결측치를 제외하고 성별로 그룹화
# income 평균을 출력
# 시각화

welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(gender) %>% 
  summarise(mean_income = mean(income)) -> gender_income

gender_income
  
# 데이터의 시각화
ggplot(data = gender_income,
       aes(x= gender, y = mean_income))+ geom_col()

welfare_copy %>% 
  filter(!is.na(income)) #%>% 
  mutate(age = 2015 - birth + 1) %>% 
  group_by(age) %>% 
  summarise(income_mean = mean(income)) -> age_income

table(is.na(welfare_copy$age))
table(is.na(welfare_copy$income))

# 시각화
ggplot(data = age_income,
       aes(x= age, y = income_mean))+ geom_line()

age_income %>% arrange(-income_mean) %>% head(5)

# 연령대를 추가
# ageg 나이가 30미만이면 'young'
# 30 이상 60 미만이면 'middle'
# 60 이상이면 'old'
# 연령대별 월급의 평균이 어떻게 되는가?
# 시각화(막대그래프)
View(welfare_copy)
ifelse(welfare_copy$age < 30, 'young',
       ifelse(welfare_copy$age < 60, 'middle', 'old')) ->welfare_copy$ageg

welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg) %>% 
  summarise(mean_income = mean(income)) -> ageg_mean


ggplot(data = ageg_mean,
       aes(x= ageg, y = mean_income))+ geom_col() +
  scale_x_discrete(limits = c('young', 'middle', 'old'))

# 연령대, 성별 월급 평균
welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg, gender) %>% 
  summarise(income_mean = mean(income)) -> ageg_gender_income

ggplot(data = ageg_gender_income,
       aes(x= ageg, y= income_mean, fill=gender)) +
  geom_col(position = 'dodge') +
  scale_x_discrete(limits = c('young', 'middle', 'old'))

# 나이, 성별 월급 평균을 비교
welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(age, gender) %>% 
  summarise(income_mean = mean(income))-> age_gender_income

ggplot(data = age_gender_income, 
       aes(x=age, y= income_mean, color = gender)) + 
  geom_line()

## 직업별로 평균 월급이 어떻게 되는가?
welfare_copy$code_job

list_job =read_excel("csv/csv/Koweps_Codebook.xlsx", sheet=2, col_names= T)
left_join(welfare_copy,list_job, by='code_job') -> welfare_copy
View(welfare_copy) 

## 직업별 평균 월급
## 직업이 결측치이고 월급이 결측치인 경우 제외
## 직업 기준으로 그룹화
## 월급의 평균 값
welfare %>% 
  select(gender, birth, marriage, religion, income, code_job, code_region) -> welfare_copy

welfare_copy$code_job

list_job =read_excel("csv/csv/Koweps_Codebook.xlsx", sheet=2, col_names= T)
left_join(welfare_copy,list_job, by='code_job') -> welfare_copy
View(welfare_copy) 

welfare_copy %>% 
  filter(!is.na(job) & !is.na(income)) %>% 
  group_by(job) %>% 
  summarise(mean_income = mean(income)) -> job_mean

job_mean %>% arrange(-mean_income) -> job_mean
# 평균 월급이 높은 상위 직업군 10개를 시각화
# 낮은 하위 직업군 10개를 시각화
ggplot(data = head(job_mean,10), 
       aes(x=job, y= mean_income)) + 
  geom_col() #x값 기준으로 정렬이 바뀜

ggplot(data = head(job_mean,10), 
       aes(x=reorder(job, mean_income), y= mean_income)) + 
  geom_col() +
  coord_flip() # 눕히기
  

ggplot(data = tail(job_mean,10), 
       aes(x=reorder(job, mean_income), y= mean_income)) + 
  geom_col() +
  coord_flip() # 눕히기

# 성별 직업의 빈도수를 체크하여 상위 10개를 출력

ifelse(welfare_copy$gender == 1, 'male', 'female') -> welfare_copy$gender
welfare_copy %>% 
  filter(!is.na(job) & gender == 'male') %>% 
  group_by(job) %>% 
  summarise(count = n()) %>% 
  arrange(-count) %>% 
  head(10) -> male_top10
male_top10

welfare_copy %>% 
  filter(!is.na(job) & gender == 'female') %>% 
  group_by(job) %>% 
  summarise(count = n()) %>% 
  arrange(-count) %>% 
  head(10) -> female_top10
female_top10

### marrriage : 3 인 경우 이론
# 새로운 파생변수 group_marriage 생성하여
# marriage가 3이면 divorce
# 1이면 marriage

welfare_copy %>% 
  mutate(age = 2015 - birth + 1) %>% 
  mutate(ageg = ifelse(age < 30, 'young',
                       ifelse(age < 60, 'middle', 'old'))) -> welfare_copy

ifelse(welfare_copy$marriage == 3, 'divorce', 
       ifelse(welfare_copy$marriage == 1, 'marriage', NA)) -> welfare_copy$group_marriage

# 연령대 별 이혼율 출력 시각화
View(welfare_copy)

welfare_copy %>% 
  filter(!is.na(group_marriage)) %>% 
  group_by(ageg, group_marriage) %>% 
  summarise(count = n()) %>% 
  mutate(total_count = sum(count)) %>% 
  mutate(pct = count/total_count*100)
  