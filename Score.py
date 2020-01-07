class Score:
    score = 0
    dead = False

    @staticmethod
    def add_score(num):
        if not Score.dead:
            Score.score += num

    @staticmethod
    def get_score():
        score = str(int(Score.score))
        score = '0' * (5 - len(score)) + score
        return score

    @staticmethod
    def clear():
        Score.score = 0
