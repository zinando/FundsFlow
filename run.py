from myapp import app, socketio

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=8036, debug=True)
    app.run(debug=True)
