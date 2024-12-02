const BASE_URL = 'http://127.0.0.1:5000';

// Helper function to handle API calls
async function fetchData(endpoint, method = 'GET', body = null) {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${BASE_URL}${endpoint}`, options);
    const result = await response.json();
    document.getElementById('result').textContent = JSON.stringify(result, null, 2);
}

// School APIs
async function createSchool() {
    const data = {
        school_name: document.getElementById('create_school_name').value,
        school_state: document.getElementById('create_school_state').value,
        city: document.getElementById('create_school_city').value,
        mascot: document.getElementById('create_school_mascot').value,
    };
    fetchData('/create_team', 'POST', data);
}

async function updateSchool() {
    const schoolName = document.getElementById('update_school_name').value;
    const data = {
        school_state: document.getElementById('update_new_school_state').value,
        city: document.getElementById('update_new_school_city').value,
        mascot: document.getElementById('update_new_school_mascot').value,
    };
    fetchData(`/update_school/${schoolName}`, 'PUT', data);
}

async function deleteSchool() {
    const schoolName = document.getElementById('delete_school_name').value;
    fetchData(`/delete_school/${schoolName}`, 'DELETE');
}

async function getSchool() {
    const schoolName = document.getElementById('get_school_name').value;
    fetchData(`/get_school/${schoolName}`, 'GET');
}

// Fetch all players in a school
async function getPlayersTeam() {
    const schoolName = document.getElementById('get_players_team_school_name').value;
    fetchData(`/get_players_team/${schoolName}`, 'GET');
}


// Player APIs
async function createPlayer() {
    const data = {
        number: document.getElementById('create_player_number').value,
        last_name: document.getElementById('create_player_last_name').value,
        first_name: document.getElementById('create_player_first_name').value,
        position: document.getElementById('create_player_position').value,
        height: document.getElementById('create_player_height').value,
        player_weight: document.getElementById('create_player_weight').value,
        player_year: document.getElementById('create_player_year').value,
        school_name: document.getElementById('create_player_school').value,
    };
    fetchData('/add_player', 'POST', data);
}

async function updatePlayer() {
    const playerId = document.getElementById('update_player_id').value;
    const data = { school_name: document.getElementById('update_new_player_school').value };
    fetchData(`/update_player/${playerId}`, 'PUT', data);
}

async function deletePlayer() {
    const playerId = document.getElementById('delete_player_id').value;
    fetchData(`/delete_player/${playerId}`, 'DELETE');
}

async function getPlayer() {
    const playerId = document.getElementById('get_player_id').value;
    fetchData(`/get_player/${playerId}`, 'GET');
}

// Conference APIs
async function createConference() {
    const data = {
        conference_name: document.getElementById('create_conference_name').value,
        division: document.getElementById('create_conference_division').value,
    };
    fetchData('/create_conference', 'POST', data);
}

async function updateConference() {
    const conferenceName = document.getElementById('update_conference_name').value;
    const data = {
        division: document.getElementById('update_new_conference_division').value,
    };
    fetchData(`/update_conference/${conferenceName}`, 'PUT', data);
}

async function deleteConference() {
    const conferenceName = document.getElementById('delete_conference_name').value;
    fetchData(`/delete_conference/${conferenceName}`, 'DELETE');
}

async function getConference() {
    const conferenceName = document.getElementById('get_conference_name').value;
    fetchData(`/get_conference_name/${conferenceName}`, 'GET');
}

async function getTeamsInConference() {
    const conferenceName = document.getElementById('get_teams_in_conference_name').value;
    fetchData(`/get_teams_conference/${conferenceName}`, 'GET');
}

// Scouting Report APIs
async function createScoutingReport() {
    const data = {
        player_id: document.getElementById('create_report_player_id').value,
        report_date: document.getElementById('create_report_date').value,
        scouting_description: document.getElementById('create_report_description').value,
    };
    fetchData('/create_scouting_report', 'POST', data);
}

async function deleteScoutingReport() {
    const playerId = document.getElementById('delete_report_player_id').value;
    const reportDate = document.getElementById('delete_report_date').value;
    fetchData(`/delete_scouting_report/${playerId}/${reportDate}`, 'DELETE');
}

async function getScoutingReport() {
    const playerId = document.getElementById('get_scouting_report_player_id').value;
    fetchData(`/get_scouting_report_id/${playerId}`, 'GET');
}

async function updateScoutingReport() {
    const playerId = document.getElementById('update_report_player_id').value;
    const reportDate = document.getElementById('update_report_date').value; // Current date
    const data = {
        report_date: document.getElementById('update_new_report_date').value, // New date
        scouting_description: document.getElementById('update_report_description').value, // New description
    };
    fetchData(`/update_scouting_report/${playerId}/${reportDate}`, 'PUT', data);
}

// Competes In Conference APIs
async function createTeamInConference() {
    const data = {
        school_name: document.getElementById('create_team_in_conference_school').value,
        school_year: document.getElementById('create_team_in_conference_year').value,
        conference_name: document.getElementById('create_team_in_conference_name').value,
    };
    fetchData('/create_competes_in_conference', 'POST', data);
}

async function deleteTeamInConference() {
    const schoolName = document.getElementById('delete_team_in_conference_school').value;
    const schoolYear = document.getElementById('delete_team_in_conference_year').value;
    fetchData(`/delete_competes_in_conference/${schoolName}/${schoolYear}`, 'DELETE');
}

async function updateTeamInConference() {
    const schoolName = document.getElementById('update_team_in_conference_school').value;
    const schoolYear = document.getElementById('update_team_in_conference_year').value;
    const newSchoolYear = document.getElementById('update_new_team_in_conference_year').value; // Optional new year
    const newConferenceName = document.getElementById('update_team_in_conference_new_conference').value;

    const data = {};
    if (newSchoolYear) {
        data.school_year = newSchoolYear;
    }
    if (newConferenceName) {
        data.conference_name = newConferenceName;
    }

    await fetchData(`/update_competes_in_conference/${schoolName}/${schoolYear}`, 'PUT', data);
}
