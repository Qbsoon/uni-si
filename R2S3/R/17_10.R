v<-1:22
v
matrix(v, byrow = TRUE, ncol = 2)
matrix(v, byrow = TRUE, nrow = 2)

goog <- c(450,451,452,445,468)
micro <- c(230,231,232,233,220)
akcje <- c(goog, micro)
akcje

m.akcje <- matrix(akcje, byrow = TRUE, nrow = 2)
m.akcje

dni <- c('PN', 'WT', 'SR', 'CZW', 'PT')
firmy <- c('Google', 'Microsoft')
colnames(m.akcje) <- dni
rownames(m.akcje) <- firmy
m.akcje

m <- matrix(1:25, byrow = T, nrow = 5)
m

m/2
m**2
2/m
2**m
2/m > m
m*5 > m**2
m[m > 15]
m+m
m/2+2/m

m%*%m

colSums(m.akcje)
rowSums(m.akcje)

colMeans(m.akcje)
rowMeans(m.akcje)

Meta <- c(111,112,113,120,145)

tech.akcje <- rbind(m.akcje, Meta)
tech.akcje

avg <- rowMeans(tech.akcje)
avg

tech.akcje <- cbind(tech.akcje, avg)
tech.akcje

m <- matrix(1:40, byrow = T, nrow = 8)
m

m[3,2]
m[,2:5]

ani <- c('p', 'k', 'p', 'k', 'k')
factor(ani)

  temp <- c('goraca','srednia','zimna','graca','zimna','zimna','goraca','zimna','srednia')
  temp
  
  f.temp <- factor(temp, ordered = T, levels = c('zimna','srednia','goraca'))
  f.temp

a <- c(1,2,3)
b <- c(4,5,6)
m <- matrix(c(a,b), byrow= T, nrow = 2)
m
c <- c(7,8,9)
m2 <- matrix(c(a,b,c), byrow = T, nrow = 3)
m2

m3 <- matrix(1:25, nrow=5)
m3

m3[3:4, 4:5]

rowSums(m3)
colSums(m3)
sum(m3)

m4 <- matrix(runif(20, 1, 100), nrow=4)
m4

USPersonalExpenditure

state.x77
data()

VADeaths
Titanic

head(state.x77)
tail(state.x77)
