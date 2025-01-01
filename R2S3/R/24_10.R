dni <- c('PN', 'WT', "SR", "CZW", "PT")
temp <- c(22.2,21,23,24.3,25)
deszcz <- c(T,T,F,F,T)

df <- data.frame(dni, temp, deszcz)
df

summary(df)

df[1,]
df[,1]
df[1:2,]
df[, 'dni']
df[1:5,1:2]
df[1:5, c('dni', 'temp')]

df$dni

subset(df, subset = deszcz == TRUE)
subset(df, subset = temp > 23)
sort.temp <- order(df[, 'temp'])
sort.temp

df[sort.temp,]

desc.temp <- order(-df[,'temp'])
desc.temp

df[desc.temp,]

pusta <- data.frame()

c1 <- 1:10
c1

letters
c2 <- letters[1:10]
c2

ll <- data.frame(liczby = c1, litery = c2)
ll

nrow(ll)
ncol(ll)

colnames(ll)

str(ll)

summary(ll)

ll[[5,2]]
ll[[5, 'litery']]

ll[[2, 'liczby']] <-99
ll

ll[1,]

ll$liczby
ll[,'liczby']
ll[,1]
ll[['liczby']]

ll['liczby']

mtcars

head(mtcars[c('mpg', 'cyl', 'gear')])

ll2 <- data.frame(liczby = 2000, litery = 'abc')
ll2


ll <- rbind(ll, ll2)
ll

ll$nliczby <- 2 * ll$liczby
ll

colnames(ll)<-c('Liczby', "Litery", "nLiczby")
ll

colnames(ll)[1] <- 'LICZBY'
ll

head(ll, 4)

ll[-2,]

mtcars[mtcars$mpg>20,]
mtcars[mtcars$mpg>20 & mtcars$cyl==6,]

subset(mtcars,mpg>20 & cyl==6)
subset(mtcars,mpg>20 & cyl==6,c('mpg', 'cyl'))

any(is.na(ll))

names <- c('Szymon', 'Franek', 'Anna')
age <- c(22,25,26)
height <- c(180, 170, 160)
genda <- c('M', 'M', 'K')

tbl <- data.frame(row.names=names, age, height, genda)
tbl


cars = mtcars

head(cars, 6)
tail(cars, 6)
cars[1:3,]
