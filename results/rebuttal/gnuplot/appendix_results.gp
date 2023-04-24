load 'defaults.gp'
load 'colors-sequential-Gray.gp'
#load 'colors-qualitative-clusterd.gp'

mpl_top    = 0.2 #inch  outer top margin, title goes here
mpl_bot    = 0.42 #inch  outer bottom margin, x label goes here
mpl_left   = 0.2 #inch  outer left margin, y label goes here
mpl_right  = 0.1 #inch  outer right margin, y2 label goes here
mpl_height = 0.6 #inch  height of individual plots
mpl_width  = 3 #inch  width of individual plots
mpl_dx     = 0 #inch  inter-plot horizontal spacing
mpl_dy     = 0.5 #inch  inter-plot vertical spacing
mpl_ny     = 3 #number of rows
mpl_nx     = 1 #number of columns

baseline_name = "Baseline"
system_name = "CODBS"

baseline_color = HKS44_100
system_color = HKS65_100

marker_1 = 5
marker_2 = 7
marker_3 = 8
marker_4 = 5

line_style = 5
line_width = 1
point_size = 1

line_colour = HKS44_100


# calculate full dimensions
# The maximum column width of a acm paper is around 3.2 inches. The values have
# to be updated to fit according to the paper column width.

xsize = mpl_left+mpl_right+(mpl_width*mpl_nx)+(mpl_nx-1)*mpl_dx
ysize = mpl_top+mpl_bot+(mpl_ny*mpl_height)+(mpl_ny-1)*mpl_dy

print xsize
print ysize
unset label 200
unset label 100

# placement functions
#   rows are numbered from bottom to top
bot(n) = (mpl_bot+(n-1)*mpl_height+(n-1)*mpl_dy)/ysize
top(n)  = 1-((mpl_top+(mpl_ny-n)*(mpl_height+mpl_dy))/ysize)

#   columns are numbered from left to right
left(n) = (mpl_left+(n-1)*mpl_width+(n-1)*mpl_dx)/xsize
right(n)  = 1-((mpl_right+(mpl_nx-n)*(mpl_width+mpl_dx))/xsize)

set terminal epslatex color dl 2.0  size xsize,ysize

set grid xtics lc rgb "#636363"

set encoding iso_8859_1
set output "plots/appendix_results.tex"
set border 3 back
set tics nomirror


#set offsets
set autoscale 
set size 1,1

set style rectangle fs solid noborder
unset key 


set multiplot

#-----------------------------------------------
#  set horizontal margins for first column
set lmargin at screen left(1)
set rmargin at screen right(1)
#  set horizontal margins for third row (top)
set tmargin at screen top(3)
set bmargin at screen bot(3)
#set title "Workload A" offset 0, -1
#set xlabel 'Number of table blocks (base 2)' offset 0, 0.7

set ylabel 'Register'

set autoscale y
set autoscale x
set ytics 2,4

#set ytics 10
plot "data/SMPC/register/update_troughput.dat" using 1:($2/100) with linespoints title "Register" ls line_style lw line_width pt marker_1 ps point_size lc rgb line_colour


#-----------------------------------------------
#  set horizontal margins for second column
set lmargin at screen left(1)
set rmargin at screen right(1)
#  set horizontal margins for third row (top)
set tmargin at screen top(2)
set bmargin at screen bot(2)
#set key horiz maxrows 1 samplen 0.5 
#set key out bot center
#set key at 26,-330 
#set ytics 100

#set title "Workload B"
#set xlabel 'Number of results' offset 0, 0.7
#set ylabel 'Avrg. Latency (ms)'

set ylabel 'GCounter'


plot "data/SMPC/gcounter/update_troughput.dat" using 1:($2/100) with linespoints title "GCounter" ls line_style lw line_width pt marker_1 ps point_size lc rgb line_colour

#-----------------------------------------------
#  set horizontal margins for second column
set lmargin at screen left(1)
set rmargin at screen right(1)
#  set horizontal margins for third row (top)
set tmargin at screen top(1)
set bmargin at screen bot(1)
#set key horiz maxrows 1 samplen 0.5 
#set key out bot center
#set key at 26,-330 
#set ytics 100

#set title "Workload B"
#set xlabel 'Number of results' offset 0, 0.7
#set ylabel 'Avrg. Latency (ms)'

set ylabel 'PNCounter'

plot "data/SMPC/pncounter/update_troughput.dat" using 1:($2/100) with linespoints title "PNCounter" ls line_style lw line_width pt marker_1 ps point_size lc rgb line_colour


unset multiplot





