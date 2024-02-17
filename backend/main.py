from configs import logger, app, db
from routes.routes import blueprint

app.register_blueprint(blueprint, url_prefix='/')

if __name__ == "__main__":
    # This allows the Flask app to accept connections from any IP address on your local network
    logger.info("Initializing app")
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5001)
