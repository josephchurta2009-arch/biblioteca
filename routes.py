from datetime import datetime, timedelta
from flask import session, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from sqlalchemy import or_
from functools import wraps
from create_users import User  # cambia esto según tu archivo real
from app import app, db
from models import Book, Loan, User, ActionLog


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('No tienes permisos de administrador.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=bool(request.form.get('remember')))
            next_page = request.args.get('next')
            flash(f'Bienvenido, {user.full_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get user's active loans
    active_loans = Loan.query.filter_by(user_id=current_user.id, status='active').all()
    
    # Get recently added books
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5).all()
    
    return render_template('student_dashboard.html', 
                         active_loans=active_loans, 
                         recent_books=recent_books)

@app.route('/books/search')
@login_required
def book_search():
    search_query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    query = Book.query
    
    if search_query:
        query = query.filter(
            or_(
                Book.title.ilike(f'%{search_query}%'),
                Book.author.ilike(f'%{search_query}%'),
                Book.isbn.ilike(f'%{search_query}%')
            )
        )
    
    if category:
        query = query.filter(Book.category == category)
    
    books = query.all()
    categories = db.session.query(Book.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('book_search.html', 
                         books=books, 
                         categories=categories,
                         search_query=search_query,
                         selected_category=category)

@app.route('/books/<int:book_id>')
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if user already has this book on loan
    user_loan = None
    if not current_user.is_admin:
        user_loan = Loan.query.filter_by(
            user_id=current_user.id,
            book_id=book_id,
            status='active'
        ).first()
    
    return render_template('book_details.html', book=book, user_loan=user_loan)

@app.route('/books/<int:book_id>/loan', methods=['POST'])
@login_required
def loan_book(book_id):
    if current_user.is_admin:
        flash('Administrators cannot loan books.', 'warning')
        return redirect(url_for('book_details', book_id=book_id))
    
    book = Book.query.get_or_404(book_id)
    
    if not book.is_available:
        flash('This book is not available for loan.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    existing_loan = Loan.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        status='active'
    ).first()

    if existing_loan:
        flash('You already have this book on loan.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # Crear el préstamo
    loan = Loan(
        user_id=current_user.id,
        book_id=book.id,
        loan_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )

    book.available_copies -= 1

    db.session.add(loan)
    db.session.commit()

    flash('Préstamo realizado exitosamente.', 'success')
    return redirect(url_for('my_loans'))

    
   
    
    # Acción para crear préstamo
@app.route('/create-loan', methods=['POST'])
@login_required
def create_loan():
    book_id = request.form.get('book_id')
    book = Book.query.get(book_id)

    if not book:
        flash('El libro no fue encontrado.', 'danger')
        return redirect(url_for('my_loans'))

    if book.available_copies < 1:
        flash('Este libro no está disponible actualmente.', 'danger')
        return redirect(url_for('my_loans'))

    # Crear préstamo y actualizar disponibilidad
    loan = Loan(
        user_id=current_user.id,
        book_id=book.id,
        loan_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    book.available_copies -= 1

    db.session.add(loan)
    db.session.commit()

    flash('Préstamo realizado exitosamente.', 'success')
    return redirect(url_for('my_loans'))
    # Update available copies
    book.available_copies -= 1
    
    db.session.add(loan)
    db.session.commit()
    
    flash('Book loaned successfully!', 'success')
    return redirect(url_for('my_loans'))

@app.route('/loans/my')
@login_required
def my_loans():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    active_loans = Loan.query.filter_by(user_id=current_user.id, status='active').all()
    returned_loans = Loan.query.filter_by(user_id=current_user.id, status='returned').order_by(Loan.return_date.desc()).limit(10).all()
    
    return render_template('my_loans.html', 
                         active_loans=active_loans,
                         returned_loans=returned_loans)

@app.route('/loans/<int:loan_id>/return', methods=['POST'])
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    # Check permissions
    if not current_user.is_admin and loan.user_id != current_user.id:
        flash('You can only return your own books.', 'error')
        return redirect(url_for('my_loans'))
    
    if loan.status != 'active':
        flash('This book has already been returned.', 'error')
        return redirect(url_for('my_loans'))
    
    # Return the book
    loan.status = 'returned'
    loan.return_date = datetime.now()
    loan.book.available_copies += 1
    
    db.session.commit()
    
    flash('Book returned successfully!', 'success')
    
    if current_user.is_admin:
        return redirect(url_for('manage_loans'))
    else:
        return redirect(url_for('my_loans'))

# Admin routes
@app.route('/admin/books')
@require_admin
def manage_books():
    search_query = request.args.get('q', '')
    
    query = Book.query
    if search_query:
        query = query.filter(
            or_(
                Book.title.ilike(f'%{search_query}%'),
                Book.author.ilike(f'%{search_query}%'),
                Book.isbn.ilike(f'%{search_query}%')
            )
        )
    
    books = query.order_by(Book.title).all()
    return render_template('manage_books.html', books=books, search_query=search_query)

@app.route('/admin/books/add', methods=['GET', 'POST'])
@require_admin
def add_book():
    if request.method == 'POST':
        book = Book()
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form.get('isbn')
        book.publisher = request.form.get('publisher')
        book.publication_year = int(request.form['publication_year']) if request.form.get('publication_year') else None
        book.category = request.form.get('category')
        book.description = request.form.get('description')
        book.total_copies = int(request.form['total_copies'])
        book.available_copies = int(request.form['total_copies'])
        
        db.session.add(book)
        db.session.commit()

        log_action(current_user, f"Agregó el libro '{book.title}'")
        flash('Book added successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('add_book.html')

@app.route('/admin/books/<int:book_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form.get('isbn')
        book.publisher = request.form.get('publisher')
        book.publication_year = int(request.form['publication_year']) if request.form.get('publication_year') else None
        book.category = request.form.get('category')
        book.description = request.form.get('description')
        
        # Handle total copies change
        new_total = int(request.form['total_copies'])
        difference = new_total - book.total_copies
        book.total_copies = new_total
        book.available_copies = max(0, book.available_copies + difference)
        
        db.session.commit()

        log_action(current_user, f"Editó el libro '{book.title}'")
        flash('Book updated successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('edit_book.html', book=book)

@app.route('/admin/books/<int:book_id>/delete', methods=['POST'])
@require_admin
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if book has active loans
    active_loans = Loan.query.filter_by(book_id=book_id, status='active').count()
    if active_loans > 0:
        flash('Cannot delete book with active loans.', 'error')
        return redirect(url_for('manage_books'))
    
    db.session.delete(book)
    db.session.commit()
    
    log_action(current_user, f"Eliminó el libro '{book.title}'")
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('manage_books'))

@app.route('/admin/loans')
@require_admin
def manage_loans():
    status_filter = request.args.get('status', 'all')
    
    query = Loan.query
    if status_filter != 'all':
        if status_filter == 'overdue':
            query = query.filter(
                Loan.status == 'active',
                Loan.due_date < datetime.now()
            )
        else:
            query = query.filter(Loan.status == status_filter)
    
    loans = query.order_by(Loan.created_at.desc()).all()
    return render_template('manage_loans.html', loans=loans, status_filter=status_filter)

@app.route('/admin/users/<int:user_id>/toggle-role', methods=['POST'])
@require_admin
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)

    if user.role == 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        
        # Impedir si es el único admin
        if admin_count <= 1:
            flash('No puedes eliminar el único administrador.', 'error')
            return redirect(url_for('manage_users'))
        
        user.role = 'student'
        flash(f'{user.full_name} ahora es un estudiante.', 'success')

    else:
        user.role = 'admin'
        log_action(current_user, f"Cambió rol de {user.full_name} a '{user.role}'")
        flash(f'{user.full_name} ahora es un administrador.', 'success')

    db.session.commit()
    return redirect(url_for('manage_users'))


@app.route('/admin/users')
@require_admin
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    log_action(current_user, f"Eliminó al usuario '{user.full_name}'")
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/users/add', methods=['GET', 'POST'])
@require_admin
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'student')

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('El usuario o correo ya existe.', 'error')
            return redirect(url_for('add_user'))

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        log_action(current_user, f"Agregó al usuario '{user.full_name}'")
        flash('Usuario agregado exitosamente.', 'success')
        return redirect(url_for('manage_users'))

    return render_template('add_user.html')

def log_action(user, description):
    from models import ActionLog
    log = ActionLog(user_id=user.id if user else None, action=description)
    db.session.add(log)
    db.session.commit()

from models import ActionLog

@app.route('/admin/dashboard')
@require_admin
def admin_dashboard():
    total_books = Book.query.count()
    total_users = User.query.count()
    active_loans = Loan.query.filter_by(status='active').count()
    overdue_loans = Loan.query.filter(
        Loan.status == 'active',
        Loan.due_date < datetime.now()
    ).count()
    recent_logs = ActionLog.query.order_by(ActionLog.timestamp.desc()).limit(5).all()

    return render_template(
        'admin_dashboard.html',
        total_books=total_books,
        total_users=total_users,
        active_loans=active_loans,
        overdue_loans=overdue_loans,
        recent_logs=recent_logs
    )

@app.route('/admin/loans/add', methods=['GET', 'POST'])
@require_admin
def admin_add_loan():
    users = User.query.filter_by(role='student').all()
    books = Book.query.filter(Book.available_copies > 0).all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        book_id = request.form.get('book_id')

        user = User.query.get(user_id)
        book = Book.query.get(book_id)

        if not user or not book:
            flash("Usuario o libro no válido.", 'error')
            return redirect(url_for('admin_add_loan'))

        loan = Loan(
            user_id=user.id,
            book_id=book.id,
            loan_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=14)
        )
        book.available_copies -= 1
        db.session.add(loan)
        db.session.commit()

        log_action(current_user, f"Agregó un préstamo para el usuario '{user.full_name}' y el libro '{book.title}'")
        flash("Préstamo creado exitosamente.", 'success')
        return redirect(url_for('manage_loans'))

    return render_template('admin_add_loan.html', users=users, books=books)

