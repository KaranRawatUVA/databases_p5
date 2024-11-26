from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class School(db.Model):
    school_name = db.Column(db.String(100), primary_key=True, nullable=False)
    school_state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    mascot = db.Column(db.String(50), nullable=False)


class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    player_weight = db.Column(db.Integer, nullable=False)
    player_year = db.Column(db.Integer, nullable=False)
    school_name = db.Column(db.String(100), db.ForeignKey('school.school_name'), nullable=False)


class Conference(db.Model):
    conference_name = db.Column(db.String(100), primary_key=True, nullable=False)
    division = db.Column(db.Integer, nullable=False)


class CompetesInConference(db.Model):
    school_name = db.Column(db.String(100), db.ForeignKey('school.school_name'), primary_key=True, nullable=False)
    school_year = db.Column(db.Integer, primary_key=True, nullable=False)
    conference_name = db.Column(db.String(100), db.ForeignKey('conference.conference_name'), nullable=False)


class ScoutingReport(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), primary_key=True, nullable=False)
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
        {"school_name": "University of Virginia", "school_state": "Virginia", "city": "Charlottesville", "mascot": "Cavalier"},
        {"school_name": "Harvard University", "school_state": "Massachusetts", "city": "Cambridge", "mascot": "Crimson"},
        {"school_name": "Stanford University", "school_state": "California", "city": "Stanford", "mascot": "Cardinal"}
    ]
    for school in schools:
        new_school = School(
            school_name=school['school_name'],
            school_state=school['school_state'],
            city=school['city'],
            mascot=school['mascot']
        )
        db.session.add(new_school)
    db.session.commit()

    players = [
        {"number": 10, "last_name": "Doe", "first_name": "John", "position": "Forward", "height": 75, "player_weight": 180, "player_year": 2023, "school_name": "University of Virginia"},
        {"number": 12, "last_name": "Smith", "first_name": "Jane", "position": "Guard", "height": 68, "player_weight": 150, "player_year": 2023, "school_name": "Harvard University"},
        {"number": 14, "last_name": "Brown", "first_name": "Charlie", "position": "Center", "height": 85, "player_weight": 220, "player_year": 2023, "school_name": "Stanford University"}
    ]
    for player in players:
        new_player = Player(
            number=player['number'],
            last_name=player['last_name'],
            first_name=player['first_name'],
            position=player['position'],
            height=player['height'],
            player_weight=player['player_weight'],
            player_year=player['player_year'],
            school_name=player['school_name']
        )
        db.session.add(new_player)

    conferences = [
        {"conference_name": "ACC", "division": 1},
        {"conference_name": "Ivy League", "division": 1},
        {"conference_name": "Pac-12", "division": 1}
    ]
    for conference in conferences:
        new_conference = Conference(
            conference_name=conference['conference_name'],
            division=conference['division']
        )
        db.session.add(new_conference)

    scouting_reports = [
        {"player_id": 1, "report_date": date(2023, 11, 1), "scouting_description": "Strong offensive skills."},
        {"player_id": 2, "report_date": date(2023, 11, 2), "scouting_description": "Excellent defensive tactics."},
        {"player_id": 3, "report_date": date(2023, 11, 3), "scouting_description": "Great at team coordination."}
    ]
    for report in scouting_reports:
        new_report = ScoutingReport(
            player_id=report['player_id'],
            report_date=report['report_date'],
            scouting_description=report['scouting_description']
        )
        db.session.add(new_report)

    competes_in_conferences = [
        {"school_name": "University of Virginia", "school_year": 2023, "conference_name": "ACC"},
        {"school_name": "Harvard University", "school_year": 2023, "conference_name": "Ivy League"},
        {"school_name": "Stanford University", "school_year": 2023, "conference_name": "Pac-12"}
    ]
    for entry in competes_in_conferences:
        new_entry = CompetesInConference(
            school_name=entry['school_name'],
            school_year=entry['school_year'],
            conference_name=entry['conference_name']
        )
        db.session.add(new_entry)

    db.session.commit()


with app.app_context():
    populate_db()


@app.route("/get_school_name/<school_name>", methods=["GET"])
def get_school_name(school_name):
    team = School.query.filter_by(school_name=school_name).first()
    if team:
        team_data = {
            "school_name": team.school_name,
            "school_state": team.school_state,
            "city": team.city,
            "mascot": team.mascot
        }
        return jsonify(team_data), 200
    else:
        return jsonify({"error": "School not found"}), 404

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
                    "player_year": player.player_year
                } for player in players
            ]
        }
        return jsonify(team_data), 200
    else:
        return jsonify({"error": "School not found"}), 404


@app.route("/create_team", methods=["POST"])
def create_team():
    data = request.get_json()
    new_team = School(
        school_name=data['school_name'],
        school_state=data['school_state'],
        city=data['city'],
        mascot=data['mascot']
    )
    db.session.add(new_team)
    db.session.commit()
    return jsonify({"message": "School created successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)
