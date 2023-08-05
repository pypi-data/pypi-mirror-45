from wavedrom import render

test = """
{"signal": [
     { "name": "CLK_I", "wave": "P...." },
     { "name": "STB_O", "wave": "0<0111><1110>0" },
     { "name": "STB_O", "wave": "0.<.1..><1.0.>0" },
     { "name": "STB_O", "wave": "0.<..1.><1.0.>0" },
     { "name": "ACK_I", "wave": "0.<..1..0.>0" }
     ],
    "config": { "hscale": 2 },
    "head": { "tick": 0 }
   }
"""

render(test)