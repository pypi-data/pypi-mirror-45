# coding:utf-8
from setuptools import setup, find_packages

setup(
    name='asched',
    description='asyncio sched',
    url='',
    version='1.2.0',
    license='MIT',
    install_requires=[
        'setuptools >= 0.7',
        'six >= 1.4.0',
        'pytz',
        'tzlocal >= 1.2',
    ],
    packages=find_packages(),

    entry_points={
        'asched.triggers': [
            'date = asched.triggers.date:DateTrigger',
            'interval = asched.triggers.interval:IntervalTrigger',
            'cron = asched.triggers.cron:CronTrigger',
            'and = asched.triggers.combining:AndTrigger',
            'or = asched.triggers.combining:OrTrigger'
        ],
        'asched.executors': [
            'debug = asched.executors.debug:DebugExecutor',
            'threadpool = asched.executors.pool:ThreadPoolExecutor',
            'processpool = asched.executors.pool:ProcessPoolExecutor',
            'asyncio = asched.executors.asyncio:AsyncIOExecutor [asyncio]'
        ],
        'asched.jobstores': [
            'memory = asched.jobstores.memory:MemoryJobStore'
        ]
    }
)
