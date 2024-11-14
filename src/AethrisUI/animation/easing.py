import math

class Easing:
    @staticmethod
    def linear(t: float) -> float:
        return t
    
    @staticmethod
    def ease_in(t: float) -> float:
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def bounce(t: float) -> float:
        if t < 4/11:
            return (121 * t * t)/16
        elif t < 8/11:
            return (363/40 * t * t) - (99/10 * t) + 17/5
        elif t < 9/10:
            return (4356/361 * t * t) - (35442/1805 * t) + 16061/1805
        else:
            return (54/5 * t * t) - (513/25 * t) + 268/25 