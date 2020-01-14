from distutils.core import setup
import TunefindPlaylist

setup(name='TunefindPlaylist',
      version= TunefindPlaylist.__version__,
      description='Google Play Music playlist generator from Tunefind',
      author='Krzysztof Krysiński',
      author_email='krysinskikrzysztof123@gmail.com',
      url="https://github.com/flabbet/TunefindPlaylist",
      packages=['TunefindPlaylist'],
      requires=['gmusicapi', 'requests', 'bs4']
      )
