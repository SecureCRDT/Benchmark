#!/usr/bin/gnuplot

# Set the number of rows and columns
rows = 3
cols = 2

# Set the size of the margins (in inches)
top_margin = 0.2
bot_margin = 0.4
left_margin = 0.2
right_margin = 0.1

# Set the size of the subplots (in inches)
subplot_height = 0.6
subplot_width = 3

# Set the spacing between the subplots (in inches)
horizontal_spacing = 0
vertical_spacing = 0.5

# Calculate the full dimensions of the plot (in inches)
xsize = left_margin + right_margin + (subplot_width * cols) + (cols - 1) * horizontal_spacing
ysize = top_margin + bot_margin + (subplot_height * rows) + (rows - 1) * vertical_spacing

# Set the terminal and output options
set terminal epslatex size xsize,ysize
set output "plot.tex"

# Set up the multiplot mode
set multiplot

# Define a function to set the margins for a given subplot
set_margins(row, col) = do for [i=1:row] {
    set tmargin at screen top(i)
    set bmargin at screen bot(i)
}
for [i=1:col] {
    set lmargin at screen left(i)
    set rmargin at screen right(i)
}

# Plot some data
set_margins(3, 1)
plot sin(x)

set_margins(3, 2)
plot cos(x)

set_margins(3, 1)
plot tan(x)


# End the multiplot mode
unset multiplot
