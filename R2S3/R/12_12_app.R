library(shiny)

ui <- fluidPage(
    textInput("imie", "Jak sie nazywasz?"),
    textOutput("powitanie")
)

server <- function(input, output, session) {
    output$powitanie <- renderText({
        paste0("Witaj, ", input$imie, "!")
    })
}

shinyApp(ui, server)


ui <- fluidPage(
    sliderInput("x", label = "Jeśli x równa się", min = 1, max = 50, value = 30),
    "to x razy 5 jest równe",
    textOutput("product")
)

server <- function(input, output, session) {
    output$product <- renderText({
        input$x * 5
    })
}

shinyApp(ui, server)


ui <- fluidPage(
    sliderInput("x", label = "Jeśli x równa się", min = 1, max = 100, value = 30),
    sliderInput("y", label = "a y równa się", min=1, max=50, value=5),
    "to x razy y jest równe",
    textOutput("product"),
    "a x razy y plus 5 jest równe",
    textOutput(("product_plus5")),
    "a x razy y plus 10 jest równe",
    textOutput("product_plus10")
)


server <- function(input, output, session) {
product <- reactive({
    input$x * input$y
})

    output$product <- renderText({
        product()
    })

    output$product_plus5 <- renderText({
        product() + 5
    })

    output$product_plus10 <- renderText({
        product() + 10
    })
}

shinyApp(ui, server)


ui <- fluidPage(
    textInput("imie", "jJak się nazywasz?"),
    passwordInput("haslo", "Podaj hasło"),
    textAreaInput("hobby", "Jakie są Twoje zainteresowania?", rows=3),
    numericInput("num", "Pierwsza liczba", value = 42, min = 0, max = 1000000),
    sliderInput("num2", "Druga liczba", value = 860000, min = 0, max = 1000000),
    sliderInput("num3", "Trzecia liczba", value = c(86,86000), min = 0, max = 1000000),

)

server <- function(input, output, session) {}

shinyApp(ui, server)

zwierzeta <- c('pies', 'kot', 'mysz', 'sowa', 'krolik', 'kon', 'inne')

ui <- fluidPage(
    dateInput('data', 'Jaka data urodzenia?', value="1939-09-01"),
    dateRangeInput("urlop", "W jakich dniach był urlop", start="1918-07-01", end="1939-09-01"),
    selectInput("stan", "Jaki jest Twój ulubiony stan Ameryki?", state.name),
    radioButtons("zwierze", "Jakiej jest Twoje ulubione zwierze", zwierzeta)
)

server <- function(input, output, session) {}

shinyApp(ui, server)



krotki_kot <- fluidPage(
    textInput('kier', "Jaki jest Twój kierunek studiów?", placeholder="Twój kierunek"),
)

server <- function(input, output, session) {}

shinyApp(krotki_kot, server)



krotki_kot <- fluidPage(
    sliderInput('sliddd', "Zakres liczb", min=0, max=9976, value=86, step=86),
)

server <- function(input, output, session) {}

shinyApp(krotki_kot, server)


krotki_kot <- fluidPage(
    sliderInput('sliddd', "Wybierz date", min=as.Date('2024-10-01'), max=as.Date('2024-12-22'), value=Sys.Date(), timeFormat= "%Y-%m-%d"),
)

server <- function(input, output, session) {}

shinyApp(krotki_kot, server)