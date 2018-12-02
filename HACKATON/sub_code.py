import os 
a=1
while a<701:
	if a%140==0:
		file = open(os.getcwd()+"\\Places\\Samarqand Darvoza\\floor","a")
		file.write(str(a) + "\n")
		file.close()

	else:
		file = open(os.getcwd()+"\\Places\\Samarqand Darvoza\\floor","a")
		file.write(str(a) + " ")
		file.close()

	a+=1
