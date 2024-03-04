import requests

def mas():
    for i in range(100):
        url = "http://120.79.74.223:7099/instruct/instructIssued"
        if (i%2)==0:
            payload = {'plate': 'SN1245',
                       'devId': '101356000000',
                       'type': '8',
                       'str': '{"brightness":45,"cameraId":213,"chroma":178,"contrast":65,"photoInterval":1,"quality":3,"resolutionRatio":1,"saturation":78,"saveMark":1,"shootCommand":0}'}
        else:
            payload = {'plate': 'SN1245',
                       'devId': '101356000000',
                       'type': '5',
                       'str': '{"brightness":45,"cameraId":213,"chroma":178,"contrast":65,"photoInterval":1,"quality":3,"resolutionRatio":1,"saturation":78,"saveMark":1,"shootCommand":0}'}

        files = [

        ]
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'sessionId': '77884eaa-b323-42f2-af9d-1b53992275c5'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)



if __name__ == '__main__':
    mas()