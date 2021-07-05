import wiotp.sdk.device
import time
import os
import datetime
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import playsound
from gtts import gTTS


authenticator = IAMAuthenticator ('GM7I_XNpNarDZ_wnMsYAdQKK-lVCiNbyVBSdadJb58kq')
text_to_speech = TextToSpeechV1 (
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/bf7d8d72-ff45-48a3-a393-702d9c12efe1')

myConfig = {
    "identity": {
        "orgId": "msyvvg",
        "typeId": "NodeMCU",
        "deviceId": "1456789"
    },
    "auth": {
        "token": "6l3W?LY!44MW((KjiM"
    }
}
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

def myCommandCallback(cmd):
    print("Message received from IBM IOT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    with open('medicine.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                'You have to take '+m+' medicine now',
                voice='en-US_Allisonv3Voice',
                accept='audio/mp3'
            ).get_result().content)
    playsound.playsound("medicine.mp3")
    os.system("mpg321 medicine.mp3")
    os.remove("medicine.mp3")
    return

while True:
#myData={'Face detection': detect}
#client.publishEvent (eventId="status", msgFormat="json", data=myData, qos=0, onPublish-None)
    client.commandCallback  = myCommandCallback
client.disconnect()
