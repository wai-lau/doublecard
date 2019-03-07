from analysis_cache import AnalysisCache

class PointsCache(AnalysisCache):
    def __init__(self, filename, rebuild=False,
                 our_points={0:2, 1:12, 2:600000},
                 their_points={0:12, 1:1000, 2:20000}):
        self.our_points = our_points
        self.their_points = their_points
        super().__init__(filename, rebuild)

    def dual_analysis(self, in_a_rows):
        # heuristic should be [0] - [1] (yours - theirs)
        ours = 0
        # since we take a subset, in_a_rows[0] is the number of doubles
        # using a multiple of 20 if it outclasses in all cases
        for i, n in enumerate(in_a_rows[2:]):
            ours = ours + self.our_points[i]*n
        theirs = 0
        # enemy triples are worth as much as a loss, since they will play that move
        for i, n in enumerate(in_a_rows[2:]):
            theirs = theirs + self.their_points[i]*n
        return (ours, theirs)

