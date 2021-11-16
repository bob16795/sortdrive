. /etc/sysconfig/functions

echo 0 > /sys/class/graphics/fbcon/cursor_blink

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

for i in $SCRIPTPATH/always/*; do
  boot_mesg running $i
  $i 2>&1 | sed 's/^/  /' && echo_ok || echo_failure
done

for i in $SCRIPTPATH/next/*; do
  boot_mesg running $i
  $i 2>&1 | sed 's/^/  /' && echo_ok || echo_failure
  mv $i $SCRIPTPATH/never
done

