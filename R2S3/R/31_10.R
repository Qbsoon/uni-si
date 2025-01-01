cars<- mtcars
mean_mpg <- mean(cars[,'mpg'])
mean_mpg
cars
subset(cars, cyl==6)
cars[cars$cyl==6,]

cars[,c('cyl', 'hp', 'gear')]

perf<- cars[,'hp']/cars[,'wt']
perf
cars = data.frame(cars, perf)
cars
cars$perf <- round(cars$hp/cars$wt, 2)
cars

mean_mpg <- mean(cars[cars$wt>2.5 & cars$hp>100, 'mpg'])
mean_mpg
mean(subset(cars, hp>100 & wt>2.5)$mpg)

cars['Hornet Sportabout', 'am']
cars['Hornet Sportabout',]$am

any(!is.na(cars)) & nrow(cars)%%2==0


#Listy

v <- c(1,2,3)
m <- matrix(1:10, nrow=2)
df <- mtcars

class(v)
class(m)
class(df)

list <- list(v, m, df)
list
class(list)

named_list <- list (vector = v, matrix = m, data_frame = df)
named_list
named_list$data_frame$mpg

class(named_list$matrix)

head(flights)

summary(flights)

head(filter(flights, month==11, day==3))
head(flights[flights$month==11 & flights$day==3,])

slice(flights, 1:10)

head(arrange(flights, month, day, desc(arr_time)))

head(select(flights, carrier))

head(rename(flights, rok=year))

distinct(select(flights, carrier))

head(mutate(flights, n_col = arr_delay - dep_delay))$n_col

to_show = (mutate(flights, n_col = arr_delay - dep_delay))
head(select(to_show, n_col))

head(transmute(flights, n_col = arr_delay - dep_delay))

summarize(flights, sr_czas_w_powietrzu = mean(air_time, na.rm = TRUE))

sample_n(flights, 10)
sample_frac(flights, 0.1)

df <- mtcars
wynik <- arrange(sample_n(filter(df, mpg> 20),5),desc(mpg))
wynik

df %>% filter(mpg>20) %>% sample_n(5) %>% arrange(desc(mpg))
flights


filter(cars, mpg>20, cyl>=6)                                                  

arrange(cars, cyl, desc(wt))

select(cars, mpg, hp)

distinct(select(cars, gear))

transmute(cars, perf=hp/wt)

summarize(cars, m_mpg = mean(mpg))

cars %>% filter(cyl==6) %>% summarize(mean(hp))

sample_n(flights[flights$origin=='JFK' & flights$month==1,c('month', 'day', 'arr_time', 'dep_time')], 10)

head(arrange(distinct(select(flights, flight, origin, dest, distance)),desc(distance) ), 10)
