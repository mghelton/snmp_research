def parse_kwargs(required,kwargs):
    counter = 0
    for arg in kwargs:
        if arg in required:
            counter += 1
            required[arg]['state'] = True
            if type(kwargs[arg]) != required[arg]['type']:
                return False,"TypeError {}".format(kwargs[arg])
    if(counter == len(required)):
        return True,''
    else:
        missing = []
        for key in required:
            if(key not in kwargs):
                missing.append(key)
        missing = "missing {}".format(missing).replace("[","").replace("]","").replace(", "," & ").replace("'","")
        return False,missing