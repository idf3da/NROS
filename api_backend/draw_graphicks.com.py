import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT

def datetime(x):
    return np.array(x, dtype=np.datetime64)

#neede date like year-month-day
const_window_size = 30
const_date = ['01-01','01-02','01-03','01-04','01-05','01-06','01-07','01-08',]
const_sales =  [100,101,102,103,104,100,101,102,]
const_prediction =  [99,102,103,104,105,99,101,102,]
  
def draw_graphic(date = AAPL['date'], sales=AAPL['adj_close'], prediction=AAPL['adj_close'], color_window = "white", color_sale = 'darkblue', color_prediction = 'darkgrey'):


    aapl = np.array(sales)
    aapl_dates = np.array(date, dtype=np.datetime64)
    window = np.ones(const_window_size)/float(const_window_size)
    aapl_avg = np.convolve(np.array(prediction), window, 'same')
    print(aapl)
    print(aapl_avg)
    graphic = figure(x_axis_type="datetime", title="Stonks")
    graphic.grid.grid_line_alpha = 0
    graphic.xaxis.axis_label = 'Date'
    graphic.yaxis.axis_label = 'Sale'
    graphic.ygrid.band_fill_color =  color_window
    graphic.ygrid.band_fill_alpha = 0.1

    graphic.circle(aapl_dates, aapl, size=4, legend_label='prediction', color=color_prediction, alpha=0.4)

    graphic.line(aapl_dates, aapl_avg, legend_label="real sales", color=color_sale)
    graphic.legend.location = "top_left"

    output_file("stoncks.html", title="graphic in Test")
    show(graphic, plot_width=400, plot_height=400) # open a browser

draw_graphic(const_date, const_sales, const_prediction)
#draw_graphic()
