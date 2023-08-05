
# -*- coding: utf-8 -*-

# Test gars module.

__all__ = ('Tests',)
__version__ = '19.04.12'

from base import TestsBase

from pygeodesy import bearingDMS, F_DM, fStr, gars, Garef


class Tests(TestsBase):

    def testCodec3(self, g, x, prec=4):
        self.test('codec3', Garef(g), g)
        t = gars.decode3(g)
        self.test('decode3', fStr(t, prec=prec), x)
        self.test('encode', gars.encode(*t), g)

    def testGars(self, LL):

        # Karney's geographiclib/1.49/examples/example-GARS.cpp
        # <http://SourceForge.net/p/geographiclib/code/ci/release/tree/examples/example-GARS.cpp>
        g = Garef('57.64911, 10.40744', precision=2)
        self.test('Garef', g, '381NH45')
        self.test('Garef', repr(g), "Garef('381NH45')")
        self.test('Garef.latlon', fStr(g.latlon, prec=5), '57.64911, 10.40744')
        t = g.toLatLon(LL)
        self.test('Garef.toLatLon', repr(t), 'LatLon(57°38′56.8″N, 010°24′26.78″E)')
        self.testCodec3(g, '57.625, 10.375, 2.0', prec=4)

        for t in range(-1, 4):
            r = gars.resolution(t)
            p = gars.precision(r)
            self.test('precision', t, p, known=t < 0 or t > 2)
            b = bearingDMS(r, form=F_DM, prec=0)
            self.test('resolution', b, b)  # just to show


if __name__ == '__main__':

    from pygeodesy import ellipsoidalVincenty

    t = Tests(__file__, __version__, gars)
    t.testGars(ellipsoidalVincenty.LatLon)
    t.results()
    t.exit()
