import astrology
import planets
import fortune
import houses
import util
import math


class Antiscion:
	'''Antiscion of a planet, LoF or AscMC'''

	ANTISCION = 0
	CONTRAANT = 1
	DODECATEMORIA = 2

	#Ids of planets are from module astrology

	#Ids
	LOF = astrology.SE_TRUE_NODE+1
	ASC = LOF+1
	MC = ASC+1

	def __init__(self, typ, Id, lon, lat, ra, decl):
		self.typ = typ
		self.Id = Id
		self.lon = lon
		self.lat = lat
		self.ra = ra
		self.decl = decl


class Antiscia:
	'''Computes antiscia of the bodies(planets, LoF, Asc and MC)'''

	CANCER0 = 90.0
	CAPRICORN0 = 270.0

	def __init__(self, pls, ascmc, lof, obl, ayanopt, ayan):
		self.obl = obl
		self.plantiscia = []
		self.plcontraant = []
		self.pldodecatemoria = []
		self.lofant = None
		self.lofcontraant = None
		self.lofdodec = None
		self.ascmcant = []
		self.ascmccontraant = []
		self.ascmcdodec = []

		self.ayanopt = ayanopt
		self.ayan = ayan

		plcants = []

		for i in range(planets.Planets.PLANETS_NUM):
			ant, cant = self.calc(pls[i].data[planets.Planet.LONG])
			dodec = self.calcDodecatemoria(pls[i].data[planets.Planet.LONG])
			lat = pls[i].data[planets.Planet.LAT]
			plcants.append((cant, lat))
			#self.pldodecatemoria.append((dodec, lat))

#			raant, declant = util.getRaDecl(ant, lat, self.obl)
			raant, declant, dist = astrology.swe_cotrans(ant, lat, 1.0, -obl)
			self.plantiscia.append(Antiscion(Antiscion.ANTISCION, i, ant, lat, raant, declant))
			self.pldodecatemoria.append(Antiscion(Antiscion.DODECATEMORIA, i, dodec, lat, raant, declant))
			
		for i in range(planets.Planets.PLANETS_NUM):
#			raant, declant = util.getRaDecl(plcants[i][0], plcants[i][1], self.obl)
			raant, declant, dist = astrology.swe_cotrans(plcants[i][0], plcants[i][1], 1.0, -obl)
			self.plcontraant.append(Antiscion(Antiscion.CONTRAANT, i, plcants[i][0], plcants[i][1], raant, declant))


		ant, cant = self.calc(lof[fortune.Fortune.LON])
		dodec = self.calcDodecatemoria(lof[fortune.Fortune.LON])
#		lat = lof[fortune.Fortune.LAT] #=0.0
		raant, declant, dist = astrology.swe_cotrans(ant, 0.0, 1.0, -self.obl)
		self.lofant = Antiscion(Antiscion.ANTISCION, Antiscion.LOF, ant, 0.0, raant, declant)
		raant, declant, dist = astrology.swe_cotrans(cant, 0.0, 1.0, -self.obl)
		self.lofcontraant = Antiscion(Antiscion.CONTRAANT, Antiscion.LOF, cant, 0.0, raant, declant)
		#Afegeixo LOF 
		raant, declant, dist = astrology.swe_cotrans(cant, 0.0, 1.0, -self.obl)
		self.lofdodec = Antiscion(Antiscion.DODECATEMORIA, Antiscion.LOF, dodec, 0.0, raant, declant)

		antasc, cantasc = self.calc(ascmc[houses.Houses.ASC])
		raantasc, declantasc, dist = astrology.swe_cotrans(antasc, 0.0, 1.0, -self.obl)
		self.ascmcant.append(Antiscion(Antiscion.ANTISCION, Antiscion.ASC, antasc, 0.0, raantasc, declantasc))

		antmc, cantmc = self.calc(ascmc[houses.Houses.MC])
		raantmc, declantmc, dist = astrology.swe_cotrans(antmc, 0.0, 1.0, -self.obl)
		self.ascmcant.append(Antiscion(Antiscion.ANTISCION, Antiscion.MC, antmc, 0.0, raantmc, declantmc))

		raantasc, declantasc, dist = astrology.swe_cotrans(cantasc, 0.0, 1.0, -self.obl)
		self.ascmccontraant.append(Antiscion(Antiscion.CONTRAANT, Antiscion.ASC, cantasc, 0.0, raantasc, declantasc))

		raantmc, declantmc, dist = astrology.swe_cotrans(cantmc, 0.0, 1.0, -self.obl)
		self.ascmccontraant.append(Antiscion(Antiscion.CONTRAANT, Antiscion.MC, cantmc, 0.0, raantmc, declantmc))

		dodecasc = self.calcDodecatemoria(ascmc[houses.Houses.ASC])
		raantasc, declantasc, dist = astrology.swe_cotrans(dodecasc, 0.0, 1.0, -self.obl)
		self.ascmcdodec.append(Antiscion(Antiscion.DODECATEMORIA, Antiscion.ASC, dodecasc, 0.0, raantasc, declantasc))

		dodecmc = self.calcDodecatemoria(ascmc[houses.Houses.MC])
		raantmc, declantmc, dist = astrology.swe_cotrans(antmc, 0.0, 1.0, -self.obl)
		self.ascmcdodec.append(Antiscion(Antiscion.DODECATEMORIA, Antiscion.MC, dodecmc, 0.0, raantmc, declantmc))

