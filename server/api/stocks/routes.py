from flask import Blueprint


stocks_blueprint = Blueprint("stocks", __name__)


@stocks_blueprint.route("/<str:ticker>/")
def get_stocks(ticker: str):
    print(f"{ticker}")
