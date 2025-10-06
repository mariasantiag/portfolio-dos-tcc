from flask import Flask, render_template, request, redirect
import datetime
import mysql.connector
from models.control_tcc import Tcc
from models.control_curso_orientador import Curso_orientador
from models.control_destaques import Destaques
from models.control_recentes import Recentes
from models.control_usuario_admin import Usuario

from flask import session
app = Flask(__name__)
app.secret_key = "seila2"