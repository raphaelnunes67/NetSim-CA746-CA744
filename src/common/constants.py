from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class FixedValuesCA746:
    INSERTION_ORDER = [6, 13, 23, 10, 16, 14, 26, 8, 11, 4, 21, 18, 7, 1, 15, 20, 12, 5, 25, 17, 22, 2, 24, 9, 3, 19]
    KWH_FOR_EACH_EV = [24, 20, 17, 4.4, 12, 20, 8, 12, 16, 17, 24, 24, 17, 24, 16, 41.8, 41.8, 20, 24, 4.4, 85, 20, 8,
                       23, 22, 85]
    PV_SHAPES = ['pv_shape_rainy', 'pv_shape_cloudy', 'pv_shape_varied', 'pv_shape_varied', 'pv_shape_rainy',
                 'pv_shape_cloudy', 'pv_shape_cloudy']
    PHASES = [(1, 2), (2, 3), (1, 2), (2, 3), (2, 3), (2, 3), (1, 3), (1, 2), (1, 2), (1, 3), (1, 3), (1, 3), (1, 2),
              (1, 3), (1, 3), (2, 3), (1, 2), (1, 3), (2, 3), (1, 2), (1, 3), (1, 2), (2, 3), (2, 3), (2, 3), (2, 3)]
    EV_CHARGERS_POWERS = [3.6, 3.6, 7.2, 7.2, 7.2, 3.6, 7.2, 7.2, 7.2, 7.2, 7.2, 7.2, 3.6, 7.2, 7.2, 7.2, 3.6, 7.2, 7.2,
                          7.2, 7.2, 7.2, 7.2, 7.2, 7.2, 7.2]
    MAX_PV_POWER = [5, 9, 10, 8, 6, 7, 6, 5, 5, 9, 8, 10, 5, 10, 8, 5, 8, 6, 8, 6, 9, 10, 8, 7, 7, 7]

    EV_SHAPES_BY_DAY = {
        1: [1638, 1397, 2232, 1965, 2215, 621, 480, 1837, 1833, 416, 4908, 1512, 1741, 3631, 2832, 4573, 2541, 1546,
            4857,
            368, 1960, 3490, 4437, 822, 897, 2692],
        2: [4968, 4954, 1630, 2753, 161, 4837, 3961, 1955, 664, 3343, 1654, 825, 1964, 2462, 2354, 4393, 607, 4410,
            3775,
            4815, 1448, 457, 117, 2529, 1024, 4539],
        3: [3881, 2286, 2420, 1533, 1288, 4341, 518, 3060, 4254, 4717, 4114, 1440, 3006, 4853, 2927, 3475, 4412, 3425,
            2043, 3754, 2132, 3712, 3328, 2379, 2356, 1472],
        4: [888, 4769, 4563, 2040, 2264, 2487, 2257, 1995, 211, 2359, 2572, 3548, 33, 458, 1218, 4777, 4898, 1258, 3700,
            2968, 1466, 3702, 2856, 3817, 2678, 2731],
        5: [107, 4130, 2830, 4783, 1472, 4868, 2421, 750, 3079, 1940, 2470, 1482, 563, 1333, 2136, 1088, 1765, 1029,
            4878,
            4234, 2873, 1651, 2309, 3684, 4724, 4805],
        6: [319, 4377, 134, 4596, 1896, 3392, 2316, 4756, 29, 2215, 73, 4552, 1563, 2938, 1171, 1814, 1600, 1946, 2703,
            630, 2308, 2494, 953, 4011, 1595, 2896],
        7: [2077, 415, 201, 2804, 2044, 4781, 444, 1616, 643, 1981, 4615, 11, 4156, 3493, 1145, 4184, 673, 3809, 4178,
            1278, 2422, 2112, 3728, 325, 4206, 2808]
    }


