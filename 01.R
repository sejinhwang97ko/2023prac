# 벡터데이터를 생성
a = c(1,2,3,4,5)
a
1:5
1:5 -> b
b

a = c(1, "test")
a # "1"    "test" # 1이 문자열로

# 행렬
d = array(1:20, dim=c(4,5))
d

e = matrix(1:20, nrow=2)
e

# 리스트 형태(python에서는 dict 형태와 흡사)
f = list(name = 'test', age = 20, phon = '01012345678')
f
f['name']
f['age']

df = data.frame(name = c('test', 'test2'),
                age = c(20, 30),
                phone = c('01012345678', '01098765432'))
df

# 조건문 (if문)
a <- 10
if(a> 15){
  print('a는 15보다 크다')
}else{
  print('a는 15보다 작거나 같다')
}

if(a> 15){
  print('a는 15보다 크다')
}else if (a==15){
  print('a는 15와 같다')
  }else{
  print('a는 15보다 작다')
  }

# which문 (python에서 find() 흡사)
name =c("test", "test2", "test3")
which(name == 'test2') # 2
which(name != 'test2') # 1 3
which(name == 'test5') # integer(0)

# 함수

