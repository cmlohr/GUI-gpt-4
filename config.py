# config.py
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

openai_api_key = config['OpenAI']['API_KEY']