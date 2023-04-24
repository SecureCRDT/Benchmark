#!/usr/bin/gnuplot

load 'defaults.gp'
load 'colors-sequential-Gray.gp'

# Set the number of rows and columns
rows = 1
cols = 1

# Set the size of the margins (in inches)
top_margin = 0.2
bot_margin = 0.4
left_margin = 0.2
right_margin = 0.1

# Set the size of the subplots (in inches)
subplot_height = 1
subplot_width = 3

# Set the spacing between the subplots (in inches)
horizontal_spacing = 0
vertical_spacing = 0

line_style = 5
line_width = 1
point_size = 1

line_colour = HKS44_100
baseline_color = HKS44_100

marker_1 = 5
marker_2 = 2
marker_3 = 4

xsize = left_margin + right_margin + (subplot_width * cols) + (cols - 1) * horizontal_spacing
ysize = top_margin + bot_margin + (subplot_height * rows) + (rows - 1) * vertical_spacing


# Set the terminal and output options
set terminal epslatex size xsize,ysize
set output "plots/minboundedcounter_update_v2.tex"

# Plot styling
set tics nomirror
set autoscale 

unset label 200
unset label 100
unset key 
set autoscale y
set autoscale x
set ytics 2,4
smpc_increment_color = HKS65_100
smpc_decrement_color = HKS07_100

# Set up the multiplot mode
set multiplot layout rows,cols
set lmargin 5
set rmargin 1.4
set tmargin 2
set bmargin 1.5

set autoscale y
set autoscale x
set logscale y 2
set logscale x 2

set key horiz maxrows 1 samplen 1 
set key out top center

set xrange [:64]

set xlabel "N. of Clients"
set ylabel "Throughput (ops/s)" offset screen 0.05,0
plot "data/SMPC/minboundedcounter/decrement_nclients.dat"  with linespoints title "Increment" ls line_style lw line_width pt marker_2 ps point_size lc rgb smpc_increment_color,\
	"data/SMPC/minboundedcounter/increment_nclients.dat" with linespoints title "Decrement" ls line_style lw line_width pt marker_3 ps point_size lc rgb smpc_decrement_color


unset multiplot
