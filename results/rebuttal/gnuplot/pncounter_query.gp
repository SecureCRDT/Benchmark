load 'defaults.gp'
load 'cdtudcolors.gp'
load 'colors-sequential-Gray.gp'

set label 200 "Latency(ms)"
set label 100 "Throughput (op/s)"

baseline_name = "Baseline"
system_name = "SMPC"

baseline_color = HKS44_100
system_color = HKS65_100

marker_1 = 6
marker_2 = 2

line_style = 5
line_width = 1
point_size = 1


set terminal postscript eps enhanced color

set output "plots/pncounter_query.eps"

set autoscale y
set autoscale x



plot "results/BASELINE/pncounter/query.dat" with linespoints title baseline_name ls line_style lw line_width pt marker_1 ps point_size lc rgb baseline_color,\
	"results/SMPC/pncounter/query.dat" with linespoints title system_name ls line_style lw line_width pt marker_2 ps point_size lc rgb system_color


unset multiplot

