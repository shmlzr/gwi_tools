from waitress import serve
import app_dash
application = app_dash.app.server

serve(application, host='0.0.0.0', port=8501)