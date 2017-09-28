with open('config_file.txt') as configFile:
    lines=configFile.readlines()
    configs={}
    for line in lines:
        configs[line.rstrip('\n').split(':')[0]]=line.rstrip('\n').split(':')[1]
    print configs
    print "File read complete"