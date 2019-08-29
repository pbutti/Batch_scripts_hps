class GeometryMapper:

    #Members

    detGeoMap = {}
    detGeoMap["nominal"]= "HPS-PhysicsRun2019-v1-4pt5"
    detGeoMap["SVT_07"] = "HPS-PhysicsRun2019-v1-4pt5-0-7mm"
    location = "detector-data/detectors/"

    def getGeoFile(self,det):
        return self.location+self.detGeoMap[det]+"/"+self.detGeoMap[det]+".lcdd"
