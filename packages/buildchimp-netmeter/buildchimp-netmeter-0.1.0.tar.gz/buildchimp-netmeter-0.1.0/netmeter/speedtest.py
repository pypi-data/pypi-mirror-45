from speedtest import Speedtest
import time

def speedtest(sender, prefix, config):
    test = Speedtest()
    test.get_best_server()

    print("Checking download speed...")
    test.download()
    print("Checking upload speed...")
    test.upload()

    now = int(time.time())
    result = test.results.dict()

    sender.send_raw(f"{prefix}.netspeed.download {result['download']} {now}")
    sender.send_raw(f"{prefix}.netspeed.upload {result['upload']} {now}")
