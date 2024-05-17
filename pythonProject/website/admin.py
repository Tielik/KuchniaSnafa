from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, session
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, engine
from . import db
from .models import Admin, Przepisy, Skladniki
import os
from .api import dishes_with_matching_ingredient_remover


admin = Blueprint('admin', __name__)

"""
Function for handling the admin index page. 
Retrieves and displays 'Przepisy' and 'Skladniki' data if the user is authenticated. 
If not authenticated, handles user login and authentication. 
Returns the rendered admin page template with 'Przepisy' and 'Skladniki' data if authenticated, else, redirects to the login page.
"""
@admin.route('/', methods=['POST', 'GET'])
def index_admin():
    if current_user.is_authenticated:
        if db.session.query(Przepisy).count() >= 1:
             dishes= db.session.query(Przepisy)
        else:
             dishes = None
        if db.session.query(Skladniki).count() >= 1:
            ingredients = db.session.query(Skladniki)
        else:
            ingredients = None
        return render_template('admin.html', przepisy=dishes, skladniki=ingredients)

    if request.method == 'POST':
        name = request.form.get('Admin')
        password = request.form.get('password')
        if not db.session.query(db.exists().where(Admin.name == name)).scalar():
            flash('Nieprawidłowy login lub hasło', category='error')
            return render_template('login.html')
        user=Admin.query.filter_by(name=name).first()
        if not check_password_hash(user.password, password):
            flash('Nieprawidłowy login lub hasło', category='error')
            return render_template('login.html')

        flash('Udało ci się zalogować!', category='success')
        login_user(user, remember=True)
        if db.session.query(Przepisy).count() >= 1:
            dishes = db.session.query(Przepisy)
        else:
            dishes = None
        if db.session.query(Skladniki).count() >= 1:
            ingredients = db.session.query(Skladniki)
        else:
            ingredients = None
        return render_template('admin.html', przepisy=dishes, skladniki=ingredients)
    else:
        return render_template('login.html')


    """
    Change the password for the currently authenticated admin user.

    This function handles the '/clp' route with both POST and GET methods. If the current user is authenticated, it retrieves the admin user with the same name as the current user from the database. If the request method is POST, it retrieves the 'Admin' and 'password' values from the request form, finds the admin user with the given name, updates the user's password with the generated hash, commits the changes to the database, and redirects to the '/admin' route. If the request method is GET, it renders the 'adminChange.html' template with the admin user and the current user's password hash.

    Returns:
        - If the current user is not authenticated, it redirects to the '/admin' route.
        - If the request method is POST, it redirects to the '/admin' route.
        - If the request method is GET, it renders the 'adminChange.html' template.

    """
@admin.route('/clp', methods=['POST', 'GET'])
def change_password():
    if current_user.is_authenticated:
        admin = Admin.query.filter_by(name=current_user.name).first()
        if request.method == 'POST':
            name = request.form.get('admin')
            password = request.form.get('password')
            user = Admin.query.filter_by(name=name).first()
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Zmieniono hasło', category='success')
            return redirect('/admin')
        return render_template('adminChange.html', admin=admin,
                               password=check_password_hash(current_user.password, admin.password))
    else:
        return redirect('/admin')

    """
    This function handles the '/przepisy' route for both GET and POST requests. It is decorated with the @admin.route decorator.

    Parameters:
    - None

    Returns:
    - If the current user is not authenticated, it redirects to the '/' route.
    - If the current user is authenticated:
        - If there are no Skladniki in the database, it sets ingredients to None and flashes an error message.
        - If there are Skladniki in the database, it queries all Skladniki and assigns the result to the ingredients variable.
        - If the request method is POST:
        - create new row in Przepisy table 
        -create image in images folder with name the same as id of new row in Przepisy table 
        - If the request method is GET, it renders the 'przepisy.html' template with the ingredients variable.

    """
