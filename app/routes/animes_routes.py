from flask import Blueprint
from app.controllers import animes_controller

bp = Blueprint('animes', __name__, url_prefix='/animes')

bp.get('')(animes_controller.animes)
bp.get('<anime_id>')(animes_controller.anime_by_id)
bp.post('')(animes_controller.create)
bp.patch('<anime_id>')(animes_controller.update)
bp.delete('<anime_id>')(animes_controller.delete)


