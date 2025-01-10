options(repos = c(CRAN = "https://cran.r-project.org"))
library(ggplot2)
library(palmerpenguins)
library(shiny)

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
                selected = "audience_score",
            ),
            # Wybierz zmienne dla osi X
            selectInput(
                inputId = "x",
                label = "X-axis:",
                choices = c("imdb_rating", "imdb_num_votes", "critics_score", "audience_score", "runtime"),
                selected = "critics_score",
            ),
            # Wybierz kolorowanie
            selectInput(
                inputId = "color",
                label = "Schemat kolorowania",
                choices = c("genre", "title_type", "mpaa_rating"),
                selected = "mpaa_rating",
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
            )
        ),
        mainPanel(
            plotOutput(outputId = "scatterplot", height = "400px")
        )
    )
)

server <- function(input, output, session) {
    # Utwórz wykres punktowy
    output$scatterplot <- renderPlot({
        ggplot(movies, aes_string(x = input$x, y = input$y, color=input$color)) +
            geom_point(size=input$size, alpha=input$alpha)
    })
}

shinyApp(ui, server)