# $language = "python"
# $interface = "1.0"

# This automatically generated script may need to be
# edited in order to work correctly.

def Main():
	crt.Screen.Synchronous = True
	crt.Screen.Send(tail -f /data/IBM/profiles/Was07App01/logs/Free_DC_was07Node10/SystemOut.log)
Main()
