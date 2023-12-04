#!/usr/bin/env python3
# -*- coding:utf-8; line-length:80 -*-

import sys
import os
import time
import argparse

class FetchInput:
    def __init__(self, args=None):
        # Default to AdventOfCode time (EST)
        os.environ['TZ'] = 'EST'
        time.tzset()

        gameTime = time.localtime()

        self.sessionKey = os.getenv('AOC_SESSION_KEY')
        self.year = gameTime.tm_year
        self.day = gameTime.tm_mday
        self.output = 'input'

        self.ParseArgs(args)

    def ParseArgs(self, args):
        parser = argparse.ArgumentParser(
            description="Grab the input for an Advent of Code puzzle",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-s', '--session-key',
                            dest='sessionKey',
                            default=self.sessionKey,
                            help=('Login session key from https://adventofcode.com/.\n'
                                  'You can retrieve it from your browser.'
                                  ' fetch_input will look for it on the command\n'
                                  'line or in $AOC_SESSION_KEY. You MUST provide'
                                  ' your own unique session key or you will get\n'
                                  'the wrong input file.'))
        parser.add_argument('-y', '--year', type=int, default=self.year,
                            help='Year from which to retrieve the input')
        parser.add_argument('-d', '--day', type=int, default=self.day,
                            help='Day from which to retrieve the input')
        parser.add_argument('-o', '--output', default=self.output,
                            help='Output file name')
        
        # Parse arguments directly into self
        parser.parse_args(args, self)
        if not self.sessionKey:
            parser.error("You must provide a valid session key,\n"
                         "either with the -s/--session-key option or in $AOC_SESSION_KEY.\n"
                         "The session key is required to get the correct input file")
            # parser.error does not return

    def Run(self):
        # Ensure that the session key starts with 'session='
        if not self.sessionKey.startswith('session='):
            self.sessionKey = 'session=' + self.sessionKey

        os.execlp(
            "curl", # command to run
            "curl", # args (including argv[0])
            "--cookie", self.sessionKey,
            "--no-progress-meter",
            "--output", self.output,
            "--write-out", ("%{filename_effective}: %{size_download} bytes"
                            " retrieved in %{time_total}s"
                            f" for {self.year} day {self.day}\n"),
            f"https://adventofcode.com/{self.year}/day/{self.day}/input"
            )
        # os.execlp does not return

if __name__ == '__main__':
    cmd = FetchInput()
    cmd.Run()
    # cmd.Run does not return
