FIRST_GPIO=504
LAST_GPIO=511
GPIOS=$(seq ${FIRST_GPIO} ${LAST_GPIO})
OFF_VALUE=0
ON_VALUE=1

gpio_export_all() {

	for gpio in ${GPIOS}; do 
		echo ${gpio} > "/sys/class/gpio/export"
	done
}

gpio_unexport_all() {

	for gpio in ${GPIOS}; do 
		echo ${gpio} > "/sys/class/gpio/unexport"
	done
}

gpio_set_all() {
	key=$1
	value=$2
	for gpio in ${GPIOS}; do 
		echo "${value}" > "/sys/class/gpio/gpio${gpio}/${key}"
	done

}
 
gpio_init() {

	gpio_export_all
	sleep 1s;
	gpio_set_all active_low 0
	gpio_set_all direction high
}

gpio_set() {

	local gpio=$1
	key=$2
	value=$3
	echo "${value}" > "/sys/class/gpio/gpio${gpio}/${key}"
}

gpio_get() {

	local gpio=$1
	key=$2
	echo "$(cat /sys/class/gpio/gpio${gpio}/${key})"
}


gpio_off() {

	local gpio=$1
	gpio_set ${gpio} value ${OFF_VALUE}
}

gpio_on() {

	local gpio=$1
	gpio_set ${gpio} value ${ON_VALUE}
}

gpio_bounce() {

	local gpio=$1
	gpio_off ${gpio}
	sleep 5s
	gpio_on ${gpio}
}

gpio_bounce_all() {

	for gpio in ${GPIOS}; do 
		gpio_bounce ${gpio}
	done
}

gpio_show() {
	
	local gpio=$1
	echo "GPIO: ${gpio} active_low: $(cat /sys/class/gpio/gpio${gpio}/active_low) direction: $(cat /sys/class/gpio/gpio${gpio}/direction) value: $(cat /sys/class/gpio/gpio${gpio}/value)" 
}

gpio_show_all() {

	for gpio in ${GPIOS}; do 
		gpio_show ${gpio}
	done
}


gpio_demo() {
	gpio_init
	gpio_show_all
	for gpio in ${GPIOS}; do
		gpio_set ${gpio} value ${OFF_VALUE}
		sleep 0.5s
	done
	gpio_show_all
	for gpio in ${GPIOS}; do
		gpio_set ${gpio} value ${ON_VALUE}
		sleep 0.5s
	done
	gpio_show_all
	gpio_unexport_all
}
