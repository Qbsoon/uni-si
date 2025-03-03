#Zadanie 1

v <- c(1:100)

even = v[v %% 2 == 0]

m = matrix(even, nrow = 5, byrow=TRUE)

m[3:4,5:9]

#Zadanie 2

studenci <- data.frame(imie = c("Alicja", "Kamil", "Julia", "Hubert", "Ryszard"),
                        wiek = c(20, 19, 22, 21, 23),
                        ocena = c("Bardzo dobra", "Dobra", "Bardzo dobra", "Dostateczna", "Niedostateczna"))

studenci[studenci$ocena == "Bardzo dobra",]

studenci$zdane <- ifelse(studenci$ocena == "Niedostateczna", "fałsz", "prawda")

#Zadanie 3

library(dplyr)
library(tidyverse)

cars <- mtcars

added <- cars$hp/cars$wt

cars$hp_wt_ratio <- added

filtered <- cars[cars$mpg > 25 & cars$hp_wt_ratio < 40,]

sorted <- filtered %>% arrange(desc(mpg))

final <- sorted[, c("mpg", "hp", "wt", "hp_wt_ratio")]

#Zadanie 4

library(ggplot2)

ggplot(iris, aes(x = Petal.Length, y = Petal.Width, color = Species)) + geom_point() + ggtitle("Wykres wymiarów płatka irysa względem gatunku") + xlab("Długość płatka (cm)") + ylab("Szerokość płatka (cm)") + labs(color = "Gatunek")
#Gatunek Virginica ma najdłuższe i najszersze płatki

#Zadanie 5

library(shiny)

ui <- fluidPage(
  titlePanel("Wizualizaacja zbioru iris"),
  sidebarLayout(
    sidebarPanel(
        textOutput("Wielkość punktów"),
        sliderInput("points_size", min=1, max=5, value=3, label="Wielkość punktów")
    ),
    mainPanel(
        plotOutput("iris_plot"),
        tableOutput("iris_table")
        )
    )
)

server <- function(input, output) {
    output$iris_plot <- renderPlot({
        ggplot(iris, aes(x = Petal.Length, y = Petal.Width, color = Species)) + geom_point(size = input$points_size) + ggtitle("Wykres wymiarów płatka irysa względem gatunku") + xlab("Długość płatka (cm)") + ylab("Szerokość płatka (cm)") + labs(color = "Gatunek")
    })
    
    output$iris_table <- renderTable({
        iris
    })
}

shinyApp(ui = ui, server = server)