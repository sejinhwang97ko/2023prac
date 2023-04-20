df = read.csv("csv/csv/example.csv")
df

head(df)
tail(df)

View(df)

dim(df)

summary(df)
# 데이터프레임의 정보를 출력
str(df)

library(dplyr)

# 컬럼의 이름 변경
rename(df, '이름' = Name)

df = read.csv("csv/csv/csv_exam.csv")
df

View(df)

# 새로운 파생변수 하나 생성
# 전체 점수의 합계 (total_score)
# 전체 점수의 평균(mean_score)
total_score = df[['math']] + df[['english']] + df[['science']]
data.frame(df,total_score) -> df
df$total_score
mean_score = (total_score)/3
data.frame(df,mean_score) -> df
df

# 평균 점수가 60점 이상이면 pass, 아니면 fail
# res 컬럼을 생성
# ifelse(조건식, 참인 경우의 값, 거짓인 경우의 값)
df$res = ifelse(df$mean_score >= 60, 'pass', 'fail')
df

# 1학년 중에 평균 점수가 가장 높은 사람의 정보를 출력
df2 = df[df$class == 1,]
df2
df3 = df2[order(-df2$mean_score),]
head(df3,1)

