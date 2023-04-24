#!/usr/bin/env bash



plots=('gcounter_query.gp' 'gcounter_update.gp' 'pncounter_decrement.gp' 'maxvalue_query.gp' 'pncounter_increment.gp' 'maxvalue_update.gp' 'pncounter_query.gp' 'minboundedcounter_decrement.gp' 'register_query.gp' 'minboundedcounter_increment.gp' 'register_update.gp' 'minboundedcounter_query.gp')

for plot in "${plots[@]}"
do
	gnuplot $plot
done
