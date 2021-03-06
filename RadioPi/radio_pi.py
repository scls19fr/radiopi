import os
import time

import pygame

from audio.player import VlcPlayer
from controller.controller import Controller
from network.network_linux import LinuxNetworkService
from radiostation.radio_browser_de_api_model import RadioBrowserDeClient
from radiostation.radioservice import RadioService
from ui.mouse_device import MouseDevice, cursor_cross, cursor_empty
from ui.view import ImageFont, UI, FrameBuilder
from view.radio_view import Images, RadioPlayView, RadioSelectView,\
    RadioSetupView, ScreensaverView, RadioSetupClockView, RadioSelectMusicView
from audiofile.audiofileservice import AudiofileService


#from ui.mouse_device import MouseDevice
radio_client = RadioBrowserDeClient()
radio_service = RadioService(radio_client)
audio_player = VlcPlayer("./controlvlc_socket.sh")
network_service = LinuxNetworkService()
audiofile_service = AudiofileService()

# os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()
pygame.font.init() 

screen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
pygame.display.set_caption("Radio PI")

font = ImageFont('gfx/font.png', (20, 20))
font_pushed = ImageFont('gfx/font_pushed.png', (20, 20))
font_inactive = ImageFont('gfx/font_inactive.png', (20, 20))
ui = UI(screen, 320, 240, (0, 0, 0))
images = Images(font, font, font_pushed, font_inactive)
framebuilder = FrameBuilder(
    images.label(Images.FRAME_TOP_LEFT),
    images.label(Images.FRAME_TOP_RIGHT),
    images.label(Images.FRAME_BOTTOM_LEFT),
    images.label(Images.FRAME_BOTTOM_RIGHT),
    images.label(Images.FRAME_LEFT),
    images.label(Images.FRAME_RIGHT),
    images.label(Images.FRAME_TOP),
    images.label(Images.FRAME_BOTTOM),
    20,20
    )
fontspath = "fonts/dejavu-fonts-ttf-2.37/ttf/"
fonts = [
    fontspath + 'DejaVuSans.ttf',
    fontspath + 'DejaVuSans-Bold.ttf',
    fontspath + 'DejaVuSans-Oblique.ttf',
    fontspath + 'DejaVuSans-BoldOblique.ttf'    
]
sizes = [12, 16, 20, 24]
#sizes = [20, 24, 28, 36]
colors = [(255,255,255), (0,255,0)]

play_view = RadioPlayView(screen, images, framebuilder, fonts, sizes, colors)
play_view.set_size(320, 240);

select_view = RadioSelectView(screen, images, framebuilder, fonts, sizes, colors)
select_view.set_size(320, 240)

select_music_view = RadioSelectMusicView(screen, images, framebuilder, fonts, sizes, colors)
select_music_view.set_size(320, 240);

setup_view = RadioSetupView(screen, images, framebuilder, fonts, sizes, colors)
setup_view.set_size(320, 240)

setup_clock_view = RadioSetupClockView(screen, images, framebuilder, fonts, sizes, colors)
setup_clock_view.set_size(320, 240)

screensaver_view = ScreensaverView(screen, images, cursor_cross, cursor_empty)
screensaver_view.set_size(320, 240)

ui.get_root().add(play_view)
ui.get_root().add(select_view)
ui.get_root().add(select_music_view)
ui.get_root().add(setup_view)
ui.get_root().add(setup_clock_view)
ui.set_screensaver(screensaver_view)

controller = Controller(play_view, select_view, select_music_view, setup_view, setup_clock_view, radio_service, audio_player, network_service, audiofile_service)

ui.get_root().show()
ui.refresh()

#pygame.mouse.set_visible(False)
#input_device = TouchDevice()
#input_device.calibration_load('calibration.ini')

input_device = MouseDevice()
pygame.mouse.set_visible(True)
pygame.mouse.set_cursor((16, 16), (7, 7), *cursor_cross)

while True:
    input_device.poll(ui)
    ui.refresh()
    time.sleep(0.05)
