'''
Copyright (C) 2018-2019  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import asyncio
from multiprocessing import Process
import time
import logging

import redis

from cryptostore.data.storage import Storage
from cryptostore.config import Config


LOG = logging.getLogger('cryptostore')


class Aggregator(Process):
    def __init__(self, config_file=None):
        self.config_file = config_file
        self.last_id = {}
        super().__init__()

    def run(self):
        loop = asyncio.get_event_loop()
        self.config = Config(file_name=self.config_file)
        loop.create_task(self.loop())
        loop.run_forever()

    async def loop(self):
        if 'start_flush' in self.config.redis and self.config.redis['start_flush']:
            LOG.info('Flushing cache')
            redis.Redis(self.config.redis['ip'], port=self.config.redis['port']).flushall()

        while True:
            start = time.time()
            delete = self.config.redis['del_after_read']
            r = redis.Redis(self.config.redis['ip'], port=self.config.redis['port'], decode_responses=True)
            for exchange in self.config.exchanges:
                for dtype in self.config.exchanges[exchange]:
                    for pair in self.config.exchanges[exchange][dtype]:
                        key = f'{dtype}-{exchange}-{pair}'
                        store = Storage(self.config)
                        LOG.info('Reading %s', key)

                        data = r.xread({key: '0-0' if key not in self.last_id else self.last_id[key]})

                        if len(data) == 0:
                            LOG.info('No data for %s', key)
                            continue

                        agg = []
                        ids = []
                        for update_id, update in data[0][1]:
                            ids.append(update_id)
                            agg.append(update)

                        self.last_id[key] = ids[-1]

                        store.aggregate(agg)
                        store.write(exchange, dtype, pair, time.time())
                        if delete:
                            r.xdel(key, *ids)
                        LOG.info("Write Complete %s", key)

            total = time.time() - start
            interval = self.config.storage_interval - total
            if interval <= 0:
                LOG.warning("Storage operations currently take %.1f seconds, longer than the interval of %d", total, self.config.storage_interval)
                interval = 0.5
            await asyncio.sleep(interval)
