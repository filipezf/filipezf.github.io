import asyncio
import websockets
import json

connections = {}

async def hello(websocket, path):
    while True:
        try:
            data = await websocket.recv()            

            group = json.loads( data)['group']
            
            if group not in connections:
                connections[group] = set()
            wsarray = connections[group]
            if websocket not in wsarray:
                wsarray.add( websocket)

            wsarray2 =  set()
            #print(1)
            for ws in wsarray:
               try:
                    await ws.send(data)
                    #print(2)
               except Exception as e:
                    print( e)
                    continue
               wsarray2.add(ws)
            connections[group] = wsarray2
        except Exception as e:
            print( e)
            return        

start_server = websockets.serve(hello, "192.168.1.106", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
