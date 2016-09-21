import time
from flask import flash
from socallt_app.Models.Conference import Conference
from socallt_app import app, db

def create(fields):
	is_valid = True
	for k, v in fields.items():
		if not v:
			flash('All fields are required', 'conf_create_err')
			return False
	if len(fields['year']) != 4:
		is_valid = False
		flash('Year should be formatted 20XX', 'conf_create_err')
	if time.strptime(fields['date']) >= time.time():
		is_valid = False
		flash('Conference date must be in the future.', 'conf_create_err')
	if fields['full_prof_cost'] < 0 or fields['day_prof_cost'] < 0:
		is_valid = False
		flash('Professional conference prices must be positive.', 'conf_create_err')		
	if fields['full_stud_cost'] < 0 or fields['day_stud_cost'] < 0:
		is_valid = False
		flash('Professional conference prices must be positive.', 'conf_create_err')
	if fields['vend_cost'] < 0:
		is_valid = False
		flash('Vendor conference prices must be positive.', 'conf_create_err')

	if is_valid:
		return True
	return False

def get_conference_by_id(id):
	conference = Conference.query.get(id)
	if not conference:
		conference = get_next_conference()
	return conference

def get_next_conference():
	return Conference.query.order_by(desc(Conference.year)).first().id
