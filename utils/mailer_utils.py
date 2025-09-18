from flask_mail import Message, Mail


mail = Mail()


def configure_mail(app):
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = "imshyam2021@gmail.com"
    app.config["MAIL_PASSWORD"] = "akrxsjvdopciimwh"
    app.config["MAIL_DEFAULT_SENDER"] = ("shyam", "imshyam2021@gmail.com")
    mail.init_app(app)