@dataclass(frozen=True)
class FixedValuesCA744:
    INSERTION_ORDER = [26, 35, 42, 29, 8, 14, 20, 23, 31, 7, 10, 17, 43, 28, 24, 4, 25, 18, 30, 41, 37, 44, 21, 33, 11,
                       46, 40, 47, 3, 36, 13, 39, 34, 27, 15, 5, 16, 45, 1, 19, 9, 32, 22, 2, 6, 12, 38]
    KWH_FOR_EACH_EV = [41.8, 4.4, 4.4, 16, 12, 4.4, 22, 24, 23, 8, 17, 85, 23, 12, 8, 85, 22, 85, 20, 22, 22, 41.8, 85,
                       23, 22, 20, 85, 12, 8, 12, 16, 61, 61, 61, 4.4, 8, 20, 85, 4.4, 41.8, 12, 4.4, 61, 20, 20, 85,
                       23]
    PV_SHAPES = ['pv_shape_rainy', 'pv_shape_cloudy', 'pv_shape_varied', 'pv_shape_varied', 'pv_shape_rainy',
                 'pv_shape_cloudy', 'pv_shape_cloudy']
    PHASES = [(1, 2), (1, 2), (1, 2), (1, 3), (2, 3), (1, 2), (1, 2), (1, 3), (1, 2), (1, 2), (1, 3), (1, 2), (1, 3),
              (2, 3), (1, 2), (1, 3), (2, 3), (1, 2), (2, 3), (1, 2), (2, 3), (1, 2), (1, 3), (1, 3), (1, 3), (1, 2),
              (1, 2), (2, 3), (2, 3), (2, 3), (1, 2), (1, 2), (1, 2), (2, 3), (2, 3), (1, 3), (1, 3), (1, 2), (2, 3),
              (1, 3), (1, 3), (2, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3)]
    EV_CHARGERS_POWERS = [7.2, 7.2, 7.2, 3.6, 7.2, 3.6, 3.6, 3.6, 7.2, 7.2, 3.6, 7.2, 7.2, 3.6, 3.6, 3.6, 7.2, 7.2, 3.6,
                          3.6, 3.6, 7.2, 7.2, 3.6, 7.2, 3.6, 7.2, 7.2, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 7.2, 7.2, 7.2,
                          7.2, 3.6, 7.2, 7.2, 3.6, 3.6, 7.2, 3.6, 3.6]
    MAX_PV_POWER = [7, 7, 8, 10, 10, 9, 6, 10, 6, 5, 7, 8, 6, 9, 6, 7, 10, 6, 6, 9, 7, 8, 9, 10, 5, 6, 5, 6, 10, 9, 5,
                    5, 9, 10, 8, 6, 6, 9, 7, 6, 6, 7, 8, 10, 10, 9, 8]

    EV_SHAPES_BY_DAY = {
        1: [3686, 3766, 342, 2613, 3986, 2960, 3508, 2978, 3950, 2593, 3288, 4292, 3463, 1740, 2736, 2743, 1701, 4015,
            142, 92, 4640, 2730, 3236, 5000, 3221, 1469, 2358, 1770, 3412, 111, 2379, 1307, 452, 211, 1774, 3573, 1076,
            2282, 3299, 3588, 1164, 3788, 579, 4838, 3453, 1460, 2208],
        2: [3258, 3720, 1572, 2728, 3598, 676, 1892, 4097, 4002, 4882, 440, 2520, 667, 1563, 1363, 3919, 4931, 361,
            2016, 1890, 4234, 158, 696, 398, 1706, 3580, 3822, 2727, 2319, 4659, 4269, 3256, 3351, 3516, 1200, 2439,
            2020, 2208, 2590, 646, 3554, 663, 1790, 4727, 826, 2785, 3524],
        3: [2595, 2965, 802, 2318, 4158, 53, 2184, 3032, 4044, 158, 1183, 2725, 2120, 1405, 102, 857, 367, 4377, 2666,
            2340, 4963, 1004, 4613, 885, 131, 3461, 3, 2952, 3024, 4841, 776, 2856, 3284, 1308, 280, 3783, 4309, 940,
            2600, 218, 1400, 1538, 3272, 1982, 3294, 3475, 717],
        4: [1514, 4570, 411, 530, 3830, 3620, 1127, 225, 4510, 1970, 819, 4555, 2473, 3049, 3103, 3039, 2286, 4138,
            3738, 689, 4611, 178, 2180, 387, 4825, 3873, 3272, 4029, 3583, 2927, 3498, 846, 3139, 4367, 3350, 4467,
            1510, 1435, 4035, 4400, 1932, 4780, 3987, 1674, 1355, 2340, 4386],
        5: [437, 240, 1461, 1911, 4504, 749, 1868, 4511, 3915, 4423, 4501, 515, 2287, 270, 1369, 4831, 2146, 510, 4408,
            1895, 4320, 2618, 1505, 1867, 76, 545, 4074, 2844, 4409, 3978, 2956, 4975, 2820, 160, 4622, 3039, 4043,
            2976, 2139, 3871, 1163, 3874, 3190, 1019, 1062, 202, 4287],
        6: [793, 2905, 1721, 4550, 2207, 2608, 2022, 2441, 1789, 2938, 3417, 4204, 4176, 3768, 4124, 3930, 4301, 2671,
            2480, 3059, 1857, 170, 1701, 1528, 442, 2937, 1767, 4191, 4921, 2028, 311, 1262, 4333, 4441, 3541, 1067,
            4175, 535, 2065, 3970, 1672, 756, 2547, 4084, 2560, 4575, 4104],
        7: [1135, 132, 1455, 1688, 3609, 1191, 2675, 660, 2798, 4551, 3395, 4323, 2954, 4456, 1271, 2001, 4687, 3148,
            1555, 3245, 535, 4511, 3758, 1979, 371, 545, 4189, 829, 2569, 2535, 4421, 3782, 2387, 3595, 194, 1028, 4680,
            3000, 1956, 746, 1545, 3898, 2607, 2191, 2723, 488, 2780]}


