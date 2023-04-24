#!/usr/bin/gnuplot

load 'defaults.gp'
load 'colors-sequential-Gray.gp'

# Set the number of rows and columns
rows = 3
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
marker_1 = 5

xsize = left_margin + right_margin + (subplot_width * cols) + (cols - 1) * horizontal_spacing
ysize = top_margin + bot_margin + (subplot_height * rows) + (rows - 1) * vertical_spacing



# Set the terminal and output options
set terminal epslatex size xsize,ysize
set output "plots/appendix_results.tex"

# Plot styling
set tics nomirror
set autoscale 

unset label 200
unset label 100
unset key 
set autoscale y
set autoscale x
set ytics 2,4

# Set up the multiplot mode
set multiplot layout 3,1
set lmargin 1
set rmargin 1
set tmargin 1
set bmargin 1.5

set key horiz maxrows 1 samplen 1 
set key top left

# Plot some data

plot "data/SMPC/register/update_troughput.dat" using 1:($2/100) with linespoints title "Register" ls line_style lw line_width pt marker_1 ps point_size lc rgb line_colour

set ylabel 'Throughput (ops/s * 100)' offset 1.2,0
plot "data/SMPC/gcounter/update_troughput.dat" using 1:($2/100) with linespoints title "GCounter" ls line_style lw line_width pt marker_1 ps point_size lc rgb line_colour
unset ylabel

set xlabel 'N. of clients'
plot "data/SMPC/pncounter/update_troughput.dat" using 1:($2/100) with linespoints title "PNCounter" ls line_style lw line_width pt marker_1 ps point_size lc rgb line_colour

# End the multiplot mode
unset multiplot
