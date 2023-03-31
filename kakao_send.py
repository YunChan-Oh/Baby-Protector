import requests
import json
    
    


def send_mesg():
    with open("kakao_code.json","r") as fp:
        tokens = json.load(fp)  

    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # kapi.kakao.com/v2/api/talk/memo/default/send 

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }

    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":"[긴급알림] 유아가 위험지역 침범",
            "link":{
                "web_url":"https://developers.kakao.com"
            }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    response.status_code

send_mesg()
