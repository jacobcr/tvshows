
from tvshow.tvshow import loader, downloaded, seasoncap, show
import unittest
import os
from StringIO import StringIO

class TvShowTest(unittest.TestCase):
    def test_loader(self):
        resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tvshow.csv')
        shows = list(loader(resource_path))
        self.assertEqual(shows[0], (['Fringe', 'fringe']))

    def test_downloaded(self):
        downlad_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        files = list(downloaded(downlad_path, [['example']]))
        
        self.assertEqual(2, len(files))

    def test_seasoncap_sox_eox(self):
        s, c = seasoncap('somfilenameS07E11.mp4')
        self.assertEqual(('07', '11'), (s, c))

        s, c = seasoncap('somfilenames07e01.mp4')
        self.assertEqual(('07', '01'), (s, c))

        s, c = seasoncap('somfilenames7e1.mp4')
        self.assertEqual(('07', '01'), (s, c))

        s, c = seasoncap('somfilenames07_01.mp4')
        self.assertEqual(('07', '01'), (s, c))

    def test_show(self):
        s = show('filefringe', [['Fringe']])
        self.assertTrue('Fringe')

