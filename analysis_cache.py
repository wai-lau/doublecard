class AnalysisCache:
    def __init__(self, level=12):
        self.cache = {}
        for i in range(3**level):
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