@admin.route('/przepisy', methods=['POST', 'GET'])
def Dishes():
    if current_user.is_authenticated:
        if db.session.query(Skladniki).count() >= 1:
            ingredients = db.session.query(Skladniki)
        else:
            ingredients = None
            flash("By dodać danie trzeba najpierw wprowadzić składniki!", category="error")
            return redirect('/admin')
        if request.method == 'POST':
            nazwa = request.form.get('nazwa')
            czas = request.form.get('czas')
            opis = request.form.get('opis')
            przepis = request.form.get('przepis')
            ListaSkladnikow = request.form.getlist('lista')
            ListaSkladnikow = " ".join(ListaSkladnikow)
            przepis = Przepisy(nazwa=nazwa, czas=czas, opis=opis, przepis=przepis,
                               ListaSkladnikow=ListaSkladnikow)
            grafika = request.files['grafika']
            grafika_name = grafika.filename
            if grafika_name != '':
                grafika_ext = os.path.splitext(grafika_name)[1]
                if grafika_ext in ['.png', '.jpg', '.jpeg', '.webp']:
                    # Pobranie id ostatniego przepisu jako string <Przepisy id>
                    przepis_last_id = str(db.session.query(Przepisy).order_by(Przepisy.id.desc()).first())
                    # Utworzenie nowego id poprzez inkrementacje wyciagnietego id ze stringa <Przepisy id>
                    print(przepis_last_id)
                    if(przepis_last_id is None):
                        przepis_new_id = int(''.join(x for x in przepis_last_id if x.isdigit())) + 1
                    else:
                        przepis_new_id = 1
                    # Zapisanie nazwy grafiki jako id.png
                    grafika_name = str(przepis_new_id) + '.png'
                    grafika.save(os.path.join('website/static/img', grafika_name))
                    db.session.add(przepis)
                    db.session.commit()
                    flash('Przepis został dodany!', category='success')
                    return redirect('/admin')
                else:
                    flash('Nieprawidłowy format grafiki!', category='error')
                    return redirect('/admin/przepisy')
        return render_template('przepisy.html', skladniki=ingredients)
    return redirect('/')

    """
    Route for handling the '/ingredients' endpoint. This endpoint is used to add new 'Skladniki' objects to the database.
    Parameters:
    - None
    Returns:
    - If the current user is not authenticated, it redirects to the '/' route.
    - If the current user is authenticated:
        - If the request method is POST:
            - Retrieves the 'Nazwa' and 'kategoria' values from the request form.
            - Adds the new object to the database.
            - Flashes a success message.
            - Redirects to the '/admin' route.
        - If the request method is GET:
            - Renders the 'skladniki.html' template.
    """
@admin.route('/skladniki', methods=['POST', 'GET'])
def Ingredients():
    if current_user.is_authenticated:
        if request.method == 'POST':
            Nazwa = request.form.get('Nazwa')
            kategoria = request.form.get('kategoria')
            ingredients = Skladniki(Nazwa=Nazwa, kategoria=kategoria)
            db.session.add(ingredients)
            db.session.commit()
            flash('Skladnik został dodany!', category='success')
            return redirect('/admin')
        return render_template('skladniki.html')
    return redirect('/')

    """
    Logout the current user and redirect to the home page.

    This function is a route handler for the '/logout' endpoint. It checks if the current user is authenticated.
     If the user is authenticated, it logs out the user by calling the `logout_user()`(that do what method is named in the flask_login) function and redirects to the home page.
      If the user is not authenticated, it redirects to the home page without logging out.

    Returns:
       redirect to the home page
    """
@admin.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    return redirect('/')

    """
    Delete a recipe with the given id.

    This function is a route handler for the '/delete/przepis/<int:id>' endpoint. It checks if the current user is authenticated.
    If the user is authenticated, it retrieves the recipe with the given id from the database, deletes the corresponding image file,
    and deletes the recipe from the database. It then redirects the user to the admin page with a success message.
    If the user is not authenticated, it redirects the user to the home page.

    Parameters:
    - id (int): The id of the recipe to be deleted.

    Returns:
    - redirect to the admin page if the user is authenticated
    - redirect to the home page if the user is not authenticated
    """
    #POPRAWIĆ
@admin.route('/delete/przepis/<int:id>')
def delete(id):
    if current_user.is_authenticated:
        przepis = Przepisy.query.filter_by(id=id).first()
        grafika_name = str(id) + '.png'
        os.remove(os.path.join('website/static/img', grafika_name))
        db.session.delete(przepis)
        db.session.commit()
        flash('Przepis został usunięty!', category='success')
        return redirect('/admin')
    return redirect('/')

    """
    A function that deletes a 'Skladnik' object from the database based on the provided ID.

    Parameters:
    - id (int): The ID of the 'Skladnik' object to be deleted.

    Returns:
    - redirect to the admin page if the user is authenticated
    - redirect to the home page if the user is not authenticated
    """
