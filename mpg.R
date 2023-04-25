library(dplyr)
library(ggplot2)

# 극단치
mpg
View(mpg)

# 극단치를 확인(시각화) minimum, 1분위, 2분위, 3분위, maximum
boxplot(mpg$hwy) # 고속도로 연비
boxplot(mpg$cty) # 도심 연비
# 극단치를 수치로 표현
boxplot(mpg$cty)$stats

mpg = ggplot2::mpg

# 이상치는 26초과이거나 9미만인 경우
# 이상치를 결측치로 변환
# 결측치의 개수를 확인
mpg$cty = ifelse(mpg$cty < 9 | mpg$cty > 26, NA, mpg$cty)
table(is.na(mpg$cty))

# dplyr 패키지를 이용하여 결측치를 제거하고 제조사(manufacturer)별로 그룹화
# 도심연비(cty)의 평균
# 도심연비가 좋은 상위 5개의 제조사를 확인

na.omit(mpg) -> mpg
table(is.na(mpg$cty))
mpg %>% 
  group_by(manufacturer) %>% 
  summarise(mean_cty = mean(cty)) %>% 
  arrange(-mean_cty) %>% 
  head(5)

#mpg %>% 
#  filter(!is.na(cty)) %>% 
#  group_by(manufacturer) %>% 
#  summarise(mean_cty = mean(cty)) %>% 
#  arrange(-mean_cty) %>% 
#  head(5)

mpg = ggplot2::mpg

# total 파생변수 생성
# total은 (cty + hwy)/2
# test 파생변수 생성
# total이 30이상이면 'A',
# 20이상이고 30미만이면 'B',
# 20미만이면 'C'

mpg %>% mutate(total = (cty + hwy)/2) ->mpg
mpg$test = ifelse(mpg$total >= 30, 'A', ifelse(mpg$total >= 20, 'B', 'C'));
table(mpg$test)

qplot(mpg$test)


midwest = ggplot2::midwest
View(midwest)
# 컬럼의 이름을 변경
# popasian 컬럼을 asian, poptotal 컬럼을 total로 변경
# ratio 파생변수 생성 -> 전체 인구수 대비 아시아의 인구수(백분율)
# group 파생변수 생성
# ratio 평균보다 ratio의 값이 크면 'large' 아니면 'small'

rename(midwest, asian = popasian) -> midwest
rename(midwest, total = poptotal) -> midwest
# rename(midwest, asian = popasian, total = poptotal) -> midwest
summary(midwest)
midwest %>% mutate(ratio = asian/total * 100) ->midwest
summary(midwest)

mean_ratio = mean(midwest$ratio)
midwest$group = ifelse(midwest$ratio > mean_ratio, 'large', 'small')
qplot(midwest$group)
table(midwest$group)
