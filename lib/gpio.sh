FIRST_GPIO=504
LAST_GPIO=511
GPIOS=$(seq ${FIRST_GPIO} ${LAST_GPIO})

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
	gpio_set_all value 0
	gpio_set_all direction out
}

gpio_set() {

	local gpio=$1
	key=$2
	value=$3
	echo "${value}" > "/sys/class/gpio/gpio${gpio}/${key}"
}

gpio_bounce() {

	local gpio=$1
	gpio_set ${gpio} value 1
	sleep 5s
	gpio_set ${gpio} value 0

}

gpio_show() {
	
	local gpio=$1
	echo "GPIO: ${gpio} direction: $(cat /sys/class/gpio/gpio${gpio}/direction) value: $(cat /sys/class/gpio/gpio${gpio}/value)" 
}

gpio_show_all() {

	for gpio in ${GPIOS}; do 
		echo "GPIO: ${gpio} direction: $(cat /sys/class/gpio/gpio${gpio}/direction) value: $(cat /sys/class/gpio/gpio${gpio}/value)" 
	done
}


gpio_demo() {
	gpio_init
	gpio_show_all
	for gpio in ${GPIOS}; do
		gpio_set ${gpio} value 1
		sleep 0.5s
	done
	gpio_show_all
	for gpio in ${GPIOS}; do
		gpio_set ${gpio} value 0
		sleep 0.5s
	done
	gpio_show_all
	gpio_unexport_all
}