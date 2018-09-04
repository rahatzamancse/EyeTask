import speech_recognition as sr


class Speech:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.commands = {
            "start": [],
            "stop": [],
            "left": [],
            "right": [],
            "video": [],
            "SMS": [],
            "music": [],
            "message": [],
            "light": [],
            "ceiling fan": [],
            "news": [],
            "wheel chair": [],
            "close": []
        }

    def recognize_speech_from_mic(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        response = {
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"

        if response["transcription"] in self.commands:
            print(response["transcription"] + " : executing ---")
            for func in self.commands[response["transcription"]]:
                func()

        else:
            print(response["transcription"])
            for func in self.commands["stop"]:
                func()

        return response
