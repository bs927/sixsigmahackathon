from shiny import App, ui, render
import pandas as pd
from app.qc import calculate_cpk

app_ui = ui.page_fluid(
    ui.h2("CPR Aerospace QC Dashboard"),
    ui.input_file("file1", "Choose Process Log CSV"),
    ui.output_text_verbatim("result")
)

def server(input, output, session):
    @render.text
    def result():
        file_infos = input.file1()
        if not file_infos:
            return "Please upload a file."
        
        df = pd.read_csv(file_infos[0]["datapath"])
        val = calculate_cpk(df['StressYield'], usl=950, lsl=850)
        return f"Calculated Cpk: {val}"

app = App(app_ui, server)
