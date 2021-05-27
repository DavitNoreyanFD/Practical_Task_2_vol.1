import ephem


class Moon:
    def __init__(self, current_time):
        self.current_time = current_time
        moon = ephem.Moon()
        moon.compute(str(self.current_time))
        self.moon_ra = moon.ra
        self.moon_dec = moon.dec

    def moon_coordinate_result_in_curr_time(self):
        result = f'moon ra is a {self.moon_ra}, moon dec is a {self.moon_dec}'
        return result