class EvKwh(Enum):
    TOYOTA_RAV4_SUV = 41.8
    TESLA_MODEL_S = 85
    TOYOTA_PRIUS_PLUG_IN = 4.4
    RENAULT_FLUENCE_RENAULT_ZOE = 22
    OPEL_AMPERA_MITSUBISHI_I_MIEV_CITROEN_C_ZERO_PEUGEOT_ION = 16
    NISSAN_LEAF_FIAT_500E = 24
    FORD_FUSION_ENERGY = 8
    MIA_MIA = 12
    FORD_FOCUS_ELECTRIC = 23
    FORD_C_MAX_ENERGY = 8
    BYD_E6 = 61
    CHEVROLET_SPARK_HONDA_FIT_EV = 20
    CHEVROLET_VOLT = 17


class PVShapesPossibilities(Enum):
    PV_SHAPE_SUNNY = 'pv_shape_sunny'
    PV_SHAPE_RAINY = 'pv_shape_rainy'
    PV_SHAPE_CLOUDY = 'pv_shape_cloudy'
    PV_SHAPE_VARIED = 'pv_shape_varied'


class EvChargerPowerKw(Enum):
    MAX_KW = 7.2
    MIN_KW = 3.6


class MaxPowerPVKW(Enum):
    MAX_KW = 10
    MIN_KW = 5

EV_CHARGER_POWER_POSSIBILITIES = [5.225, 14.167, 2.933, 2.444, 10.72, 6.286, 2.286, 3.429, 3.2, 16.4, 19.0, 6.0, 3.2,
                                  4.989, 6.667, 6.892]


