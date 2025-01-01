krotki_kot <- fluidPage(
    textOutput("text"),
    verbatimTextOutput("code")
)

server <- function(input, output, session) {
    output$text <- renderText("Witaj!")

    output$code <- renderPrint(
        "Witaj!"
    )
}



krotki_kot <- fluidPage(
    tableOutput("statyczna"),
    dataTableOutput("dynamiczna")
)

server <- function(input, output, session) {
    output$statyczna <- renderTable(head(mtcars))

    output$dynamiczna <- renderDataTable(mtcars, options = list(pageLength = 5))
}



krotki_kot <- fluidPage(
    plotOutput("plot", width= "400px")
)

server <- function(input, output, session) {
    output$plot <- renderPlot(plot(1:5), res = 86)
}



krotki_kot <- fluidPage(
    plotOutput("plot", width= "400px", click = "plot_click"),
    tableOutput("data")
)

server <- function(input, output, session) {
    output$plot <- renderPlot(plot(mtcars$wt, mtcars$mpg), res=96)

    output$data <- renderTable({
        req(input$plot_click)
        nearPoints(mtcars, input$plot_click, xvar = "wt", yvar= "mpg")
    })
}



krotki_kot <- fluidPage(
    plotOutput("plot", width= "480px", click = "plot_click"),
    tableOutput("data")
)

server <- function(input, output, session) {
    output$plot <- renderPlot(ggplot(mtcars, aes(x=wt, y=mpg)) + geom_point(), res=96)

    output$data <- renderTable({
        req(input$plot_click)
        nearPoints(mtcars, input$plot_click, xvar = "wt", yvar= "mpg")
    })
}



krotki_kot <- fluidPage(
    plotOutput("plot", width= "480px", brush = "plot_brush"),
    tableOutput("data")
)

server <- function(input, output, session) {
    output$plot <- renderPlot(ggplot(mtcars, aes(x=wt, y=mpg)) + geom_point(), res=96)

    output$data <- renderTable({
        req(input$plot_brush)
        brushedPoints(mtcars, input$plot_brush)
    })
}
shinyApp(krotki_kot, server)
