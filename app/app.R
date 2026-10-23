library(shiny)
source("qc.R")

# Define UI
ui <- fluidPage(
    titlePanel("Six Sigma Quality Control Analysis"),
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins", "Number of bins:", 1, 50, 30),
            numericInput("usl", "Upper Specification Limit:", 950),
            numericInput("lsl", "Lower Specification Limit:", 850)
        ),
        mainPanel(
            plotOutput("distPlot"),
            verbatimTextOutput("qcResults")
        )
    )
)

# Define server
server = function(input, output) {
    
    # Load your data here - assuming 'data/capable.csv' exists as a sample
    data <- reactive({
        read.csv("../data/capable.csv")
    })
    
    analysis <- reactive({
        compute_qc_analysis(data(), value_col = "Stress_Yield_MPa", usl = input$usl, lsl = input$lsl)
    })

    output$distPlot = renderPlot({
        vals <- data()$Stress_Yield_MPa
        hist(vals, breaks = input$bins, col = 'darkgray', border = 'white',
             main = 'Distribution of Stress Yield')
    })
    
    output$qcResults = renderPrint({
        res <- analysis()
        cat("Grand Mean:", res$grand_mean, "\n")
        cat("Cp:", res$cp, "\n")
        cat("Cpk:", res$cpk, "\n")
        cat("Shapiro-Wilk p-value:", res$shapiro_p, "\n")
    })
}

shinyApp(ui = ui, server = server)
