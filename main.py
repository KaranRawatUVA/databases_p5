from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
from datetime import date, datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///teams.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class School(db.Model):
    school_name = db.Column(db.String(100), primary_key=True, nullable=False)
    school_state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    mascot = db.Column(db.String(50), nullable=False)


class Player(db.Model):
    player_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    number = db.Column(db.Integer, nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    player_weight = db.Column(db.Integer, nullable=False)
    player_year = db.Column(db.Integer, nullable=False)
    school_name = db.Column(
        db.String(100), db.ForeignKey("school.school_name"), nullable=False
    )


class Conference(db.Model):
    conference_name = db.Column(db.String(100), primary_key=True, nullable=False)
    division = db.Column(db.Integer, nullable=False)


class CompetesInConference(db.Model):
    school_name = db.Column(
        db.String(100),
        db.ForeignKey("school.school_name"),
        primary_key=True,
        nullable=False,
    )
    school_year = db.Column(db.Integer, primary_key=True, nullable=False)
    conference_name = db.Column(
        db.String(100), db.ForeignKey("conference.conference_name"), nullable=False
    )


class ScoutingReport(db.Model):
    player_id = db.Column(
        db.Integer, db.ForeignKey("player.player_id"), primary_key=True, nullable=False
    )
    report_date = db.Column(db.Date, primary_key=True, nullable=False)
    scouting_description = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


def clear_db():
    db.drop_all()
    db.create_all()


def populate_db():
    clear_db()
    schools = [
        {
            "school_name": "University of Virginia",
            "school_state": "Virginia",
            "city": "Charlottesville",
            "mascot": "Cavalier",
        },
        {
            "school_name": "Harvard University",
            "school_state": "Massachusetts",
            "city": "Cambridge",
            "mascot": "Crimson",
        },
        {
            "school_name": "Stanford University",
            "school_state": "California",
            "city": "Stanford",
            "mascot": "Cardinal",
        },
    ]
    for school in schools:
        new_school = School(
            school_name=school["school_name"],
            school_state=school["school_state"],
            city=school["city"],
            mascot=school["mascot"],
        )
        db.session.add(new_school)
    db.session.commit()

    players = [
        {
            "number": 10,
            "last_name": "Doe",
            "first_name": "John",
            "position": "Forward",
            "height": 75,
            "player_weight": 180,
            "player_year": 2023,
            "school_name": "University of Virginia",
        },
        {
            "number": 12,
            "last_name": "Smith",
            "first_name": "Jane",
            "position": "Guard",
            "height": 68,
            "player_weight": 150,
            "player_year": 2023,
            "school_name": "University of Virginia",
        },
        {
            "number": 14,
            "last_name": "Brown",
            "first_name": "Charlie",
            "position": "Center",
            "height": 85,
            "player_weight": 220,
            "player_year": 2023,
            "school_name": "Stanford University",
        },
    ]
    for player in players:
        new_player = Player(
            number=player["number"],
            last_name=player["last_name"],
            first_name=player["first_name"],
            position=player["position"],
            height=player["height"],
            player_weight=player["player_weight"],
            player_year=player["player_year"],
            school_name=player["school_name"],
        )
        db.session.add(new_player)

    conferences = [
        {"conference_name": "ACC", "division": 1},
        {"conference_name": "Ivy League", "division": 1},
        {"conference_name": "Pac-12", "division": 1},
    ]
    for conference in conferences:
        new_conference = Conference(
            conference_name=conference["conference_name"],
            division=conference["division"],
        )
        db.session.add(new_conference)

    scouting_reports = [
        {
            "player_id": 1,
            "report_date": date(2023, 11, 1),
            "scouting_description": "Strong offensive skills.",
        },
        {
            "player_id": 1,
            "report_date": date(2023, 11, 2),
            "scouting_description": "Excellent defensive tactics.",
        },
        {
            "player_id": 3,
            "report_date": date(2023, 11, 3),
            "scouting_description": "Great at team coordination.",
        },
    ]
    for report in scouting_reports:
        new_report = ScoutingReport(
            player_id=report["player_id"],
            report_date=report["report_date"],
            scouting_description=report["scouting_description"],
        )
        db.session.add(new_report)

    competes_in_conferences = [
        {
            "school_name": "University of Virginia",
            "school_year": 2023,
            "conference_name": "ACC",
        },
        {
            "school_name": "Harvard University",
            "school_year": 2023,
            "conference_name": "Ivy League",
        },
        {
            "school_name": "Stanford University",
            "school_year": 2023,
            "conference_name": "ACC",
        },
    ]
    for entry in competes_in_conferences:
        new_entry = CompetesInConference(
            school_name=entry["school_name"],
            school_year=entry["school_year"],
            conference_name=entry["conference_name"],
        )
        db.session.add(new_entry)

    db.session.commit()


with app.app_context():
    populate_db()


@app.route("/get_school/<school_name>", methods=["GET"])
def get_school_name(school_name):
    team = School.query.filter_by(school_name=school_name).first()
    if team:
        team_data = {
            "school_name": team.school_name,
            "school_state": team.school_state,
            "city": team.city,
            "mascot": team.mascot,
        }
        return jsonify(team_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


# get all the players in a certain school
@app.route("/get_players_team/<school_name>", methods=["GET"])
def get_players_team(school_name):
    team = School.query.filter_by(school_name=school_name).first()
    if team:
        players = Player.query.filter_by(school_name=school_name).all()
        team_data = {
            "school_name": team.school_name,
            "school_state": team.school_state,
            "city": team.city,
            "mascot": team.mascot,
            "players": [
                {
                    "player_id": player.player_id,
                    "number": player.number,
                    "last_name": player.last_name,
                    "first_name": player.first_name,
                    "position": player.position,
                    "height": player.height,
                    "player_weight": player.player_weight,
                    "player_year": player.player_year,
                }
                for player in players
            ],
        }
        return jsonify(team_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


# get player information for a certain id
@app.route("/get_player/<player_id>", methods=["GET"])
def get_player_id(player_id):
    player = Player.query.filter_by(player_id=player_id).first()
    if player:
        player_data = {
            "player_id": player.player_id,
            "number": player.number,
            "last_name": player.last_name,
            "first_name": player.first_name,
            "position": player.position,
            "height": player.height,
            "player_weight": player.player_weight,
            "player_year": player.player_year,
            "school_name": player.school_name,
        }
        return jsonify(player_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


@app.route("/get_conference_name/<conference_name>", methods=["GET"])
def get_conference_name(conference_name):
    conference = Conference.query.filter_by(conference_name=conference_name).first()
    if conference:
        conference_data = {
            "conference_name": conference.conference_name,
            "division": conference.division,
        }
        return jsonify(conference_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


@app.route("/get_teams_conference/<conference_name>", methods=["GET"])
def get_teams_conference(conference_name):
    conference = Conference.query.filter_by(conference_name=conference_name).first()
    if conference:
        teams = CompetesInConference.query.filter_by(
            conference_name=conference_name
        ).all()
        conference_data = {
            "conference_name": conference.conference_name,
            "division": conference.division,
            "teams": [
                {"school_name": team.school_name, "year": team.school_year}
                for team in teams
            ],
        }
        return jsonify(conference_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


@app.route("/get_scouting_report_id/<player_id>", methods=["GET"])
def get_scouting_report_id(player_id):
    player = Player.query.filter_by(player_id=player_id).first()
    if player:
        reports = ScoutingReport.query.filter_by(player_id=player_id).all()
        report_data = {
            "player_id": player.player_id,
            "number": player.number,
            "last_name": player.last_name,
            "first_name": player.first_name,
            "position": player.position,
            "height": player.height,
            "player_weight": player.player_weight,
            "player_year": player.player_year,
            "report": [
                {
                    "report_date": report.report_date,
                    "scouting_description": report.scouting_description,
                }
                for report in reports
            ],
        }
        return jsonify(report_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


@app.route("/create_team", methods=["POST"])
def create_team():
    data = request.get_json()
    new_team = School(
        school_name=data["school_name"],
        school_state=data["school_state"],
        city=data["city"],
        mascot=data["mascot"],
    )
    db.session.add(new_team)
    db.session.commit()
    return jsonify({"message": "School created successfully"}), 201


@app.route("/add_player", methods=["POST"])
def add_player():
    data = request.get_json()
    team = School.query.filter_by(school_name=data["school_name"]).first()
    if not team:
        return jsonify({"message": "Player not added due wrong team data"}), 409
    new_player = Player(
        number=data["number"],
        last_name=data["last_name"],
        first_name=data["first_name"],
        position=data["position"],
        height=data["height"],
        player_weight=data["player_weight"],
        player_year=data["player_year"],
        school_name=data["school_name"],
    )
    db.session.add(new_player)
    db.session.commit()
    return jsonify({"message": "Player added successfully"}), 201


@app.route("/create_conference", methods=["POST"])
def create_conference():
    data = request.get_json()
    new_conference = Conference(
        conference_name=data["conference_name"],
        division=data["division"],
    )
    db.session.add(new_conference)
    db.session.commit()
    return jsonify({"message": "Conference created successfully"}), 201


@app.route("/create_competes_in_conference", methods=["POST"])
def create_competes_in_conference():
    data = request.get_json()
    team = School.query.filter_by(school_name=data["school_name"]).first()
    if not team:
        return jsonify({"message": "Data not added due wrong team data"}), 409
    conference = Conference.query.filter_by(
        conference_name=data["conference_name"]
    ).first()
    if not conference:
        return jsonify({"message": "Data not added due wrong conference data"}), 409
    new_conference_info = CompetesInConference(
        conference_name=data["conference_name"],
        school_name=data["school_name"],
        school_year=data["school_year"],
    )
    db.session.add(new_conference_info)
    db.session.commit()
    return jsonify({"message": "Conference created successfully"}), 201


@app.route("/create_scouting_report", methods=["POST"])
def create_scouting_report():
    data = request.get_json()
    player = Player.query.filter_by(player_id=data["player_id"]).first()
    if not player:
        return (
            jsonify({"message": "Scouting Report not created due wrong player data"}),
            409,
        )
    new_scouting_report = ScoutingReport(
        player_id=data["player_id"],
        report_date=datetime.strptime(data["report_date"], "%Y-%m-%d"),
        scouting_description=data["scouting_description"],
    )
    db.session.add(new_scouting_report)
    db.session.commit()
    return jsonify({"message": "Scouting Report added successfully"}), 201


@app.route("/update_school/<school_name>", methods=["PUT"])
def update_school(school_name):
    school = School.query.filter_by(school_name=school_name).first()
    if not school:
        return jsonify({"message": "School not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    new_school_name = data.get("school_name")
    new_school_state = data.get("school_state")
    new_city = data.get("city")
    new_mascot = data.get("mascot")

    if new_school_name:
        school.school_name = new_school_name
    if new_school_state:
        school.school_state = new_school_state
    if new_city:
        school.city = new_city
    if new_mascot:
        school.mascot = new_mascot

    db.session.commit()
    return jsonify({"message": "School updated successfully"}), 200


@app.route("/update_player/<player_id>", methods=["PUT"])
def update_player(player_id):
    player = Player.query.filter_by(player_id=player_id).first()
    if not player:
        return jsonify({"message": "Player not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    new_player_id = data.get("player_id")
    new_number = data.get("number")
    new_last_name = data.get("last_name")
    new_first_name = data.get("first_name")
    new_position = data.get("position")
    new_height = data.get("height")
    new_player_weight = data.get("player_weight")
    new_player_year = data.get("player_year")
    new_school_name = data.get("school_name")

    if new_player_id:
        player.player_id = new_player_id
    if new_number:
        player.number = new_number
    if new_last_name:
        player.last_name = new_last_name
    if new_first_name:
        player.first_name = new_first_name
    if new_position:
        player.position = new_position
    if new_height:
        player.height = new_height
    if new_player_weight:
        player.player_weight = new_player_weight
    if new_player_year:
        player.new_player_year = new_player_year
    if new_school_name:
        player.school_name = new_school_name

    db.session.commit()
    return jsonify({"message": "Player updated successfully"}), 200


@app.route("/update_conference/<conference_name>", methods=["PUT"])
def update_conference(conference_name):
    conference = Conference.query.filter_by(conference_name=conference_name).first()
    if not conference:
        return jsonify({"message": "Conference not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    new_conference_name = data.get("conference_name")
    new_division = data.get("division")

    if new_conference_name:
        conference.conference_name = new_conference_name
    if new_division:
        conference.division = new_division

    db.session.commit()
    return jsonify({"message": "Conference updated successfully"}), 200


@app.route(
    "/update_competes_in_conference/<school_name>/<school_year>", methods=["PUT"]
)
def update_competes_in_conference(school_name, school_year):
    team_in_conference = CompetesInConference.query.filter_by(
        school_name=school_name, school_year=school_year
    ).first()
    if not team_in_conference:
        return jsonify({"message": "Team in conference not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    new_school_name = data.get("school_name")
    new_school_year = data.get("school_year")
    new_conference_name = data.get("conference_name")

    if new_school_name:
        team_in_conference.school_name = new_school_name
    if new_school_year:
        team_in_conference.school_year = new_school_year
    if new_conference_name:
        team_in_conference.conference_name = new_conference_name

    db.session.commit()
    return jsonify({"message": "Team in conference updated successfully"}), 200


@app.route("/update_scouting_report/<player_id>/<report_date>", methods=["PUT"])
def update_scouting_report(player_id, report_date):
    scouting_report = ScoutingReport.query.filter_by(
        player_id=player_id, report_date=report_date
    ).first()
    if not scouting_report:
        return jsonify({"message": "Scouting report not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    new_player_id = data.get("player_id")
    new_report_date = data.get("report_date")
    new_scouting_description = data.get("scouting_description")

    if new_player_id:
        scouting_report.player_id = new_player_id
    if new_report_date:
        scouting_report.report_date = new_report_date
    if new_scouting_description:
        scouting_report.scouting_description = new_scouting_description

    db.session.commit()
    return jsonify({"message": "Scouting report updated successfully"}), 200


@app.route("/delete_school/<school_name>", methods=["DELETE"])
def delete_school(school_name):
    school = School.query.filter_by(school_name=school_name).first()
    if not school:
        return jsonify({"message": "School not found"}), 404

    db.session.delete(school)
    db.session.commit()
    return jsonify({"message": "School deleted successfully"}), 200


@app.route("/delete_player/<player_id>", methods=["DELETE"])
def delete_player(player_id):
    player = Player.query.filter_by(player_id=player_id).first()
    if not player:
        return jsonify({"message": "Player not found"}), 404

    db.session.delete(player)
    db.session.commit()
    return jsonify({"message": "Player deleted successfully"}), 200


@app.route("/delete_conference/<conference_name>", methods=["DELETE"])
def delete_conference(conference_name):
    conference = Conference.query.filter_by(conference_name=conference_name).first()
    if not conference:
        return jsonify({"message": "Conference not found"}), 404

    db.session.delete(conference)
    db.session.commit()
    return jsonify({"message": "Conference deleted successfully"}), 200


@app.route(
    "/delete_competes_in_conference/<school_name>/<school_year>", methods=["DELETE"]
)
def delete_competes_in_conference(school_name, school_year):
    team_in_conference = CompetesInConference.query.filter_by(
        school_name=school_name, school_year=school_year
    ).first()
    if not team_in_conference:
        return jsonify({"message": "Team in conference not found"}), 404

    db.session.delete(team_in_conference)
    db.session.commit()
    return jsonify({"message": "Team in conference deleted successfully"}), 200


@app.route("/delete_scouting_report/<player_id>/<report_date>", methods=["DELETE"])
def delete_scouting_report(player_id, report_date):
    scouting_report = ScoutingReport.query.filter_by(
        player_id=player_id, report_date=report_date
    ).first()
    if not scouting_report:
        return jsonify({"message": "Scouting report not found"}), 404

    db.session.delete(scouting_report)
    db.session.commit()
    return jsonify({"message": "Scouting report deleted successfully"}), 200


# Serve the frontend (index.html)
@app.route("/")
def serve_frontend():
    return send_from_directory("frontend", "index.html")


# Serve other static files (like script.js or stylesheets)
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("frontend", path)


if __name__ == "__main__":
    app.run(debug=True)
