from analysis_cache import AnalysisCache

class BlockCache(AnalysisCache):
    def __init__(self, filename, rebuild=False,
                 our_points={"xxff":1, "xxrf":3, "xxxf":57,
                             "xxrr":79,"xxxr":1000,"xxxx":1000000},
                 their_points={"xxff":2, "xxrf":7, "xxxf":251,
                               "xxrr":277,"xxxr":10000,"xxxx":100000}
                ):
        self.our_points = our_points
        self.their_points = their_points
        super().__init__(filename, rebuild)

    def generate_cache(self):
        # Vert Blocks
        terms = 5**4
        for i in range(terms):
            t = self.pent(i)
            self.cache[t] = self.check_line(t)
        # Horz/Dag Blocks
        for i in range(terms):
            print("Loading data:",round((i/terms)*100, 0),"%    \r",end='')
            t = self.pent(i)
            for m in range(5-len(t)):
                line = m*"0"+t
            for b in self.gen_all_bin(8):
                self.cache[line+b] = self.check_line(line+b)
        print()

    def gen_all_bin(self, level):
        i = 0
        while i < 2**level:
            yield "{:08b}".format(i)
            i += 1

    def pent(self, n):
        e = n//5
        q = n%5
        if n == 0:
            return '0'
        elif e == 0:
            return str(q)
        else:
            return self.pent(e) + str(q)

    #0 *  #1 WO  #2 WX  #3 RO  #4 RX
    def check_vert(self, line):
        dots = 0
        dreal = 0
        dfake = 0
        colors = 0
        creal = 0
        cfake = 0
        for h in range(3):
            if (("2" not in line[h:] and "4" not in line[h:]) or
                ("1" not in line[h:] and "3" not in line[h:])):
                for e in line[h:]:
                    dots += 1
                if dots == 2:
                    dfake = 1
                    dreal = 1
                elif dots == 3:
                    dreal = 1
                break

        for h in range(3):
            if (("1" not in line[h:] and "2" not in line[h:]) or
                ("3" not in line[h:] and "4" not in line[h:])):
                for e in line[h:]:
                    colors += 1
                if colors == 2:
                    cfake = 1
                    creal = 1
                elif colors == 3:
                    creal = 1
                break

        return self.dual_analysis((
            {"x":dots, "r":dreal, "f":dfake},
            {"x":colors, "r":creal, "f":cfake}
        ))
        
    
    # 0: dots perspective   1: colors perspective
    def dual_analysis(self, values):
        score = [0, 0]
        s = 0
        perspectives = ["ours", "theirs"]
        for v in values:
            for p in perspectives:
                if v["x"] == 4:
                    score[s%2] += self.get_score(p, "xxxx")
                elif v["x"] == 3:
                    if v["f"] == 1:
                        score[s%2] += self.get_score(p, "xxxf")
                    else:
                        score[s%2] += self.get_score(p, "xxxr")
                elif v["x"] == 2:
                    if v["f"] == 2:
                        score[s%2] += self.get_score(p, "xxff")
                    elif v["f"] == 1:
                        score[s%2] += self.get_score(p, "xxrf")
                    else:
                        score[s%2] += self.get_score(p, "xxrr")
                s += 1
            perspectives = ["theirs", "ours"]
        return tuple(score)

    def get_score(self, perspective, pattern):
        if perspective == "ours":
            return self.our_points[pattern]
        else:
            return -1*self.their_points[pattern]

    def check_horz_or_dag(self, line):
        dots = 0
        dreal = 0
        dfake = 0
        colors = 0
        creal = 0
        cfake = 0
        if (("2" not in line[:4] and "4" not in line[:4]) or
            ("1" not in line[:4] and "3" not in line[:4])):
            for i, e in enumerate(line[:4]):
                if e == "0":
                    if line[4+i] == "0" and line[8+i] == "0":
                        dfake += 1
                    else:
                        dreal += 1
                else:
                    dots += 1

        if (("1" not in line[:4] and "2" not in line[:4]) or
            ("3" not in line[:4] and "4" not in line[:4])):
            for i, e in enumerate(line[:4]):
                if e == "0":
                    if line[4+i] == "0" and line[8+i] == "0":
                        cfake += 1
                    else:
                        creal += 1
                else:
                    colors += 1
        
        return self.dual_analysis((
            {"x":dots, "r":dreal, "f":dfake},
            {"x":colors, "r":creal, "f":cfake}
        ))
            
    def check_line(self, line):
        if len(line) <= 4:
            return self.check_vert(line)
        else:
            return self.check_horz_or_dag(line)


