import core.save_logs as log
import push.send
import asyncio

if __name__ == "__main__":
    msg = log.download()
    asyncio.run(push.send.main('Dogee[OK]: CDN Log Download', msg))

