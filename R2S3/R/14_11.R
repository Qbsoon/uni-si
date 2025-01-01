library(ggplot2)
library(palmerpenguins)

penguins

ggplot(penguins, aes(x=flipper_length_mm, y=body_mass_g)) + geom_point(aes(color=species)) + geom_smooth(method='lm')

ggplot(penguins, aes(x=species)) + geom_bar(fill = 'purple')

ggplot(penguins, aes(x=body_mass_g)) + geom_histogram(binwidth = 20)

ggplot(penguins, aes(x=body_mass_g)) + geom_density()

ggplot(penguins, aes(x=species, y=body_mass_g)) + geom_boxplot()

ggplot(penguins, aes(x= island, fill = species)) + geom_bar()


mpg
mtcars

#Zadanie 1
ggplot(mpg, aes(x=hwy)) + geom_histogram(fill = 'chocolate', bins=15)

#Zadanie 2
ggplot(mtcars, aes(x=wt, y=mpg)) +geom_point(color='mediumorchid4', size=0.05)+geom_smooth(method='lm', color='red', fill='tan2', linewidth=0.05)

#Zadanie 3
ggplot(mpg, aes(x=class, fill=drv)) + geom_bar() + labs(y='drv')

       