#		self.printants()


	def calc(self, lon):
		ant = 0.0

		#round because the antiscion was a little bit different
#		d,m,s = util.decToDeg(lon)
#		lon = float(d)+float(m)/60.0+float(s)/3600.0

		if lon == Antiscia.CANCER0 or lon == Antiscia.CAPRICORN0:
			ant = lon
		elif lon > Antiscia.CANCER0 and lon < Antiscia.CAPRICORN0:
			ant = util.normalize(Antiscia.CAPRICORN0+(Antiscia.CAPRICORN0-lon))
		elif lon < Antiscia.CANCER0:
			ant = util.normalize(Antiscia.CANCER0+(Antiscia.CANCER0-lon))
		elif lon > Antiscia.CAPRICORN0:
			ant = util.normalize(Antiscia.CAPRICORN0-(lon-Antiscia.CAPRICORN0))

		if self.ayanopt != 0:
			ant -= self.ayan
			ant = util.normalize(ant)

		cant = util.normalize(ant+180.0)

		return ant, cant


	def calcDodecatemoria(self, lon):
		if self.ayanopt != 0:
			lon -= self.ayan
			lon = util.normalize(lon)

		return self.KeepInZodiac(30*self.getSign(lon) + 12*self.getRelativeLon(lon))

	def KeepBetweenLimit(self, lon, lim):
		""" Keep the longitude between 0..lim """
		""" lon must be positive """
		return lon - math.floor(lon / lim) * lim
	
	def KeepInZodiac(self, lon):
		""" Keep the longitude between 0..360 """
		return self.KeepBetweenLimit(lon, 360)

	def getRelativeLon(self, lon):
		""" Returns the longitude relative to the zodiac """
		""" Ex. lon = 36 will return 6 (Taurus 6)"""
		return self.KeepBetweenLimit(lon, 30)

	def getSign(self, lon):
		""" Returns the sign: 0 - Aries, 1 - Taurus, 2 - Gemini..."""
		""" lon must be positive """
		return lon // 30

	def printants(self):
		plstxt = ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'AscNode', 'DescNode')
		anttxt = ('Antiscia', 'Contraantiscia')

		print ''
		print 'Antiscia'
		i = 0
		for ant in self.antiscia:
			if i < planets.Planets.PLANETS_NUM*2:
				print '%s %s %f %f %f %f' % (anttxt[ant.typ], plstxt[ant.Id], ant.lon, ant.lat, ant.ra, ant.decl)
			elif i == Antiscia.LOFANT or i == Antiscia.LOFCANT:
				print '%s %s %f %f %f %f' % (anttxt[ant.typ], 'LoF', ant.lon, ant.lat, ant.ra, ant.decl)
			elif i == Antiscia.ASCANT or i == Antiscia.ASCCANT:
				print '%s %s %f %f %f %f' % (anttxt[ant.typ], 'Asc', ant.lon, ant.lat, ant.ra, ant.decl)
			elif i == Antiscia.MCANT or i == Antiscia.MCCANT:
				print '%s %s %f %f %f %f' % (anttxt[ant.typ], 'MC', ant.lon, ant.lat, ant.ra, ant.decl)

			i += 1