TARGET_LOADS_CA744 = """New Load.residence1    phases=3 bus1=CA744RES1    kV=0.220  kW=2.14002976    	pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence2    phases=3 bus1=CA744RES2    kV=0.220  kW=1.21622024      	pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence3    phases=3 bus1=CA744RES3    kV=0.220  kW=2.3452381    	pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence4    phases=3 bus1=CA744RES4    kV=0.220  kW=1.28571429    	pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence5    phases=3 bus1=CA744RES5    kV=0.220  kW=1.5921131   		pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence6    phases=3 bus1=CA744RES6    kV=0.220  kW=1.31934524       pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence7    phases=3 bus1=CA744RES7    kV=0.220  kW=1.53854167  		pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence8    phases=3 bus1=CA744RES8    kV=0.220  kW=2.05550595  		pf=0.92 model=1 conn=wye status=variable daily=RES-Type8-WE
    New Load.residence9    phases=3 bus1=CA744RES9    kV=0.220  kW=2.2756  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence10   phases=3 bus1=CA744RES10   kV=0.220  kW=2.1396	   		pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence11   phases=3 bus1=CA744RES11   kV=0.220  kW=2.1243  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence12   phases=3 bus1=CA744RES12   kV=0.220  kW=2.3327381  		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence13   phases=3 bus1=CA744RES13   kV=0.220  kW=1.490625    		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence14   phases=3 bus1=CA744RES14   kV=0.220  kW=1.2813    		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence15   phases=3 bus1=CA744RES15   kV=0.220  kW=1.05580357    	pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence16   phases=3 bus1=CA744RES16   kV=0.220  kW=1.54360119       pf=0.92 model=1 conn=wye status=variable daily=COM-Type4-WE
    New Load.residence17   phases=3 bus1=CA744RES17   kV=0.220  kW=1.4981 			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence18   phases=3 bus1=CA744RES18   kV=0.220  kW=1.9201			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence19   phases=3 bus1=CA744RES19   kV=0.220  kW=1.303  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence20   phases=3 bus1=CA744RES20   kV=0.220  kW=2.0966   		pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence21   phases=3 bus1=CA744RES21   kV=0.220  kW=2.3192 			pf=0.92 model=1 conn=wye status=variable daily=COM-Type4-WE
    New Load.residence22   phases=3 bus1=CA744RES22   kV=0.220  kW=1.17142857  		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence23   phases=3 bus1=CA744RES23   kV=0.220  kW=1.33630952   	pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence24   phases=3 bus1=CA744RES24   kV=0.220  kW=1.5518    		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence25   phases=3 bus1=CA744RES25   kV=0.220  kW=1.2792     		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence26   phases=3 bus1=CA744RES26   kV=0.220  kW=2.0719        	pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence27   phases=3 bus1=CA744RES27   kV=0.220  kW=1.4481  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence28   phases=3 bus1=CA744RES28   kV=0.220  kW=1.3716  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type10-WE
    New Load.residence29   phases=3 bus1=CA744RES29   kV=0.220  kW=2.2131  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence30   phases=3 bus1=CA744RES30   kV=0.220  kW=0.8829  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence31   phases=3 bus1=CA744RES31   kV=0.220  kW=2.1625  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence32   phases=3 bus1=CA744RES32   kV=0.220  kW=2.2475  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence33   phases=3 bus1=CA744RES33   kV=0.220  kW=2.36860119  		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence34   phases=3 bus1=CA744RES34   kV=0.220  kW=1.614   			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence35   phases=3 bus1=CA744RES35   kV=0.220  kW=1.11354167    	pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence36   phases=3 bus1=CA744RES36   kV=0.220  kW=2.1438       	pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence37   phases=3 bus1=CA744RES37   kV=0.220  kW=2.19300595 		pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence38   phases=3 bus1=CA744RES38   kV=0.220  kW=2.48154762 		pf=0.92 model=1 conn=wye status=variable daily=COM-Type1-WE
    New Load.residence39   phases=3 bus1=CA744RES39   kV=0.220  kW=0.9234  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence40   phases=3 bus1=CA744RES40   kV=0.220  kW=2.1765   		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence41   phases=3 bus1=CA744RES41   kV=0.220  kW=2.3603 			pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence42   phases=3 bus1=CA744RES42   kV=0.220  kW=1.6631  			pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence43   phases=3 bus1=CA744RES43   kV=0.220  kW=1.8725			pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence44   phases=3 bus1=CA744RES44   kV=0.220  kW=1.25952381    	pf=0.92 model=1 conn=wye status=variable daily=RES-Type9-WE
    New Load.residence45   phases=3 bus1=CA744RES45   kV=0.220  kW=2.0213      		pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence46   phases=3 bus1=CA744RES46   kV=0.220  kW=2.2362       	pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence47   phases=3 bus1=CA744RES47   kV=0.220  kW=2.2312 			pf=0.92 model=1 conn=wye status=variable daily=COM-Type8-WE """

