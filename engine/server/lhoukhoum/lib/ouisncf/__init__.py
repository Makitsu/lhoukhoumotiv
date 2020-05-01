from enum import Enum

_STOP_UIC = [87756486,87713040,87718007,87713412,87673202,87484006,87487603,87171926,87171009,87478404,87192039,87193003,87281006,87286005,87286542,87317263,87317586,87672006,87677005,87212027,87182014,87182063,87765008,87396002,87413013,87571000,87586008,87742007,87393009,87319012,87583005,87318964,87172270,87474007,87174276,87673400,87581009,87781005,87615286,87174003,87757625,87741009,87281071,87317057,87393702,87478073,87393579,87147322,87142109,87726000,87476317,87481788,87485227,87485490,87141002,87144006,87571216,87317065,87582478,87775007,87672253,87473207,87747006,87713131,87725689,87742320,87753657,87286302,87762906,87481754,87473108,87671339,87223263,87141150,87723197,87722025,87485003,87476002,87486449,87753004,87725705,87111849,87773002,87751008,87381509,87764001,87474338,87756056,87746008,87485300,87481002,87113001,87391003,87271007,87686006,87784009,87575001,87473181,87324095,87342014,87471003,87144451,87474155,87396408,87215012,87473009,87172254,87212225,87481705,87313882,87755009,87611004,87474098,87411017,87761007,87763029,87476606,87582668,87781278,87741132,87757674,87175042,87342006,87713545,87673004,87694109,87725002,87575142,87172007,87345009,87755629,87677120,87474239,87345025,87584052,87756403,87611244,87781104,87765107,87471300,87486019,87755447,87478107,87571240,87757526,87773200,87671008,87144014,87191007,87476200,87343004,87471508,87300822,87300863,87703975,8768666]

_STOP_CODE = ['FRXMT','FRABA','FRABG','FRACE','FRACG','FRACL','FRACN','FREAH','FRRHE','FRACR','FRADE','FRBQT','FRADI','FRADJ','FRADM','FRAEA','FRAEB','FRAEE','FRAEF','FRAEG','FRAEJ','FRAEK','FRAES','FRAET','FRAEZ','FRAFW','FRAGF','FRAGR','FRDHT','FRAIE','FRANG','FRAVG','FRBDT','FRBES','FRBFO','FRBIQ','FRBOJ','FRBZR','FRCCF','FRXCR','FRJCA','FRCMF','FRSTH','FRCVU','FRDJU','FRDOL','FRMPU','FREAJ','FREAM','FRHHD','FRECO','FREGU','FREIP','FREJC','FRENC','FREPL','FRESL','FRETA','FRFAC','FRFNI','FRGFI','FRGGP','FRGNB','FRGWE','FRHGU','FRHPN','FRHZA','FRHZK','FRJDQ','FRJEE','FRLAM','FRLDE','FRLLE','FRLNE','FRLPD','FRLPE','FRLRH','FRLRT','FRLSO','FRMAZ','FRMLT','FRMLV','FRMPL','FRMSC','FRMTE','FRXMK','FRMXN','FRNIC','FRNCY','FRNIT','FRNTE','FRPST','FRPMO','FRPNO','FRPLY','FRPGF','FRPIS','FRPLT','FRTGO','FRQRV','FRRNS','FRRNT','FRRSP','FRSAB','FRSBG','FRSBK','FRXSW','FRSNE','FRSNR','FRTHP','FRTLN','FRXYT','FRUIP','FRURD','FRVAF','FRVLA','FRVNE','FRXAC','FRXAG','FRXAI','FRXAT','FRXBD','FRXBH','FRXBV','FRXBY','FRXCC','FRXCD','FRXCX','FRXCZ','FRXDN','FRXHE','FRXJZ','FRXLD','FRXLE','FRXLR','FRXMM','FRXMW','FRXNA','FRXOG','FRXRN','FRXRO','FRXRS','FRXSB','FRXSH','FRXSK','FRXSY','FRXTB','FRXTD','FRXTH','FRXUY','FRXVS','FRXVT','FRTJA','FRTJB','FRXZP','FRPBE']

