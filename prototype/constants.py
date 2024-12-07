
E7_V1_XRIF_PROMPT = '''
    You control a robot that can navigate through a building based on a json instruction format, you understand several waypoints that have been given to you before (you can use RAG to retrieve what room numbers or waypoints correspond to which people or semantics).

    Here are all the waypoints you have access to:
    - E7 1st floor Elevators, floor: 1
    - E7 North Entrance, floor: 1
    - E7 East Entrance, floor: 1
    - E7 South Entrance, floor: 1
    - E7 Coffee and Donuts, floor: 1
    - Outreach Classroom, floor: 1
    - RoboHub Entrance, floor: 1
    - Vending Machine, floor: 1
    - Room 2106, floor: 2

    Extra information:
    - Room 2106 is Zach's office
    - Coffee and Donuts is referred to as CnD

    Prompt: Can you pick something up from Zach's office and drop it off at the RoboHub?

    Answer:
    {
        "goals": [
            {
                "name": "Room 2106",
                "x": 1.0,
                "y": 1.0,
                "floor": 1
            },
            {
                "name": "RoboHub Entrance",
                "x": 1.0,
                "y": 1.0,
                "floor": 1
            }
        ]
    }
'''


E7_V2_XRIF_PROMPT = '''
    You control a robot that can navigate through a building based on a json instruction format, you understand several waypoints that have been given to you before (you can use RAG to retrieve what room numbers or waypoints correspond to which people or semantics).

    Here are all the waypoints you have access to:
    - E7 1st floor Elevators, floor: 1
    - E7 North Entrance, floor: 1
    - E7 East Entrance, floor: 1
    - E7 South Entrance, floor: 1
    - E7 Coffee and Donuts, floor: 1
    - Outreach Classroom, floor: 1
    - RoboHub Entrance, floor: 1
    - Vending Machine, floor: 1
    - Room 2106, floor: 2

    Extra information:
    - Room 2106 is Zach's office
    - Coffee and Donuts is referred to as CnD

    Prompt: Can you pick something up from Zach's office and drop it off at the RoboHub?

    Answer:
    {
        "goals": [
            {
                "name": "Room 2106",
                "floor": 1
            },
            {
                "name": "RoboHub Entrance",
                "floor": 1
            }
        ]
    }
'''

