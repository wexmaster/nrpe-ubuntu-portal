#!/bin/bash
  
# Configuration
check_dummy=/usr/lib/nagios/plugins/check_dummy
check_icmp=/usr/lib/nagios/plugins/check_icmp
log=/var/log/centreon/centplugins/
awk=/usr/bin/awk
sed=/bin/sed
egrep=/bin/egrep
mtr=/usr/bin/mtr

# Command line parameters
hosts=$1
num_icmp=$2
warning=$3
critical=$4
min_hosts_alive=$5
for host in $hosts ; do
        log="${log}hosts_alive_${host}.log";
        break;
done;

#Config
timeout=15
echo "$(date) - ************* Starting script *************" >> $log
output_bruto=$($check_icmp -n $num_icmp -w $warning -c $critical -m $min_hosts_alive -v -t $timeout -H $hosts)
output=$(echo "$output_bruto" | $egrep "OK|WARNING|CRITICAL|UNKNOWN|min_hosts_alive")
echo "$output_bruto" | grep -v "handle_random_icmp" >> $log
state=`echo $output | $awk '{printf $1}'`
text=`echo "$output" | $egrep "min_hosts_alive"`
perf=`echo $text | $awk -F "," '{printf $3" ; "$4}' | $sed 's/ //g' | $sed 's/:/=/g'`

case $state in
  OK)
        $check_dummy 0 "$text | $perf"
        echo "$(date) - ************* Ending script *************" >> $log
        exit 0
        ;;
  WARNING)
        $check_dummy 1 "$text | $perf"
        echo "$(date) - ************* Ending script *************" >> $log
        exit 1
        ;;
  CRITICAL)
        $check_dummy 2 "$text | $perf"
        for host in $hosts ; do
                echo "MTR to $host" >> $log;
                $mtr -r -c 1 --no-dns $host >> $log;
        done;
        echo "$(date) - ************* Ending script *************" >> $log
        exit 2
        ;;
  *)
        $check_dummy 3 "$text | $perf"
        echo "$(date) - ************* Ending script *************" >> $log
        exit 3
        ;;
esac
