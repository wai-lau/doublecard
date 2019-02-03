import shelve

class AnalysisCache:
    def __init__(self, rebuild=False):
        self.cache = {}
        with shelve.open("analysis.pkl") as shelf:
            if rebuild or not shelf:
                self.generate_cache(level=12)
                shelf['cache'] = self.cache
            else:
                self.cache = shelf['cache']

    def generate_cache(self, level=12):
        terns = 3**level
        percentages = list(range(0,terns,int(terns/100)))
        percent_complete = 0
        for i in range(terns):
            if i in percentages:
                print("Generating cache:", percent_complete,"%    \r",end='')
                percent_complete = percent_complete + 1
            t = self.ternary(i)
            for m in range(13-len(t)):
                line = m*"0"+t
                self.cache[line] = self.check_line_tern(line)

    def ternary(self, n):
        e = n//3
        q = n%3
        if n == 0:
            return '0'
        elif e == 0:
            return str(q)
        else:
            return self.ternary(e) + str(q)

    def check_line_tern(self, line):
        groups = len(line)-3
        points = [0,0,0,0,0]

        if groups <= 0:
            return points

        for s in range(groups):
            group = [l for l in line[s:s+4] if l!="0"]

            if "1" not in group or "2" not in group:
                points[len(group)] = points[len(group)]+1

        return points


