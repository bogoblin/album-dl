from flask import render_template
import json

events = []


def process_event(download_event):
    events.append(download_event)
