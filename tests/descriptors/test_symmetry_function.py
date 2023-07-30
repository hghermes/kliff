import itertools
from collections import OrderedDict

import numpy as np

from kliff.dataset import Configuration
from kliff.descriptors import SymmetryFunction

zeta_ref = [
    [
        8.26552746e-01,
        8.21898457e-01,
        7.76968604e-01,
        8.23872603e-01,
        7.82434629e-01,
        1.09924878e-02,
        8.97010397e-02,
        3.12057742e-02,
        2.19188995e-01,
    ],
    [
        1.97203988e00,
        1.96235440e00,
        1.86742677e00,
        1.96646887e00,
        1.87994799e00,
        1.33160610e-01,
        3.59292937e-02,
        1.94138336e00,
        3.60417941e-01,
    ],
    [
        1.12436604e00,
        1.11713094e00,
        1.04704155e00,
        1.12020088e00,
        1.05573420e00,
        1.44717148e-02,
        6.77068300e-02,
        4.65310973e-01,
        2.10094069e-01,
    ],
    [
        6.14948682e-01,
        6.10954381e-01,
        5.72406435e-01,
        6.12648545e-01,
        5.77088606e-01,
        7.40196968e-04,
        6.38212636e-03,
        5.59365334e-02,
        4.53723038e-02,
    ],
    [
        1.14547465e00,
        1.13801776e00,
        1.06581102e00,
        1.14118167e00,
        1.07474500e00,
        1.55422421e-02,
        8.48799596e-02,
        4.80992881e-01,
        2.40807811e-01,
    ],
    [
        5.85871635e-01,
        5.81613611e-01,
        5.40597021e-01,
        5.83419313e-01,
        5.45526214e-01,
        6.59891283e-04,
        5.86380395e-03,
        6.00226823e-02,
        4.85641661e-02,
    ],
    [
        1.04728862e00,
        1.04008269e00,
        9.70373031e-01,
        1.04313984e00,
        9.78952121e-01,
        1.14097233e-02,
        6.60188471e-02,
        3.84706149e-01,
        2.02570556e-01,
    ],
    [
        5.57949531e-01,
        5.53995531e-01,
        5.15882607e-01,
        5.55672409e-01,
        5.20480097e-01,
        5.08434077e-04,
        3.87820957e-03,
        5.09993748e-02,
        3.56988064e-02,
    ],
]


