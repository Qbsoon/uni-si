options(repos = c(CRAN = "https://cran.r-project.org"))
library(ggplot2)
library(palmerpenguins)
library(shiny)
library(tidyverse)

load("/SI/R2S3/R/movies.RData")

ui <- fluidPage(
    # Nazwa aplikacji
    titlePanel("Movie Browser"),

    # Kompozycja panelu bocznego
    sidebarLayout(
        # Panel boczny dla wejść użytkownika
        sidebarPanel(
            # Wybierz zmienne dla osi Y
            selectInput(
                inputId = "y",
                label = "Y-axis:",
                choices = c("imdb_rating", "imdb_num_votes", "critics_score", "audience_score", "runtime"),
                selected = "audience_score"
            ),
            # Wybierz zmienne dla osi X
            selectInput(
                inputId = "x",
                label = "X-axis:",
                choices = c("imdb_rating", "imdb_num_votes", "critics_score", "audience_score", "runtime"),
                selected = "critics_score"
            ),
            # Wybierz kolorowanie
            selectInput(
                inputId = "color",
                label = "Schemat kolorowania",
                choices = c("genre", "title_type", "mpaa_rating"),
                selected = "mpaa_rating"
            ),
            # Suwak przezroczystości alpha
            sliderInput(
                inputId = "alpha",
                label = "Transparency:",
                min = 0.1, max = 1, value = 0.5
            ),
            # Suwak określajacy wielkość punktów na wykresie
            sliderInput(
                inputId = "size",
                label = "Size:",
                min = 1, max = 7, value = 2
            ),
            checkboxInput(
                inputId = "show_table",
                label = "Show data table",
                value = TRUE
            ),
            #Dopasuj wielkość próby
            numericInput(
                inputId = "sample_size",
                label = "Sample size:",
                value = 1,
                min = 1,
                max = nrow(movies)
            ),
            # Pole tekstowe ustawienia nazwy dla wykresu
            textInput(
                inputId = "plot_title",
                label = "Plot title",
                placeholder = "Enter a plot title"
            ),
            # Pole wyboru gatunku filmu
            checkboxGroupInput(
                inputId = "type",
                label = "Typ:",
                choices = unique(movies$title_type),
                selected = unique(movies$title_type)
            )
        ),
        mainPanel(
            plotOutput(outputId = "scatterplot", height = "400px"),
            # Tabela na wyjściu jeśli spełniony warunek
            conditionalPanel(
                condition = "input.show_table == true",
                tableOutput(outputId = "data_table")
            )
        )
    )
)

server <- function(input, output, session) {
    filtered <- reactive({
        subset(
            movies,
            title_type %in% input$type
        ) %>%
        head(input$sample_size)
    })
    # Utwórz wykres punktowy
    output$scatterplot <- renderPlot({
        ggplot(filtered(), aes_string(x = input$x, y = input$y, color=input$color)) +
            geom_point(size=input$size, alpha=input$alpha) + labs(title = input$plot_title)
    })
    # Utwórz tabelę z danymi
    output$data_table <- renderTable({
        filtered()
    })
}

shinyApp(ui, server)

runExample("03_reactivity", display.mode = "showcase")

system.file("examples", package="shiny")