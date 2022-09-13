import os  # fix OpenGL 1.1
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.core.window import Window
Window.size = (450, 800)

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.label import MDLabel
from kivy.utils import platform
from kivy_garden.mapview import MapView, MapMarker, MapSource
from plyer import gps, notification
import numpy as np

self_lat = 25.0341
self_lon = 121.565
Amb_list = np.array([[0, 0]])
Amb_list = np.append(Amb_list, [[25.034, 121.564]], axis=0)
Amb = []
Amb.append(MapMarker(lat=float(Amb_list[1, 0]), lon=float(Amb_list[1, 1]), source='Icon/Map/ambulance.png'))

if platform == 'android':
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])


class HomeScreen(Screen):
    def login(self):
        Main.sm.current = 'Login'
        Main.sm.transition.direction = 'right'

    def Reg(self):
        Main.sm.current = 'Reg'
        Main.sm.transition.direction = 'right'


class LoginScreen(Screen):
    def login(self, id, password):
        if id == '' and password == '':
            Main.sm.current = 'Main'
            Main.sm.transition.direction = 'left'
            notification.notify(title='Safe Driving', message="GPS is closed", timeout=3, toast=True)
            return True
        else:
            return False


class RegScreen(Screen):
    def Reg(self, id, password, password_check, car_brand, number):
        if password == password_check:
            Main.sm.current = 'Home'
            Main.sm.transition.direction = 'left'
            return True
        else:
            return False


class MainScreen(Screen):
    Is_GPS = False
    Is_Amb = False
    IsSOS = False
    IsMES = False

    def amb(self):
        if not self.Is_Amb:
            self.Is_Amb = True
            self.ids['amb_icon'].icon = r'./Icon/ambulance.png'
            for i in range(len(Amb)):
                self.ids['Map'].add_widget(Amb[i])
            notification.notify(title='Safe Driving', message="Ambulance tracking", timeout=3, toast=True)
        elif self.Is_Amb:
            self.Is_Amb = False
            self.ids['amb_icon'].icon = r'./Icon/map.png'
            for i in range(len(Amb)):
                self.ids['Map'].remove_widget(Amb[i])
            notification.notify(title='Safe Driving', message="Ambulance untracking", timeout=3, toast=True)
        print(self.Is_Amb)

    def update_locations(self, **kwargs):
        self_lat = kwargs['lat']
        self_lon = kwargs['lon']
        self.ids['user'].lat = self_lat
        self.ids['user'].lon = self_lon
        self.ids['Map'].center_on(self_lat, self_lon)
        if self.Is_Amb:
            for i in range(1, len(Amb_list)):
                Amb.append(MapMarker(lat=float(Amb_list[i, 0]), lon=float(Amb_list[i, 1]), source='Icon/Map/ambulance.png'))
                self.ids['Map'].add_marker(Amb[i])
        print(kwargs)

    def logout(self):
        Main.sm.current = 'Home'
        Main.sm.transition.direction = 'left'

    def GPS(self, checkbox, value):
        if value:
            self.Is_GPS = True
            notification.notify(title='Safe Driving', message="GPS is opened", timeout=3, toast=True)
            if platform == 'android':
                gps.configure(on_location=self.update_locations)
                gps.start(minTime=5000, minDistance=0)
        else:
            self.Is_GPS = False
            notification.notify(title='Safe Driving', message="GPS is closed", timeout=3, toast=True)
            if platform == 'android':
                gps.stop()

    def sos(self, checkbox, value):
        if value:
            self.IsSOS = True
        else:
            self.IsSOS = False
        print(self.IsSOS)

    def message(self, checkbox, value):
        if value:
            self.IsMES = True
        else:
            self.IsMES = False
        print(self.IsMES)


class Main(MDApp):
    IsSOS = True
    IsMES = True
    sm = ScreenManager()

    def build(self):
        Builder.load_file('screen.kv')
        Main.sm.add_widget(HomeScreen(name='Home'))
        Main.sm.add_widget(LoginScreen(name='Login'))
        Main.sm.add_widget(RegScreen(name='Reg'))
        Main.sm.add_widget(MainScreen(name='Main'))
        return Main.sm


if __name__ == '__main__':
    Main().run()