dzetadr_forces_ref = np.asarray(
    [
        [
            [4.36847504e-01, 4.56082915e-01, 4.50519405e-01],
            [-1.84069542e-01, -2.01194024e-01, -2.02724165e-01],
            [1.76857943e-03, -1.16115206e-01, -1.07502830e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.37353130e-01, -7.41597016e-03, -1.44139663e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.17193411e-01, -1.31357715e-01, 3.84725255e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [4.35016626e-01, 4.54048374e-01, 4.48711580e-01],
            [-1.84606520e-01, -2.01780958e-01, -2.03315563e-01],
            [1.74955899e-03, -1.14866428e-01, -1.06346675e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.36132117e-01, -7.35004524e-03, -1.42858320e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.16027547e-01, -1.30050942e-01, 3.80897930e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [4.17313856e-01, 4.34532633e-01, 4.31282231e-01],
            [-1.89728358e-01, -2.07379294e-01, -2.08956476e-01],
            [1.56788129e-03, -1.02938469e-01, -9.53034243e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.24321156e-01, -6.71234782e-03, -1.30463787e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.04832223e-01, -1.17502522e-01, 3.44145661e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [4.35793365e-01, 4.54910819e-01, 4.49478310e-01],
            [-1.84378999e-01, -2.01532270e-01, -2.03064983e-01],
            [1.75761853e-03, -1.15395574e-01, -1.06836574e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.36650159e-01, -7.37801536e-03, -1.43401958e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.16521825e-01, -1.30604960e-01, 3.82520558e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [4.19485544e-01, 4.36820838e-01, 4.33386273e-01],
            [-1.89148627e-01, -2.06745630e-01, -2.08317992e-01],
            [1.58864896e-03, -1.04301961e-01, -9.65657843e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.25772937e-01, -6.79073237e-03, -1.31987299e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.06152629e-01, -1.18982515e-01, 3.48480318e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [2.13547824e-02, 1.92739839e-02, 1.96052494e-02],
            [-2.14110507e-03, 3.72433199e-04, -1.80943940e-03],
            [-7.00252608e-04, -7.25832918e-03, -6.77879924e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-9.74799430e-03, -2.49068235e-03, -1.04166739e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-8.76543043e-03, -9.89740553e-03, -6.00336878e-04],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [1.29547740e-01, 1.29289130e-01, 1.36661542e-01],
            [5.77441299e-05, -1.95793422e-02, -9.69770698e-03],
            [1.35724929e-02, -6.24556733e-02, -5.67006195e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-8.52130601e-02, 1.82240210e-02, -8.83871026e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-5.79649175e-02, -6.54781359e-02, 1.81238875e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [6.41890870e-02, 6.38945753e-02, 5.84221889e-02],
            [-1.12089714e-02, -5.12865512e-03, -6.85855696e-03],
            [-6.01462738e-03, -2.04174966e-02, -1.95087873e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-2.28203652e-02, -1.19130547e-02, -2.40873379e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-2.41451231e-02, -2.64353689e-02, -7.96750667e-03],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
        [
            [3.23269932e-01, 3.41218095e-01, 3.35457366e-01],
            [-5.55305103e-02, -7.31208733e-02, -7.00558196e-02],
            [1.25248109e-02, -1.34365073e-01, -1.23415939e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.53245101e-01, 9.51729598e-03, -1.60433445e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
            [-1.27019131e-01, -1.43249445e-01, 1.84478383e-02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00],
        ],
    ]
).reshape(9, -1)

dzetadr_stress_ref = [
    [
        -8.27068658e-01,
        -9.22355278e-01,
        -8.90346571e-01,
        -5.40885540e-01,
        -5.57258314e-01,
        -5.49963350e-01,
    ],
    [
        -8.21666479e-01,
        -9.15858933e-01,
        -8.84650751e-01,
        -5.38245556e-01,
        -5.54811509e-01,
        -5.47206762e-01,
    ],
    [
        -7.69540279e-01,
        -8.53612009e-01,
        -8.29828262e-01,
        -5.13004587e-01,
        -5.31047742e-01,
        -5.20682746e-01,
    ],
    [
        -8.23957878e-01,
        -9.18612486e-01,
        -8.87066084e-01,
        -5.39364283e-01,
        -5.55850024e-01,
        -5.48375658e-01,
    ],
    [
        -7.75860518e-01,
        -8.60862624e-01,
        -8.36382569e-01,
        -5.15907778e-01,
        -5.34034418e-01,
        -5.23848521e-01,
    ],
    [
        -4.84237285e-02,
        -4.79243243e-02,
        -4.69958169e-02,
        -2.41700870e-02,
        -2.91529809e-02,
        -3.01895869e-02,
    ],
    [
        -3.58145732e-01,
        -3.77940811e-01,
        -3.92062577e-01,
        -1.31536449e-01,
        -1.83687217e-01,
        -1.35187197e-01,
    ],
    [
        -1.28646089e-01,
        -1.38565920e-01,
        -1.21160400e-01,
        -8.80616524e-02,
        -8.64183187e-02,
        -1.00120179e-01,
    ],
    [
        -7.58145220e-01,
        -8.58974738e-01,
        -8.23791155e-01,
        -3.96243998e-01,
        -4.23061086e-01,
        -4.03289631e-01,
    ],
]


def get_descriptor():
    cutfunc = "cos"
    cutvalue = {"Si-Si": 4.5}
    desc_params = OrderedDict()

    desc_params["g1"] = None
    desc_params["g2"] = [{"eta": 0.0009, "Rs": 0.0}, {"eta": 0.01, "Rs": 0.0}]
    desc_params["g3"] = [{"kappa": 0.03214}, {"kappa": 0.13123}]
    desc_params["g4"] = [
        {"zeta": 1, "lambda": -1, "eta": 0.0001},
        {"zeta": 2, "lambda": 1, "eta": 0.003},
    ]
    desc_params["g5"] = [
        {"zeta": 1, "lambda": -1, "eta": 0.0001},
        {"zeta": 2, "lambda": 1, "eta": 0.003},
    ]

    desc = SymmetryFunction(cutvalue, cutfunc, desc_params)

    return desc


def test_desc(test_data_dir):
    config = Configuration.from_file(test_data_dir / "configs" / "Si.xyz")

    desc = get_descriptor()

    for fit_forces, fit_stress in itertools.product([False, True], [False, True]):
        zeta, dzetadr_forces, dzetadr_stress = desc.transform(
            config, fit_forces, fit_stress
        )
        assert np.allclose(zeta, zeta_ref)
        if fit_forces:
            assert np.allclose(dzetadr_forces[0], dzetadr_forces_ref)
        if fit_stress:
            assert np.allclose(dzetadr_stress[0], dzetadr_stress_ref)