_STOP_NAME = ['menton','dijon ville','besançon viotte','dole ville','dax','angers st-laud','saumur','champagne-ardenne tgv','reims ville','laval','metz','forbach','dunkerque','lille-flandres','tourcoing','calais ville','boulogne-sur-mer ville','pau','hendaye','strasbourg','colmar','mulhouse','avignon centre','le mans','le havre','tours','agen','modane','versailles-chantiers','aix-en-provence tgv','angoulême','avignon tgv','rethel','brest','vitry-le-françois','biarritz','bordeaux st-jean','béziers','carcassonne','châlons-en-champagne','cannes','chambéry challes-les-eaux','calais fréthun','rang-du-fliers—verton','massy tgv','dol-de-bretagne','massy—palaiseau','meuse tgv','lorraine tgv','st-étienne châteaucreux','quimperlé','le croisic','surgères','st-maixent','nancy','épinal','vendôme—villiers-sur-loir','etaples—le touquet','facture—biganos','nîmes centre','orthez','guingamp','grenoble','montbard','mâcon ville','st-jean-de-maurienne—arvan','arles','hazebrouck','lyon st-exupéry tgv','la baule-escoublac','lamballe','lourdes','lille-europe','lunéville','lyon part-dieu','lyon perrache','la rochelle ville','lorient','les sables-d’olonne','miramas','mâcon—loché tgv','marne-la-vallée—chessy','montpellier st-roch','marseille st-charles','mantes-la-jolie','montélimar','morlaix','nice ville','annecy','niort','nantes','paris gare de l’est','paris montparnasse','paris gare du nord','paris gare de lyon','perpignan','poitiers','plouaret—trégor','futuroscope','arras','rennes','remiremont','rosporden','sablé-sur-sarthe','sarrebourg','st-brieuc','sedan','saverne','st-nazaire','haute-picardie tgv','toulon','toulouse matabiau','quimper','rouen rive droite','valence ville','valence tgv','vannes','arcachon','agde','aix-les-bains—le revard','antibes','bar-le-duc','béthune','beaune','bayonne','le creusot tgv','chalon-sur-saône','châtellerault','charleville-mézières','douai','hyères','st-jean-de-luz—ciboure','landerneau','lens','libourne','monaco—monte-carlo','montauban ville bourbon','narbonne','orange','redon','la roche-sur-yon','les arcs—draguignan','st-malo','st-pierre-des-corps','st-raphaël—valescure','sète','tarbes','st-dié','thionville','auray','valenciennes','vitré','belfort—montbéliard tgv','besançon-franche-comté tgv','nîmes pont du gard','paris bercy']

_STOP_POS = [(0,0)]

# class Price(object):
#     def __init__(self,price,category,type):
#         self.price =

class Category(Enum):
    S = 'seconde classe'
    SM = 'seconde classe (billet modifiable)'
    P = 'premiere classe'
    PM = 'premier classe (billet modifiable)'
    BP = 'business premiere'
    BPM = 'business premiere (billet modifiable)'

class Leg(object):
    def __init__(self,departure,arrival,distance=None):
        self.departure = departure
        self.arrival = arrival
        if distance is not None:
            self.distance = distance

    def _get_departure(self):
        return self.departure


class Trip(Leg):
    def __init__(self,departure,arrival,distance,departure_time=None,arrival_time=None,price=None,type=None):
        super().__init__(self,departure,arrival,distance)
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        if distance is not None:
            self.distance = distance
        if price is not None:
            self.price = price
        if type is not None:
            self.type = type

class Station(object):
    def __init__(self,name=None,code_uic=None,code_fr=None,lon=None,lat=None):
        if name is not None:
            self.name = name
        if code_uic is not None:
            self.code_uic = code_uic
        if code_fr is not None:
            self.code_fr = code_fr
        if lon is not None:
            self.lon = lon
        if lat is not None:
            self.lat = lat

    @classmethod
    def from_uic(cls, code_uic):
        idx = _STOP_UIC.index(code_uic)
        return cls(_STOP_NAME[idx],code_uic,_STOP_CODE[idx])

    @classmethod
    def from_code(cls,code_fr):
        idx = _STOP_CODE.index(code_fr)
        return cls(_STOP_NAME[idx],_STOP_UIC[idx],code_fr)

    @classmethod
    def from_name(cls,name):
        idx = _STOP_NAME.index(name)
        return cls(name,_STOP_UIC[idx],_STOP_CODE[idx])




print(Station.from_code('FRPBE').name)