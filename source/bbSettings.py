cfg = {}
settingsFile = 'data/bbSettings.txt'
for line in open(settingsFile):
    l   = line.split(' ')
    try:
        cfg[l[0]] = float(l[-1].strip())
    except:
        cfg[l[0]] = l[-1].strip()
