from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, DATABASE_NAME
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secrect_key'

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]
users_collection = db['users']
program_studi_collection = db['program_studi']
kelas_collection = db['kelas']
shift_collection = db['shift']
apel_collection = db['apel']
pengumuman_collection = db['pengumuman']
laporan_collection = db['laporan']

@app.route('/')
def index():
    return render_template('home/landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            flash('Login berhasil', 'success')
            return redirect(url_for('profile', username=username))
        flash('Login gagal, periksa username dan password Anda', 'danger')
    return render_template('home/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'user'

        if users_collection.find_one({'username': username}):
            flash('username sudah terdaftar', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        }
        users_collection.insert_one(user_data)
        flash('Registrasi berhasil', 'success')
        return redirect(url_for('login'))
    return render_template('home/register.html')

@app.route('/registerAdmin', methods=['GET', 'POST'])
def registerAdmin():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'admin'

        if users_collection.find_one({'username': username}):
            flash('username sudah terdaftar', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        }
        users_collection.insert_one(user_data)
        flash('Registrasi berhasil', 'success')
        return redirect(url_for('login'))
    return render_template('home/register_admin.html')

@app.route('/form_user', methods=['GET', 'POST'])
def form_user():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'role'

        if users_collection.find_one({'username': username}):
            flash('username sudah terdaftar', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        }
        users_collection.insert_one(user_data)
        flash('Registrasi berhasil', 'success')
        return redirect(url_for('list_user'))
    return render_template('user/form_user.html')

@app.route('/list_user', methods=['GET', 'POST'])
def list_user():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        search_query = request.form['search']
        order = request.form['order'] if 'order' in request.form else None
        
        if order == 'ascending':
            list_user = users_collection.find({
                '$or': [
                    {'username': {'$regex': search_query, '$options': 'i'}},
                    {'name': {'$regex': search_query, '$options': 'i'}},
                    {'email': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('username', 1)
        elif order == 'descending':
            list_user = users_collection.find({
                '$or': [
                    {'username': {'$regex': search_query, '$options': 'i'}},
                    {'name': {'$regex': search_query, '$options': 'i'}},
                    {'email': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('username', -1)
        else:
            list_user = users_collection.find({
                '$or': [
                    {'username': {'$regex': search_query, '$options': 'i'}},
                    {'name': {'$regex': search_query, '$options': 'i'}},
                    {'email': {'$regex': search_query, '$options': 'i'}}
                ]
            })
    else:
        list_user = users_collection.find()
    return render_template('user/list_user.html', data_user=list_user)
    

@app.route('/edit_user/<id>', methods=['GET', 'POST'])
def edit_user(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        user_data = {
            'username': username,
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'role': role
        }
        users_collection.update_one({'_id': ObjectId(id)}, {'$set': user_data})
        
        flash('Data pengguna berhasil diperbarui', 'success')
        return redirect(url_for('list_user'))
    
    user = users_collection.find_one({'_id': ObjectId(id)})
    return render_template('user/edit_user.html', user=user)

@app.route('/delete_user/<id>', methods=['POST'])
def delete_user(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    users_collection.delete_one({'_id': ObjectId(id)})
    flash('Pengguna berhasil dihapus', 'success')
    return redirect(url_for('list_user'))

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user_data = {
            'name': name,
            'email': email
        }
        if password:
            user_data['password'] = generate_password_hash(password)

        users_collection.update_one({'username': username}, {'$set': user_data})

        flash('Profil berhasil diperbarui', 'success')
        return redirect(url_for('profile', username=username))

    user = users_collection.find_one({'username': session['username']})
    return render_template('user/profile_user.html', user=user)

@app.route('/shift_apel_user', methods=['GET'])
def shift_apel_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    
    shifts = shift_collection.find()
    shifts_with_classes = []
    for shift in shifts:
        kelas = kelas_collection.find_one({'_id': shift['kelas_id']})
        shift['kelas_nama'] = kelas['kelas'] if kelas else 'Belum ada'
        shifts_with_classes.append(shift)

    apels = apel_collection.find()
    apel_with_kelas_shift = []
    for apel in apels:
        kelas_info = kelas_collection.find_one({'_id': apel['kelas_id']})
        kelas_nama = kelas_info['kelas'] if kelas_info else 'Belum ada'
        shift_info = shift_collection.find_one({'_id': apel['shift_id']})
        shift_jenis = shift_info['jenis_shift'] if shift_info else 'Belum ada'
        apel['tanggal'] = apel['tanggal'].strftime('%Y-%m-%d')
        apel['kelas_nama'] = kelas_nama
        apel['shift_jenis'] = shift_jenis
        apel_with_kelas_shift.append(apel)

    return render_template('user/shift_apel_user.html', shifts=shifts_with_classes, apels=apel_with_kelas_shift)


@app.route('/pengumuman_user', methods=['GET'])
def pengumuman_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    pengumuman = pengumuman_collection.find().sort('tanggal', -1)
    return render_template('user/pengumuman_user.html', pengumuman=pengumuman)

@app.route('/form_program_studi', methods=['GET', 'POST'])
def form_program_studi():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        program_studi = request.form.get('program_studi')
        
        program_studi_data = {
            'program_studi': program_studi
        }
        program_studi_collection.insert_one(program_studi_data)
        flash('Program studi berhasil ditambahkan', 'success')
        return redirect(url_for('list_program_studi'))
    program_studi = list(program_studi_collection.find())
    return render_template('program_studi/form_program_studi.html', program_studi=program_studi)

@app.route('/list_program_studi', methods=['GET', 'POST'])
def list_program_studi():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        search_query = request.form['search']
        order = request.form['order'] if 'order' in request.form else None
        
        if order == 'ascending':
            list_program_studi = program_studi_collection.find({
                '$or': [
                    {'program_studi': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('program_studi', 1)
        elif order == 'descending':
            list_program_studi = program_studi_collection.find({
                '$or': [
                    {'program_studi': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('program_studi', -1)
        else:
            list_program_studi= program_studi_collection.find({
                '$or': [
                    {'program_studi': {'$regex': search_query, '$options': 'i'}}
                ]
            })
    else:
        list_program_studi = program_studi_collection.find()
    return render_template('program_studi/list_program_studi.html', data_program_studi=list_program_studi)


@app.route('/edit_program_studi/<id>', methods=['GET', 'POST'])
def edit_program_studi(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        program_studi = request.form['program_studi']
        
        program_studi_data = {
            'program_studi': program_studi
        }
        program_studi_collection.update_one({'_id': ObjectId(id)}, {'$set': program_studi_data})
        flash('Data program studi berhasil diperbarui', 'success')
        return redirect(url_for('list_program_studi'))
    
    program_studi_data = program_studi_collection.find_one({'_id': ObjectId(id)})
    return render_template('program_Studi/edit_program_studi.html', program_studi=program_studi_data)

@app.route('/delete_program_studi/<id>', methods=['POST'])
def delete_program_studi(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    program_studi_collection.delete_one({'_id': ObjectId(id)})
    flash('Program Studi berhasil dihapus', 'success')
    return redirect(url_for('list_program_studi'))

@app.route('/form_kelas', methods=['GET', 'POST'])
def form_kelas():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        kelas = request.form['kelas']
        program_studi_id = ObjectId(request.form['program_studi_id'])

        
        kelas_data = {
            'kelas': kelas,
            'program_studi_id': program_studi_id
        }
        kelas_collection.insert_one(kelas_data)
        flash('Kelas berhasil ditambahkan', 'success')
        return redirect(url_for('list_kelas'))
    program_studi = list(program_studi_collection.find())
    return render_template('kelas/form_kelas.html', program_studi=program_studi)


@app.route('/edit_kelas/<id>', methods=['GET', 'POST'])
def edit_kelas(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        kelas = request.form['kelas']
        program_studi_id = ObjectId(request.form['program_studi_id'])
        
        kelas_data = {
            'kelas': kelas,
            'program_studi_id': program_studi_id
        }
        kelas_collection.update_one({'_id': ObjectId(id)}, {'$set': kelas_data})
        flash('Data kelas berhasil diperbarui', 'success')
        return redirect(url_for('list_kelas'))
    
    kelas_data = kelas_collection.find_one({'_id': ObjectId(id)})
    program_studi = list(program_studi_collection.find())
    return render_template('kelas/edit_kelas.html', kelas=kelas_data, program_studi=program_studi)

@app.route('/list_kelas', methods=['GET', 'POST'])
def list_kelas():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        search_query = request.form['search']
        order = request.form['order'] if 'order' in request.form else None
        
        if order == 'ascending':
            kelas = kelas_collection.find({
                '$or': [
                    {'kelas': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('kelas', 1)
        elif order == 'descending':
            kelas = kelas_collection.find({
                '$or': [
                    {'kelas': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('kelas', -1)
        else:
            kelas = kelas_collection.find({
                '$or': [
                    {'kelas': {'$regex': search_query, '$options': 'i'}}
                ]
            })
    else:
        kelas = kelas_collection.find()
    kelas_with_program_studi = []
    for kls in kelas:
        program_studi = program_studi_collection.find_one({'_id': kls['program_studi_id']})
        kls['program_studi'] = program_studi['program_studi'] if program_studi else 'Belum ada'
        kelas_with_program_studi.append(kls)

    return render_template('kelas/list_kelas.html', kelas=kelas_with_program_studi)

@app.route('/delete_kelas/<id>', methods=['POST'])
def delete_kelas(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    kelas_collection.delete_one({'_id': ObjectId(id)})
    flash('Kelas berhasil dihapus', 'success')
    return redirect(url_for('list_kelas'))

@app.route('/form_shift', methods=['GET', 'POST'])
def form_shift():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    kelas_list = list(kelas_collection.find())
    if request.method == 'POST':
        jenis_shift = request.form['jenis_shift']
        waktu_mulai = request.form['waktu_mulai']
        waktu_berakhir = request.form['waktu_berakhir']
        kelas_id = ObjectId(request.form['kelas_id'])
        
        shift_data = {
            'jenis_shift': jenis_shift,
            'waktu_mulai': waktu_mulai,
            'waktu_berakhir': waktu_berakhir,
            'kelas_id': kelas_id
        }
        shift_collection.insert_one(shift_data)
        flash('Shift berhasil ditambahkan', 'success')
        return redirect(url_for('list_shift'))
    
    return render_template('shift/form_shift.html', kelas_list=kelas_list)

@app.route('/list_shift', methods=['GET', 'POST'])
def list_shift():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        search_query = request.form['search']
        order = request.form['order'] if 'order' in request.form else None
        
        if order == 'ascending':
            shifts = shift_collection.find({
                '$or': [
                    {'jenis_shift': {'$regex': search_query, '$options': 'i'}},
                    {'kelas_id': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('jenis_shift', 1)
        elif order == 'descending':
            shifts = shift_collection.find({
                '$or': [
                    {'jenis_shift': {'$regex': search_query, '$options': 'i'}},
                    {'kelas_id': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('jenis_shift', -1)
        else:
            shifts = shift_collection.find({
                '$or': [
                    {'jenis_shift': {'$regex': search_query, '$options': 'i'}},
                    {'kelas_id': {'$regex': search_query, '$options': 'i'}}
                ]
            })
    else:
        shifts = shift_collection.find()
    
    shifts_with_classes = []
    for shift in shifts:
        kelas = kelas_collection.find_one({'_id': shift['kelas_id']})
        shift['kelas_nama'] = kelas['kelas'] if kelas else 'Belum ada'
        shifts_with_classes.append(shift)

    return render_template('shift/list_shift.html', shifts=shifts_with_classes)

@app.route('/edit_shift/<id>', methods=['GET', 'POST'])
def edit_shift(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    kelas_list = list(kelas_collection.find())
    if request.method == 'POST':
        jenis_shift = request.form['jenis_shift']
        waktu_mulai = request.form['waktu_mulai']
        waktu_berakhir = request.form['waktu_berakhir']
        kelas_id = ObjectId(request.form['kelas_id'])
        
        shift_data = {
            'jenis_shift': jenis_shift,
            'waktu_mulai': waktu_mulai,
            'waktu_berakhir': waktu_berakhir,
            'kelas_id': kelas_id
        }
        shift_collection.update_one({'_id': ObjectId(id)}, {'$set': shift_data})
        flash('Data shift berhasil diperbarui', 'success')
        return redirect(url_for('list_shift'))
    
    shift_data = shift_collection.find_one({'_id': ObjectId(id)})
    return render_template('shift/edit_shift.html', shift=shift_data, kelas_list=kelas_list)

@app.route('/delete_shift/<id>', methods=['POST'])
def delete_shift(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    shift_collection.delete_one({'_id': ObjectId(id)})
    flash('Shift berhasil dihapus', 'success')
    return redirect(url_for('list_shift'))

@app.route('/form_apel', methods=['GET', 'POST'])
def form_apel():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        kelas_id = ObjectId(request.form['kelas_id'])
        shift_id = ObjectId(request.form['shift_id'])
        tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d')

        apel_data = {
            'kelas_id': kelas_id,
            'shift_id': shift_id,
            'tanggal': tanggal
        }
        apel_collection.insert_one(apel_data)
        flash('Jadwal apel berhasil ditambahkan', 'success')
        return redirect(url_for('list_apel'))

    kelas_list = kelas_collection.find()
    shift_list = shift_collection.find()
    return render_template('apel/form_apel.html', kelas_list=kelas_list, shift_list=shift_list)

@app.route('/list_apel', methods=['GET', 'POST'])
def list_apel():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    apels = apel_collection.find()
    apel_with_kelas_shift = []
    for apel in apels:
        kelas_info = kelas_collection.find_one({'_id': apel['kelas_id']})
        kelas_nama = kelas_info['kelas'] if kelas_info else 'Belum ada'
        shift_info = shift_collection.find_one({'_id': apel['shift_id']})
        shift_jenis = shift_info['jenis_shift'] if shift_info else 'Belum ada'
        apel['tanggal'] = apel['tanggal'].strftime('%Y-%m-%d')
        apel['kelas_nama'] = kelas_nama
        apel['shift_jenis'] = shift_jenis
        apel_with_kelas_shift.append(apel)

    return render_template('apel/list_apel.html', apels=apel_with_kelas_shift)

@app.route('/edit_apel/<id>', methods=['GET', 'POST'])
def edit_apel(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        kelas_id = ObjectId(request.form['kelas_id'])
        shift_id = ObjectId(request.form['shift_id'])
        tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()

        apel_data = {
            'kelas_id': kelas_id,
            'shift_id': shift_id,
            'tanggal': tanggal
        }
        apel_collection.update_one({'_id': ObjectId(id)}, {'$set': apel_data})
        flash('Data jadwal apel berhasil diperbarui', 'success')
        return redirect(url_for('list_apel'))

    apel_data = apel_collection.find_one({'_id': ObjectId(id)})
    kelas_list = kelas_collection.find()
    shift_list = shift_collection.find()
    return render_template('apel/edit_apel.html', apel=apel_data, kelas_list=kelas_list, shift_list=shift_list)

@app.route('/delete_apel/<id>', methods=['POST'])
def delete_apel(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    apel_collection.delete_one({'_id': ObjectId(id)})
    flash('Jadwal apel berhasil dihapus', 'success')
    return redirect(url_for('list_apel'))


@app.route('/form_pengumuman', methods=['GET', 'POST'])
def form_pengumuman():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        judul = request.form['judul']
        tanggal = request.form['tanggal']
        isi = request.form['isi']
        pengirim = session['username']
        pengumuman_data = {
            'judul': judul,
            'tanggal': datetime.strptime(tanggal, '%Y-%m-%d'),
            'isi': isi,
            'pengirim': pengirim
        }
        pengumuman_collection.insert_one(pengumuman_data)
        flash('Pengumuman berhasil ditambahkan', 'success')
        return redirect(url_for('list_pengumuman'))
    
    return render_template('pengumuman/form_pengumuman.html')

@app.route('/list_pengumuman', methods=['GET', 'POST'])
def list_pengumuman():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        search_query = request.form['search']
        order = request.form['order'] if 'order' in request.form else None
        
        if order == 'ascending':
            pengumuman = pengumuman_collection.find({
                '$or': [
                    {'judul': {'$regex': search_query, '$options': 'i'}},
                    {'isi': {'$regex': search_query, '$options': 'i'}},
                    {'pengirim': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('tanggal', 1)
        elif order == 'descending':
            pengumuman = pengumuman_collection.find({
                '$or': [
                    {'judul': {'$regex': search_query, '$options': 'i'}},
                    {'isi': {'$regex': search_query, '$options': 'i'}},
                    {'pengirim': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('tanggal', -1)
        else:
            pengumuman = pengumuman_collection.find({
                '$or': [
                    {'judul': {'$regex': search_query, '$options': 'i'}},
                    {'isi': {'$regex': search_query, '$options': 'i'}},
                    {'pengirim': {'$regex': search_query, '$options': 'i'}}
                ]
            })
    else:
        pengumuman = pengumuman_collection.find()
    
    return render_template('pengumuman/list_pengumuman.html', pengumuman=pengumuman)


@app.route('/edit_pengumuman/<id>', methods=['GET', 'POST'])
def edit_pengumuman(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        judul = request.form['judul']
        tanggal = request.form['tanggal']
        isi = request.form['isi']
        
        pengumuman_data = {
            'judul': judul,
            'tanggal': datetime.strptime(tanggal, '%Y-%m-%d'),
            'isi': isi
        }
        pengumuman_collection.update_one({'_id': ObjectId(id)}, {'$set': pengumuman_data})
        flash('Pengumuman berhasil diperbarui', 'success')
        return redirect(url_for('list_pengumuman'))
    
    pengumuman_data = pengumuman_collection.find_one({'_id': ObjectId(id)})
    return render_template('pengumuman/edit_pengumuman.html', pengumuman=pengumuman_data)

@app.route('/delete_pengumuman/<id>', methods=['POST'])
def delete_pengumuman(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    pengumuman_collection.delete_one({'_id': ObjectId(id)})
    flash('Pengumuman berhasil dihapus', 'success')
    return redirect(url_for('list_pengumuman'))

@app.route('/form_laporan_saran', methods=['GET', 'POST'])
def form_laporan_saran():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            flash('Anda harus login terlebih dahulu', 'danger')
            return redirect(url_for('login'))
        
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            flash('User tidak ditemukan', 'danger')
            return redirect(url_for('login'))
        
        jenis_laporan = request.form['jenis_laporan']
        laporan_saran= request.form['laporan_saran']
        date = datetime.utcnow()

        laporan_saran_data = {
            'user': {
                '_id': user['_id'],
                'username': user['username'],
                'email': user['email']
            },
            'date': date,
            'jenis_laporan': jenis_laporan,
            'laporan_saran': laporan_saran,
        }
        laporan_collection.insert_one(laporan_saran_data)
        flash('Laporan atau saran berhasil ditambahkan', 'success')
        return redirect(url_for('list_laporan_saran'))
    
    return render_template('laporan_saran/form_laporan_saran.html')

@app.route('/list_laporan_saran', methods=['GET', 'POST'])
def list_laporan_saran():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    if session.get('role') == 'admin':
        list_laporan_saran = laporan_collection.find()
    else:
        list_laporan_saran = laporan_collection.find({'user._id': ObjectId(user_id)})
    
    if request.method == 'POST':
        search_query = request.form['search']
        order = request.form['order'] if 'order' in request.form else None
        
        if session.get('role') == 'admin':
            query_filter = {'$or': [{'laporan_saran': {'$regex': search_query, '$options': 'i'}}, {'user.username': {'$regex': search_query, '$options': 'i'}}]}
        else:
            query_filter = {'$and': [{'user._id': ObjectId(user_id)}, {'$or': [{'laporan_saran': {'$regex': search_query, '$options': 'i'}}, {'user.username': {'$regex': search_query, '$options': 'i'}}]}]}
        
        if order == 'ascending':
            list_laporan_saran = laporan_collection.find(query_filter).sort('date', 1)
        elif order == 'descending':
            list_laporan_saran = laporan_collection.find(query_filter).sort('date', -1)
        else:
            list_laporan_saran = laporan_collection.find(query_filter)
    return render_template('laporan_saran/list_laporan_saran.html', data_laporan_saran=list_laporan_saran)


@app.route('/edit_laporan_saran/<id>', methods=['GET', 'POST'])
def edit_laporan_saran(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            flash('Anda harus login terlebih dahulu', 'danger')
            return redirect(url_for('login'))
        
        jenis_laporan = request.form['jenis_laporan']
        laporan_saran = request.form['laporan_saran']

        laporan_saran_data = {
            'jenis_laporan': jenis_laporan,
            'laporan_saran': laporan_saran
        }
        laporan_collection.update_one({'_id': ObjectId(id)}, {'$set': laporan_saran_data})
        flash('Laporan dan saran berhasil diperbarui', 'success')
        return redirect(url_for('list_laporan_saran'))
    
    laporan_saran_data = laporan_collection.find_one({'_id': ObjectId(id)})
    return render_template('laporan_saran/edit_laporan_saran.html', laporan=laporan_saran_data)

@app.route('/delete_laporan_saran/<id>', methods=['POST'])
def delete_laporan_saran(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    laporan_collection.delete_one({'_id': ObjectId(id)})
    flash('Laporan dan saran berhasil dihapus', 'success')
    return redirect(url_for('list_laporan_saran'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)