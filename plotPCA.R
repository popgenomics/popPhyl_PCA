library(shiny)
library(plotly)
library(tidyverse)
library(shinycssloaders)

ui <- basicPage(
	uiOutput('select_tables'),
	uiOutput('select_PC'),
	withSpinner(uiOutput('PCA_page'))
	
)

server <- function(input, output) {
	options(shiny.maxRequestSize=4000*1024^2)
		
	output$PCA_page <- renderUI({
		fileName1 = input$coord
		fileName2 = input$contrib

		if(is.null(fileName1) | is.null(fileName2)) {
			return()
		}else{
			fluidPage(
				fluidRow( width = 12, withSpinner(plotlyOutput( outputId = 'plot_PCA')))
			)
		}
	})

	output$select_tables <- renderUI({
		fluidPage(
			column(3, fileInput("coord", label = h4("table with PCA coordinates"))),
			column(3, fileInput("contrib", label = h4("table with eigen values")))
		)
	})


	output$select_PC <- renderUI({
		fluidPage(
			column(3, selectInput("axeX", label=h4('x-axis'), choices = list("PC1" = 1, "PC2" = 2, "PC3" = 3), selected = 1)),
			column(3, selectInput("axeY", label=h4('y-axis'), choices = list("PC1" = 1, "PC2" = 2, "PC3" = 3), selected = 2)),
			column(3, checkboxInput("annotation", label = "annotate individuals?", value = TRUE))
		)
	})
	
	
	allData <- reactive({
		fileName1 = input$coord
		fileName2 = input$contrib
		if(is.null(fileName1) | is.null(fileName2)) {
			return (NULL)
		}else{
			coord = read.table(input$coord$datapath, h=T)
			contrib = read.table(input$contrib$datapath, h=T)
			
			res = list()
			res[['resPCA']] = coord[, -c(1,2)]
			res[['species']] = coord[,1]
			res[['individuals']] = coord[,2]
			res[['contrib']] = as.numeric(contrib)
			return(res)
		}
	})
	
	output$plot_PCA <- renderPlotly({
		resPCA = allData()[['resPCA']]
		coordPCA = tibble(axe_x=resPCA[,as.numeric(input$axeX)], axe_y=resPCA[,as.numeric(input$axeY)], individual=allData()[['individuals']], species=allData()[['species']])
		per_var_x = allData()[['contrib']][as.numeric(input$axeX)]
		per_var_y = allData()[['contrib']][as.numeric(input$axeY)]


		# plot
		t <- list(
			family = "Arial",
			size = 20,
			color = 'black')

		# PC1 : PC2
		#p <- plot_ly(data = coordPCA, x = ~axe_x, y = ~axe_y, type='scatter', mode='markers', hoverinfo='text', text=~paste('Individual: ', individual, '<br>Group: ', species, sep=''), color= ~species, marker=list(size=20), colors='Set1', width = 1*as.numeric(input$dimension[1]), height = 1*as.numeric(input$dimension[2]) ) %>%
		p <- plot_ly(data = coordPCA, x = ~axe_x, y = ~axe_y, type='scatter', mode='markers', hoverinfo='text', text=~paste('Individual: ', individual, '<br>Group: ', species, sep=''), color= ~species, marker=list(size=20), colors='Set1', width = 1200, height = 600 ) %>%
			layout(font=t) %>%
			layout(xaxis = list(title=paste('PC', input$axeX, ' (', per_var_x,'%)', sep=''))) %>%
			layout(yaxis = list(title=paste('PC', input$axeY, ' (', per_var_y,'%)', sep=''))) %>%
			layout(hoverlabel=list(font=list(family='Arial', size=20)))
		if(input$annotation == 1){
			p = p %>% add_annotations(x = coordPCA$axe_x, y = coordPCA$axe_y, text = coordPCA$individual)
		}
		return(p)
	})
}

shinyApp(ui, server)

