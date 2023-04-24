load 'defaults.gp'
load 'cdtudcolors.gp'
load 'colors-sequential-Gray.gp'

unset label 200
unset label 100


#set xlabel ""
#set ylabel "Throughput (ops/s * 10)" offset screen 0.05,0

gcounter_name = "GCounter"
register_name = "Register"
pncounter_name = "PNCounter"

gcounter_color = HKS44_100
pncounter_color = HKS65_100
register_color = HKS07_100

marker_1 = 6
marker_2 = 2
marker_3 = 4

line_style = 5
line_width = 1
point_size = 1


#set terminal postscript eps enhanced color
set terminal epslatex color dl 2.0 size 2.6,1.8

set output "plots/pncounter_troughput.tex"

set autoscale y
set autoscale x

set key horiz maxrows 1 samplen 1 
set key out top center

set ytics 2,4


plot "data/SMPC/pncounter/update_troughput.dat" using 1:($2/100) with linespoints title "PNCounter" ls line_style lw line_width pt marker_1 ps point_size lc rgb gcounter_color



unset multiplot