@admin.route('/delete/skladnik/<int:id>')
def deleteS(id):
    if current_user.is_authenticated:
        skladnik = Skladniki.query.filter_by(id=id).first()
        db.session.delete(skladnik)
        db.session.commit()
        dishes_with_matching_ingredient_remover(id)
        flash('Składnik został usunięty!', category='success')
        return redirect('/admin')
    return redirect('/')

    """
    Route for handling the '/edit/skladnik/<int:id>' endpoint. This endpoint is used to edit a 'Skladnik' object in the database.

    Parameters:
    - id (int): The ID of the 'Skladnik' object to be edited.

    Returns:
    - If the user is authenticated and the request method is 'POST', the 'Nazwa' and 'kategoria' fields of the 'Skladnik' object are updated with the values from the request form. 
    The changes are committed to the database and a success message is flashed. The user is then redirected to the '/admin' page.
    - If the user is authenticated and the request method is 'GET', the 'editSkladnik.html' template is rendered with the 'skladnik' object passed as a parameter.
    - If the user is not authenticated, the user is redirected to the home page.
    """
@admin.route('/edit/skladnik/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if current_user.is_authenticated:
        skladnik = Skladniki.query.filter_by(id=id).first()
        if request.method == 'POST':
            skladnik.Nazwa = request.form.get('Nazwa')
            skladnik.kategoria = request.form.get('kategoria')
            db.session.commit()
            flash('Skladnik został edytowany!', category='success')
            return redirect('/admin')
        return render_template('editSkladnik.html', skladnik=skladnik)
    return redirect('/')

    """
    Route for handling the '/edit/przepis/<int:id>' endpoint. This endpoint is used to edit a 'Przepis' object in the database.

    Parameters:
    - id (int): The ID of the 'Przepis' object to be edited.

    Returns:
    - If the user is authenticated and the request method is 'POST',
     the 'nazwa', 'czas', 'opis', 'skladniki', and 'przepis' fields of the 'Przepis' object are updated with the values from the request form. 
    The changes are committed to the database and a success message is flashed. The user is then redirected to the '/admin' page.
    - If the user is authenticated and the request method is 'GET', the 'editPrzepis.html' template is rendered with the 'przepis' and 'skladniki' objects passed as parameters.
    - If the user is not authenticated, the user is redirected to the home page.
    """
@admin.route('/edit/przepis/<int:id>', methods=['POST', 'GET'])
def editP(id):
    if current_user.is_authenticated:
        if db.session.query(Skladniki).count() >= 1:
            ingredients = db.session.query(Skladniki)
        else:
            ingredients = None
        przepis = Przepisy.query.filter_by(id=id).first()
        if request.method == 'POST':
            przepis.nazwa = request.form.get('nazwa')
            przepis.czas = request.form.get('czas')
            przepis.opis = request.form.get('opis')
            przepis.przepis = request.form.get('przepis')
            przepis.ListaSkladnikow = request.form.getlist('lista')
            przepis.ListaSkladnikow = " ".join(przepis.ListaSkladnikow)
            db.session.commit()
            przepis.grafika = request.files['grafika']
            grafika_name = przepis.grafika.filename
            if grafika_name != '':
                grafika_ext = os.path.splitext(grafika_name)[1]
                if grafika_ext in ['.png', '.jpg', '.jpeg', '.webp']:
                    grafika_name = str(id) + '.png'
                    przepis.grafika.save(os.path.join('website/static/img', grafika_name))
                    db.session.add(przepis)
                    db.session.commit()
                    flash('Przepis został edytowany!', category='success')
                    return redirect('/admin')
                else:
                    flash('Nieprawidłowy format grafiki!', category='error')
                    return redirect(f'/admin/edit/przepis/{id}')
            else:
                db.session.add(przepis)
                db.session.commit()
                flash('Przepis został edytowany!', category='success')
                return redirect('/admin')
        return render_template('editPrzepis.html', przepis=przepis, skladniki=ingredients)
    return redirect('/')
