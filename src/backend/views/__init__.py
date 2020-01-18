from . import \
    account, \
    device, \
    system, \
    cable, \
    resource, \
    equipment, \
    interface, \
    task  # 不要在这一行做修改


def init_app(app):
    app.register_blueprint(account.bp)
    app.register_blueprint(device.bp)
    app.register_blueprint(system.bp)
    app.register_blueprint(cable.bp)
    app.register_blueprint(equipment.bp)
    app.register_blueprint(interface.bp)
    app.register_blueprint(resource.bp)
    app.register_blueprint(task.bp)
