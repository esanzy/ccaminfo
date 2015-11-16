#-*-coding:utf-8-*-
# 공유 패키지에서 함수를 호출하기 위해 path지정을 해줌
import os, sys

reload(sys)
sys.setdefaultencoding('utf8')

cur_dir = os.path.dirname(os.path.abspath(__file__)) #현재 디렉터리 위치를 프로그램적으로 반환해줌 info.hadiye/site/app`
root_dir = os.path.dirname(os.path.dirname(cur_dir)) #부모의 부모 디렉터리를 반환해줌 info.hadiye
sys.path.insert(0,root_dir) #info.hadiye를 path환경변수에 추가하여 core 패키지에 접근할 수 있도록 함.


from flask import Flask, render_template, request

context = Flask(__name__)
context.secret_key = 'Kjo86yHb5jbERTZ8TpXV5.._E-h7<I#h*$hs9'

from views import context as view
context.register_blueprint(view)
