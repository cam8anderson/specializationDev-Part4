from flask import Flask, render_template, redirect, url_for, request, flash
from forms import TeamForm, ProjectForm
from model import db, User, Team, Projects, connect_to_db

app = Flask(__name__)

app.secret_key = 'keep this secret'

user_id = 1

@app.route('/')
def home():
        team_form = TeamForm()
        project_form = ProjectForm()
        project_form.update_teams(User.query.get(user_id).teams)
        
        return render_template("home.html", team_form = team_form, project_form = project_form)

@app.route('/add_team', methods = ['POST'])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        print(team_form.team_name.data)
        return redirect(url_for('home'))
    else:
        print('Form failed to validate on submit')
        return redirect(url_for('home'))

@app.route('/add-project', methods=['POST'])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        new_project = Projects(project_name, description, completed, team_id)
        db.session.add(new_project)
        db.session.commit()

        print(project_form.project_name.data)
        return redirect(url_for('home'))
    else:
        print('Project form failed to validate on submit')
        return redirect(url_for('home'))
    
@app.route('/teams', methods=['GET'])
def team_html():
     teams = Team.query.all()
     projects = Projects.query.all()
     return render_template('teams.html', teams=teams, projects=projects)

@app.route('/team_switch', methods=['POST'])
def team_switch():
    project_id = request.form.get('project_id')
    new_team_id = request.form.get('new_team_id')
     
    project = Projects.query.get(project_id)
    project.team_id = new_team_id

    db.session.commit()

    return redirect(url_for('team_html'))

@app.route('/delete_project', methods=['POST'])
def delete_project():
    project_id = request.form.get('project_id')

    if not project_id:
        flash('Invalid project ID.')
        return redirect(url_for('team_html'))

    project = Projects.query.get(project_id)

    if not project:
        flash('Project not found.')
        return redirect(url_for('team_html'))


    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('team_html'))
if __name__ == '__main__':
        connect_to_db(app)
        app.run(debug=True)