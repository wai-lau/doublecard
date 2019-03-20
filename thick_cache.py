from analysis_cache import AnalysisCache

class ThickCache(AnalysisCache):
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
        # Vert 4s
        terms = 3**5
        for i in range(terms):
            t = self.tern(i)
            self.cache[t] = self.check_line(t)
        # Horz/Dag Blocks
        terms = 3**8
        for i in range(terms):
            print("Loading data:",round((i/terms)*100, 0),"%    \r",end='')
            t = self.tern(i)
            for m in range((8+1)-len(t)):
                line = m*"0"+t
                if len(line) >= 4:
                    for b in self.gen_all_bin(len(line)):
                        self.cache[line + " " + b] = \
                                self.check_line(line + " " + b)
        print()

    def gen_all_bin(self, level):
        i = 0
        while i < 2**level:
            yield ("{:0"+str(level)+"b}").format(i)
            i += 1

    def tern(self, n):
        e = n//3
        q = n%3
        if n == 0:
            return '0'
        elif e == 0:
            return str(q)
        else:
            return self.tern(e) + str(q)

    def check_vert(self, line):
        x = r = f = 0
        if len(line) == 5:
            if ("1" not in line[:4] or "2" not in line[:4]):
                return self.dual_analysis((4, 0, 0))
            line = line[1:5]
        for h in range(3):
            if ("1" not in line[h:] or "2" not in line[h:]):
                x = len(line[h:])
                if x == 2:
                    f = 1
                    r = 1
                elif x == 3:
                    r = 1
                break
        return self.dual_analysis((x, r, f))
        

    def get_score(self, perspective, pattern):
        if perspective == "ours":
            return self.our_points[pattern]
        else:
            return self.their_points[pattern]

    def check_horz_or_dag(self, line):
        top, bot = line.split()
        group_count = len(top)-3
        
        groups = []
        for s in range(group_count):
            t_group = [t for t in top[s:s+4]]
            b_group = [b for b in bot[s:s+4]]
            groups.append((t_group, b_group))

        groups = map(self.xrf, groups)
        groups = list(map(self.dual_analysis, groups))

        ours, theirs = list(zip(*groups))
        return sum(ours), sum(theirs)

    def xrf(self, group):
        x = r = f = 0
        if "1" not in group[0] or "2" not in group[0]:
            for i, e in enumerate(group[0]):
                if e == "0":
                    if group[1][i] == "0":
                        f += 1
                    else:
                        r += 1
                else:
                    x += 1
            return (x, r, f)
        return (0, 0, 0)
    
    def dual_analysis(self, xrf):
        # (ours, theirs)
        score = [0,0]
        s = 0
        perspectives = ["ours", "theirs"]
        for p in perspectives:
            if xrf[0] == 4:
                score[s%2] += self.get_score(p, "xxxx")
            elif xrf[0] == 3:
                if xrf[2] == 1:
                    score[s%2] += self.get_score(p, "xxxf")
                else:
                    score[s%2] += self.get_score(p, "xxxr")
            elif xrf[0] == 2:
                if xrf[2] == 2:
                    score[s%2] += self.get_score(p, "xxff")
                elif xrf[2] == 1:
                    score[s%2] += self.get_score(p, "xxrf")
                else:
                    score[s%2] += self.get_score(p, "xxrr")
            s += 1
        return tuple(score)

    def check_line(self, line):
        if " " not in line:
            return self.check_vert(line)
        else:
            return self.check_horz_or_dag(line)


