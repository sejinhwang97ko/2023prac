# 결측치에 대한 계산
# 결측치는 연산이 되지 않는다.
# 필터를 걸게되면 무조건 출력
c1 = c(1,2,NA,NA,5)
c2 = c(1,2,3,4,5)
c3 = c(NA, 2, 3, 4, 5)
df = data.frame(c1,c2,c3)
df

# # 결측치를 확인하는 방법
is.na(df)
is.na(df$c1)

#dpylr 패키지를 이용하여 결측치를 제거한 데이터를 확인하는 방법
df %>% filter(!is.na(c1))

na.omit(df)
#결측치를 제외하고 연산
mean(df$c1) #NA
mean(df$c2) #3
mean(df$c3) #NA
mean(df$c1, na.rm = T)

exam = read.csv("csv/csv/csv_exam.csv")
# 결측치로 만들기 
exam[c(5,7), 3] = NA
exam

View(exam)
# 수학 점수의 평균 값 출력
# 결측치인 값을 수학 점수의 평균으로 대체
# ifelse() 함수를 이용하여 결측치에 수학점수의 평균값을 대입
mean(exam$math, na.rm = T) ->mean_math
is.na(exam$math)
ifelse(is.na(exam$math), mean_math, exam$math) ->exam$math
exam
