def sanitize(time_string):
    if '-' in time_string:
        splitize = '-'
        (mins, secs)=time_string.split(splitize)
    elif ':' in time_string:
        splitize = ':'
        (mins, secs)=time_string.split(splitize)
    else:
        return(time_string)
    return(mins+'.'+secs)
class AthleteList (list):
                def __init__(self,a_name,a_dob=None,a_times=[]):
                    list.__init__([])
                    self.name = a_name
                    self.dob = a_dob
                    self.extend(a_times)
                def top3(self):
                    return(sorted(set([sanitize(t) for t in self]))[0:3])