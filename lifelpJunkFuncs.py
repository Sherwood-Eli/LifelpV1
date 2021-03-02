#junk func
def findSunday(today):
	global dataKeys
	global dataIndex
	temp = today[0:7]
	tempKeys = dataKeys[temp]
	for x in range(0,len(tempKeys)):
		if today == tempKeys[x]:
			dataIndex = x
			temp = x - 3
			for y in range(0,7):
				if ((temp - y)%7) == 0:
					return (x-y)

