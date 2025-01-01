library(ggplot2)
options(vsc.dev.args = list(width= 700, height = 500))
ggplot(mpg, aes(x=displ, y=hwy, color=drv)) + geom_point() +
labs(
    title = "Wykres zależności między zużyciem paliwa a rozmiarem silnika"
) +
theme(
    legend.position = "inside",
    legend.position.inside = c(0.6, 0.7),
    legend.direction = "horizontal",
    legend.box.background = element_rect(color="black"),
    plot.title = element_text(face = "bold"),
    plot.title.position = "panel"
)

head(iris)

ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width, color=Species)) + geom_point() +
labs(
    title = "Wymiary działki kielicha a gatunek irysa",
    x = "Długość działki kielicha",
    y = "Szerokość działki kielicha",
    caption = "Na podstawie zbioru danych: iris",
    color = "Gatunek"
) +
theme(
    legend.position = "inside",
    legend.position.inside = c(0.7, 0.9),
    legend.direction = "horizontal",
    legend.box.background =  element_rect(color="black"),
    plot.title = element_text(face= "bold"),
    plot.title.position = "panel"
)