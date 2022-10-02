# from exampleData import exampleData

def parser(readData):

    # function to process each time-instance of the read data
    def parseReadings(readData):
        time = readData['readTime']
        readings = readData['readingValues']
        output = map(lambda x: parseValues(x,time),readings)
        return output

    # function to process the readings for each time-instance
    def parseValues(readData,time):
        out = {'fields':{}, 'tags': {}, 'time': time, "measurement": "smartmeter"}
        for key in readData.keys():
            val = readData[key]
            if  val is None:
                return 
            elif type(val) == int or type(val) == float or type(val) == int:
                # add it as field
                out['fields'][key] = val*1.0
            else:
                # add it as tag
                out['tags'][key] = val
        return out

    # flattens the resulting map objects to a single list
    def flatten(mainlist):
        flat_list = []
        for sublist in mainlist:
            for item in sublist:
                if item is not None:
                    flat_list.append(item)
        return flat_list

    # only look at the readings of the read data
    readings = readData['readings']
    output = map(parseReadings,readings)

    return flatten(output)


# output = parser(exampleData)
# print(output)