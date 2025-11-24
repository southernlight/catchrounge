from app.route.auth_routes import auth_bp,init_auth_routes
from app.route.main_routes import main_bp,init_main_routes
from app.route.table_routes import table_bp,init_table_routes
from app.route.reservation_routes import reservation_bp,init_reservation_routes
from app.route.simulation_routes import simulation_bp

def init_blueprints(app, services):

    app.register_blueprint(auth_bp)
    init_auth_routes(services['auth_service'])

    app.register_blueprint(main_bp)
    init_main_routes(services['user_service'], services['table_service'])

    app.register_blueprint(table_bp)
    init_table_routes(services['table_service'])

    app.register_blueprint(reservation_bp)
    init_reservation_routes(services['reservation_service'])

    app.register_blueprint(simulation_bp)
    