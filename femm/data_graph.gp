reset
set style line 1 lc rgb '#0D4F8B' lt 1 lw 2 pt 1 pi -1 ps .7 #indigo dye
#set style line 2 lc rgb '#C71585' lt 1 lw 2 pt 1 pi -1 ps .7 #Medium Violet Red
#set style line 3 lc rgb '#1874CD' lt 1 lw 2 pt 2 pi -1 ps .7 #dodger blue
#set style line 4 lc rgb '#FF1493' lt 1 lw 2 pt 2 pi -1 ps .7 # deep pink
#set style line 5 lc rgb '#007FFF' lt 1 lw 2 pt 3 pi -1 ps .7 #slate blue
#set style line 6 lc rgb '#FF69B4' lt 1 lw 2 pt 3 pi -1 ps .7 #hot pink
#set style line 7 lc rgb '#7EB6FF' lt 1 lw 2 pt 4 pi -1 ps .7 #forget me nots
#set style line 8 lc rgb '#FFB6C1' lt 1 lw 2 pt 4 pi -1 ps .7 #light pink

#set style line 1 lc rgb '#AB82FF' lt 1 lw 2 pt 1 pi -1 ps .7 #indigo dye
set style line 2 lc rgb '#EEAD0E' lt 1 lw 2 pt 1 pi -1 ps .7 #Medium Violet Red
set style line 3 lc rgb '#436EEE' lt 1 lw 2 pt 2 pi -1 ps .7 #dodger blue
set style line 4 lc rgb '#EE4000' lt 1 lw 2 pt 2 pi -1 ps .7 # deep pink
set style line 5 lc rgb '#00F5FF' lt 1 lw 2 pt 3 pi -1 ps .7 #slate blue
set style line 6 lc rgb '#FFD700' lt 1 lw 2 pt 3 pi -1 ps .7 #hot pink
set style line 7 lc rgb '#00C957' lt 1 lw 2 pt 4 pi -1 ps .7 #forget me nots
set style line 8 lc rgb '#800000' lt 1 lw 2 pt 4 pi -1 ps .7 #light pink

	#436EEE
#AB82FF
#00F5FF
#4EEE94

set title "FEMM Torque Profile" font 'Verdana,24'

#set style line 1 lc rgb '#FF4500' pt 1 ps 1.2 pi 60 lt 1 lw 2
set terminal pngcairo enhanced font 'Verdana,14' size 1200,600
set output 'force_profile.png'
set style line 100 lc rgb '#778899'
set key inside right bottom autotitle columnhead
set key box
set key font 'Verdana, 14'

set datafile separator ','


#set lmargin screen .08
#set tmargin screen .92
#set rmargin screen .9
#set bmargin screen 0.15
set style line 50 lc rgb '#808080' lt 0 lw 1
set grid back ls 50
set xtics
set xlabel 'Angle (deg)' font 'Verdana,12'
set ylabel 'Torque (N * m)' font 'Verdana, 12'


set ytics
set mytics

plot 'force-results.txt' using 1:4 axis x1y1 with lines ls 1 title "Torque"
