"""
the moon module is approximately intended for calculating the coordinate of the moon at a certain time,
the calculations are not very accurate since a circle instead of an ellipse is taken for the triangle of
the moon's rotation around the earth, which in turn causes some inaccuracies
"""
import datetime
import math
import ephem
import datetime as dt


class Moon:
    """
    the Moon class where object attributes are the coordinates of the
    moon at a specified time and date of these coordinates
    """
    def __init__(self, date_for_calc: datetime.datetime = dt.datetime.now()):
        self.ra = None
        self.dec = None
        self.date_for_calc = date_for_calc
        # start date with which we will compare to get the coordinates of the current date
        self.start_date = dt.datetime(2021, 5, 29, 23, 59, 59)
        # time difference in seconds from the start date to the current date
        self.time_of_result = int((self.date_for_calc - self.start_date).total_seconds())
        # declination of the plane of the movement of the moon with a comparison of the celestial equator
        self.angle_slope = (23.44 + 5.14) * 3600
        # the period of the full rotation of the moon around the earth in seconds
        self.period_for_on_cycle = 27.3 * 24 * 60 * 60
        # angle of full rotation of the moon around the earth in seconds
        self.perimeter = 360 * 3600
        # the angle of movement of the moon in 1 second
        self.one_sec_walk = self.perimeter / self.period_for_on_cycle
        # rough calculation of the change in the ra coordinate in one second
        self.one_sec_walk_ra = math.cos(self.angle_slope) * self.one_sec_walk
        # rough calculation of the change in the dec coordinate in one second
        self.one_sec_walk_dec = math.sin(self.angle_slope) * self.one_sec_walk
        # the epham package is used to take the starting coordinates of the moon for calculation
        self.moon = ephem.Moon()
        self.moon.compute('2021/5/29 23:59:59')
        self.ra_ephem_start = self.moon.ra
        self.dec_ephem_start = self.moon.dec
        self.ra_start_list = str(self.ra_ephem_start).split(':')
        self.dec_start_list = str(self.dec_ephem_start).split(':')
        self.ra_start = float(self.ra_start_list[0]) * 3600 + float(self.ra_start_list[1]) * 60 + float(
            self.ra_start_list[2])
        self.dec_start = float(self.dec_start_list[0]) * 3600 + float(self.dec_start_list[1]) * 60 + float(
            self.dec_start_list[2])

    def moon_ra_dec_calc(self) -> str:
        """
        the function calculates the coordinates of the moon at a certain time,
        for this you need the starting coordinates and the date of these coordinates,
        the point is to calculate the delta ra and delta dec in 1 second and cyclically
        add the previous coordinate until the required coordinates are calculated
        """
        for sec in range(self.time_of_result):
            if 0 <= self.ra_start + self.one_sec_walk_ra < 360 * 3600:
                self.ra = self.ra_start + self.one_sec_walk_ra
                self.ra_start = self.ra
            else:
                self.ra = self.ra_start + self.one_sec_walk_ra - 360 * 3600
                self.ra_start = self.ra
            if self.dec_start >= 0:
                if self.dec_start + self.one_sec_walk_dec <= self.angle_slope:
                    self.dec = self.dec_start + self.one_sec_walk_dec
                    self.dec_start = self.dec
                else:
                    self.dec = self.dec_start + self.one_sec_walk_dec - self.angle_slope
                    self.dec_start = self.dec
            elif self.dec_start < 0:
                if self.dec_start - self.one_sec_walk_dec >= -self.angle_slope:
                    self.dec = self.dec_start - self.one_sec_walk_dec
                    self.dec_start = self.dec
                else:
                    self.dec = self.dec_start - self.one_sec_walk_dec + self.angle_slope
                    self.dec_start = self.dec

        ra_res = f'{int(self.ra // 3600)}:{int((self.ra % 3600) // 60)}:{round(float((self.ra % 3600) % 60), 1)}'
        dec_res = f'{int(self.dec // 3600)}:{int((self.dec % 3600) // 60)}:{round(float((self.dec % 3600) % 60), 1)}'

        return 'moon ra is a  ' + ra_res + '--' + 'moon dec is a ' + dec_res
