library(tidyverse)

mtcars

firma <- c(1,1,1,2,2,2,3,3,3)
rok <- c(1998,1999,2000,1998,1999,2000,1998,1999,2000)
q1 <- runif(9, min = 10000, max = 250000)
q2 <- runif(9, min = 10000, max = 250000)
q3 <- runif(9, min = 10000, max = 250000)
q4 <- runif(9, min = 10000, max = 250000)
df <- data.frame(Firma = firma, Rok = rok, Q1 = q1, Q2 = q2, Q3 = q3, Q4 = q4)
df

pivot_longer(df, cols= starts_with("Q"), names_to="Quater", values_to= "Income")

bb = billboard

pivot_longer(bb, cols = starts_with("wk"), names_to = "week", values_to= "ranking", values_drop_na = T)

long <- pivot_longer(bb, cols=starts_with('wk'), names_to = "week", values_to='ranking')

pivot_wider(long, names_from=week, values_from=ranking)

df <- data.frame(colu = c(NA, "aRx", "bRy", "cRz"))
df

sd_s <- separate(df, colu, c('a', 'o'), "R")

unite(sd_s, 'colu', c('a', 'o'), sep="R", na.rm=TRUE)

sd_s %>% unite(nowa, a, o, sep='R', na.rm=TRUE) %>% mutate(nowa=na_if(nowa,''))
