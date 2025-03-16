from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import random
import string
from flask import flash


app = Flask(__name__)
app.secret_key = 'super_secret_key'

# MySQL configurations
db_config = {
    'user': 'root',
    'password': 'rafa@1234',
    'host': 'localhost',
    'database': 'project'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/fpassword.html')
def fpassword_page():
    return render_template('fpassword.html')

@app.route('/details.html')
def details_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('details.html')

@app.route('/main.html')
def main_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('main.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = generate_password_hash(data['password'])
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        user_id = cursor.lastrowid
        session['user_id'] = user_id
        cursor.close()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'message': f'Error registering user: {err}'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        return jsonify({'message': 'Login successful'}), 200
    else:
       return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/details', methods=['GET', 'POST'])
def details():
    user_id = session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    if request.method == 'GET':
        try:
            conn = get_db_connection()
            if conn is None:
                return jsonify({'error': 'Database connection failed'}), 500
            cursor = conn.cursor(dictionary=True)

            # Fetch user details
            cursor.execute('SELECT name FROM Details WHERE user_id = %s', (user_id,))
            user_details = cursor.fetchone()

            conn.close()

            # Prepare response
            if user_details:
                response = {
                    "name": user_details["name"]
                }
            else:
                response = {"name": ""}

            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        data = request.json  # Expecting a JSON object with 'name'
        name = data.get('name')

        if not name:
            return jsonify({'error': 'Invalid input'}), 400

        try:
            conn = get_db_connection()
            if conn is None:
                return jsonify({'error': 'Database connection failed'}), 500
            cursor = conn.cursor()

            # Insert or update details in the database
            cursor.execute('''
                INSERT INTO Details (user_id, name, entry_date)
                VALUES (%s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), entry_date = NOW()
            ''', (user_id, name))

            conn.commit()
            conn.close()
            return jsonify({'message': 'Details saved successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    
    # Route to handle redirection for blocks
@app.route('/redirect/<section>')
def redirect_section(section):
    if section == "energy":
        return redirect(url_for('energy_page'))  # Assuming you have an endpoint for energy.html
    elif section == "travel":
        return redirect(url_for('travel_page'))  # Replace with your travel page endpoint
    elif section == "food":
        return redirect(url_for('food_page'))  # Replace with your food page endpoint
    elif section == "waste":
        return redirect(url_for('waste_page'))  # Replace with your waste page endpoint
    else:
        return jsonify({'error': 'Invalid section'}), 400

# Placeholder route for energy page
@app.route('/energy.html', methods=['GET'])
def energy_page():
    return render_template('energy.html')

# Placeholder routes for other sections (travel, food, waste)
@app.route('/travel', methods=['GET'])
def travel_page():
    return render_template('travel.html')

@app.route('/food', methods=['GET'])
def food_page():
    return render_template('food.html')

@app.route('/waste.html', methods=['GET'])
def waste_page():
    return render_template('waste.html')

@app.route('/energycalc.html')
def energy_calc_page():
    return render_template('energycalc.html')


@app.route('/wastecalc.html')
def waste_calc_page():
    return render_template('wastecalc.html')
@app.route('/submit_waste', methods=['POST'])
def submit_waste():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = session['user_id']
    data = request.get_json()
    waste_carbon = data.get('wasteCarbon')  # Total carbon footprint from frontend

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert or update the total waste carbon footprint
        cursor.execute('''
            INSERT INTO submissions (user_id, waste, last_submit)
            VALUES (%s, %s, NOW())
            ON DUPLICATE KEY UPDATE waste = %s, last_submit = NOW()
        ''', (user_id, waste_carbon, waste_carbon))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Waste data submitted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/save_energy_devices', methods=['POST'])
def save_energy_devices():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    data = request.get_json()
    devices = data.get('devices')  # Expecting a comma-separated string

    if not devices:
        return jsonify({'error': 'No devices selected'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Clear existing devices for the user
        cursor.execute('DELETE FROM energy_devices WHERE user_id = %s', (user_id,))

        # Insert the comma-separated devices into the database
        cursor.execute('INSERT INTO energy_devices (user_id, device_name) VALUES (%s, %s)', (user_id, devices))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Devices saved successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_energy_devices', methods=['GET'])
def get_energy_devices():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = session['user_id']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT device_name FROM energy_devices WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # Split the comma-separated string back into a list
        devices = result[0].split(', ') if result else []
        return jsonify({'devices': devices}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_energy_data', methods=['POST'])
def save_energy_data():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = session['user_id']
    data = request.get_json().get('data', {})

    # Store saved data in session or temporary storage
    session[f'saved_data_{user_id}'] = data
    return jsonify({'message': 'Data saved successfully!'}), 200
@app.route('/submit_energy_data', methods=['POST'])
def submit_energy_data():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = session['user_id']
    data = request.get_json()
    carbon_footprint = data.get('carbon')  # Total carbon footprint sent from the frontend

    from datetime import datetime, timedelta
    now = datetime.now()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the user has already submitted today
        cursor.execute('SELECT last_submit FROM submissions WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()

        if result:
            last_submit = result['last_submit']
            if last_submit.date() == now.date():  # Submission already exists for today
                cursor.close()
                conn.close()
                return jsonify({'error': 'You can only submit once per day.'}), 400

        # Insert or update the submission
        cursor.execute('''
            INSERT INTO submissions (user_id, data, last_submit)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE data = %s, last_submit = %s
        ''', (user_id, carbon_footprint, now, carbon_footprint, now))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Carbon footprint submitted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_waste', methods=['POST'])
def save_waste():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401  # Ensure the user is authenticated

    user_id = session['user_id']  # Get the logged-in user's ID
    data = request.get_json().get('selectedWaste', [])  # Get the selected waste data from the frontend

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete any existing waste data for the user to avoid duplicates
        cursor.execute('DELETE FROM waste WHERE user_id = %s', (user_id,))

        # Insert the new waste data into the database
        for waste in data:
            cursor.execute('INSERT INTO waste (user_id, type, category) VALUES (%s, %s, %s)', 
                           (user_id, waste['type'], waste['category']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Waste data saved successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/community.html', methods=['GET', 'POST'])
def community_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    create_error_message = None
    join_error_message = None
    created_communities = []
    joined_communities = []

    if request.method == 'POST':
        if 'create_community' in request.form:
            community_name = request.form.get('community_name')

            if not community_name:
                create_error_message = "Community name is required."
            else:
                unique_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO communities (name, unique_code, created_by, admin_id)
                        VALUES (%s, %s, %s, %s)
                    """, (community_name, unique_code, user_id, user_id))
                    conn.commit()
                    flash(f"Community '{community_name}' created successfully! Your unique code: {unique_code}", 'create_success')
                except Exception as e:
                    conn.rollback()
                    create_error_message = f"An error occurred: {str(e)}"
                finally:
                    cursor.close()
                    conn.close()

        elif 'join_community' in request.form:
            unique_code = request.form.get('unique_code')

            if not unique_code:
                join_error_message = "Community code is required."
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT id FROM communities WHERE unique_code = %s", (unique_code,))
                    community = cursor.fetchone()

                    if not community:
                        join_error_message = "Invalid community code."
                    else:
                        community_id = community[0]
                        cursor.execute("""
                            SELECT * FROM community_members WHERE user_id = %s AND community_id = %s
                        """, (user_id, community_id))
                        if cursor.fetchone():
                            join_error_message = "You are already a member of this community."
                        else:
                            cursor.execute("""
                                INSERT INTO community_members (user_id, community_id) VALUES (%s, %s)
                            """, (user_id, community_id))
                            conn.commit()
                            flash("Successfully joined the community!", 'join_success')
                except Exception as e:
                    conn.rollback()
                    join_error_message = f"An error occurred: {str(e)}"
                finally:
                    cursor.close()
                    conn.close()

    # Fetch communities created by the user
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, unique_code FROM communities WHERE created_by = %s", (user_id,))
        created_communities = cursor.fetchall()

        # Fetch communities joined by the user
        cursor.execute("""
            SELECT c.id, c.name, c.unique_code
            FROM community_members cm
            INNER JOIN communities c ON cm.community_id = c.id
            WHERE cm.user_id = %s
        """, (user_id,))
        joined_communities = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template(
        'community.html',
        create_error_message=create_error_message,
        join_error_message=join_error_message,
        created_communities=created_communities,
        joined_communities=joined_communities
    )
@app.route('/delete_community/<int:community_id>', methods=['POST'])
def delete_community(community_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verify the user is the creator of the community
        cursor.execute("SELECT created_by FROM communities WHERE id = %s", (community_id,))
        community = cursor.fetchone()

        if not community or community[0] != user_id:
            flash("You are not authorized to delete this community.", "error")
            return redirect(url_for('community_page'))

        # Delete the community and its members
        cursor.execute("DELETE FROM community_members WHERE community_id = %s", (community_id,))
        cursor.execute("DELETE FROM communities WHERE id = %s", (community_id,))
        conn.commit()
        flash("Community deleted successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"An error occurred: {str(e)}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('community_page'))


@app.route('/leave_community/<int:community_id>', methods=['POST'])
def leave_community(community_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete the user from the community_members table
        cursor.execute("""
            DELETE FROM community_members WHERE user_id = %s AND community_id = %s
        """, (user_id, community_id))
        conn.commit()
        flash("You have left the community.", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"An error occurred: {str(e)}", 'error')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('community_page'))

@app.route('/community_details/<int:community_id>')
def community_details(community_id):
    if 'user_id' not in session:  # Ensure the user is logged in
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch community details and admin's name
        cursor.execute("""
            SELECT c.name, c.unique_code, d.name AS admin_name
            FROM communities c
            INNER JOIN details d ON c.admin_id = d.user_id
            WHERE c.id = %s
        """, (community_id,))
        community = cursor.fetchone()

        if not community:
            return "Community not found", 404

        community_name, unique_code, admin_name = community

        # Fetch member names
        cursor.execute("""
            SELECT d.name
            FROM community_members cm
            INNER JOIN details d ON cm.user_id = d.user_id
            WHERE cm.community_id = %s
        """, (community_id,))
        members = cursor.fetchall()  # List of member names
    finally:
        cursor.close()
        conn.close()

    return render_template(
        'community_details.html',
        community_name=community_name,
        unique_code=unique_code,
        admin_name=admin_name,
        members=members
    )


@app.route('/store_home', methods=['POST'])
def store_home():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    user_id = session['user_id']
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO HomeDetails (user_id, devices, devices_result, total_result, entry_date) VALUES (%s, %s, %s, %s, %s)",
        (user_id, ','.join(data['devices']), data['devices_result'], data['total_result'], date.today()))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Home details stored successfully'}), 201

@app.route('/transportation.html')
def transportation_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('transportation.html')

@app.route('/personal.html')
def personal_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('personal.html')

@app.route('/home.html')
def home_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('home.html')

@app.route('/report.html')
def report_page():
    if 'user_id' not in session:  # Ensure the user is logged in
        return redirect(url_for('login_page'))
    return render_template('report.html')


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        # Placeholder for sending reset email
        print(f"A reset link would be sent to {email}")
        cursor.close()
        conn.close()
        return jsonify({'message': 'A reset link has been sent to your email'}), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({'message': 'Email not found'}), 400
    
@app.route('/profile.html')
def profile_page():
    if 'user_id' not in session:  # Ensure the user is logged in
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch user details and profile data
        cursor.execute("""
            SELECT name, household_members, transportation, devices 
            FROM Details 
            WHERE user_id = %s
        """, (user_id,))
        user_data = cursor.fetchone()  # Fetch a single row

        # Prepare the user profile data
        if user_data:
            user_profile = {
                'name': user_data[0],  # User's name
                'household_members': user_data[1],  # Household members
                'transportation': user_data[2],  # Preferred transportation
                'devices': user_data[3]  # Devices used
            }
        else:
            user_profile = None  # No data found
    finally:
        # Ensure the database cursor and connection are closed
        cursor.close()
        conn.close()

    return render_template('profile.html', user_profile=user_profile)


if __name__ == '__main__':
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) UNIQUE, password VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Details (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, name VARCHAR(255), household_members INT, transportation TEXT, devices TEXT, entry_date DATE, FOREIGN KEY (user_id) REFERENCES users(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS HomeDetails (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, devices TEXT, devices_result VARCHAR(255), total_result VARCHAR(255), entry_date DATE, FOREIGN KEY (user_id) REFERENCES users(id))")
    cursor.close()
    conn.close()
    app.run(debug=True)