TARGET_LOADS_CA746 = """New Load.residence1   phases=3 bus1=CA746RES1   kV=0.220  kW=2.500     pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence2   phases=3 bus1=CA746RES2   kV=0.220  kW=3.024   pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence3   phases=3 bus1=CA746RES3   kV=0.220  kW=2.604   pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence4   phases=3 bus1=CA746RES4   kV=0.220  kW=2.749  pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence5   phases=3 bus1=CA746RES5   kV=0.220  kW=2.635   pf=0.92 model=1 conn=wye status=variable daily=RES-Type5-WE
    New Load.residence6   phases=3 bus1=CA746RES6   kV=0.220  kW=2.377   pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence7   phases=3 bus1=CA746RES7   kV=0.220  kW=2.170   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence8   phases=3 bus1=CA746RES8   kV=0.220  kW=2.995   pf=0.92 model=1 conn=wye status=variable daily=RES-Type7-WE
    New Load.residence9   phases=3 bus1=CA746RES9   kV=0.220  kW=3.135   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence10  phases=3 bus1=CA746RES10  kV=0.220  kW=3.126   pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence11  phases=3 bus1=CA746RES11  kV=0.220  kW=2.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence12  phases=3 bus1=CA746RES12  kV=0.220  kW=2.700   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence13  phases=3 bus1=CA746RES13  kV=0.220  kW=2.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence14  phases=3 bus1=CA746RES14  kV=0.220  kW=2.726   pf=0.92 model=1 conn=wye status=variable daily=RES-Type4-WE
    New Load.residence15  phases=3 bus1=CA746RES15  kV=0.220  kW=2.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type5-WE
    New Load.residence16  phases=3 bus1=CA746RES16  kV=0.220  kW=2.300   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence17  phases=3 bus1=CA746RES17  kV=0.220  kW=2.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence18  phases=3 bus1=CA746RES18  kV=0.220  kW=2.726   pf=0.92 model=1 conn=wye status=variable daily=RES-Type8-WE
    New Load.residence19  phases=3 bus1=CA746RES19  kV=0.220  kW=2.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type9-WE
    New Load.residence20  phases=3 bus1=CA746RES20  kV=0.220  kW=2.817   pf=0.92 model=1 conn=wye status=variable daily=RES-Type1-WE
    New Load.residence21  phases=3 bus1=CA746RES21  kV=0.220  kW=3.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type2-WE
    New Load.residence22  phases=3 bus1=CA746RES22  kV=0.220  kW=3.726   pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence23  phases=3 bus1=CA746RES23  kV=0.220  kW=3.875   pf=0.92 model=1 conn=wye status=variable daily=RES-Type3-WE
    New Load.residence24  phases=3 bus1=CA746RES24  kV=0.220  kW=2.800   pf=0.92 model=1 conn=wye status=variable daily=RES-Type6-WE
    New Load.residence25  phases=3 bus1=CA746RES25  kV=0.220  kW=2.620   pf=0.92 model=1 conn=wye status=variable daily=RES-Type7-WE
    New Load.residence26  phases=3 bus1=CA746RES26  kV=0.220  kW=2.300   pf=0.92 model=1 conn=wye status=variable daily=RES-Type7-WE"""


PL_PERCENTAGES = (20, 40, 60, 80, 100)

class ColumnsMapVoltages(Enum):
    V1 = 1
    V2 = 3
    V3 = 5