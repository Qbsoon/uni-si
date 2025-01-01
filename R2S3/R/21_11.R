library(ggplot2)
library(tidyverse)

ggplot(mpg, aes(x = displ, y = hwy)) + geom_point() + coord_cartesian(xlim = c(1,4), ylim=c(15,30))

ggplot(mpg, aes(x = displ, y = hwy)) + geom_point() + facet_wrap(~cyl)

ggplot(mpg, aes(x = displ, y = hwy)) + geom_point() + facet_grid(drv~cyl)

mtcars

#z1

ggplot(mtcars, aes(x = wt, y = mpg)) + geom_point(color="steelblue2", size=3) + coord_cartesian(xlim = c(3, 5), ylim = c(15,30))

#z2

ggplot(mtcars, aes(x = drat, y = mpg)) + geom_point(color="lightsalmon2") + facet_wrap(~cyl)
ggplot(mtcars, aes(x = drat, y = mpg)) + geom_point(color="lightsalmon2") + facet_grid(am~cyl)

#Koniec zadań

diamonds

ggplot(diamonds, aes(x = y)) + geom_histogram(binwidth = 0.5)
ggplot(diamonds, aes(x=y)) + geom_histogram(binwidth = 0.5)+coord_cartesian(ylim=c(0,50))

unusual <- diamonds %>% filter(y<3 | y>20) %>% select(price, x, y, z) %>% arrange(y)

unusual

d2 <- diamonds %>% mutate(y = replace(y, y<3 | y>20, NA))
d2 %>% filter(is.na(y)) %>% select(price, y)
