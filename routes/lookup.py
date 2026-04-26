from flask import Blueprint, request, jsonify
from flask_login import login_required

from utils.dxcc import PREFIXES, EXACT_CALLS, get_country

lookup_bp = Blueprint("lookup", __name__)


@lookup_bp.route("/lookup")
@login_required
def lookup():
    call = request.args.get("call", "").strip().upper()
    if not call:
        return jsonify({"country": ""})
    country = get_country(call, PREFIXES, EXACT_CALLS)
    return jsonify({"country": country})
