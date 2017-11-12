# coding: utf-8

import asyncio
import logging
import os

from dopplerr.config import DopplerrConfig
from dopplerr.singleton import singleton
from dopplerr.tasks.periodic import PeriodicTask

log = logging.getLogger(__name__)

SPEED_LIMIT = 10
SPEED_WAIT_SEC = 0.1
VIDEO_FILES_EXT = [
    'asf',
    'avc',
    'avi',
    'divx',
    'm4v',
    'mkv',
    'mov',
    'mp4',
    'mpg',
    'ogv',
    'qt',
    'viv',
    'vp3',
    'wmv',
]


@singleton
class DiskScanner(PeriodicTask):
    job_id = 'scan_disk'
    seconds = 0
    minutes = 0
    hours = None
    enable_cfg = 'scanner.enable'

    def init(self):
        self.hours = DopplerrConfig().get_cfg_value('scanner.interval_hours')

    async def _run(self):
        basedir = DopplerrConfig().get_cfg_value('general.basedir')
        mapping = DopplerrConfig().get_cfg_value('general.mapping')
        media_dirs = []
        for mapp in mapping:
            _src, _, dst = mapp.partition('=')
            media_dirs.append(dst)
        log.debug("Scanning %s with media directories: %r", basedir, media_dirs)
        await self._scan(basedir, media_dirs=media_dirs)

    async def _scan(self, root, media_dirs=None):
        i = 0
        with os.scandir(root) as it:
            for entry in it:
                i += 1
                if i > SPEED_LIMIT:
                    # this allows the event loop to update
                    await asyncio.sleep(SPEED_WAIT_SEC)
                    i = 0
                if self.stopped:
                    return
                if media_dirs:
                    if entry.name in media_dirs:
                        await self._scan(entry.path, media_dirs=None)
                elif not entry.name.startswith('.'):
                    if entry.is_dir(follow_symlinks=False):
                        await self._scan(entry.path, media_dirs=None)
                    else:
                        if entry.name.rpartition('.')[2] in VIDEO_FILES_EXT:
                            await self._refresh_video(entry.path)

    async def _refresh_video(self, filepath):
        log.info("Video file found: %s", filepath)

    @property
    def interval_hours(self):
        return self.hours
