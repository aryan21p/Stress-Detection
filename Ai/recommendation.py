class Recommendation:

    def get(
        self,
        fatigue,
        stress,
        attention,
        emotion
    ):

        if fatigue >= 70:
            return "Take a 10 min break"

        if stress == "High":
            return "Practice deep breathing"

        if attention < 70:
            return "Stay focused on screen"

        if emotion == "Sleepy":
            return "Get some rest"

        return "You are healthy"