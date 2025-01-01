install.packages("shiny")

library(shiny)

ui <- fluidPage(
    "Hello, World!"
)

server <- function(input, output, session)

shinyApp(ui, server)




ui <- fluidPage(
    selectInput("dataset", label = "Dataset", choice = ls("package:datasets")),
    verbatimTextOutput("summary"),
    tableOutput("table")
)

server <- function(input, output, session) {
    output$summary <- renderPrint({
        dataset <- get(input$dataset, "package:datasets")
        summary(dataset)
    })

    output$table <- renderTable({
        dataset <- get(input$dataset, "package:datasets")
        dataset
    })
}

shinyApp(ui, server)



ui <- fluidPage(
    selectInput("dataset", label = "Dataset", choice = ls("package:datasets")),
    verbatimTextOutput("summary"),
    tableOutput("table")
)

server <- function(input, output, session) {
    dataset <- reactive({
        get(input$dataset, "package:datasets")
    })

    output$summary <- renderPrint({
        summary(dataset())
    })

    output$table <- renderTable({
        dataset()
    })
}

shinyApp(ui, server)