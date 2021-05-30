"""

"""
import math
import ephem
import datetime as dt


class Moon:
    """

    """
    def __init__(self, date_for_calc=dt.datetime.now()):
        self.ra = None
        self.dec = None
        self.date_for_calc = date_for_calc
        self.start_date = dt.datetime(2021, 5, 25, 23, 59, 59)
        self.time_of_result = int((self.date_for_calc - self.start_date).total_seconds())
        self.angle_slope = (23.44 + 5.14) * 3600
        self.period_for_on_cycle = 27.3 * 24 * 60 * 60
        self.perimeter = 360 * 3600
        self.one_sec_walk = self.perimeter / self.period_for_on_cycle
        self.one_sec_walk_ra = math.sin(self.angle_slope) * self.one_sec_walk
        self.one_sec_walk_dec = math.cos(self.angle_slope) * self.one_sec_walk
        self.moon = ephem.Moon()
        self.moon.compute('2021/5/25 23:59:59')
        self.ra_ephem_start = self.moon.ra
        self.dec_ephem_start = self.moon.dec
        self.ra_start_list = str(self.ra_ephem_start).split(':')
        self.dec_start_list = str(self.dec_ephem_start).split(':')
        self.ra_start = float(self.ra_start_list[0]) * 3600 + float(self.ra_start_list[1]) * 60 + float(
            self.ra_start_list[2])
        self.dec_start = float(self.dec_start_list[0]) * 3600 + float(self.dec_start_list[1]) * 60 + float(
            self.dec_start_list[2])

    def moon_ra_dec_calc(self):
        """

        :return:
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
