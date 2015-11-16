#-*-coding:utf-8-*-
from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from jinja2 import TemplateNotFound
from simplepam import authenticate
from core.database import db

context = Blueprint('site', __name__, template_folder='templates')

@context.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
            userid = request.form.get('userid', None)
            password = request.form.get('pwd', None)
            print userid
            print password
            if authenticate(str(userid), str(password)):
                session['userid'] = userid
                return redirect(url_for('.summary'))
            else:
                return 'Invalid user id or password'
    return render_template('home.html')

@context.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('.home'))

@context.route('/summary')
def summary():
    if not 'userid' in session:
        flash('Not Allowed Error. Session expired or abnormal access.')
        return redirect(url_for('.home'))

    year = request.args.get('year', None)
    month = request.args.get('month', None)

    if year is not None:
        where_clause = "WHERE ((`user_accesses`.`timestamp` >= '%s-%s-01 00:00:00') and (`user_accesses`.`timestamp` < '%s-%s-30 00:00:00'))" % (year, month, year, int(month)+5)
    else:
        where_clause = ""

    stat = db.select_all("""
        SELECT
            `user_accesses`.`country` AS `country`,
            count(`user_accesses`.`id`) AS `accesses`,
            count((case `user_accesses`.`accepted` when 'yes' then 1 else NULL end)) AS `accepted`,
            count(distinct `user_accesses`.`email`) AS `email`
        FROM `user_accesses`
        %s
        GROUP BY `user_accesses`.`country`
        UNION
        SELECT
            'TOTAL' AS `country`,
            count(`user_accesses`.`id`) AS `accesses`,
            count((case `user_accesses`.`accepted` when 'yes' then 1 else NULL end)) AS `accepted`,
            count(distinct `user_accesses`.`email`) AS `email`
        FROM `user_accesses`
        %s
    """ % (where_clause, where_clause))

    return render_template('summary.html', stat=stat)
