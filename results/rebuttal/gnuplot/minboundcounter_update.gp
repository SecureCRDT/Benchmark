load 'defaults.gp'
load 'cdtudcolors.gp'
load 'colors-sequential-Gray.gp'

unset label 200
unset label 100


set xlabel "N. of Clients"
set ylabel "Throughput (ops/s)" offset screen 0.05,0

baseline_name = "Baseline"
smpc_increment = "Increment"
smpc_decrement = "Decrement"

baseline_color = HKS44_100
smpc_increment_color = HKS65_100
smpc_decrement_color = HKS07_100

marker_1 = 6
marker_2 = 2
marker_3 = 4

line_style = 5
line_width = 1
point_size = 1

set terminal epslatex color dl 2.0

# set terminal postscript eps enhanced color

#set output "plots/minboundedcounter_update.eps"
set output "plots/minboundedcounter_update.tex"

set autoscale y
set autoscale x
set logscale y 2
set logscale x 2

set key horiz maxrows 1 samplen 1 
set key out top center

plot "results/SMPC/minboundedcounter/decrement_nclients.dat"  with linespoints title smpc_decrement ls line_style lw line_width pt marker_2 ps point_size lc rgb smpc_increment_color,\
	"results/SMPC/minboundedcounter/increment_nclients.dat" with linespoints title smpc_increment ls line_style lw line_width pt marker_3 ps point_size lc rgb smpc_decrement_color


unset multiplot

