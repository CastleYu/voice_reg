import os.path
import traceback

import numpy as np
from flask import Flask, request, redirect, flash, jsonify
from flask_cors import CORS

import config
from action.action_matcher import *
from action.intent_recg import IntentRecognition
from audio.asr import PaddleSpeechRecognition, SpeechRecognitionAdapter
from audio.vector import PaddleSpeakerVerification, SpeakerVerificationAdapter
from config import AUDIO_TABLE, USER_TABLE, UPLOAD_FOLDER
from const import SUCCESS, FAILED
from dao import *
from utils.audioU import pre_process
from utils.fileU import check_file_in_request, save_file
from utils.responseU import QuickResponse as qr
