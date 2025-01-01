library(ggplot2)
options(vsc.dev.args = list(width= 700, height = 500))
ggplot(mpg, aes(x=displ, y=hwy)) + geom_point(aes(color=class)) + geom_smooth(se = FALSE) +
labs(x='Objetosc silnika w litrach', y='Mile na galon paliwa na autostradzie', color='Typ samochodu', title= 'Wykres zależności między zużyciem paliwa a rozmiarem silnika', subtitle = 'Zużycie paliwa generalnie rośnie wraz z wielkością silnika', caption = "Dane pochodzą z fueleconomy.gov")

ggplot(mpg, aes(x=class, fill=drv)) + geom_bar(position='dodge', width=0.7, color='mediumorchid4') + labs(x="Typ samochodu", y="Liczba samochodów", color="Rodzaj napędu", title="Rozkład typów samochodu zewzględu na rodzaj napędu", subtitle= "Wszystkie minivany ze zbioru danych mają napęd przedni")

install.packages('scales')
library(scales)

ggplot(mpg, aes(x=displ, y=hwy, color=drv)) + geom_point() + scale_y_continuous(breaks=seq(15,40,by=5))

ggplot(mpg, aes(x=displ, y=hwy, color=drv)) + geom_point() + scale_x_continuous(labels=NULL) + scale_y_continuous(labels=NULL) + scale_color_discrete(labels = c("4" = "4x4", "f" = "przedni", 'r' = "tylny"))

ggplot(mpg, aes(x = displ, y=hwy)) + geom_point(aes(color=class)) + scale_x_continuous() + scale_y_continuous() + scale_color_discrete()

ggplot(diamonds, aes(x= price, y= cut)) + geom_boxplot(alpha = 0.05) + scale_x_continuous(labels= label_dollar(scale = 1/1000, suffix = "K"), breaks = seq(1000, 19000, by = 6000))

ggplot(diamonds, aes(x=cut, fill= clarity)) + geom_bar(position='fill') + scale_y_continuous(name = "Percentage", labels= label_percent())

wykres <- ggplot(mpg, aes(x = displ, y=hwy, color=class)) + geom_point()
wykres
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")
wykres + theme(legend.position="left")
wykres + theme(legend.position="top")
wykres + theme(legend.position="right")
wykres + theme(legend.position="bottom")

wykres + theme(legend.position = "top") + guides(col = guide_legend(nrow = 3))

ggplot(mpg, aes(x = displ, y = hwy)) + geom_point(aes(color = class)) + geom_smooth(se = FALSE) + theme_bw()

ggplot(mpg, aes(x = displ, y = hwy)) + geom_point(aes(color = class)) + geom_smooth(se = FALSE) + theme_void()



mpg
diamonds
